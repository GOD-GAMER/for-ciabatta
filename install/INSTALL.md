# BakeBot Installation Guide

This guide covers installing and launching BakeBot via the GUI, obtaining a Twitch OAuth token, and optionally wiring up EventSub for channel points.

## Quick Start (GUI)

1. Install Python 3.10+
2. Open a terminal in the project folder
3. Install dependencies:
   - pip install -r requirements.txt
4. Launch the GUI:
   - python -m bot.gui
5. In the GUI:
   - Click "Get Token" and sign in with your bot account
   - Enter your Twitch channel name
   - Click "Start Bot"
6. Open the leaderboard in a browser:
   - http://localhost:8080/leaderboard

## Getting a Twitch OAuth Token (built-in flow)

1. Create a Twitch Application at https://dev.twitch.tv/console/apps
2. Add a redirect URL: http://127.0.0.1:53682/callback
3. Copy the Client ID into the GUI (Twitch Client ID)
4. Click "Get Token" — a browser will request chat:read and chat:edit
5. The GUI captures the token automatically and fills it as `oauth:...`

Notes:
- Keep your token secret; revoke it from your Twitch security settings if needed.
- If a browser doesn’t open, copy the URL from the GUI log and open it manually.

## EventSub and Channel Points (optional)

BakeBot includes a minimal EventSub webhook listener for channel point redemptions.

Steps:
1. Set these in .env or via the GUI:
   - ENABLE_EVENTSUB=true
   - EVENTSUB_SECRET=<your-random-secret>
   - EVENTSUB_PORT=8081 (default)
2. Expose your local EventSub endpoint using a tunnel (ngrok/cloudflared) or port forwarding:
   - http(s)://YOUR_HOST:8081/eventsub
3. Create an EventSub subscription for:
   - channel.channel_points_custom_reward_redemption.add
4. In Twitch, create custom rewards and title them to match the bot mapping (editable in bot/commands.py):
   - "XP Boost" -> xp_boost
   - "Confetti" -> confetti
   - "Double XP (5 min)" -> doublexp
5. Redemptions will trigger the same effects as !redeem, without deducting in-bot tokens.

Troubleshooting:
- Signature verification errors: secret mismatch; ensure EVENTSUB_SECRET matches
- 403/timeout from Twitch: your tunnel/endpoint may be unreachable or missing HTTPS
- You can test rewards without EventSub using chat: !redeem xp_boost

---

## Port Forwarding and Firewall (Public Links)

Goal: make your BakeBot leaderboard (and optional EventSub) reachable from the internet so viewers can open links you share in chat.

Default ports
- Bot web/leaderboard: TCP 8080 (configurable via WEB_PORT)
- EventSub webhook (optional): TCP 8081 (configurable via EVENTSUB_PORT)

Before you start
- Decide which PC runs BakeBot. Reserve its LAN IP (DHCP reservation) so it doesn’t change.
- Find your PC LAN IP (Local IPv4) from the GUI Network tab or run: `ipconfig` (Windows) and look for "IPv4 Address".
- Add Windows Firewall rules for the ports (PowerShell below).
- If your ISP uses CGNAT (LTE/5G/WISP), port forwarding likely won’t work. Use a tunnel instead (see Tunnel Alternatives).

Generic router steps
1) Log in to your router admin page
   - Typical: http://192.168.0.1, http://192.168.1.1, http://192.168.50.1
2) Locate Port Forwarding / NAT / Virtual Server
3) Create a rule for BakeBot web
   - External/WAN Port: 8080 TCP
   - Internal/LAN IP: <your PC Local IPv4>
   - Internal Port: 8080 TCP
   - Description: BakeBot Web
4) (Optional) Create a rule for EventSub
   - External/WAN Port: 8081 TCP
   - Internal/LAN IP: <your PC Local IPv4>
   - Internal Port: 8081 TCP
   - Description: BakeBot EventSub
5) Apply/Save and reboot router if needed
6) Test from cellular data: http://YOUR_PUBLIC_IP:8080/leaderboard
7) In the GUI, set PUBLIC_BASE_URL to http://YOUR_PUBLIC_IP:8080 and Save

Router quick paths (brand-specific)
- TP?Link Archer (new UI): Advanced > NAT Forwarding > Virtual Servers > Add New
- TP?Link Archer (old UI): Forwarding > Virtual Servers > Add New
- TP?Link Deco: More > Advanced > NAT Forwarding > Add
- Netgear Nighthawk: Advanced > Advanced Setup > Port Forwarding/Triggering > Add Custom Service
- ASUSWRT (RT?AC/AX): WAN > Virtual Server / Port Forwarding > Add
- ASUS TUF/ROG: Advanced Settings > WAN > Port Forwarding
- Linksys Smart Wi?Fi: Security > Apps and Gaming > Single Port Forwarding
- D?Link: Features > Port Forwarding > Add Rule
- Ubiquiti UniFi / Dream Machine: Settings > Security & Gateway > Port Forwarding > Create New Rule
- MikroTik RouterOS: IP > Firewall > NAT > Add dstnat rule (dst-port 8080), then IP > Services if needed
- Zyxel: NAT > Port Forwarding > Add Rule
- Xfinity xFi (Comcast): xFi app > Network > Advanced Settings > Port Forwarding > Add Port Forward
- Verizon Fios (G3100/CR1000A): Advanced > Security > Port Forwarding > Add Rule
- AT&T BGW210/BGW320: Firewall > NAT/Gaming > Custom Service > Add
- Spectrum: Router admin or Spectrum App > Services > Router > Advanced > Port Forwarding
- BT Smart Hub 2: Advanced Settings > Port Forwarding > Add new rule
- Sky Q Hub: Advanced > Security > Port Forwarding > Add new rule
- Virgin Media Hub 3/4/5: Advanced Settings > Security > Port Forwarding > Create Rule
- Plusnet Hub: Advanced Settings > Port Forwarding > Add new rule
- TalkTalk: Internet > Port Forwarding > Add
- T?Mobile Home Internet: App > Network > Port Forwarding (may be blocked by CGNAT)
- Starlink: App > Advanced > Bypass mode + your own router; then forward on your router
- Huawei/ZTE CPE (4G/5G): Security > NAT > Port Forwarding (beware CGNAT)

Tips
- If the UI asks for “External” and “Internal” ports, set both to the same number (8080, 8081).
- Some UIs call this Virtual Server, NAT Mapping, or Pinholes.
- Create a DHCP reservation (Static Lease) for your PC so the LAN IP doesn’t change.

### Windows Firewall (PowerShell)
Run PowerShell as Administrator.

Open ports
- Allow BakeBot web (TCP 8080):
```
New-NetFirewallRule -DisplayName "BakeBot Web 8080" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8080
```
- Allow EventSub (TCP 8081):
```
New-NetFirewallRule -DisplayName "BakeBot EventSub 8081" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8081
```

Allow by program (python.exe)
```
$py = (Get-Command python).Source
New-NetFirewallRule -DisplayName "BakeBot Python" -Direction Inbound -Action Allow -Program $py
```

Verify / inspect
```
Get-NetFirewallRule | Where-Object DisplayName -like "*BakeBot*" | Format-Table -AutoSize
Get-NetTCPConnection -State Listen | Where-Object LocalPort -in 8080,8081 | Format-Table -AutoSize
# or
netstat -ano | findstr ":8080"
```

Remove rules
```
Remove-NetFirewallRule -DisplayName "BakeBot Web 8080"
Remove-NetFirewallRule -DisplayName "BakeBot EventSub 8081"
```

Find which process uses a port
```
Get-Process -Id (Get-NetTCPConnection -LocalPort 8080 | Select-Object -First 1).OwningProcess
```

### Tunnel Alternatives (no router changes)
- cloudflared: `cloudflared tunnel --url http://127.0.0.1:8080`
- ngrok: `ngrok http 8080`
Copy the printed https URL and set PUBLIC_BASE_URL in the GUI.

### Troubleshooting
- CGNAT: If your WAN IP (router status) is 100.64.x.x/10.x.x.x, the ISP is NATing you. Use a tunnel.
- Double NAT: Two routers in series; either forward on both, or put one in Bridge/AP mode.
- ISP modem/router: Switch to Bridge/Pass-through to avoid double NAT.
- Firewall: Temporarily disable to test (not recommended to leave off). Re-enable and add proper rules.
- OS binding: The bot web binds to WEB_HOST. Use 0.0.0.0 to listen on all interfaces.
- Online test: Use https://canyouseeme.org with your port.
- Alternate ports: If blocked, try 8088/8089 and update GUI + router.
