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
        self.oauth_btn = QtWidgets.QPushButton('Get Token')
        token_row.addWidget(self.oauth_btn)

        form.addRow('Twitch OAuth Token (oauth:...)', token_row)
        form.addRow('Twitch Client ID (for Get Token)', self.client_id_edit)
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
        self.oauth_btn.clicked.connect(self.on_oauth)
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
    def on_oauth(self):
        asyncio.create_task(self.oauth_flow())

    async def oauth_flow(self):
        from aiohttp import web
        client_id = (self.client_id_edit.text() or '').strip()
        if not client_id:
            self.log_area.appendPlainText('Client ID required for OAuth. Visit https://dev.twitch.tv/console/apps to create one and add http://127.0.0.1:53682/callback as a redirect URL.')
            return
        port = 53682
        redirect_uri = f'http://127.0.0.1:{port}/callback'
        scopes = 'chat:read chat:edit'
        app = web.Application()
        token_future: asyncio.Future = asyncio.get_running_loop().create_future()

        async def callback(request):
            logging.getLogger('BakeBot.GUI').info('OAuth callback received')
            html = f"""
            <html><body>
            <p>Completing Twitch sign-in...</p>
            <script>
              (function(){{
                const hash = window.location.hash.substring(1);
                const params = new URLSearchParams(hash);
                const token = params.get('access_token');
                if(token){{
                  fetch('/token', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify({{token}})}})
                    .then(_=>document.body.innerText='Token received. You may close this tab.');
                }} else {{
                  document.body.innerText='No token found in URL.';
                }}
              }})();
            </script>
            </body></html>
            """
            return web.Response(text=html, content_type='text/html')

        async def receive_token(request):
            try:
                data = await request.json()
                token = data if isinstance(data, str) else data.get('token')
                if token and not token_future.done():
                    token_future.set_result(token)
                logging.getLogger('BakeBot.GUI').info('OAuth token captured')
                return web.json_response({'ok': True})
            except Exception:
                logging.getLogger('BakeBot.GUI').exception('Failed to parse token JSON')
                return web.json_response({'ok': False}, status=400)

        app.add_routes([
            web.get('/callback', callback),
            web.post('/token', receive_token),
        ])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '127.0.0.1', port)
        await site.start()
        auth_url = (
            'https://id.twitch.tv/oauth2/authorize'
            f'?client_id={client_id}'
            f'&redirect_uri={redirect_uri}'
            '&response_type=token'
            f'&scope={scopes.replace(" ", "+")}'

            '&force_verify=true'
        )
        logging.getLogger('BakeBot.GUI').info('Opening browser for Twitch authorization')
        QDesktopServices.openUrl(QUrl(auth_url))
        try:
            access_token = await asyncio.wait_for(token_future, timeout=180)
            self.token_edit.setText(f'oauth:{access_token}')
            logging.getLogger('BakeBot.GUI').info('Token filled into GUI')
        except asyncio.TimeoutError:
            logging.getLogger('BakeBot.GUI').warning('Timed out waiting for token')
        finally:
            await runner.cleanup()


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
