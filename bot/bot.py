import os
import asyncio
import time
import logging
from twitchio.ext import commands as tcommands
from dotenv import load_dotenv

from .storage import Storage
from .utils import CooldownManager, RateLimiter
from .games import BakingGames
from .commands import CommandHandler
from .web import create_app
from .eventsub import EventSubServer
from .logging_config import setup_logging
from aiohttp import web

class TwitchContextWrapper:
    def __init__(self, ctx):
        self.ctx = ctx
    async def send(self, message: str):
        await self.ctx.send(message)

class BakeBot(tcommands.Bot):
    def __init__(self):
        self.logger = setup_logging().getChild("BakeBot")
        load_dotenv()
        token = os.getenv('TWITCH_TOKEN')
        client_id = os.getenv('TWITCH_CLIENT_ID')
        channel = os.getenv('TWITCH_CHANNEL')
        if not token or not channel:
            self.logger.error('Missing TWITCH_TOKEN or TWITCH_CHANNEL in environment')
            raise RuntimeError('Missing TWITCH_TOKEN or TWITCH_CHANNEL in environment')
        prefix = os.getenv('PREFIX', '!')
        super().__init__(token=token, prefix=prefix, initial_channels=[channel])
        self._prefix = prefix
        self._channel = channel
        self.storage = Storage()
        self.cooldowns = CooldownManager()
        self.rate_limiter = RateLimiter(max_per_window=8, window_seconds=10)
        self.web_runner = None
        self.web_site = None
        self.eventsub: EventSubServer | None = None

        async def award_cb(user):
            self.logger.debug("Award participation XP to %s", user)
            await self.command_handler.award_participation(user)
        async def win_cb(user):
            self.logger.info("Game win by %s", user)
            await self.command_handler.award_win(user)

        self.games = BakingGames(award_cb, win_cb)
        self.command_handler = CommandHandler(self.storage, self.games, self.cooldowns, self.rate_limiter, {
            'leaderboard': f"http://{os.getenv('WEB_HOST', '127.0.0.1')}:{os.getenv('WEB_PORT', '8080')}/leaderboard"
        })
        self.logger.info('Bot initialized; prefix=%s channel=%s', self._prefix, channel)

    async def event_ready(self):
        self.logger.info('Logged in as %s', self.nick)
        await self.storage.init()
        # Load season from metadata
        season = await self.storage.get_metadata('season')
        self.logger.debug('Loaded season from metadata: %s', season)
        if season:
            self.games.set_season(season or None)
        await self.start_web()
        # Optionally start EventSub
        if os.getenv('ENABLE_EVENTSUB', 'false').lower() in ('1','true','yes'):
            try:
                self.eventsub = EventSubServer(self.storage, self.on_channel_point_redeem)
                await self.eventsub.start(host='127.0.0.1', port=int(os.getenv('EVENTSUB_PORT','8081')))
                self.logger.info('EventSub server started')
            except Exception as e:
                self.logger.exception('Failed to start EventSub: %s', e)

    async def event_message(self, message):
        try:
            if message.echo:
                return
            author = message.author.name.lower()
            self.logger.debug('Message from %s: %s', author, message.content)
            
            # Log chat message for persistence
            await self.storage.log_chat_message(author, message.content, self._channel)
            
            user = await self.storage.get_or_create_user(author)
            # Check if user is banned
            if user.get('is_banned', False):
                self.logger.debug('Ignoring message from banned user: %s', author)
                return
                
            # Update last seen
            await self.storage.set_last_seen(author, int(time.time()))
            
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
        except Exception:
            self.logger.exception('Error handling message')

    async def on_channel_point_redeem(self, user: str, reward_title: str):
        self.logger.info('Channel point redeem from %s: %s', user, reward_title)
        class DummyCtx:
            skip_token_check = True
            async def send(self, msg: str):
                pass
        key = self.command_handler.channel_point_map.get(reward_title)
        if key:
            await self.command_handler.apply_reward(DummyCtx(), user.lower(), key)
        else:
            self.logger.warning('Unmapped reward title: %s', reward_title)

    async def start_web(self):
        try:
            app = await create_app(self.storage.db_path if hasattr(self.storage, 'db_path') else 'bot_data.sqlite3')
            runner = web.AppRunner(app)
            await runner.setup()
            host = os.getenv('WEB_HOST', '127.0.0.1')
            port = int(os.getenv('WEB_PORT', '8080'))
            site = web.TCPSite(runner, host, port)
            await site.start()
            self.web_runner = runner
            self.web_site = site
            self.logger.info('Web server running at http://%s:%s', host, port)
        except Exception:
            self.logger.exception('Failed to start web server')
            raise

    async def stop_web(self):
        if self.web_runner:
            self.logger.info('Stopping web server')
            await self.web_runner.cleanup()
            self.web_runner = None
            self.web_site = None
        if self.eventsub:
            self.logger.info('Stopping EventSub server')
            await self.eventsub.stop()
            self.eventsub = None

    async def shutdown(self):
        self.logger.info('Shutdown requested')
        await self.stop_web()
        await self.close()


def main():
    bot = BakeBot()
    bot.run()

if __name__ == '__main__':
    main()
