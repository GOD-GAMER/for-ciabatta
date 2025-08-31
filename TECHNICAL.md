# BakeBot Technical Documentation

This document provides comprehensive technical information for developers, advanced users, and those looking to customize or extend BakeBot.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Configuration Reference](#configuration-reference)
- [Database Schema](#database-schema)
- [API Reference](#api-reference)
- [Customization Guide](#customization-guide)
- [Extension Development](#extension-development)
- [Security Considerations](#security-considerations)
- [Performance Tuning](#performance-tuning)
- [Troubleshooting](#troubleshooting)

---

## Architecture Overview

BakeBot is built using modern Python async/await patterns with a modular architecture:

```
???????????????????    ???????????????????    ???????????????????
?   Web Interface ?    ?   Twitch Bot    ?    ?   Game Engine   ?
?    (Flask)      ??????   (TwitchIO)    ??????   (AsyncIO)     ?
???????????????????    ???????????????????    ???????????????????
         ?                       ?                       ?
         ?                       ?                       ?
???????????????????    ???????????????????    ???????????????????
?   SQLite DB     ?    ?  Configuration  ?    ?   Token Economy ?
?   (aiosqlite)   ?    ?     (.env)      ?    ?   (Commands)    ?
???????????????????    ???????????????????    ???????????????????
```

### Core Components

- **`bot.py`**: Main Twitch bot using TwitchIO
- **`gui.py`**: Flask web interface with Socket.IO
- **`games.py`**: Game engine and bread fighting system
- **`commands.py`**: Command handlers and token economy
- **`storage.py`**: Async SQLite database operations
- **`web.py`**: HTTP API and web routes

---

## Project Structure

```
twitch-bot/
??? bot/
?   ??? __init__.py              # Package initialization
?   ??? bot.py                   # Main Twitch bot class
?   ??? commands.py              # Command handlers & economy
?   ??? games.py                 # Mini-games & bread fights
?   ??? storage.py               # Database operations
?   ??? gui.py                   # Flask web interface
?   ??? web.py                   # HTTP API routes
?   ??? eventsub.py             # Twitch EventSub handler
?   ??? utils.py                 # Utility functions
?   ??? icons.py                 # Icon management system
?   ??? logging_config.py        # Logging configuration
?   ??? config.example.env       # Example configuration
?   ??? templates/               # HTML templates
?       ??? dashboard.html       # Main control panel
?       ??? oauth_wizard.html    # OAuth setup guide
?       ??? shop.html           # Bakery shop interface
?       ??? games.html          # Games control panel
?       ??? users.html          # User management
?       ??? logs.html           # Application logs
??? install/
?   ??? INSTALL.md              # Installation guide
??? requirements.txt            # Python dependencies
??? README.md                   # User-facing documentation
??? TECHNICAL.md               # This file
??? .env                       # Configuration (create from example)
```

---

## Development Setup

### Prerequisites

- **Python 3.10+** (async/await syntax, modern type hints)
- **Git** for version control
- **Node.js** (optional, for frontend development)

### Local Development

1. **Clone and Setup:**
```bash
git clone https://github.com/your-repo/bakebot.git
cd bakebot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configuration:**
```bash
cp bot/config.example.env .env
# Edit .env with your settings
```

3. **Database Initialization:**
```bash
# Database auto-creates on first run
python -c "import asyncio; from bot.storage import Storage; asyncio.run(Storage().init())"
```

4. **Run Development Server:**
```bash
python -m bot.gui  # Starts Flask on port 5000
```

### Development Commands

```bash
# Run tests (if you add them)
python -m pytest

# Code formatting
python -m black bot/

# Type checking
python -m mypy bot/

# Database schema export
sqlite3 bot_data.sqlite3 .schema
```

---

## Configuration Reference

### Environment Variables (.env)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `TWITCH_TOKEN` | string | - | OAuth token (oauth:xxxxx) |
| `TWITCH_CLIENT_ID` | string | - | Twitch application client ID |
| `TWITCH_CHANNEL` | string | - | Your channel name (lowercase) |
| `PREFIX` | string | ! | Command prefix |
| `WEB_HOST` | string | 127.0.0.1 | Web server bind address |
| `WEB_PORT` | int | 8080 | Bot web server port |
| `GUI_HOST` | string | 127.0.0.1 | GUI server bind address |
| `GUI_PORT` | int | 5000 | GUI server port |
| `LOG_LEVEL` | string | INFO | DEBUG/INFO/WARNING/ERROR |
| `ENABLE_EVENTSUB` | bool | false | Enable Channel Points integration |
| `EVENTSUB_SECRET` | string | changeme | EventSub webhook secret |
| `EVENTSUB_PORT` | int | 8081 | EventSub listener port |
| `SECRET_KEY` | string | auto | Flask secret key |

### Advanced Configuration

```python
# bot/config.py (custom config module)
class BotConfig:
    # Game settings
    GAME_TIMEOUT = 30  # seconds
    XP_PER_PARTICIPATION = 1
    XP_PER_WIN = 25
    TOKENS_PER_WIN = 5
    
    # Economy settings
    DAILY_BONUS_BASE = 10
    DAILY_STREAK_MAX = 20
    HOURLY_BONUS = 3
    WORK_COOLDOWN = 300  # 5 minutes
    
    # Combat settings
    FIGHT_TIMEOUT = 60
    FIGHT_TURN_TIME = 15
    QUESTION_ACCURACY_THRESHOLD = 75
    
    # Rate limiting
    COMMAND_COOLDOWN = 3
    PARTICIPATION_COOLDOWN = 15
    RATE_LIMIT_MESSAGES = 8
    RATE_LIMIT_WINDOW = 10
```

---

## Database Schema

### Tables

**users**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    xp INTEGER NOT NULL DEFAULT 0,
    tokens INTEGER NOT NULL DEFAULT 0,
    wins INTEGER NOT NULL DEFAULT 0,
    last_seen INTEGER NOT NULL DEFAULT 0,
    notes TEXT DEFAULT '',
    is_banned INTEGER DEFAULT 0
);
```

**redemptions**
```sql
CREATE TABLE redemptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    reward TEXT NOT NULL,
    cost INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username)
);
```

**metadata**
```sql
CREATE TABLE metadata (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

**chat_logs**
```sql
CREATE TABLE chat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    channel TEXT NOT NULL
);
```

### Database Operations

```python
from bot.storage import Storage

# Initialize
storage = Storage()
await storage.init()

# User operations
user = await storage.get_or_create_user("username")
await storage.add_xp("username", 25)
await storage.add_tokens("username", 5)

# Query operations
top_users = await storage.top_users_by_xp(10)
all_users = await storage.get_all_users()

# Metadata
await storage.set_metadata("season", "halloween")
season = await storage.get_metadata("season")
```

---

## API Reference

### Web API Endpoints

**Configuration**
- `POST /api/save-config` - Save bot configuration
- `GET /api/config` - Get current configuration

**Bot Control**
- `POST /api/start-bot` - Start the Twitch bot
- `POST /api/stop-bot` - Stop the Twitch bot
- `GET /api/status` - Get bot status

**Data Access**
- `GET /api/users` - Get all users (paginated)
- `GET /api/users/{username}` - Get specific user
- `PUT /api/users/{username}` - Update user data
- `GET /api/leaderboard` - Get top users by XP
- `GET /api/chat_logs` - Get chat history

**Shop & Economy**
- `GET /api/shop` - Get all shop items
- `POST /api/purchase` - Process item purchase
- `GET /api/economy/stats` - Get economy statistics

### Socket.IO Events

**Client ? Server**
```javascript
// Connect to get status
socket.emit('get_status');

// Request user data
socket.emit('get_users', { page: 1, limit: 50 });
```

**Server ? Client**
```javascript
// Status updates
socket.on('status_update', (data) => {
    console.log(data.status, data.message);
});

// User data
socket.on('user_data', (users) => {
    updateUserTable(users);
});
```

---

## Customization Guide

### Adding New Commands

1. **Add to CommandHandler class:**

```python
# bot/commands.py
async def cmd_my_command(self, ctx, author: str, args):
    """Your custom command"""
    await ctx.send(f"Hello {author}! Args: {args}")

async def handle(self, ctx, author: str, content: str):
    # ... existing commands ...
    elif cmd == '!mycmd':
        await self.cmd_my_command(ctx, author, args)
```

2. **Add cooldowns/permissions:**

```python
async def cmd_my_command(self, ctx, author: str, args):
    # Check cooldown
    if not self.cooldowns.check(f"mycmd:{author}", 60):
        await ctx.send("Command on cooldown!")
        return
    
    # Check permissions (example: broadcaster only)
    is_broadcaster = getattr(ctx.ctx.author, 'is_broadcaster', False)
    if not is_broadcaster:
        await ctx.send("Broadcaster only command!")
        return
    
    # Your command logic here
```

### Adding New Shop Items

```python
# bot/commands.py - BakeryShop class
self.shop_items['my_item'] = {
    'name': 'My Custom Item',
    'description': 'Does something amazing',
    'cost': 30,
    'category': 'utility',
    'effect': 'my_custom_effect'
}

# Handle the effect
async def apply_shop_effect(self, ctx, author: str, effect: str, item: dict):
    # ... existing effects ...
    elif effect == 'my_custom_effect':
        await self.my_custom_logic(author)
        await ctx.send(f"{author} activated {item['name']}!")
```

### Adding New Mini-Games

```python
# bot/games.py
async def start_my_game(self, ctx, duration=30):
    if self.current_game:
        await ctx.send('Another game is running!')
        return
    
    # Set up game state
    self.current_game = {
        'type': 'my_game',
        'answer': 'correct_answer',
        'end': time.time() + duration,
        'data': {}  # Custom game data
    }
    
    await ctx.send(f"My Game started! You have {duration} seconds!")
    
    # Auto-end after timeout
    await asyncio.sleep(duration)
    if self.current_game and self.current_game['type'] == 'my_game':
        await ctx.send("Game ended!")
        self.current_game = None

# Handle answers in on_message
async def on_message(self, author: str, message: str, ctx=None, storage=None):
    if not self.current_game:
        return None
    
    if self.current_game['type'] == 'my_game':
        if message.lower() == self.current_game['answer']:
            self.current_game = None
            await self.win_cb(author)
            return f"Correct, {author}! You win!"
    
    # ... existing game logic ...
```

### Customizing Web Interface

1. **Add new routes:**

```python
# bot/gui.py
@app.route('/my-page')
def my_page():
    return render_template('my_page.html')
```

2. **Create template:**

```html
<!-- bot/templates/my_page.html -->
<!DOCTYPE html>
<html>
<head>
    <title>My Custom Page</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>My Custom Page</h1>
    <!-- Your content here -->
</body>
</html>
```

3. **Add navigation:**

```html
<!-- Update all templates -->
<nav class="nav">
    <!-- ... existing links ... -->
    <a href="/my-page">My Page</a>
</nav>
```

### Custom Bread Fight Questions

```python
# bot/games.py - BreadFightGame class
self.fight_questions.extend([
    {"question": "What's your custom question?", "answer": "answer", "difficulty": 2},
    {"question": "Another question?", "answer": "another answer", "difficulty": 1},
    # Add more questions...
])
```

---

## Extension Development

### Plugin Architecture

Create a plugin system by extending the bot:

```python
# plugins/my_plugin.py
class MyPlugin:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message):
        """Handle all chat messages"""
        if message.content.startswith('!myplugin'):
            await message.channel.send("Plugin response!")
    
    async def on_user_join(self, user):
        """Handle user joins"""
        pass

# bot/bot.py - Load plugins
def load_plugins(self):
    import importlib
    plugin_module = importlib.import_module('plugins.my_plugin')
    self.plugins.append(plugin_module.MyPlugin(self))
```

### Custom Storage Backends

```python
# bot/storage_redis.py
import aioredis

class RedisStorage:
    def __init__(self, redis_url="redis://localhost"):
        self.redis_url = redis_url
    
    async def init(self):
        self.redis = await aioredis.from_url(self.redis_url)
    
    async def get_or_create_user(self, username: str):
        # Redis implementation
        pass
    
    # Implement all storage methods...
```

### Integration with External APIs

```python
# bot/integrations.py
import aiohttp

class TwitchAPIClient:
    def __init__(self, client_id: str, access_token: str):
        self.client_id = client_id
        self.access_token = access_token
    
    async def get_stream_info(self, username: str):
        """Get stream information"""
        async with aiohttp.ClientSession() as session:
            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {self.access_token}'
            }
            async with session.get(
                f'https://api.twitch.tv/helix/streams?user_login={username}',
                headers=headers
            ) as response:
                return await response.json()

class DiscordWebhook:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_notification(self, message: str):
        """Send Discord notification"""
        async with aiohttp.ClientSession() as session:
            payload = {"content": message}
            async with session.post(self.webhook_url, json=payload) as response:
                return response.status == 204
```

---

## Security Considerations

### Token Security

- **Never commit tokens** to version control
- **Use environment variables** for all secrets
- **Rotate tokens regularly** (every 60 days recommended)
- **Use minimum required scopes** (chat:read, chat:edit)

### Input Validation

```python
# Validate user input
import re

def validate_username(username: str) -> bool:
    """Validate Twitch username format"""
    return bool(re.match(r'^[a-zA-Z0-9_]{1,25}$', username))

def sanitize_message(message: str) -> str:
    """Sanitize chat messages"""
    # Remove potentially harmful content
    return message[:500]  # Limit length
```

### Database Security

```python
# Always use parameterized queries
async def safe_query(self, username: str):
    # GOOD: Parameterized
    await db.execute('SELECT * FROM users WHERE username = ?', (username,))
    
    # BAD: String concatenation (SQL injection risk)
    # await db.execute(f'SELECT * FROM users WHERE username = "{username}"')
```

### Web Interface Security

```python
# CSRF protection
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/sensitive-endpoint', methods=['POST'])
@limiter.limit("5 per minute")
def sensitive_endpoint():
    pass
```

---

## Performance Tuning

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_users_xp ON users(xp DESC);
CREATE INDEX idx_users_last_seen ON users(last_seen);
CREATE INDEX idx_chat_logs_timestamp ON chat_logs(timestamp);
CREATE INDEX idx_redemptions_username ON redemptions(username);
```

### Memory Management

```python
# Limit chat log storage
class Storage:
    async def cleanup_old_logs(self, days: int = 30):
        """Remove chat logs older than N days"""
        cutoff = int(time.time()) - (days * 86400)
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('DELETE FROM chat_logs WHERE timestamp < ?', (cutoff,))
                await db.commit()
```

### Async Performance

```python
# Use connection pooling for database
class Storage:
    def __init__(self, db_path: str, pool_size: int = 10):
        self.db_path = db_path
        self.pool = asyncio.BoundedSemaphore(pool_size)
    
    async def execute_query(self, query: str, params: tuple):
        async with self.pool:
            async with aiosqlite.connect(self.db_path) as db:
                return await db.execute(query, params)
```

### Caching

```python
from functools import lru_cache
import asyncio

class CachedStorage:
    def __init__(self):
        self._user_cache = {}
        self._cache_ttl = 300  # 5 minutes
    
    @lru_cache(maxsize=128)
    async def get_user_cached(self, username: str):
        """Cached user lookup"""
        cache_key = f"user:{username}"
        now = time.time()
        
        if cache_key in self._user_cache:
            cached_data, timestamp = self._user_cache[cache_key]
            if now - timestamp < self._cache_ttl:
                return cached_data
        
        # Fetch from database
        user_data = await self.get_or_create_user(username)
        self._user_cache[cache_key] = (user_data, now)
        return user_data
```

---

## Troubleshooting

### Common Issues

**Bot won't connect:**
```python
# Debug connection issues
import logging
logging.basicConfig(level=logging.DEBUG)

# Check token format
token = os.getenv('TWITCH_TOKEN')
if not token.startswith('oauth:'):
    print(f"Invalid token format: {token}")
```

**Database locked errors:**
```python
# Use connection timeout
async with aiosqlite.connect(self.db_path, timeout=30.0) as db:
    # Your operations
```

**Memory leaks:**
```python
# Monitor memory usage
import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB
```

**High CPU usage:**
```python
# Profile async tasks
import asyncio

# Add task monitoring
async def monitor_tasks():
    while True:
        tasks = [t for t in asyncio.all_tasks() if not t.done()]
        print(f"Active tasks: {len(tasks)}")
        await asyncio.sleep(30)
```

### Debugging Tools

```python
# Enable debug mode
import logging
logging.getLogger('bot').setLevel(logging.DEBUG)

# Add performance timing
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

# Monitor database queries
@timing_decorator
async def timed_query(self, query: str, params: tuple):
    # Your database operation
```

### Log Analysis

```bash
# Filter logs by level
grep "ERROR" logs/bakebot.log

# Monitor real-time logs
tail -f logs/bakebot.log

# Analyze performance
grep "took" logs/bakebot.log | sort -k3 -n
```

---

## Contributing

### Code Style

```python
# Follow PEP 8
# Use type hints
def process_user(user: Dict[str, Any]) -> Optional[str]:
    """Process user data and return status."""
    pass

# Use async/await consistently
async def async_operation():
    result = await some_async_function()
    return result

# Document functions
async def complex_function(param1: str, param2: int) -> bool:
    """
    Detailed description of what this function does.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
    
    Returns:
        Boolean indicating success/failure
    
    Raises:
        ValueError: If parameters are invalid
    """
    pass
```

### Testing

```python
# test_bot.py
import pytest
import asyncio
from bot.storage import Storage

@pytest.fixture
async def storage():
    storage = Storage(':memory:')  # Use in-memory database for tests
    await storage.init()
    return storage

@pytest.mark.asyncio
async def test_user_creation(storage):
    user = await storage.get_or_create_user('testuser')
    assert user['username'] == 'testuser'
    assert user['xp'] == 0
    assert user['tokens'] == 0

@pytest.mark.asyncio
async def test_xp_addition(storage):
    await storage.add_xp('testuser', 25)
    user = await storage.get_or_create_user('testuser')
    assert user['xp'] == 25
```

### Pull Request Guidelines

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/my-feature`
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Follow code style** guidelines
6. **Create pull request** with detailed description

---

## License & Legal

### Open Source License
This project is licensed under MIT License - see LICENSE file for details.

### Twitch Developer Agreement
By using this bot, you agree to comply with:
- [Twitch Developer Services Agreement](https://dev.twitch.tv/docs/terms)
- [Twitch Community Guidelines](https://safety.twitch.tv/s/article/Community-Guidelines)

### Data Privacy
- User chat data is stored locally only
- No data is transmitted to external services (except Twitch API)
- Users can request data deletion
- Implement proper data retention policies

---

*For additional help, create an issue on GitHub or refer to the main README.md for basic usage.*