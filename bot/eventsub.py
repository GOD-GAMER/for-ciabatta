import os
import hmac
import hashlib
import json
import asyncio
from aiohttp import web, ClientSession

# Minimal EventSub handler: verifies Twitch signatures and dispatches channel point redemptions
# This provides a simple local webhook server. For production, use a public HTTPS endpoint and proper secret management.

class EventSubServer:
    def __init__(self, storage, redeem_handler):
        self.storage = storage
        self.redeem_handler = redeem_handler
        self.secret = os.getenv('EVENTSUB_SECRET', 'changeme')
        self.session = None

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
        print(f'EventSub listening on http://{host}:{port}/eventsub')

    async def stop(self):
        if self._runner:
            await self._runner.cleanup()
        if self.session:
            await self.session.close()

    async def _handle(self, request: web.Request):
        body = await request.read()
        # Verify signature
        message_id = request.headers.get('Twitch-Eventsub-Message-Id', '')
        timestamp = request.headers.get('Twitch-Eventsub-Message-Timestamp', '')
        signature = request.headers.get('Twitch-Eventsub-Message-Signature', '')
        computed = 'sha256=' + hmac.new(self.secret.encode(), (message_id + timestamp + body.decode()).encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, computed):
            return web.Response(status=403)
        data = json.loads(body.decode())
        msg_type = request.headers.get('Twitch-Eventsub-Message-Type')
        if msg_type == 'webhook_callback_verification':
            return web.Response(text=data['challenge'])
        if msg_type == 'notification':
            event = data.get('event', {})
            if data.get('subscription', {}).get('type') == 'channel.channel_points_custom_reward_redemption.add':
                # Normalize to our redeem handler
                user = event.get('user_name', '')
                reward = event.get('reward', {}).get('title', '')
                asyncio.create_task(self.redeem_handler(user, reward))
        return web.Response(status=200)
