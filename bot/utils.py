import asyncio
import time
from collections import defaultdict
from typing import Dict, Callable

class CooldownManager:
    def __init__(self):
        self._cooldowns: Dict[str, float] = {}

    def check(self, key: str, seconds: float) -> bool:
        now = time.time()
        last = self._cooldowns.get(key, 0)
        if now - last >= seconds:
            self._cooldowns[key] = now
            return True
        return False

class RateLimiter:
    def __init__(self, max_per_window: int = 20, window_seconds: int = 30):
        self.max_per_window = max_per_window
        self.window_seconds = window_seconds
        self.history: Dict[str, list] = defaultdict(list)

    def allow(self, user: str) -> bool:
        now = time.time()
        window = self.history[user]
        window[:] = [t for t in window if now - t < self.window_seconds]
        if len(window) < self.max_per_window:
            window.append(now)
            return True
        return False

async def run_with_timeout(coro, timeout: float):
    return await asyncio.wait_for(coro, timeout)
