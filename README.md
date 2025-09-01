# ?? BakeBot - Fun Twitch Chat Bot for Streamers

[![GitHub release](https://img.shields.io/github/v/release/GOD-GAMER/for-ciabatta)](https://github.com/GOD-GAMER/for-ciabatta/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ?? What is BakeBot?

BakeBot is a **fun chat bot for Twitch streamers**! It's like having a friendly helper in your chat that:
- Plays fun baking games with your viewers ??
- Gives out virtual tokens (like coins) that viewers can collect ??
- Shows a leaderboard of your most active fans ??
- Works through an **easy website** - no coding needed! ???

**Perfect for:** Cooking streamers, baking enthusiasts, or anyone who wants their chat to be more fun and interactive!

---

## ?? What Can BakeBot Do?

### ?? Fun Games Your Viewers Will Love
- **Guess the Ingredient** - "Is it flour or sugar?"
- **Oven Trivia** - Baking questions with prizes
- **Bread Fights** - Viewers battle with baking knowledge
- **Seasonal Events** - Special holiday-themed games

### ?? Token System (Like a Fun Economy)
- Viewers earn tokens by chatting and playing games
- Daily bonuses for regular viewers
- Virtual shop with fun rewards
- Viewers can gift tokens to each other

### ?? Community Features  
- **Leaderboard** - Show off your most active fans
- **Recipe Sharing** - Share your favorite recipes with viewers
- **Custom Titles** - Give special titles to your best supporters

---

## ?? Super Easy Setup (Anyone Can Do This!)

### Step 1: Download Python
1. Go to [python.org](https://python.org/downloads/)
2. Click the big **"Download Python"** button
3. Run the installer and **check "Add Python to PATH"**
4. Click **"Install Now"**

### Step 2: Download BakeBot
1. Click **[here to download BakeBot](https://github.com/GOD-GAMER/for-ciabatta/releases)** (get the latest ZIP file)
2. **Extract** the ZIP file to a folder (like your Desktop)
3. Remember where you put it!

### Step 3: Install BakeBot
1. **Open Command Prompt** (search "cmd" in Windows)
2. **Type this:** `cd Desktop\for-ciabatta` (or wherever you put the folder)
3. **Press Enter**
4. **Type this:** `pip install -r requirements.txt`
5. **Press Enter** and wait for it to finish

### Step 4: Start BakeBot
1. **Type this:** `python -m bot.gui`
2. **Press Enter**
3. A website will open automatically! ??

### Step 5: Connect to Twitch (Super Important!)
1. In the website that opened, click **"OAuth Wizard"**
2. It will take you to Twitch - **log in with your streaming account**
3. Click **"Authorize"** to give BakeBot permission
4. You'll be sent back automatically ?

### Step 6: Tell BakeBot Your Channel
1. Go to **"Configuration"** tab
2. In **"Twitch Channel"** box, type your Twitch username (lowercase)
3. Click **"Save Configuration"**

### Step 7: Start the Bot!
1. Click the big **"Start Bot"** button
2. Wait for it to say "Bot Running" ?
3. Go to your Twitch chat and type `!help`
4. If BakeBot responds, **you did it!** ??

---

## ?? How Your Viewers Use BakeBot

### Basic Commands (Anyone Can Use)
- `!help` - Shows all available commands
- `!tokens` - Check how many tokens they have
- `!daily` - Get free daily tokens (10-30 tokens!)
- `!shop` - See what they can buy with tokens
- `!level` - See their stats and level

### Fun Game Commands
- `!guess` - Start the ingredient guessing game
- `!oventrivia` - Answer baking trivia questions
- `!fight @username` - Challenge someone to a bread fight!
- `!accept` - Accept a bread fight challenge

### Special Commands (Only You Can Use)
- `!give @viewer 50` - Give tokens to a viewer
- `!ban @user` - Ban someone from using the bot
- `!title @user Baker` - Give someone a cool title

---

## ?? How to Add Your Recipes (Easy!)

Your viewers will love seeing your favorite recipes! Here's how to add them:

### Method 1: Add One Recipe at a Time
1. Open the BakeBot website (it should still be open at `http://127.0.0.1:5000`)
2. Click the **"Recipes"** tab at the top
3. Fill in your recipe:
   - **Title:** "My Amazing Chocolate Cookies"
   - **URL:** Link to the full recipe (optional)
   - **Description:** "The best cookies ever!"
4. Click **"Add"**
5. Done! Your viewers can now see it at `http://localhost:8080/recipes`

### Method 2: Add Many Recipes at Once
1. In the **"Bulk Import"** box, paste recipes like this:
   ```
   Chocolate Cookies|https://example.com/cookies|Super yummy cookies
   Banana Bread|https://example.com/bread|Moist and delicious
   Apple Pie|https://example.com/pie|Classic American dessert
   ```
2. Click **"Import"**
3. All your recipes are added instantly!

### Method 3: Try the Examples First
1. Click **"Fill Demo"** to see example recipes
2. Click **"Import"** to add them
3. Now you can edit them to be your own recipes

---

## ?? Share Your Leaderboard with Viewers

Your viewers will love seeing who's winning! Here's how to share it:

### Easy Way (Works Right Away)
- Tell your viewers to visit: `http://localhost:8080/leaderboard`
- This only works if they're on the same WiFi as you

### Advanced Way (Share with the Internet)
This is a bit more technical, but lets anyone see your leaderboard:

1. **Set up Port Forwarding** (ask a tech-savvy friend to help):
   - Open your router settings
   - Forward port 8080 to your computer
   - Get your public IP address
2. **Or use a Tunnel Service** (easier):
   - Download [ngrok](https://ngrok.com/)
   - Run: `ngrok http 8080`
   - Share the link it gives you!

**Need Help?** Check our [Port Forwarding Guide](docs/PORT_FORWARDING.md) for detailed steps.

---

## ??? Using the Dashboard

The BakeBot website has several tabs to help you:

### ?? Control Tab
- **Start/Stop the bot** - Big green and red buttons
- **See if it's working** - Shows "Bot Running" or "Bot Stopped"
- **Quick links** to guides and help

### ?? Configuration Tab  
- **Change settings** like your Twitch channel name
- **Get your token** using the OAuth Wizard
- **Adjust ports** if needed (usually don't need to change)

### ?? Network Tab
- **See your IP addresses** for sharing publicly
- **Copy links** to share with viewers
- **Port forwarding helpers**

### ?? EventSub Tab (Advanced)
- **Connect channel points** to bot rewards
- **Set up follows/subs** to give automatic tokens
- **Advanced users only** - skip if you're just starting

### ?? Recipes Tab
- **Add your favorite recipes** for viewers to see
- **Import many at once** using copy-paste
- **Manage and edit** existing recipes

---

## ?? Help! Something's Not Working

### Bot Won't Start
- **Check:** Did you enter your Twitch channel name?
- **Check:** Did you complete the OAuth Wizard?
- **Try:** Click "Stop Bot" then "Start Bot" again

### Commands Don't Work in Chat
- **Check:** Is the bot actually running? (should say "Bot Running")
- **Check:** Are you typing in the right Twitch channel?
- **Try:** Type `!help` to test

### Website Won't Open
- **Try:** Go to `http://127.0.0.1:5000` manually
- **Check:** Did you run `python -m bot.gui`?
- **Try:** Close everything and start over from Step 4

### Viewers Can't See Leaderboard
- **Check:** Are they using `http://localhost:8080/leaderboard`?
- **Remember:** This only works for people on your same WiFi
- **Advanced:** Set up port forwarding for internet access

### Need More Help?
- **Check our guides:** Look in the `docs/` folder for detailed help
- **Common issues:** See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **Ask for help:** Create an issue on GitHub

---

## ?? You Did It!

Congratulations! You now have:
- ? A fun chat bot running in your stream
- ? Games for your viewers to play
- ? A token economy to keep people engaged
- ? A leaderboard to show your most active fans
- ? Recipe sharing for your baking content

**Your viewers will love the interactive features!** 

---

## ?? Keep Your Bot Safe

- **Never share your `.env` file** - it contains your secret tokens
- **Keep the dashboard private** - only you should access `127.0.0.1:5000`
- **Only share the leaderboard** - `localhost:8080/leaderboard` is safe to share
- **Don't share your Twitch token** with anyone

---

## ?? Want to Help Make BakeBot Better?

We love when people help improve BakeBot! If you know how to code:

1. **Fork** this repository on GitHub
2. **Make your changes** or add new features  
3. **Test everything** works properly
4. **Submit a pull request** to share your improvements

**Ideas for improvements:**
- New mini-games
- More shop items
- Better graphics for the website
- New features for streamers

---

## ?? What's New (Latest Updates)

### Version 0.2.5 (Current)
- ? Much easier to understand documentation
- ? Step-by-step setup guide anyone can follow
- ? Combined all guides into one simple README

### Previous Updates
- Recipe sharing system with easy bulk import
- EventSub integration for channel points
- Professional web dashboard
- Automatic OAuth token setup
- Network tools for public sharing

---

**Made with ?? love for streamers and their communities!**

*Perfect for cooking streamers, baking enthusiasts, and anyone who wants their Twitch chat to be more fun and interactive!*