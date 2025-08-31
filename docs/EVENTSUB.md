# EventSub / Channel Points Setup

This project includes a minimal EventSub webhook server to process Channel Points redemptions.

Requirements:
- Twitch Application (Client ID)
- Public HTTPS URL (tunnel e.g., ngrok or cloudflared)
- Secret string (EVENTSUB_SECRET)

Steps:
1. Run the bot GUI and start the bot (or start the EventSub server separately if you prefer).
2. Expose http://127.0.0.1:8081/eventsub via a public HTTPS tunnel.
3. Create an EventSub subscription for channel.channel_points_custom_reward_redemption.add pointing to your public URL.
4. Set the same secret you configured in .env.
5. Configure reward titles to match or update mapping in bot/commands.py channel_point_map.

Example subscription request (replace placeholders):
- Use Twitch API (requires App or User OAuth token with channel:read:redemptions):
  - See https://dev.twitch.tv/docs/eventsub/ (create subscription request body and POST to https://api.twitch.tv/helix/eventsub/subscriptions)

Security:
- We verify the Twitch-Eventsub-Message-Signature using EVENTSUB_SECRET.
- Use HTTPS and a unique long secret.

Mapping reference (default):
- "XP Boost" -> xp_boost
- "Confetti" -> confetti
- "Double XP (5 min)" -> doublexp

Note:
- For a production-grade EventSub manager (including auto subscription management), consider using a Twitch SDK or your own management utility.
