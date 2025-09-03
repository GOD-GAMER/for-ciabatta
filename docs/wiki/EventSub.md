# EventSub (Channel Points)

Connect Twitch events to in-bot rewards.

## Enable
1) Turn on EventSub in dashboard
2) Set a long random secret
3) Choose a port (default 8081)

## Expose HTTPS
- Use a tunnel (ngrok/cloudflared) or reverse proxy
- Callback URL: PUBLIC_BASE_URL + /eventsub

## Map Events
Use the Mapping JSON to customize actions and cooldowns.
```
{
  "channel.follow": {"action":"xp","amount":10,"cooldown":60},
  "channel.subscribe": {"action":"tokens","amount":20,"cooldown":30}
}
```

## Tips
- Keep cooldowns to avoid spam
- Use tokens per 100 bits for cheers
- Award raid bonuses