import os
import hmac
import hashlib
import json
import asyncio
import logging
from aiohttp import web, ClientSession

# Minimal EventSub handler: verifies Twitch signatures and dispatches channel point redemptions

class EventSubServer:
    def __init__(self, storage, redeem_handler):
        self.storage = storage
        self.redeem_handler = redeem_handler
        self.secret = os.getenv('EVENTSUB_SECRET', 'changeme')
        self.session = None
        self._runner = None
        self._site = None
        self.logger = logging.getLogger('BakeBot.EventSub')

    async def start(self, host='127.0.0.1', port=8081):
        self.session = ClientSession()
        app = web.Application()
        app.add_routes([web.post('/eventsub', self._handle)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        self._runner = runner
        self._site = site
        self.logger.info('EventSub listening on http://%s:%s/eventsub', host, port)

    async def stop(self):
        self.logger.info('Stopping EventSub')
        if self._runner:
            await self._runner.cleanup()
        if self.session:
            await self.session.close()

    async def _handle(self, request: web.Request):
        body = await request.read()
        message_id = request.headers.get('Twitch-Eventsub-Message-Id', '')
        timestamp = request.headers.get('Twitch-Eventsub-Message-Timestamp', '')
        signature = request.headers.get('Twitch-Eventsub-Message-Signature', '')
        payload = body.decode()
        computed = 'sha256=' + hmac.new(self.secret.encode(), (message_id + timestamp + payload).encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, computed):
            self.logger.warning('Signature mismatch id=%s ts=%s', message_id, timestamp)
            return web.Response(status=403)
        data = json.loads(payload)
        msg_type = request.headers.get('Twitch-Eventsub-Message-Type')
        self.logger.debug('EventSub message type=%s id=%s', msg_type, message_id)
        if msg_type == 'webhook_callback_verification':
            self.logger.info('Verification challenge received')
            return web.Response(text=data['challenge'])
        if msg_type == 'notification':
            event = data.get('event', {})
            sub_type = data.get('subscription', {}).get('type')
            self.logger.info('Notification type=%s user=%s', sub_type, event.get('user_name'))
            if sub_type == 'channel.channel_points_custom_reward_redemption.add':
                user = event.get('user_name', '')
                reward = event.get('reward', {}).get('title', '')
                asyncio.create_task(self.redeem_handler(user, reward))
        return web.Response(status=200)
