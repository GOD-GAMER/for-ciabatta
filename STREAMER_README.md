# BakeBot - Streamer Release

Thank you for downloading BakeBot! This is a cozy Twitch baking-themed chat bot with mini-games, token economy, and interactive features for your viewers.

## ?? What's Included

- **Complete BakeBot system** - All Python files and web interface
- **Setup documentation** - Step-by-step installation guide
- **Configuration tools** - Web-based GUI for easy setup
- **Streamer guides** - How to use during streams

## ?? Quick Start (5 minutes)

1. **Install Python 3.10+** from [python.org](https://python.org/downloads/)
2. **Extract this ZIP** to your desired folder
3. **Open PowerShell/Terminal** in the extracted folder
4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
5. **Start BakeBot:**
   ```
   python -m bot.gui
   ```
6. **Browser opens automatically** - Follow the setup wizard!

## ?? First-Time Setup

1. **OAuth Setup** - Click "OAuth Wizard" to get your Twitch token
2. **Configure** - Enter your Twitch channel name
3. **Start Bot** - Click "Start Bot" in the dashboard
4. **Test** - Type `!help` in your chat to verify it's working

## ?? Documentation

- **`docs/SETUP.md`** - Detailed installation guide
- **`docs/COMMANDS.md`** - All bot commands
- **`docs/USER_GUIDE.md`** - How to use during streams
- **`README.md`** - Complete feature overview

## ?? Key Features for Streamers

- **Mini-Games**: `!guess`, `!oventrivia`, `!seasonal`
- **Bread Fights**: PvP combat with trivia questions
- **Economy**: Tokens, daily rewards, shop system
- **Leaderboard**: Public web page for viewers
- **EventSub**: Channel points integration
- **Recipes**: Share your favorite baking recipes

## ?? Public Features

- **Leaderboard**: `http://localhost:8080/leaderboard`
- **Recipes Page**: `http://localhost:8080/recipes`
- **Port Forwarding Guide**: See `docs/PORT_FORWARDING.md`

## ?? Configuration Files

- **`.env`** - Created automatically (keep this private!)
- **`bot_data.sqlite3`** - Your viewer data (auto-created)
- **Dashboard**: `http://127.0.0.1:5000` (GUI interface)

## ?? Need Help?

- **Troubleshooting**: `docs/TROUBLESHOOTING.md`
- **Port Forwarding**: `docs/PORT_FORWARDING.md`
- **Security**: `docs/SECURITY.md`

## ?? Chat Commands Preview

- `!help` - Show help
- `!tokens` - Check balance
- `!daily` - Daily bonus
- `!shop` - View items
- `!guess` - Start ingredient game
- `!fight @username` - Challenge to bread fight
- `!leaderboard` - Get leaderboard link

**Admin Commands (Broadcaster only):**
- `!give @user 50` - Give tokens
- `!ban @user` / `!unban @user`
- `!title @user Baker` - Give custom title

## ?? Security Note

- Never share your `.env` file or Twitch tokens
- Keep the GUI dashboard private (localhost only)
- Only share the public leaderboard link

---

**Have fun baking with your community! ????**

*For technical support or feature requests, check the documentation or community resources.*