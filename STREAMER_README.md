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
- `!recipes` - Get recipes link

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