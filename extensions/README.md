# BakeBot Twitch Extension (Panel)

This folder contains a simple Twitch Extension Panel UI that displays:
- Leaderboard (top XP and wins)
- Recipes (public, visible recipes)

It calls your BakeBot public endpoints (PUBLIC_BASE_URL) using:
- GET /ext/leaderboard ? { data: [{ username, xp, wins }] }
- GET /ext/recipes ? { data: [{ title, url, description }] }

## How to Host in Twitch Extensions
1) Go to https://dev.twitch.tv/console/extensions
2) Create a new Extension (Panel)
3) In Asset Hosting ? Upload these files as your Panel assets:
   - panel.html
   - panel.js
   - styles.css
4) In the Extension Config or Panel UI, the broadcaster must set PUBLIC_BASE_URL
   (e.g., https://yourdomain.example or your tunnel URL). The panel reads it from localStorage.

Note: For production, consider adding a simple Config page to set PUBLIC_BASE_URL via Twitch config service.

## Local Testing
- Serve these files locally (any static server) and open panel.html
- Before loading, set localStorage:
```
localStorage.setItem('bakebot_base_url', 'https://<your public base url>');
```
- The panel will fetch JSON from /ext/leaderboard and /ext/recipes.
