# EventSub (Channel Points) Guide

BakeBot can react to Channel Points redemptions using Twitch EventSub.

## Requirements
- Public HTTPS callback URL (via tunnel or reverse proxy)
- A secret string to sign/verify events

## Steps
1. In the GUI (EventSub tab):
   - `ENABLE_EVENTSUB=true`
   - `EVENTSUB_SECRET=<long random string>`
   - `EVENTSUB_PORT=8081` (or your choice)
2. Expose the listener publicly:
   - cloudflared: `cloudflared tunnel --url http://127.0.0.1:8081`
   - ngrok: `ngrok http 8081`
3. Start the bot (the webhook listener starts with it).
4. Create a subscription in the Twitch Developer Console ? EventSub:
   - Type: `channel.channel_points_custom_reward_redemption.add`
   - Callback: `PUBLIC_BASE_URL + /eventsub`
   - Secret: same as `EVENTSUB_SECRET`
5. Redeem a reward and watch the GUI logs for activity.

## Tips
- HTTPS is required for Twitch validation
- If validation fails (403), verify the secret and URL
- If Twitch can’t reach you (timeout), your port/tunnel isn’t accessible
