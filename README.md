# ?? BakeBot

A Twitch baking-themed chat bot with cozy mini-games, redemptions, a tiny leaderboard website, and a simple GUI. Built with Python, twitchio, aiosqlite, aiohttp, and PySide6.

---

## ? Features
- GUI-first setup (no CLI gymnastics)
- Persistent SQLite storage (XP, tokens, wins, redemptions)
- Baking games: Guess the Ingredient, Oven Timer Trivia, Seasonal Event
- XP and token economy with simple redemptions
- Lightweight web server (leaderboard, recipe links, QR generator)
- Optional EventSub listener for Channel Points
- Cooldowns and rate limits to reduce spam

---

## ?? Requirements
- Python 3.10+
- A Twitch account for your bot
- Optional: Twitch Developer Application (for built-in OAuth and EventSub)

---

## ?? Quick Start (GUI)
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the GUI
   ```bash
   python -m bot.gui
   ```
3. In the GUI
   - Click Get Token
   - Sign in with your bot account and authorize
   - Enter your channel name
   - Click Start Bot
4. Open the leaderboard
   - http://localhost:8080/leaderboard

---

## ?? Get a Twitch OAuth Token (built-in)
1. Create a Twitch Application: https://dev.twitch.tv/console/apps
2. Add redirect URL: `http://127.0.0.1:53682/callback`
3. Paste your Client ID into the GUI
4. Click Get Token and authorize `chat:read chat:edit`
5. The GUI fills `TWITCH_TOKEN` as `oauth:...`

Tip: Keep your token secret. Revoke it in Twitch security settings if needed.

---

## ?? Configuration (.env)
The GUI writes these values to `.env` for you. You can also edit manually.

| Key | Description | Default |
|-----|-------------|---------|
| TWITCH_TOKEN | OAuth token (starts with `oauth:`) | — |
| TWITCH_CLIENT_ID | Needed for GUI Get Token flow | — |
| TWITCH_CHANNEL | Your channel login name | — |
| PREFIX | Command prefix | `!` |
| ENABLE_EVENTSUB | Enable Channel Points listener | `false` |
| EVENTSUB_SECRET | Secret for EventSub signature verification | `changeme` |
| EVENTSUB_PORT | Local EventSub port | `8081` |
| WEB_HOST | Web server host | `127.0.0.1` |
| WEB_PORT | Web server port | `8080` |

---

## ?? Commands (chat)
- `!recipe` — Share a cookie recipe link
- `!bakeoff` — Hype line and suggests games
- `!ovenstatus` — Fun oven status line
- `!leaderboard` — Post the leaderboard link
- `!guess` — Start Guess the Ingredient
- `!oventrivia` — Start Oven Timer Trivia
- `!seasonal` — Start a seasonal mini-game
- `!setseason <name|off>` — Broadcaster only (e.g., `halloween`, `holiday`)
- `!redeem <xp_boost|confetti|doublexp>` — Spend in-bot tokens

Cooldowns:
- Commands: 3s per user
- Participation XP: 15s per user
- Rate limit: 8 messages per 10s per user

---

## ?? Games
- Guess the Ingredient
  - Bot posts a hint; first correct answer wins
- Oven Timer Trivia
  - Baking trivia; first correct answer wins
- Seasonal Event
  - Themed mystery ingredient (season-dependent pool)

---

## ?? XP, Tokens, Redemptions
- Participation: +1 XP per user every 15s
- Win a game: +25 XP and +5 tokens
- `!redeem xp_boost` ? +50 XP (costs 10 tokens)
- `!redeem confetti` ? fun effect (5 tokens)
- `!redeem doublexp` ? flavor message (20 tokens)

All data is stored persistently in `bot_data.sqlite3`.

---

## ?? Web and QR
- Leaderboard: `http://localhost:8080/leaderboard`
- Recipes: `http://localhost:8080/recipes`
- QR codes: `http://localhost:8080/qr?url=http://localhost:8080/leaderboard`

Change host/port via `WEB_HOST` / `WEB_PORT`.

---

## ??? EventSub + Channel Points (optional)
Enable channel point rewards to trigger bot effects without spending in-bot tokens.

1. In `.env` (or GUI), set:
   - `ENABLE_EVENTSUB=true`
   - `EVENTSUB_SECRET=<random-long-string>`
   - `EVENTSUB_PORT=8081`
2. Expose your local endpoint with HTTPS (tunnel):
   - `http://127.0.0.1:8081/eventsub`
3. In your Twitch app, create an EventSub subscription for:
   - `channel.channel_points_custom_reward_redemption.add`
4. Create rewards in Twitch with titles mapped to bot rewards (editable in `bot/commands.py`):
   - "XP Boost" ? `xp_boost`
   - "Confetti" ? `confetti`
   - "Double XP (5 min)" ? `doublexp`

Notes:
- Signature validation uses `EVENTSUB_SECRET`.
- If you don’t want to tunnel yet, test with chat `!redeem` commands.

---

## ?? Seasonal Events
- Set current season: `!setseason halloween` (broadcaster only)
- Start a round: `!seasonal`
- Disable: `!setseason off`

---

## ??? Troubleshooting
- Bot won’t connect
  - Token invalid/missing `oauth:` prefix ? Click Get Token again
  - Channel name wrong ? Use login name (lowercase)
- Can’t send chat
  - Bot not a mod or Twitch rate-limiting ? Mod the bot, slow down
  - Prefix mismatch ? Check `PREFIX`
- Web not loading
  - Port busy ? Change `WEB_PORT`
- EventSub issues
  - 403 / signature failed ? Secret mismatch or wrong URL
  - Tunnel not reachable ? Ensure public HTTPS URL is active
  - Reward title mismatch ? Update `channel_point_map` in `bot/commands.py`

---

## ?? Security
- Never commit `.env` or share your token/secret
- Use a strong random `EVENTSUB_SECRET`
- Revoke compromised tokens in Twitch settings

---

## ?? License
For your channel use. No warranty.
