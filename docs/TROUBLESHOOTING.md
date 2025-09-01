# Troubleshooting

Common issues and quick fixes.

## Bot won’t start
- Ensure `TWITCH_TOKEN` and `TWITCH_CHANNEL` are set in the GUI
- Click Save Configuration, then Start Bot

## Leaderboard not visible
- Bot must be running
- Ensure your web port is correct (default 8080)
- If accessing from another device or the internet, use `WEB_HOST=0.0.0.0` and configure router or tunnel

## Port forwarding doesn’t work
- See [Port Forwarding](./PORT_FORWARDING.md)
- Check Windows Firewall rules
- Some ISPs use CGNAT; use a tunnel (ngrok/cloudflared)

## EventSub validation fails (403)
- Twitch requires HTTPS
- The secret must match `EVENTSUB_SECRET`
- The callback must be `PUBLIC_BASE_URL + /eventsub`

## Games/commands slow or unresponsive
- Set `LOG_LEVEL=DEBUG` and watch the Logs page
- Check internet connectivity and Twitch status

## Database locked
- If you killed the process, SQLite may be busy; wait or restart Windows
- Avoid multiple instances writing to the DB at the same time
