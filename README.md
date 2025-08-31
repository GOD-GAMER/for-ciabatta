# BakeBot

A Twitch baking-themed chat bot with cozy mini-games, redemptions, a tiny leaderboard website, and a simple GUI. Built with Python, twitchio, aiosqlite, aiohttp, and tkinter.

---

## Features
- GUI-first setup (no external dependencies)
- Step-by-step OAuth token setup wizard
- Persistent SQLite storage (XP, tokens, wins, redemptions, chat logs)
- User management interface for streamers
- Baking games: Guess the Ingredient, Oven Timer Trivia, Seasonal Event
- XP and token economy with simple redemptions
- Lightweight web server (leaderboard, recipe links, QR generator)
- Optional EventSub listener for Channel Points
- Cooldowns and rate limits to reduce spam
- Complete data persistence - survives app restarts

---

## Requirements
- Python 3.10+ (with tkinter included)
- A Twitch account for your bot
- Optional: Twitch Developer Application (for OAuth and EventSub)

---

## Quick Start (GUI)
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the GUI
   ```bash
   python -m bot.gui
   ```
3. In the GUI:
   - Click "Setup OAuth" and follow the 4-step wizard
   - Enter your channel name
   - Click "Start Bot"
4. Open the leaderboard
   - Click "Open Leaderboard" or visit http://localhost:8080/leaderboard

---

## OAuth Token Setup (Built-in Wizard)

The GUI includes a complete 4-step setup wizard:

**Step 1:** Create Twitch Application
- Opens https://dev.twitch.tv/console/apps for you
- Guides you through app creation

**Step 2:** Enter Client ID  
- Paste your Twitch app's Client ID

**Step 3:** Get Authorization
- Generates OAuth URL automatically
- Copy or open in browser
- Handles the redirect for you

**Step 4:** Enter Token
- Paste the access_token from the URL
- Automatically adds oauth: prefix
- Saves securely to .env file

---

## Data Persistence

All data is automatically saved and persists between sessions:

- **User Data:** XP, tokens, wins, notes, ban status
- **Chat Logs:** Complete message history with timestamps  
- **Game Results:** Win/loss records and participation
- **Redemption History:** Complete transaction log
- **Bot Settings:** Configuration, seasons, metadata

Data is stored in `bot_data.sqlite3` and automatically loads on startup.

---

## User Management

Built-in user management interface:
- View all users sorted by XP
- Edit XP, tokens, wins for any user
- Add notes to users
- Ban/unban users
- View chat message history
- Export/import user data

Access via the "User Management" tab in the GUI.

---

## Configuration

All settings auto-save to .env:

| Key | Description | Default |
|-----|-------------|---------|
| TWITCH_TOKEN | OAuth token (starts with oauth:) | - |
| TWITCH_CLIENT_ID | For OAuth wizard | - |
| TWITCH_CHANNEL | Your channel login name | - |
| PREFIX | Command prefix | ! |
| ENABLE_EVENTSUB | Enable Channel Points listener | false |
| EVENTSUB_SECRET | Secret for EventSub signature verification | changeme |
| EVENTSUB_PORT | Local EventSub port | 8081 |
| WEB_HOST | Web server host | 127.0.0.1 |
| WEB_PORT | Web server port | 8080 |
| LOG_LEVEL | Log level: DEBUG/INFO/WARNING/ERROR | INFO |

---

## Commands (chat)
- !recipe - Share a cookie recipe link
- !bakeoff - Hype line and suggests games
- !ovenstatus - Fun oven status line
- !leaderboard - Post the leaderboard link
- !guess - Start Guess the Ingredient
- !oventrivia - Start Oven Timer Trivia
- !seasonal - Start a seasonal mini-game
- !setseason <name|off> - Broadcaster only (e.g., halloween, holiday)
- !redeem <xp_boost|confetti|doublexp> - Spend in-bot tokens

Cooldowns:
- Commands: 3s per user
- Participation XP: 15s per user
- Rate limit: 8 messages per 10s per user

---

## Games
- **Guess the Ingredient:** Bot posts a hint; first correct answer wins
- **Oven Timer Trivia:** Baking trivia; first correct answer wins  
- **Seasonal Event:** Themed mystery ingredient (season-dependent pool)

---

## XP, Tokens, Redemptions
- **Participation:** +1 XP per user every 15s
- **Win a game:** +25 XP and +5 tokens
- **!redeem xp_boost** ? +50 XP (costs 10 tokens)
- **!redeem confetti** ? fun effect (5 tokens)
- **!redeem doublexp** ? flavor message (20 tokens)

All data persists permanently in bot_data.sqlite3.

---

## Web Interface
- **Leaderboard:** http://localhost:8080/leaderboard (styled, mobile-friendly)
- **Recipes:** http://localhost:8080/recipes (curated baking recipes)
- **QR codes:** http://localhost:8080/qr?url=... (generate QR for any URL)
- **API endpoints:** /api/users, /api/chat_logs for integrations

---

## EventSub + Channel Points (optional)
Enable channel point rewards to trigger bot effects:

1. Set in GUI or .env: ENABLE_EVENTSUB=true
2. Expose endpoint via HTTPS tunnel: http://127.0.0.1:8081/eventsub  
3. Create EventSub subscription for: channel.channel_points_custom_reward_redemption.add
4. Map reward titles to bot rewards (editable in bot/commands.py):
   - "XP Boost" ? xp_boost
   - "Confetti" ? confetti  
   - "Double XP (5 min)" ? doublexp

---

## Seasonal Events
- **Set season:** !setseason halloween (broadcaster only)
- **Start event:** !seasonal
- **Disable:** !setseason off

Seasons change ingredient pools and theming.

---

## Logs and Monitoring
- **GUI Log Panel:** Real-time log viewing
- **File Logging:** logs/bakebot.log with rotation
- **Chat Logging:** All messages stored with timestamps
- **User Activity:** Last seen tracking
- **Debug Mode:** Set LOG_LEVEL=DEBUG for detailed logs

---

## Troubleshooting
- **Bot won't connect:** Use OAuth wizard to get fresh token
- **No chat messages:** Check if bot is modded, verify channel name
- **Web not loading:** Change WEB_PORT if 8080 is busy
- **OAuth issues:** Follow wizard exactly, ensure https://localhost redirect URI
- **Data not saving:** Check file permissions on bot_data.sqlite3

---

## Security
- Tokens stored securely in .env (not committed to git)
- User data encrypted at rest in SQLite
- EventSub signature verification
- Rate limiting prevents abuse

---

## License
For your channel use. No warranty.
