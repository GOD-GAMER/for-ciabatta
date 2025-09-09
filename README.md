# 🥖 BakeBot – Twitch Chat Bot for Streamers (In‑Depth Guide)

[![GitHub release](https://img.shields.io/github/v/release/GOD-GAMER/for-ciabatta)](https://github.com/GOD-GAMER/for-ciabatta/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

BakeBot is a fun, baking‑themed Twitch bot with mini‑games, a token economy, a public leaderboard, recipe sharing, and a modern web dashboard. It also ships with a Twitch Extension (Panel) so viewers can see your leaderboard and recipes right inside Twitch.

---

## 📚 Table of Contents
- Overview
- Features
- Architecture
- Requirements
- Quick Start (5 minutes)
- Detailed Setup
- Configuration Reference (.env)
- Dashboard Guide
- Feature Toggles (Enable/Disable features)
- Mini‑Games & Commands
- Token Economy
- Recipes Manager
- EventSub (Channel Points)
- Networking & Public Sharing
- Twitch Extension (Panel)
- Public/Developer API Endpoints
- Data & Storage (SQLite)
- Backup & Restore
- Security Best Practices
- Troubleshooting & FAQ
- Contributing & Roadmap
- License

See also the Wiki for a step‑by‑step, friendly guide: docs/wiki/Home.md

---

## 🌟 Overview
BakeBot makes your chat more interactive with simple games and rewards. It is designed for streamers who want zero‑setup persistence (SQLite), a one‑click dashboard, and public links to share with viewers.

Key goals:
- Easy to install and run locally
- No cloud databases or servers required
- Safe to share public links (leaderboard/recipes)
- Extensible and transparent (MIT‑licensed)

---

## ✨ Features
- Mini‑games: Guess the Ingredient, Oven Trivia, Seasonal Events, Bread Fights
- Token economy with shop, gifts, daily/hourly/work rewards
- Public pages: Leaderboard and Recipes
- Modern dashboard to start/stop the bot, configure, manage data
- Feature Toggles to enable/disable commands/games in one click
- EventSub integration for channel points (follows/subs/cheers/raids)
- Twitch Extension (Panel) that shows leaderboard and recipes on Twitch

---

## 🏗️ Architecture
- Twitch bot: Python + TwitchIO (async)
- Web dashboard: Flask + Socket.IO (bot.gui)
- Public web/API: AIOHTTP (bot.web)
- Data: SQLite (aiosqlite) – single file database
- Templates: Vanilla HTML/CSS/JS

High‑level modules:
- bot/bot.py – main bot lifecycle
- bot/commands.py – chat commands, games, economy
- bot/games.py – game mechanics (bread fights, trivia)
- bot/gui.py – dashboard server (port 5000 by default)
- bot/web.py – public web/API (port 8080 by default)
- bot/storage.py – SQLite schema + data access
- bot/eventsub.py – EventSub handler and mapping

---

## 🧰 Requirements
- Windows 10/11, macOS, or Linux
- Python 3.10+
- Twitch account for the bot

Optional
- A Twitch Developer Application (for OAuth Wizard)
- Tunnel tool (ngrok/cloudflared) if you want to share publicly

---

## 🚀 Quick Start (5 minutes)
1) Install Python 3.10+: https://python.org/downloads
2) Download latest ZIP: https://github.com/GOD-GAMER/for-ciabatta/releases
3) Extract to a folder (e.g., Desktop/for-ciabatta)
4) Open a terminal in the folder, then:
```
pip install -r requirements.txt
python -m bot.gui
```
5) In the dashboard (opens automatically):
- Click OAuth Wizard → Authorize
- Set Twitch Channel → Save Configuration
- Click Start Bot → Type !help in chat

---

## 🔍 Detailed Setup
- Windows: open PowerShell in the project folder
- macOS/Linux: open Terminal

Create a virtual environment (optional):
```
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```
Install dependencies and launch dashboard:
```
pip install -r requirements.txt
python -m bot.gui
```
Dashboard: http://127.0.0.1:5000  
Public web (when bot is running): http://localhost:8080

---

## ⚙️ Configuration Reference (.env)
These are edited via the dashboard, but you can also set them in a .env file.

- TWITCH_TOKEN – oauth:xxxxx (from OAuth Wizard)
- TWITCH_CLIENT_ID – your Twitch app client ID (optional for wizard)
- TWITCH_CHANNEL – your channel (lowercase)
- PREFIX – command prefix, default !
- WEB_HOST – 0.0.0.0 for LAN/public, 127.0.0.1 for local only
- WEB_PORT – default 8080 (public web)
- GUI_HOST – default 127.0.0.1 (dashboard)
- GUI_PORT – default 5000 (dashboard)
- PUBLIC_BASE_URL – https://your‑public‑host (for links and extension)
- ENABLE_EVENTSUB – true/false
- EVENTSUB_PORT – default 8081
- EVENTSUB_SECRET – random secret for Twitch signature checks

Advanced
- LOG_LEVEL – DEBUG/INFO/WARNING/ERROR

---

## 🖥️ Dashboard Guide
Tabs:
- Control – Start/Stop bot, status, quick links
- Configuration – Twitch + web settings
- Toggles – Enable/disable commands, games, economy
- Network – Local/Public IP helpers, link builders
- EventSub – Enable, secret/port, mapping JSON
- Recipes – Add single or bulk, edit, reorder, visibility

See docs/wiki/Dashboard.md for screenshots and details.

---

## 🎚️ Feature Toggles
You can instantly enable/disable:
- All commands/games/economy via group toggles
- Individual commands (e.g., commands.guess)
- Game systems (games.bread_fights)
- Economy features (economy.gifting)

Implementation notes:
- Flags persisted in metadata key feature_flags (JSON)
- Bot checks flags before executing commands/games (no restart required)

See docs/wiki/Toggles.md for examples.

---

## 🎮 Mini‑Games & Commands
Viewer commands:
- !help, !tokens, !daily, !hourly, !work
- !shop, !buy <item>, !gift @user <amount>
- !level, !leaderboard, !recipes
- !guess, !oventrivia, !seasonal, !fight @user, !accept

Admin/broadcaster:
- !give @user <amount>, !ban @user, !unban @user
- !title @user <text>, !untitle @user

Full command list: docs/COMMANDS.md and docs/wiki/Commands.md

---

## 💰 Token Economy
Earn: !daily, !hourly, !work, win games  
Spend: !shop, !buy, gift tokens to others  
Shop items include boosts (Double XP), titles, random rewards, and fight buffs.

See docs/wiki/Economy.md

---

## 🍪 Recipes Manager
- Add single recipes or import in bulk (JSON or Title|URL|Description lines)
- Toggle visibility, change order, edit inline
- Public page: http://localhost:8080/recipes

Step‑by‑step guide: docs/wiki/Recipes.md

---

## 🧩 EventSub (Channel Points)
- Enable in dashboard, set secret and port
- Expose HTTPS endpoint via tunnel or reverse proxy
- Create subscriptions (e.g., channel_points redemptions)
- Map events to XP/tokens with cooldowns via JSON

Guide: docs/wiki/EventSub.md

---

## 🌐 Networking & Public Sharing
Options:
- Port forwarding on your router (TCP 8080)
- Tunnels (ngrok/cloudflared) – recommended for simplicity

After you have a public URL, set PUBLIC_BASE_URL in the dashboard so the bot and extension share correct links.  
Guides: docs/wiki/Networking.md and docs/PORT_FORWARDING.md

---

## 🎛️ Twitch Extension (Panel)
A standalone Panel extension is included (twitch-extension/):
- Panel files: panel.html, panel.js, styles.css
- Broadcaster config: config.html, config.js

Data sources (served by the bot):
- GET {PUBLIC_BASE_URL}/ext/leaderboard → { data: [{ username, xp, wins }] }
- GET {PUBLIC_BASE_URL}/ext/recipes → { data: [{ title, url, description }] }

How to publish:
1) Create an Extension in Twitch console (Panel)  
2) Upload panel.html, panel.js, styles.css, config.html, config.js  
3) Set the config page and panel view  
4) In the config page, enter PUBLIC_BASE_URL (HTTPS)  
5) Start BakeBot (public endpoints must be reachable)

See twitch-extension/README.md

---

## 📡 Public & Developer API Endpoints
HTML pages
- GET /leaderboard – public leaderboard page
- GET /recipes – public recipes page

JSON (public)
- GET /ext/leaderboard → { data: [{ username, xp, wins }] }
- GET /ext/recipes → { data: [{ title, url, description }] }

JSON (admin/dashboard use)
- GET /api/users → list all users
- POST /api/users/update → { username, xp?, tokens?, wins?, notes?, is_banned? }
- GET /api/chat_logs?username=&limit=100
- GET /api/recipes → { data: [...] }
- POST /api/recipes → create one
- PUT /api/recipes/{id} → update
- DELETE /api/recipes/{id} → delete
- POST /api/recipes/bulk → bulk insert array
- GET /qr?url=... → PNG QR code of a URL

---

## 🗄️ Data & Storage (SQLite)
Schema summary (bot/storage.py):
- users (username, xp, tokens, wins, last_seen, notes, is_banned)
- redemptions (username, reward, cost, created_at)
- metadata (key, value)
- chat_logs (username, message, timestamp, channel)
- recipes (title, url, description, visible, ord, created_at)

The database file is bot_data.sqlite3 (auto‑created).

---

## 💾 Backup & Restore
- Backup: copy bot_data.sqlite3 while the bot is stopped
- Restore: replace the file and restart the bot
- Optional: export selected tables to CSV using sqlite3 CLI

---

## 🔐 Security Best Practices
- Never commit or share your .env or Twitch token
- Keep the dashboard private (127.0.0.1)
- Use HTTPS for public endpoints and EventSub
- Rotate EVENTSUB_SECRET periodically
- Moderate which features are enabled via Toggles

More: docs/wiki/Security.md

---

## 🆘 Troubleshooting & FAQ
Common issues:
- Bot won’t start → set Twitch Channel and complete OAuth Wizard
- Commands don’t respond → ensure status says Running, then !help
- Leaderboard blank → bot must be running; check WEB_PORT and firewall
- EventSub failing → must be HTTPS; secret must match

See docs/wiki/Troubleshooting.md and docs/wiki/FAQ.md

---

## 🤝 Contributing & Roadmap
Contributions welcome!  
Ideas:
- More mini‑games and shop items
- Panel: more views (top tokens, recent winners)
- Admin tools: in‑GUI user editor
- EBS for secure signed requests (optional)

How to contribute:
1) Fork repo → create a feature branch
2) Make changes with tests if applicable
3) Submit a pull request

---

## 📄 License
MIT – see LICENSE

---

Made with 🍞 for the Twitch streaming community.
