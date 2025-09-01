# Web & Hosting (Leaderboard, Public Links)

BakeBot exposes:
- Leaderboard/recipes pages for viewers
- JSON APIs for users and logs

## Ports
- Web (leaderboard/APIs): TCP 8080 (configurable via `WEB_PORT`)
- EventSub webhook (optional): TCP 8081 (configurable via `EVENTSUB_PORT`)

## Options to Share Publicly

### A) Port Forwarding (router)
- Forward external TCP 8080 to your PC’s Local IPv4 on TCP 8080
- Test: `http://YOUR_PUBLIC_IP:8080/leaderboard`
- Set `PUBLIC_BASE_URL` in the GUI to `http://YOUR_PUBLIC_IP:8080`
- Also forward 8081 if you use EventSub

See [Port Forwarding](./PORT_FORWARDING.md) for brand?specific paths and Windows Firewall commands.

### B) Tunnel (no router changes)
- cloudflared: `cloudflared tunnel --url http://127.0.0.1:8080`
- ngrok: `ngrok http 8080`
- Copy the printed `https://...` URL and set it as `PUBLIC_BASE_URL`

## Security
- Keep the GUI on `127.0.0.1:5000` or behind a reverse proxy
- Only share the public web (leaderboard) outside
- Use HTTPS when possible

## Troubleshooting
- “Site not reachable”: check Windows Firewall and that the bot is running
- “Timed out” from outside: router forwarding missing or CGNAT – use a tunnel
