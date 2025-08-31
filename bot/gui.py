import os
import asyncio
from typing import Optional
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtCore import QUrl
import qasync
from dotenv import set_key
from aiohttp import web
import logging

from .bot import BakeBot
from .logging_config import setup_logging

class LogHandler(QtCore.QObject, logging.Handler):
    new_record = QtCore.Signal(str)
    def __init__(self):
        QtCore.QObject.__init__(self)
        logging.Handler.__init__(self)
    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        self.new_record.emit(msg)

class BotWorker(QtCore.QObject):
    started = QtCore.Signal()
    stopped = QtCore.Signal()
    error = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._bot: Optional[BakeBot] = None
        self._task: Optional[asyncio.Task] = None

    async def start_bot(self):
        try:
            self._bot = BakeBot()
            self.started.emit()
            self._task = asyncio.create_task(self._bot.start())
        except Exception as e:
            self.error.emit(str(e))

    async def stop_bot(self):
        try:
            if self._bot:
                await self._bot.shutdown()
            if self._task:
                self._task.cancel()
            self.stopped.emit()
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('BakeBot Setup')
        self.resize(800, 640)

        # Logging
        setup_logging()
        self.qt_log_handler = LogHandler()
        self.qt_log_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s', datefmt='%H:%M:%S'))
        logging.getLogger().addHandler(self.qt_log_handler)

        self.token_edit = QtWidgets.QLineEdit()
        self.token_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.client_id_edit = QtWidgets.QLineEdit()
        self.channel_edit = QtWidgets.QLineEdit()
        self.prefix_edit = QtWidgets.QLineEdit('!')
        self.web_host_edit = QtWidgets.QLineEdit('127.0.0.1')
        self.web_port_edit = QtWidgets.QSpinBox()
        self.web_port_edit.setRange(1, 65535)
        self.web_port_edit.setValue(8080)

        self.load_env()

        form = QtWidgets.QFormLayout()

        token_row = QtWidgets.QHBoxLayout()
        token_row.addWidget(self.token_edit)
        self.oauth_btn = QtWidgets.QPushButton('Get Token (Manual)')
        token_row.addWidget(self.oauth_btn)

        form.addRow('Twitch OAuth Token (oauth:...)', token_row)
        form.addRow('Twitch Client ID (for manual OAuth)', self.client_id_edit)
        form.addRow('Channel', self.channel_edit)
        form.addRow('Prefix', self.prefix_edit)
        form.addRow('Web Host', self.web_host_edit)
        form.addRow('Web Port', self.web_port_edit)

        self.start_btn = QtWidgets.QPushButton('Start Bot')
        self.stop_btn = QtWidgets.QPushButton('Stop Bot')
        self.stop_btn.setEnabled(False)

        self.log_area = QtWidgets.QPlainTextEdit()
        self.log_area.setReadOnly(True)
        self.qt_log_handler.new_record.connect(self.log_area.appendPlainText)

        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(self.start_btn)
        btns.addWidget(self.stop_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btns)
        layout.addWidget(self.log_area)

        central = QtWidgets.QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.worker = BotWorker()
        self.start_btn.clicked.connect(self.on_start)
        self.stop_btn.clicked.connect(self.on_stop)
        self.oauth_btn.clicked.connect(self.on_manual_oauth)
        self.worker.started.connect(self.on_bot_started)
        self.worker.stopped.connect(self.on_bot_stopped)
        self.worker.error.connect(self.on_bot_error)

    def load_env(self):
        self.token_edit.setText(os.getenv('TWITCH_TOKEN', ''))
        self.client_id_edit.setText(os.getenv('TWITCH_CLIENT_ID', ''))
        self.channel_edit.setText(os.getenv('TWITCH_CHANNEL', ''))
        self.prefix_edit.setText(os.getenv('PREFIX', '!'))
        self.web_host_edit.setText(os.getenv('WEB_HOST', '127.0.0.1'))
        self.web_port_edit.setValue(int(os.getenv('WEB_PORT', '8080')))

    def persist_env(self):
        env_path = os.path.abspath('.env')
        set_key(env_path, 'TWITCH_TOKEN', self.token_edit.text())
        set_key(env_path, 'TWITCH_CLIENT_ID', self.client_id_edit.text())
        set_key(env_path, 'TWITCH_CHANNEL', self.channel_edit.text())
        set_key(env_path, 'PREFIX', self.prefix_edit.text() or '!')
        set_key(env_path, 'WEB_HOST', self.web_host_edit.text())
        set_key(env_path, 'WEB_PORT', str(self.web_port_edit.value()))

    @QtCore.Slot()
    def on_start(self):
        self.persist_env()
        logging.getLogger('BakeBot.GUI').info('Starting bot...')
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        asyncio.create_task(self.worker.start_bot())

    @QtCore.Slot()
    def on_stop(self):
        logging.getLogger('BakeBot.GUI').info('Stopping bot...')
        asyncio.create_task(self.worker.stop_bot())

    @QtCore.Slot()
    def on_bot_started(self):
        logging.getLogger('BakeBot.GUI').info('Bot started.')

    @QtCore.Slot()
    def on_bot_stopped(self):
        logging.getLogger('BakeBot.GUI').info('Bot stopped.')
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    @QtCore.Slot(str)
    def on_bot_error(self, msg: str):
        logging.getLogger('BakeBot.GUI').error('Error: %s', msg)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    @QtCore.Slot()
    def on_manual_oauth(self):
        client_id = (self.client_id_edit.text() or '').strip()
        if not client_id:
            msg = """Manual OAuth Steps:
1. Create a Twitch Application at https://dev.twitch.tv/console/apps
2. Add a redirect URL: https://localhost (HTTPS required)
3. Paste your Client ID above
4. Click this button again to open the auth URL
5. Authorize, then copy the access_token from the URL fragment
6. Paste it as oauth:TOKEN in the token field"""
            QtWidgets.QMessageBox.information(self, 'OAuth Setup', msg)
            return
        
        # Generate manual OAuth URL
        auth_url = (
            'https://id.twitch.tv/oauth2/authorize'
            f'?client_id={client_id}'
            '&redirect_uri=https://localhost'
            '&response_type=token'
            '&scope=chat:read+chat:edit'
            '&force_verify=true'
        )
        
        msg = f"""Manual OAuth Process:
1. Click 'Copy URL' to copy the authorization URL
2. Open it in your browser and authorize
3. Copy the access_token from the redirected URL (after #access_token=)
4. Paste it in the token field as: oauth:ACCESS_TOKEN

URL: {auth_url}"""
        
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle('Manual OAuth')
        msgBox.setText(msg)
        copy_btn = msgBox.addButton('Copy URL', QtWidgets.QMessageBox.ActionRole)
        open_btn = msgBox.addButton('Open in Browser', QtWidgets.QMessageBox.ActionRole)
        msgBox.addButton('Cancel', QtWidgets.QMessageBox.RejectRole)
        
        msgBox.exec()
        
        if msgBox.clickedButton() == copy_btn:
            QtWidgets.QApplication.clipboard().setText(auth_url)
            self.log_area.appendPlainText('OAuth URL copied to clipboard')
        elif msgBox.clickedButton() == open_btn:
            QDesktopServices.openUrl(QUrl(auth_url))
            self.log_area.appendPlainText('OAuth URL opened in browser')


def main():
    # Set High DPI rounding policy before creating the QApplication (if available)
    try:
        QtCore.QCoreApplication.setHighDpiScaleFactorRoundingPolicy(
            QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    except AttributeError:
        pass

    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_forever()

if __name__ == '__main__':
    main()
