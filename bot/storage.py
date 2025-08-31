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
    last_seen INTEGER NOT NULL DEFAULT 0
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
                async with db.execute('SELECT username, xp, tokens, wins, last_seen FROM users WHERE username = ?', (username,)) as cur:
                    row = await cur.fetchone()
                    if not row:
                        raise RuntimeError('Failed to load or create user')
                    return {
                        'username': row[0], 'xp': row[1], 'tokens': row[2], 'wins': row[3], 'last_seen': row[4]
                    }

    async def add_xp(self, username: str, amount: int):
        username = username.lower()
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('UPDATE users SET xp = xp + ? WHERE username = ?', (amount, username))
                await db.commit()

    async def add_tokens(self, username: str, amount: int):
        username = username.lower()
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('UPDATE users SET tokens = tokens + ? WHERE username = ?', (amount, username))
                await db.commit()

    async def add_win(self, username: str):
        username = username.lower()
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('UPDATE users SET wins = wins + 1 WHERE username = ?', (username,))
                await db.commit()

    async def set_last_seen(self, username: str, ts: int):
        username = username.lower()
        async with self._lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('UPDATE users SET last_seen = ? WHERE username = ?', (ts, username))
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

    async def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        username = username.lower()
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT username, xp, tokens, wins, last_seen FROM users WHERE username = ?', (username,)) as cur:
                row = await cur.fetchone()
                if row:
                    return {'username': row[0], 'xp': row[1], 'tokens': row[2], 'wins': row[3], 'last_seen': row[4]}
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
