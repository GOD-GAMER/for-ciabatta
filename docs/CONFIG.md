# Configuration (.env)

Environment variables (GUI writes these to .env):

- TWITCH_TOKEN: oauth:... (from GUI Get Token)
- TWITCH_CLIENT_ID: Client ID (only needed for GUI token flow)
- TWITCH_CHANNEL: your channel login name
- PREFIX: command prefix, default '!'
- ENABLE_EVENTSUB: true/false to enable channel points listener
- EVENTSUB_SECRET: shared secret with Twitch EventSub
- EVENTSUB_PORT: local port for EventSub, default 8081
- WEB_HOST: web server host, default 127.0.0.1
- WEB_PORT: web server port, default 8080

Notes:
- If you change WEB_PORT or HOST, update any shared URLs/QRs.
- Ensure redirect URI is added in your Twitch app for Get Token:
  - http://127.0.0.1:53682/callback
