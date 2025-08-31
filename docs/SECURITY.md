# Security Notes

- Keep your OAuth and EventSub secrets private; never commit .env
- Revoke OAuth tokens from Twitch security settings if compromised
- Use HTTPS for EventSub (tunnel or reverse proxy)
- Use a strong random EVENTSUB_SECRET
- Limit privileges on your bot account
