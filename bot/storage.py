import aiosqlite
import asyncio
from typing import Optional, Dict, Any, List

DB_PATH = 'bot_data.sqlite3'

SCHEMA = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    xp INTEGER NOT NULL DEFAULT 0,
    tokens INTEGER NOT NULL DEFAULT 0,
    wins INTEGER NOT NULL DEFAULT 0,
    last_seen INTEGER NOT NULL DEFAULT 0,
    notes TEXT DEFAULT '',
    is_banned INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS redemptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    reward TEXT NOT NULL,
    cost INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS chat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    channel TEXT NOT NULL
);
'''

class Storage:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._lock = asyncio.Lock()

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript(SCHEMA)
            await db.commit()

    async def get_or_create_user(self, username: str) -> Dict[str, Any]:
        username = username.lower()
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('INSERT OR IGNORE INTO users(username) VALUES (?)', (username,))
                await db.commit()
                async with db.execute('SELECT username, xp, tokens, wins, last_seen, notes, is_banned FROM users WHERE username = ?', (username,)) as cur:
                    row = await cur.fetchone()
                    if not row:
                        raise RuntimeError('Failed to load or create user')
                    return {
                        'username': row[0], 'xp': row[1], 'tokens': row[2], 'wins': row[3], 
                        'last_seen': row[4], 'notes': row[5] or '', 'is_banned': bool(row[6])
                    }

    async def update_user(self, username: str, **fields):
        username = username.lower()
        if not fields:
            return
        set_clause = ', '.join(f'{k} = ?' for k in fields.keys())
        values = list(fields.values()) + [username]
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(f'UPDATE users SET {set_clause} WHERE username = ?', values)
                await db.commit()

    async def add_xp(self, username: str, amount: int):
        await self.update_user(username, xp=f'xp + {amount}')

    async def add_tokens(self, username: str, amount: int):
        await self.update_user(username, tokens=f'tokens + {amount}')

    async def add_win(self, username: str):
        await self.update_user(username, wins='wins + 1')

    async def set_last_seen(self, username: str, ts: int):
        await self.update_user(username, last_seen=ts)

    async def log_chat_message(self, username: str, message: str, channel: str):
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('INSERT INTO chat_logs(username, message, timestamp, channel) VALUES (?,?,?,?)', 
                                (username.lower(), message, int(asyncio.get_event_loop().time()), channel.lower()))
                await db.commit()

    async def record_redemption(self, username: str, reward: str, cost: int, created_at: int):
        username = username.lower()
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('INSERT INTO redemptions(username, reward, cost, created_at) VALUES (?,?,?,?)', (username, reward, cost, created_at))
                await db.commit()

    async def top_users_by_xp(self, limit: int = 10) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT username, xp, wins FROM users ORDER BY xp DESC LIMIT ?', (limit,)) as cur:
                rows = await cur.fetchall()
                return [{'username': r[0], 'xp': r[1], 'wins': r[2]} for r in rows]

    async def get_all_users(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT username, xp, tokens, wins, last_seen, notes, is_banned FROM users ORDER BY xp DESC') as cur:
                rows = await cur.fetchall()
                return [{'username': r[0], 'xp': r[1], 'tokens': r[2], 'wins': r[3], 
                        'last_seen': r[4], 'notes': r[5] or '', 'is_banned': bool(r[6])} for r in rows]

    async def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        username = username.lower()
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT username, xp, tokens, wins, last_seen, notes, is_banned FROM users WHERE username = ?', (username,)) as cur:
                row = await cur.fetchone()
                if row:
                    return {'username': row[0], 'xp': row[1], 'tokens': row[2], 'wins': row[3], 
                           'last_seen': row[4], 'notes': row[5] or '', 'is_banned': bool(row[6])}
                return None

    async def get_metadata(self, key: str) -> Optional[str]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT value FROM metadata WHERE key = ?', (key,)) as cur:
                row = await cur.fetchone()
                return row[0] if row else None

    async def set_metadata(self, key: str, value: str):
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('INSERT INTO metadata(key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, value))
                await db.commit()
