# Troubleshooting

## Bot Won't Start
- Set Twitch Channel in Configuration
- Complete OAuth Wizard
- Check logs in the Logs page

## Commands Don’t Respond
- Make sure bot status is Running
- Type `!help` to test
- Verify you’re in the right channel

## Leaderboard Not Loading
- Bot must be running
- Check WEB_HOST/WEB_PORT
- If public, ensure forwarding/tunnel works

## EventSub Failing
- Must be HTTPS
- Secret must match exactly
- Check the dashboard logs for errors