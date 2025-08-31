# Troubleshooting

Bot won’t connect
- Token invalid or missing oauth: prefix — use GUI Get Token
- Channel name wrong — use lowercase login name

No messages sent
- Bot not a mod? Some messages may be rate-limited by Twitch
- Prefix mismatch — check PREFIX in .env

Leaderboard not loading
- Port 8080 busy — change WEB_PORT in .env

EventSub issues
- Signature failed — EVENTSUB_SECRET mismatch
- Twitch can’t reach you — tunnel not running or wrong URL
- Reward titles don’t match — edit channel_point_map in bot/commands.py
