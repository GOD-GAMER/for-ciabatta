# Networking & Sharing

## Local Access
- Leaderboard: http://localhost:8080/leaderboard
- Recipes: http://localhost:8080/recipes

## Public Sharing Options
1) Port Forwarding on your router (TCP 8080)  
2) Tunnel services like ngrok or cloudflared

## Steps (Tunnel Example)
1) Install ngrok
2) Run: `ngrok http 8080`
3) Copy the https URL and share it
4) Set PUBLIC_BASE_URL in dashboard

## Troubleshooting
- Check firewall allows inbound TCP 8080
- Avoid CGNAT limits with tunnels
- Verify service is running: bot must be started