# BakeBot

A Twitch baking-themed chat bot with cozy mini-games, redemptions, a tiny leaderboard website, and a beautiful modern GUI. Built with Python, twitchio, aiosqlite, aiohttp, and Flet.

---

## Features
- **Modern Flutter-based GUI** with beautiful baking-themed design
- **Universal icon support** - emoji, symbols, or ASCII text based on system capabilities
- Step-by-step OAuth token setup wizard with smooth animations
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
- Python 3.10+
- A Twitch account for your bot
- Optional: Twitch Developer Application (for OAuth and EventSub)

---

## Quick Start (Modern GUI)
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the beautiful GUI
   ```bash
   python -m bot.gui
   ```
3. In the GUI:
   - Choose your preferred icon style (Emoji/Symbol/Text) from the dropdown
   - Click "Setup OAuth" and follow the animated 4-step wizard
   - Enter your channel name in the sleek input field
   - Click the "?? Start Bot" button
4. Open the styled leaderboard
   - Click "?? Open Leaderboard" or visit http://localhost:8080/leaderboard

---

## Beautiful Modern Interface

**?? Design Features:**
- Flutter-rendered GUI with smooth animations
- Baking-themed color scheme (warm browns, creams, golds)
- Card-based layout with elevation and shadows  
- **Adaptive icons** - automatically detects system capabilities
- **3 icon styles**: Emoji ??, Symbol ?, Text [B]
- Responsive tabs: Dashboard, Logs, Users, Games
- Real-time status indicators with color coding
- Snackbar notifications for user feedback

**?? OAuth Wizard:**
- 4-step tabbed interface with progress indicators
- Integrated browser launching
- Clipboard integration for easy copying
- Form validation with helpful error messages
- Automatic token formatting and saving

**?? Icon System:**
- **Emoji Mode**: Beautiful Unicode emojis (?? ?? ?? ??)
- **Symbol Mode**: Clean Unicode symbols (? ? ? ?)  
- **Text Mode**: ASCII fallbacks ([B] [L] [>] [#])
- **Auto-detection**: Automatically chooses best option for your system
- **Manual override**: Dropdown to switch styles anytime

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

Built-in user management interface with modern cards:
- View all users with stats cards showing totals
- Edit XP, tokens, wins for any user
- Add notes to users with rich text
- Ban/unban users with visual indicators
- View chat message history in scrollable lists
- Export/import user data with progress indicators

Access via the "?? Users" tab in the GUI.

---

## Game Controls

Interactive game control panel:
- **Game Cards:** Visual cards for each game type with themed icons
- **One-click start:** Launch games directly from GUI
- **Season Controls:** Dropdown to change seasonal themes
- **Live Status:** See active games and their progress

Access via the "?? Games" tab.

---

## Configuration

Beautifully organized settings panel with auto-save:

| Key | Description | Default |
|-----|-------------|---------|
| TWITCH_TOKEN | OAuth token (secured input field) | - |
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

Seasons change ingredient pools and theming. Control via GUI dropdown.

---

## Logs and Monitoring
- **Colorized Log Panel:** Real-time log viewing with syntax highlighting
- **Auto-scroll:** Latest logs always visible
- **Log Management:** Clear logs button, limited history
- **File Logging:** logs/bakebot.log with rotation
- **Chat Logging:** All messages stored with timestamps
- **User Activity:** Last seen tracking with visual indicators

---

## Icon Support
BakeBot's GUI includes a comprehensive icon system that works on all systems:

**?? Icon Styles:**
- **Emoji (??)**: Beautiful Unicode emojis for modern systems
- **Symbol (?)**: Clean Unicode symbols for better compatibility  
- **Text ([B])**: ASCII fallbacks that work everywhere

**?? Features:**
- **Auto-detection**: Automatically chooses the best option for your system
- **Manual selection**: Use the dropdown in the GUI header to switch styles
- **Themed colors**: Icons automatically match the baking color scheme
- **Consistent mapping**: Same meaning across all icon styles

**?? Icon Categories:**
- Core: bread, gear, lock, rocket, stop
- Interface: home, chart, logs, users, games
- Actions: search, download, save, edit, trash
- Status: ready, loading, success, error, warning
- Seasonal: pumpkin, tree, sun, flower
- Gaming: trophy, medal, crown, star, coin

---

## Troubleshooting
- **Bot won't connect:** Use OAuth wizard to get fresh token
- **No chat messages:** Check if bot is modded, verify channel name
- **Web not loading:** Change WEB_PORT if 8080 is busy
- **OAuth issues:** Follow wizard exactly, ensure https://localhost redirect URI
- **Data not saving:** Check file permissions on bot_data.sqlite3
- **GUI not loading:** Ensure Flet is installed: `pip install flet>=0.24.1`
- **Icons not displaying:** Try switching icon style in the GUI dropdown
- **Question marks instead of icons:** Use "Text" mode for universal compatibility

---

## Security
- Tokens stored securely in .env (not committed to git)
- Password-masked input fields in GUI
- User data encrypted at rest in SQLite
- EventSub signature verification
- Rate limiting prevents abuse

---

## License
For your channel use. No warranty.
