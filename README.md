# ?? BakeBot - Twitch Chat Bot

[![GitHub release](https://img.shields.io/github/v/release/GOD-GAMER/for-ciabatta)](https://github.com/GOD-GAMER/for-ciabatta/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A cozy Twitch baking-themed chat bot with mini-games, token economy, bread fights, and a modern web dashboard. Perfect for streamers who want to engage their community with fun interactive features!

## ? Key Features

?? **Interactive Mini-Games**
- Guess the Ingredient challenges
- Oven trivia questions  
- Seasonal baking events
- Turn-based bread fights with trivia

?? **Token Economy**
- Daily/hourly rewards
- Virtual shop system
- Token gifting between viewers
- Admin tools for management

?? **Modern Web Dashboard**
- Start/stop bot control
- Live configuration editor
- User management interface
- Public leaderboard page

?? **Twitch Integration**
- EventSub for channel points
- Follow/sub/cheer rewards
- OAuth wizard for easy setup
- Automatic token capture

## ?? Quick Start for Streamers

### Download & Extract
1. **Download:** [Latest Release](https://github.com/GOD-GAMER/for-ciabatta/releases)
2. **Extract** the ZIP to your desired folder
3. **Install Python 3.10+** if not already installed

### Setup (5 minutes)
```bash
# Install dependencies
pip install -r requirements.txt

# Start BakeBot
python -m bot.gui
```

### Configure
1. Browser opens automatically to `http://127.0.0.1:5000`
2. Click **"OAuth Wizard"** to get your Twitch token
3. Enter your **Twitch channel name**
4. Click **"Save Configuration"**
5. Click **"Start Bot"**

That's it! Type `!help` in your chat to test.

## ?? How to Add Recipes (Step-by-Step)

BakeBot includes a recipe sharing feature! Here's how to add your favorite recipes:

### Method 1: Single Recipe (Easy)
1. **Open Dashboard** - Go to `http://127.0.0.1:5000` in your browser
2. **Click "Recipes" Tab** - Located in the top navigation
3. **Fill in Recipe Details:**
   - **Title** - Recipe name (e.g., "Classic Chocolate Chip Cookies")
   - **URL** - Optional link to full recipe (e.g., AllRecipes link)
   - **Description** - Short description (e.g., "The ultimate comfort cookie")
   - **Order** - Display order (0 = first, higher numbers appear later)
   - **Visible** - Show on public recipes page (Yes/No)
4. **Click "Add"** - Recipe is saved instantly
5. **View Result** - Visit `http://localhost:8080/recipes` to see your recipe

### Method 2: Bulk Import (Multiple Recipes)
1. **Prepare Your Data** in one of these formats:

   **Format A: Simple Lines (Title|URL|Description)**
   ```
   Classic Chocolate Chip Cookies|https://allrecipes.com/recipe/10813|The ultimate comfort cookie
   Fluffy Pancakes|https://kingarthurbaking.com/recipes/238|Perfect weekend breakfast treat
   Cinnamon Rolls|https://example.com/cinnamon-rolls|Soft, sweet, and irresistible
   ```

   **Format B: JSON Array**
   ```json
   [
     {
       "title": "Classic Chocolate Chip Cookies",
       "url": "https://allrecipes.com/recipe/10813",
       "description": "The ultimate comfort cookie",
       "visible": true,
       "ord": 0
     },
     {
       "title": "Fluffy Pancakes", 
       "url": "https://kingarthurbaking.com/recipes/238",
       "description": "Perfect weekend breakfast treat",
       "visible": true,
       "ord": 1
     }
   ]
   ```

2. **Paste in Bulk Import Box** - Located below the single recipe form
3. **Click "Import"** - All recipes are added at once
4. **Success!** - You'll see a confirmation message

### Method 3: Try the Demo
1. **Click "Fill Demo"** - Adds sample recipes to see the format
2. **Click "Import"** - Imports the demo recipes
3. **Edit as Needed** - Modify the demo recipes in the table below

### Managing Your Recipes
- **Edit** - Click in any table cell to modify recipes
- **Save** - Click "Save" button for individual recipes
- **Delete** - Click red "Delete" button to remove recipes
- **Reorder** - Change the "Order" number and save

### Share with Viewers
Once you've added recipes, share the public page:
- **Local Link**: `http://localhost:8080/recipes`
- **Public Link**: See port forwarding guide to make it accessible online
- **In Chat**: Bot automatically shares the recipes link when viewers ask

## ?? Chat Commands

### Viewer Commands
- `!help` - Show available commands
- `!tokens` - Check token balance
- `!daily` - Claim daily bonus (10-30 tokens)
- `!hourly` - Claim hourly bonus (3 tokens)
- `!work` - Work for tokens (2-5 tokens, 5min cooldown)
- `!shop` - View shop items
- `!buy <item>` - Purchase shop items
- `!gift @user <amount>` - Gift tokens to others
- `!level` - Show your stats and level
- `!leaderboard` - Get leaderboard link
- `!recipes` - Get recipes link

### Mini-Games
- `!guess` - Start ingredient guessing game (5 XP + tokens)
- `!oventrivia` - Baking trivia questions (5 XP + tokens) 
- `!seasonal` - Seasonal baking events
- `!fight @user` - Challenge someone to bread combat
- `!accept` - Accept a bread fight challenge

### Admin Commands (Broadcaster/Mods)
- `!give @user <amount>` - Give tokens to user
- `!ban @user` / `!unban @user` - Bot ban/unban
- `!title @user <title>` / `!untitle @user` - Custom titles
- `!note @user <text>` - Add notes to users

## ?? Public Features

### Leaderboard
Share with your community: `http://localhost:8080/leaderboard`
- Top viewers by XP and wins
- Real-time updates
- Mobile-friendly design

### Recipes Page
Share your favorites: `http://localhost:8080/recipes`
- Add recipes via GUI
- Bulk import support
- Public recipe sharing

### Port Forwarding
Make your leaderboard public with our detailed guides:
- Router-specific instructions
- Windows Firewall commands
- Tunnel alternatives (ngrok, cloudflared)

## ?? Advanced Features

### EventSub Integration
Connect Twitch channel points to bot rewards:
- Automatic token distribution for follows/subs
- Configurable reward amounts and cooldowns
- GUI-based mapping editor
- Support for bits, raids, and more

### Token Economy
- **Shop Items:** XP boosts, custom titles, confetti effects
- **Daily Streaks:** Increasing rewards for consecutive days
- **Work System:** Earn tokens with short tasks
- **Gifting:** Community interaction through token sharing

### Bread Fight System
Turn-based combat with baking knowledge:
- Health, attack, defense stats
- Trivia questions for bonus damage
- Win/loss tracking
- Spectator-friendly combat

## ?? Dashboard Features

Access at `http://127.0.0.1:5000`:

### Control Panel
- Start/stop bot with one click
- Real-time status monitoring
- Quick access to public links

### Configuration
- OAuth wizard for easy token setup
- Environment variable editor
- Network configuration helpers

### User Management
- View all registered users
- Edit tokens, XP, notes
- Ban/unban functionality
- User activity tracking

### Event Management
- Configure EventSub mappings
- Set up channel point rewards
- Customize cooldowns and limits

## ??? Installation & Setup

### Requirements
- Python 3.10 or newer
- Windows 10/11 (Linux/macOS also supported)
- Twitch account for bot authentication

### Detailed Setup
See our comprehensive guides:
- **[Setup Guide](docs/SETUP.md)** - Step-by-step installation
- **[Commands Reference](docs/COMMANDS.md)** - Complete command list  
- **[Port Forwarding](docs/PORT_FORWARDING.md)** - Make leaderboard public
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and fixes

### Development
```bash
# Clone repository
git clone https://github.com/GOD-GAMER/for-ciabatta.git
cd for-ciabatta

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Start development
python -m bot.gui
```

## ?? Security

- **Keep tokens private** - Never share your `.env` file
- **Local GUI only** - Dashboard stays on localhost
- **HTTPS for public** - Use secure tunnels for EventSub
- **Regular updates** - Keep dependencies current

## ?? Contributing

We welcome contributions! Please read our guidelines:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes with tests
4. **Submit** a pull request

### Development Areas
- New mini-games and challenges
- Additional shop items and effects
- Enhanced web dashboard features
- Integration with other platforms
- Performance optimizations

## ?? Changelog

### v0.2.4 (Latest)
- ? Comprehensive recipe adding guide
- ? Step-by-step documentation for streamers
- ? Enhanced streamer experience with detailed instructions

### v0.2.3
- ? Professional GitHub README with badges and features
- ? Contribution guidelines and development setup
- ? Enhanced documentation structure

### v0.2.2
- ? Streamer-ready release package
- ? Enhanced documentation and setup guides
- ? Improved build scripts for distribution

### v0.2.1
- ? EventSub expansion (follows, subs, cheers, raids)
- ? GUI mapping editor with cooldowns
- ? Metadata API for configuration storage

### Previous Versions
- Dynamic recipes system with GUI management
- Automatic OAuth token capture
- Bulk recipe import/export
- Network tools and public IP detection

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for complete changelog.

## ?? Support

- **Documentation:** Check the `docs/` folder
- **Issues:** [GitHub Issues](https://github.com/GOD-GAMER/for-ciabatta/issues)
- **Security:** Report privately to maintainers

## ?? License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

**Made with ?? for the Twitch streaming community**

*Get your viewers engaged with baking-themed fun! Perfect for cooking streamers, community builders, and anyone who wants interactive chat features.*