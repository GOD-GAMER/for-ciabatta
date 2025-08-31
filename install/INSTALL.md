# BakeBot Installation Guide

This guide covers installing and launching BakeBot via the GUI, obtaining a Twitch OAuth token, and optionally wiring up EventSub for channel points.

## Quick Start (GUI)

1. Install Python 3.10+
2. Open a terminal in the project folder
3. Install dependencies:
   - pip install -r requirements.txt
4. Launch the GUI:
   - python -m bot.gui
5. In the GUI:
   - Click "Get Token" and sign in with your bot account
   - Enter your Twitch channel name
   - Click "Start Bot"
6. Open the leaderboard in a browser:
   - http://localhost:8080/leaderboard

## Getting a Twitch OAuth Token (built-in flow)

1. Create a Twitch Application at https://dev.twitch.tv/console/apps
2. Add a redirect URL: http://127.0.0.1:53682/callback
3. Copy the Client ID into the GUI (Twitch Client ID)
4. Click "Get Token" — a browser will request chat:read and chat:edit
5. The GUI captures the token automatically and fills it as `oauth:...`

Notes:
- Keep your token secret; revoke it from your Twitch security settings if needed.
- If a browser doesn’t open, copy the URL from the GUI log and open it manually.

## EventSub and Channel Points (optional)

BakeBot includes a minimal EventSub webhook listener for channel point redemptions.

Steps:
1. Set these in .env or via the GUI:
   - ENABLE_EVENTSUB=true
   - EVENTSUB_SECRET=<your-random-secret>
   - EVENTSUB_PORT=8081 (default)
2. Expose your local EventSub endpoint using a tunnel (ngrok/cloudflared):
   - http://127.0.0.1:8081/eventsub
3. Create an EventSub subscription for:
   - channel.channel_points_custom_reward_redemption.add
4. In Twitch, create custom rewards and title them to match the bot mapping (editable in bot/commands.py):
   - "XP Boost" -> xp_boost
   - "Confetti" -> confetti
   - "Double XP (5 min)" -> doublexp
5. Redemptions will trigger the same effects as !redeem, without deducting in-bot tokens.

Troubleshooting:
- Signature verification errors: secret mismatch; ensure EVENTSUB_SECRET matches
- 403/timeout from Twitch: your tunnel/endpoint may be unreachable or missing HTTPS
- You can test rewards without EventSub using chat: !redeem xp_boost
