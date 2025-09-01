# BakeBot

A cozy Twitch baking-themed chat bot with mini-games, token economy, bread fights, and a modern web dashboard. Built with Python (TwitchIO, Flask-SocketIO, AIOHTTP) and SQLite.

---

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Run the GUI](#run-the-gui)
- [Configure the Bot](#configure-the-bot)
- [Share Public Links (Port Forwarding or Tunnel)](#share-public-links-port-forwarding-or-tunnel)
- [EventSub (Channel Points)](#eventsub-channel-points)
- [Commands (Quick Reference)](#commands-quick-reference)
- [Recipes Manager](#recipes-manager)
- [Production Notes](#production-notes)
- [Troubleshooting](#troubleshooting)
- [Security Best Practices](#security-best-practices)
- [License](#license)

---

## Features
- Baking mini-games: Guess the Ingredient, Oven Trivia, Seasonal events
- PvP Bread Fights: turn-based combat with knowledge questions and stats
- Token economy: shop, daily/hourly, work system, gifting, admin tools
- Persistent storage: SQLite database, zero-setup
- Web dashboard: start/stop bot, configure, logs, users, games, shop
- Public web: leaderboard, simple recipes page, JSON APIs
- Optional Twitch EventSub for channel points

---

## Quick Start
1) Install Python 3.10+
2) Install dependencies
   - Windows PowerShell
     - python -m pip install --upgrade pip
     - pip install -r requirements.txt
3) Run the GUI
   - python -m bot.gui
4) In your browser (opens automatically):
   - Click OAuth Wizard to get a chat token
   - Enter your Twitch channel
   - Save Configuration
   - Click Start Bot
5) Open the leaderboard
   - http://localhost:8080/leaderboard

---

## Installation
- Python 3.10+ required
- Recommended: a virtual environment
  - py -3 -m venv .venv
  - .\.venv\Scripts\Activate
  - pip install -r requirements.txt

---

## Run the GUI
Start the dashboard locally:
- python -m bot.gui
- Opens at: http://127.0.0.1:5000

If a browser doesn’t open, copy the link from the terminal and paste it manually.

---

## Configure the Bot
Open the dashboard and go to Configuration.
- Twitch OAuth Token: Click OAuth Wizard to obtain one (chat:read, chat:edit)
- Twitch Channel: yourchannel (lowercase)
- Optional:
  - PREFIX (default !)
  - WEB_HOST (0.0.0.0 for LAN/public, 127.0.0.1 for local only)
  - WEB_PORT (default 8080)
  - PUBLIC_BASE_URL (for public links in chat, see next section)
- Save Configuration ? Start Bot

---

## Share Public Links (Port Forwarding or Tunnel)
You can share your leaderboard publicly via:

Option A) Port Forwarding (router)
- Forward external TCP 8080 ? your PC’s Local IPv4 on TCP 8080
- Test from mobile data: http://YOUR_PUBLIC_IP:8080/leaderboard
- In the GUI, set PUBLIC_BASE_URL to http://YOUR_PUBLIC_IP:8080 and Save
- Detailed brand-specific steps and Windows Firewall commands:
  - See install/INSTALL.md (Port Forwarding and Firewall section)

Option B) Tunnel (no router changes)
- cloudflared: cloudflared tunnel --url http://127.0.0.1:8080
- ngrok: ngrok http 8080
- Copy the https URL and set PUBLIC_BASE_URL to it in the GUI

Network automation in the GUI
- Network tab shows Local IPv4 and Public IP
- One-click copy of a shareable leaderboard link

---

## EventSub (Channel Points)
Optional integration for custom reward redemptions.
1) In Configuration/EventSub tabs:
   - ENABLE_EVENTSUB=true
   - EVENTSUB_SECRET: a long random value
   - EVENTSUB_PORT: 8081 (default)
2) Expose https://YOUR_HOST:8081/eventsub via tunnel or port forwarding
3) Start the bot
4) In Twitch Developer Console ? EventSub ? create subscription:
   - Type: channel.channel_points_custom_reward_redemption.add
   - Callback: PUBLIC_BASE_URL + /eventsub
   - Secret: same as EVENTSUB_SECRET
5) Redeem rewards and watch the GUI logs

More details and examples: docs/EVENTSUB.md (if provided) or install/INSTALL.md.

---

## Commands (Quick Reference)
Core
- !help – show help
- !leaderboard – link to leaderboard
- !level – show your stats

Economy
- !tokens – show balance
- !daily – daily reward
- !hourly – hourly reward
- !work – earn a few tokens
- !shop – list shop items
- !buy <item> – purchase item
- !gift @user <amount> – gift tokens

Games
- !guess – Guess the Ingredient
- !oventrivia – Baking trivia
- !seasonal – Seasonal event

Bread Fights
- !fight @user – challenge
- !accept – accept a challenge

Admin (broadcaster)
- !ban @user, !unban @user
- !give @user <amount>
- !title @user <Title>, !untitle @user
- !note @user <text>

---

## Recipes Manager
- Add and edit recipes from the GUI (Recipes tab if enabled)
- Public page: http://HOST:PORT/recipes

---

## Production Notes
- Run the GUI behind a reverse proxy (Caddy/Nginx) or provide real TLS certs
- Environment examples:
  - GUI_HOST=127.0.0.1, GUI_PORT=5000 (reverse proxy binds public HTTPS)
  - For direct HTTPS, set GUI_CERT_FILE and GUI_KEY_FILE and run python -m bot.gui
- Keep the GUI port private; only the public web (leaderboard) needs exposure

---

## Troubleshooting
- Bot won’t start: ensure TWITCH_TOKEN and TWITCH_CHANNEL are set, then Save
- Nothing loads at /leaderboard: bot must be running and bound to WEB_HOST/WEB_PORT
- Public not reachable: forward TCP port or use a tunnel; verify Windows Firewall rules
- EventSub 403/timeout: use HTTPS, confirm secret and callback URL
- See install/INSTALL.md for Windows Firewall commands and router paths

---

## Security Best Practices
- Do not share or commit tokens; keep .env private
- Limit exposure: keep the GUI private; only share the public web as needed
- Use HTTPS for EventSub and public sharing when possible

---

## License
MIT
