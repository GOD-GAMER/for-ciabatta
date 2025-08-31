# Setup Guide (GUI)

1. Install Python 3.10+
2. Open a terminal in this folder
3. Install dependencies: pip install -r requirements.txt
4. Launch GUI: python -m bot.gui
5. Create a Twitch Application at https://dev.twitch.tv/console/apps
   - Add redirect URL: http://127.0.0.1:53682/callback
   - Copy the Client ID
6. In the GUI, paste the Client ID and click Get Token. Authorize the bot account.
7. Enter your Twitch channel and click Start Bot.
8. Open http://localhost:8080/leaderboard for the leaderboard

## EventSub and Channel Points (Quick setup)

- Local endpoint: http://127.0.0.1:8081/eventsub
- Set EVENTSUB_SECRET in .env (any random string, keep it secret)
- Use a tunnel (ngrok/cloudflared) to expose the endpoint publicly with HTTPS
- Create an EventSub subscription for channel.channel_points_custom_reward_redemption.add
- Ensure reward titles match bot/commands.py channel_point_map:
  - XP Boost -> xp_boost
  - Confetti -> confetti
  - Double XP (5 min) -> doublexp
- Redemptions via EventSub apply effects without consuming in-bot tokens

Troubleshooting:
- Signature verification failures: secret mismatch or body tampered
- 403 from Twitch: your endpoint not reachable or invalid SSL
- Test without EventSub by using !redeem in chat
