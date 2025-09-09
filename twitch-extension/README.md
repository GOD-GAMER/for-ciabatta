# BakeBot Twitch Extension (New Project)

This is a standalone Twitch Extension project for BakeBot. It provides a Panel UI and a Broadcaster Config page. The panel fetches leaderboard and recipes from your running BakeBot instance using PUBLIC_BASE_URL.

No server is required for the extension itself. Assets are uploaded to Twitch and the panel reads configuration via the Twitch Extensions Configuration Service.

## What’s Included
- Panel (viewer) UI: `panel.html`, `panel.js`, `styles.css`
- Broadcaster Config page: `config.html`, `config.js`
- Uses Twitch Extension Helper APIs

## How It Works
- The broadcaster sets PUBLIC_BASE_URL (e.g., your tunnel or domain) in the Config page.
- The Panel reads that value from the Extensions Configuration Service.
- The Panel fetches JSON from:
  - `GET {PUBLIC_BASE_URL}/ext/leaderboard`
  - `GET {PUBLIC_BASE_URL}/ext/recipes`

Ensure your BakeBot is running and PUBLIC_BASE_URL is reachable via HTTPS.

## Create the Extension in Twitch Console
1) Go to https://dev.twitch.tv/console/extensions and click “Create Extension”.
2) Choose Panel extension type.
3) Fill in basic info and save.

## Upload Assets (Asset Hosting)
- Upload these files:
  - `panel.html`
  - `panel.js`
  - `styles.css`
  - `config.html`
  - `config.js`
- Set Panel view to `panel.html`
- Set Config page to `config.html`

## Configure (Broadcaster)
1) Open the extension’s configuration page in the Twitch dashboard.
2) Enter your PUBLIC_BASE_URL (e.g., `https://your-tunnel.example`).
3) Click Save.

## Test Locally
You can test by serving these files locally and mocking the Twitch helper:
- Simple static server (for example):
```
python -m http.server 8089  # then open http://localhost:8089/panel.html
```
- In dev, the panel will not have access to the real configuration service. You can hardcode a fallback in panel.js for local testing.

## Security Notes
- Do not embed secrets in the extension front-end.
- The extension only performs GET requests to public JSON endpoints.
- If you need secure, signed requests, implement an EBS (server) and JWT.

## JSON Contracts
- `/ext/leaderboard` ? `{ data: [{ username: string, xp: number, wins: number }] }`
- `/ext/recipes` ? `{ data: [{ title: string, url?: string, description?: string }] }`

## Troubleshooting
- Panel says “Not configured” ? Set PUBLIC_BASE_URL in the Config page.
- “Failed to load” ? Ensure your BakeBot is reachable over HTTPS and running.
- CORS ? BakeBot sets permissive CORS headers for GET/OPTIONS on these public endpoints.
