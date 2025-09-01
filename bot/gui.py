import asyncio
import threading
import webbrowser
import os
import logging
from datetime import datetime
from dotenv import set_key, load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit
import json
import socket
import re
import requests
from pathlib import Path

from .bot import BakeBot
from .logging_config import setup_logging

class BotManager:
    def __init__(self, socketio=None):
        self.bot = None
        self.bot_task = None
        self.loop = None
        self.thread = None
        self.socketio = socketio
        self.status = "stopped"

    def start_bot(self):
        if self.thread and self.thread.is_alive():
            return False
        self.thread = threading.Thread(target=self._run_bot)
        self.thread.daemon = True
        self.thread.start()
        return True

    def _run_bot(self):
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.bot = BakeBot()
            self.status = "running"
            if self.socketio:
                self.socketio.emit('status_update', {'status': 'running', 'message': 'Bot Running'})
            self.loop.run_until_complete(self.bot.start())
        except Exception as e:
            self.status = "error"
            if self.socketio:
                self.socketio.emit('status_update', {'status': 'error', 'message': f'Error: {str(e)}'})

    def stop_bot(self):
        if self.loop and self.bot:
            self.status = "stopping"
            if self.socketio:
                self.socketio.emit('status_update', {'status': 'stopping', 'message': 'Stopping...'})
            asyncio.run_coroutine_threadsafe(self.bot.shutdown(), self.loop)
            self.status = "stopped"
            if self.socketio:
                self.socketio.emit('status_update', {'status': 'stopped', 'message': 'Bot Stopped'})

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger('BakeBot.WebGUI')
# Quiet noisy access logs; keep our app logs readable for troubleshooting
for noisy in (
    'werkzeug',
    'geventwebsocket.handler',
    'engineio.server',
    'socketio.server',
    'urllib3.connectionpool',
):
    logging.getLogger(noisy).setLevel(logging.WARNING)

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOCS_PATH = os.path.join(PROJECT_ROOT, 'docs')
DOCS_DIR = Path(DOCS_PATH)
ENV_PATH = os.path.abspath('.env')

# Create Flask app
app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
           static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'bakebot-secret-key-change-me')

# Create SocketIO instance (suppress engineio/socketio internal logs)
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

# Create bot manager
bot_manager = BotManager(socketio)

def _get_local_ipv4():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            if ip and not ip.startswith('127.'):
                return ip
    except Exception:
        pass
    try:
        hostname = socket.gethostname()
        ips = socket.gethostbyname_ex(hostname)[2]
        for ip in ips:
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', ip) and not ip.startswith('127.'):
                return ip
    except Exception:
        pass
    return ''

@app.route('/api/network-info')
def network_info():
    ip = _get_local_ipv4()
    logger.debug('GUI: network-info local_ipv4=%s', ip)
    return jsonify({ 'local_ipv4': ip })

@app.route('/api/public-ip')
def public_ip():
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text.strip()
    except Exception as e:
        logger.warning('GUI: public-ip fetch failed: %s', e)
        ip = ''
    return jsonify({ 'public_ip': ip })

@app.route('/docs/')
@app.route('/docs')
def docs_index():
    if not DOCS_DIR.exists():
        return 'No docs available', 404
    items = []
    for p in sorted(DOCS_DIR.glob('*.md')):
        items.append(f"<li><a href='/docs/{p.name}'>{p.name}</a></li>")
    html = f"""
    <html><head><title>Docs</title></head>
    <body><h3>Documentation</h3><ul>{''.join(items) or '<li>No .md files</li>'}</ul></body></html>
    """
    return html

@app.route('/docs/<path:filename>')
def serve_docs(filename):
    # Normalize and try to locate the file case-insensitively
    name = os.path.normpath(filename).replace('\\', '/').lstrip('/')
    cand = DOCS_DIR / name
    if cand.exists():
        return send_from_directory(DOCS_PATH, name)
    # Case-insensitive lookup within docs dir (flat)
    try:
        lower = name.lower()
        for p in DOCS_DIR.glob('*'):
            if p.is_file() and p.name.lower() == lower:
                return send_from_directory(DOCS_PATH, p.name)
    except Exception:
        pass
    # Not found
    return ('Not Found', 404)

# OAuth callback to capture access_token from fragment
@app.route('/oauth-callback')
def oauth_callback():
    # Serve a tiny page that posts the access_token to our API then redirects back to wizard
    return '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>OAuth Callback</title></head>
    <body><p>Completing OAuth...</p>
    <script>
    (function(){
      try {
        var hash = window.location.hash || '';
        var m = /access_token=([^&]+)/.exec(hash);
        if (m && m[1]) {
          var token = m[1];
          fetch('/api/oauth-captured-token', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: token })
          }).then(function(){ window.location = '/oauth-wizard?captured=1'; })
          .catch(function(){ window.location = '/oauth-wizard?captured=0'; });
        } else {
          window.location = '/oauth-wizard?captured=0';
        }
      } catch(e){ window.location = '/oauth-wizard?captured=0'; }
    })();
    </script></body></html>'''

@app.route('/api/oauth-captured-token', methods=['POST','GET'])
def oauth_captured_token():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        token = (data.get('token') or '').strip()
        if not token:
            return jsonify({ 'success': False, 'error': 'no token' }), 400
        final_token = token if token.startswith('oauth:') else f'oauth:{token}'
        try:
            set_key(ENV_PATH, 'TWITCH_TOKEN', final_token)
            load_dotenv(override=True)
            logger.info('GUI: OAuth token captured and saved')
            return jsonify({ 'success': True })
        except Exception as e:
            logger.exception('GUI: failed to save OAuth token')
            return jsonify({ 'success': False, 'error': str(e) }), 500
    # GET can return whether a token is present
    return jsonify({ 'token_set': bool(os.getenv('TWITCH_TOKEN','')) })

# Lightweight GUI click logging endpoint
@app.post('/api/log-ui')
def log_ui():
    data = request.get_json(silent=True) or {}
    action = (data.get('action') or 'unknown').strip()
    extra = {k: v for k, v in data.items() if k != 'action'}
    logger.info('GUI click: %s %s', action, extra if extra else '')
    return jsonify({'success': True})

@app.route('/')
def dashboard():
    """Main dashboard page"""
    env_vars = {
        'TWITCH_TOKEN': os.getenv('TWITCH_TOKEN', ''),
        'TWITCH_CLIENT_ID': os.getenv('TWITCH_CLIENT_ID', ''),
        'TWITCH_CHANNEL': os.getenv('TWITCH_CHANNEL', ''),
        'PREFIX': os.getenv('PREFIX', '!'),
        'WEB_HOST': os.getenv('WEB_HOST', '127.0.0.1'),
        'WEB_PORT': os.getenv('WEB_PORT', '8080'),
        'PUBLIC_BASE_URL': os.getenv('PUBLIC_BASE_URL', ''),
        'ENABLE_EVENTSUB': os.getenv('ENABLE_EVENTSUB', 'false'),
        'EVENTSUB_SECRET': os.getenv('EVENTSUB_SECRET', ''),
        'EVENTSUB_PORT': os.getenv('EVENTSUB_PORT', '8081'),
        'SECRET_KEY': os.getenv('SECRET_KEY', 'bakebot-secret-key-change-me'),
    }
    return render_template('dashboard.html', env_vars=env_vars, status=bot_manager.status)

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/oauth-wizard')
def oauth_wizard():
    return render_template('oauth_wizard.html')

@app.route('/api/save-config', methods=['POST'])
def save_config():
    try:
        data = request.json or {}
        env_path = os.path.abspath('.env')
        allowed = [
            'TWITCH_TOKEN', 'TWITCH_CLIENT_ID', 'TWITCH_CHANNEL',
            'PREFIX', 'WEB_HOST', 'WEB_PORT', 'PUBLIC_BASE_URL',
            'ENABLE_EVENTSUB', 'EVENTSUB_SECRET', 'EVENTSUB_PORT', 'SECRET_KEY'
        ]
        for key, value in data.items():
            if key in allowed:
                set_key(env_path, key, str(value))
        load_dotenv(override=True)
        logger.info('GUI: save-config keys=%s', [k for k in data.keys() if k in allowed])
        return jsonify({'success': True, 'message': 'Configuration saved successfully'})
    except Exception as e:
        logger.exception('GUI: save-config failed')
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/start-bot', methods=['POST'])
def start_bot():
    try:
        logger.info('GUI: start-bot requested')
        success = bot_manager.start_bot()
        if success:
            return jsonify({'success': True, 'message': 'Bot starting...'})
        else:
            return jsonify({'success': False, 'message': 'Bot already running'})
    except Exception as e:
        logger.exception('GUI: start-bot failed')
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/stop-bot', methods=['POST'])
def stop_bot():
    try:
        logger.info('GUI: stop-bot requested')
        bot_manager.stop_bot()
        return jsonify({'success': True, 'message': 'Bot stopping...'})
    except Exception as e:
        logger.exception('GUI: stop-bot failed')
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/open-leaderboard', methods=['POST'])
def open_leaderboard():
    try:
        host = os.getenv('WEB_HOST', '127.0.0.1')
        port = os.getenv('WEB_PORT', '8080')
        base = os.getenv('PUBLIC_BASE_URL', '').strip()
        if base:
            url = f"{base.rstrip('/')}/leaderboard"
        else:
            url = f"http://{host}:{port}/leaderboard"
        logger.info('GUI: open-leaderboard %s', url)
        webbrowser.open(url)
        return jsonify({'success': True, 'message': f'Opened {url}'})
    except Exception as e:
        logger.exception('GUI: open-leaderboard failed')
        return jsonify({'success': False, 'message': str(e)})

@socketio.on('connect')
def handle_connect():
    emit('status_update', {'status': bot_manager.status, 'message': f'Bot {bot_manager.status.title()}'})

@app.get('/api/metadata')
def get_metadata_api():
    from .storage import Storage
    key = request.args.get('key','')
    if not key:
        return jsonify({ 'success': False, 'message': 'key required' }), 400
    try:
        # read directly from DB through Storage to avoid race
        import asyncio as _aio
        store = Storage()
        # Storage.init ensures tables; but we can just query
        async def _read():
            await store.init()
            return await store.get_metadata(key)
        loop = _aio.new_event_loop()
        try:
            _aio.set_event_loop(loop)
            val = loop.run_until_complete(_read())
        finally:
            loop.close()
        return jsonify({ 'success': True, 'key': key, 'value': val or '' })
    except Exception as e:
        logger.exception('GUI: metadata get failed')
        return jsonify({ 'success': False, 'message': str(e) }), 500

@app.post('/api/metadata')
def set_metadata_api():
    from .storage import Storage
    data = request.get_json(silent=True) or {}
    key = (data.get('key') or '').strip()
    value = (data.get('value') or '')
    if not key:
        return jsonify({ 'success': False, 'message': 'key required' }), 400
    try:
        import asyncio as _aio
        store = Storage()
        async def _write():
            await store.init()
            await store.set_metadata(key, value)
        loop = _aio.new_event_loop()
        try:
            _aio.set_event_loop(loop)
            loop.run_until_complete(_write())
        finally:
            loop.close()
        return jsonify({ 'success': True, 'message': 'Saved' })
    except Exception as e:
        logger.exception('GUI: metadata set failed')
        return jsonify({ 'success': False, 'message': str(e) }), 500

def main():
    print("BakeBot Web GUI")
    print("=================")
    print("Opening web interface...")
    host = '127.0.0.1'
    port = 5000
    url = f"http://{host}:{port}"
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    print(f"Web GUI available at: {url}")
    print("Press Ctrl+C to stop")
    try:
        socketio.run(app, host=host, port=port, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
