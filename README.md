# BakeBot

A Twitch baking-themed chat bot with mini-games, token economy, bread fights, and a modern web interface. Built with Python and Flask.

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the bot**
   ```bash
   python -m bot.gui
   ```

3. **Setup in browser** (opens automatically at http://127.0.0.1:5000)
   - Click "OAuth Wizard" to connect your Twitch account
   - Enter your channel name
   - Click "Start Bot"

4. **View leaderboard** at http://localhost:8080/leaderboard

## Core Features

- **Baking-themed mini-games** with XP and token rewards
- **Token economy** with daily bonuses and bakery shop
- **PvP bread fights** using baking knowledge questions
- **Web interface** for management and shop browsing
- **Persistent data** - everything saves automatically

## Games & Commands

**Games:**
- `!guess` - Guess the baking ingredient
- `!oventrivia` - Baking knowledge trivia
- `!seasonal` - Themed seasonal events
- `!fight @user` - Challenge someone to bread combat

**Token Economy:**
- `!shop` - Browse the bakery shop
- `!buy <item>` - Purchase power-ups and cosmetics
- `!daily` - Claim daily bonus (with streak rewards)
- `!hourly` - Claim hourly bonus
- `!work` - Work in the bakery for tokens
- `!tokens` - Check your balance

**Other Commands:**
- `!level` - Show your stats and combat power
- `!leaderboard` - Link to web leaderboard
- `!recipe` - Get a random baking recipe

## Bakery Shop

Spend tokens on baking-themed items:

- **Flour Power Boost** (25??) - Double XP for 10 minutes
- **Golden Whisk** (50??) - [Master Baker] chat title
- **Sourdough Shield** (40??) - Extra health in bread fights
- **Cookie Jar** (12??) - Mystery box with random rewards
- **Rainbow Sprinkles** (15??) - Colorful chat effects

*Browse the full shop at `/shop` or use `!shop` in chat*

## Bread Fighting System

Challenge other viewers to turn-based combat:

1. **Challenge:** `!fight @username`
2. **Accept:** `!accept` (60 second window)
3. **Combat:** Take turns answering bread knowledge questions
4. **Victory:** Correct answers deal damage based on your level and accuracy

**Combat Stats:**
- Level = XP ÷ 100
- Health = 50 + (level × 10)
- Damage = 10 + (level × 2) + accuracy bonus

## Token Earning

- **Daily bonus:** 10+ tokens (streak bonuses up to +20)
- **Hourly bonus:** 3 tokens every hour  
- **Work system:** 3-12 tokens per bakery job
- **Win games:** 5 tokens + 25 XP
- **Participation:** 1 XP every 15 seconds

## Web Interface

- **Management GUI:** http://127.0.0.1:5000 (Dashboard, OAuth setup)
- **Bakery Shop:** http://127.0.0.1:5000/shop (Browse all items)
- **Leaderboard:** http://localhost:8080/leaderboard (Public scoreboard)

## Requirements

- Python 3.10+
- Twitch account for your bot
- Optional: Twitch Developer App for OAuth

## Configuration

All settings managed through the web interface:
- Twitch OAuth token and channel
- Command prefix (default: !)
- Web server ports
- EventSub for channel points (optional) - see docs/EVENTSUB.md

Data persists in `bot_data.sqlite3` - no setup required.

---

*A cozy baking bot for your Twitch community* ??
