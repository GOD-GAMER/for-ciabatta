import os
import asyncio
import time
from twitchio.ext import commands as tcommands
from dotenv import load_dotenv

from .storage import Storage
from .utils import CooldownManager, RateLimiter
from .games import BakingGames
from .commands import CommandHandler
from .web import create_app
from .eventsub import EventSubServer
from aiohttp import web

class TwitchContextWrapper:
    def __init__(self, ctx):
        self.ctx = ctx
    async def send(self, message: str):
        await self.ctx.send(message)

class BakeBot(tcommands.Bot):
    def __init__(self):
        load_dotenv()
        token = os.getenv('TWITCH_TOKEN')
        client_id = os.getenv('TWITCH_CLIENT_ID')
        channel = os.getenv('TWITCH_CHANNEL')
        if not token or not channel:
            raise RuntimeError('Missing TWITCH_TOKEN or TWITCH_CHANNEL in environment')
        prefix = os.getenv('PREFIX', '!')
        super().__init__(token=token, prefix=prefix, initial_channels=[channel])
        self._prefix = prefix
        self.storage = Storage()
        self.cooldowns = CooldownManager()
        self.rate_limiter = RateLimiter(max_per_window=8, window_seconds=10)
        self.web_runner = None
        self.web_site = None
        self.eventsub: EventSubServer | None = None

        async def award_cb(user):
            await self.command_handler.award_participation(user)
        async def win_cb(user):
            await self.command_handler.award_win(user)

        self.games = BakingGames(award_cb, win_cb)
        self.command_handler = CommandHandler(self.storage, self.games, self.cooldowns, self.rate_limiter, {
            'leaderboard': f"http://{os.getenv('WEB_HOST', '127.0.0.1')}:{os.getenv('WEB_PORT', '8080')}/leaderboard"
        })

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        await self.storage.init()
        # Load season from metadata
        season = await self.storage.get_metadata('season')
        if season:
            self.games.set_season(season or None)
        await self.start_web()
        # Optionally start EventSub
        if os.getenv('ENABLE_EVENTSUB', 'false').lower() in ('1','true','yes'):
            self.eventsub = EventSubServer(self.storage, self.on_channel_point_redeem)
            await self.eventsub.start(host='127.0.0.1', port=int(os.getenv('EVENTSUB_PORT','8081')))

    async def event_message(self, message):
        if message.echo:
            return
        author = message.author.name.lower()
        await self.storage.get_or_create_user(author)
        # Participation XP once every 15s per user
        if self.cooldowns.check(f"xp:{author}", 15):
            await self.command_handler.award_participation(author)
        # Games capture
        resp = await self.games.on_message(author, message.content)
        if resp:
            await message.channel.send(resp)
            return
        # Commands
        if message.content.startswith(self._prefix):
            ctx = TwitchContextWrapper(message.channel)
            await self.command_handler.handle(ctx, author, message.content)

    async def on_channel_point_redeem(self, user: str, reward_title: str):
        # Map reward title to internal reward and apply without token deduction
        class DummyCtx:
            skip_token_check = True
            async def send(self, msg: str):
                pass
        key = self.command_handler.channel_point_map.get(reward_title)
        if key:
            await self.command_handler.apply_reward(DummyCtx(), user.lower(), key)

    async def start_web(self):
        app = await create_app(self.storage.db_path if hasattr(self.storage, 'db_path') else 'bot_data.sqlite3')
        runner = web.AppRunner(app)
        await runner.setup()
        host = os.getenv('WEB_HOST', '127.0.0.1')
        port = int(os.getenv('WEB_PORT', '8080'))
        site = web.TCPSite(runner, host, port)
        await site.start()
        self.web_runner = runner
        self.web_site = site
        print(f'Web server running at http://{host}:{port}')

    async def stop_web(self):
        if self.web_runner:
            await self.web_runner.cleanup()
            self.web_runner = None
            self.web_site = None
        if self.eventsub:
            await self.eventsub.stop()
            self.eventsub = None

    async def shutdown(self):
        await self.stop_web()
        await self.close()


def main():
    bot = BakeBot()
    bot.run()

if __name__ == '__main__':
    main()
