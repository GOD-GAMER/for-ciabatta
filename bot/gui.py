import asyncio
import threading
import webbrowser
import os
import logging
from datetime import datetime
from dotenv import set_key, load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
import json

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

# Create Flask app
app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
           static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'bakebot-secret-key-change-me')

# Create SocketIO instance
socketio = SocketIO(app, cors_allowed_origins="*")

# Create bot manager
bot_manager = BotManager(socketio)

@app.route('/')
def dashboard():
    """Main dashboard page"""
    env_vars = {
        'TWITCH_TOKEN': os.getenv('TWITCH_TOKEN', ''),
        'TWITCH_CLIENT_ID': os.getenv('TWITCH_CLIENT_ID', ''),
        'TWITCH_CHANNEL': os.getenv('TWITCH_CHANNEL', ''),
        'PREFIX': os.getenv('PREFIX', '!'),
        'WEB_HOST': os.getenv('WEB_HOST', '127.0.0.1'),
        'WEB_PORT': os.getenv('WEB_PORT', '8080')
    }
    return render_template('dashboard.html', env_vars=env_vars, status=bot_manager.status)

@app.route('/logs')
def logs():
    """Logs page"""
    return render_template('logs.html')

@app.route('/users')
def users():
    """Users management page"""
    return render_template('users.html')

@app.route('/games')
def games():
    """Games control page"""
    return render_template('games.html')

@app.route('/shop')
def shop():
    """Bakery shop page"""
    return render_template('shop.html')

@app.route('/oauth-wizard')
def oauth_wizard():
    """OAuth setup wizard"""
    return render_template('oauth_wizard.html')

@app.route('/api/save-config', methods=['POST'])
def save_config():
    """Save configuration to .env file"""
    try:
        data = request.json
        env_path = os.path.abspath('.env')
        
        for key, value in data.items():
            if key in ['TWITCH_TOKEN', 'TWITCH_CLIENT_ID', 'TWITCH_CHANNEL', 'PREFIX', 'WEB_HOST', 'WEB_PORT']:
                set_key(env_path, key, value)
        
        return jsonify({'success': True, 'message': 'Configuration saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/start-bot', methods=['POST'])
def start_bot():
    """Start the bot"""
    try:
        success = bot_manager.start_bot()
        if success:
            return jsonify({'success': True, 'message': 'Bot starting...'})
        else:
            return jsonify({'success': False, 'message': 'Bot already running'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/stop-bot', methods=['POST'])
def stop_bot():
    """Stop the bot"""
    try:
        bot_manager.stop_bot()
        return jsonify({'success': True, 'message': 'Bot stopping...'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/open-leaderboard', methods=['POST'])
def open_leaderboard():
    """Open leaderboard in browser"""
    try:
        host = os.getenv('WEB_HOST', '127.0.0.1')
        port = os.getenv('WEB_PORT', '8080')
        url = f"http://{host}:{port}/leaderboard"
        webbrowser.open(url)
        return jsonify({'success': True, 'message': 'Leaderboard opened in browser'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status_update', {'status': bot_manager.status, 'message': f'Bot {bot_manager.status.title()}'})

def main():
    """Run the web GUI"""
    print("?? BakeBot Web GUI")
    print("=================")
    print("Opening web interface...")
    
    # Open browser
    host = '127.0.0.1'
    port = 5000
    url = f"http://{host}:{port}"
    
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    
    print(f"Web GUI available at: {url}")
    print("Press Ctrl+C to stop")
    
    try:
        socketio.run(app, host=host, port=port, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
