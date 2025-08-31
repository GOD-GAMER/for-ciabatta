# User Guide (Streamers)

What you need
- Twitch account for your bot
- Twitch Application (Client ID)
- Python 3.10+

Start the bot
- pip install -r requirements.txt
- python -m bot.gui
- Click Get Token, sign in with your bot account
- Enter your channel, click Start Bot
- Open http://localhost:8080/leaderboard

Daily use
- Start bot with the GUI before going live
- Use !seasonal, !guess, !oventrivia to run games
- Use !leaderboard to share the link
- Use !setseason halloween (or holiday) to switch themes

Channel points (optional)
- Enable EventSub: set ENABLE_EVENTSUB=true in .env
- Expose http://127.0.0.1:8081/eventsub via ngrok/cloudflared
- Create rewards matching mapping (Commands reference)

Tips
- Make your bot a mod for better chat reliability
- Share the leaderboard via a QR on stream: http://localhost:8080/qr?url=http://localhost:8080/leaderboard
