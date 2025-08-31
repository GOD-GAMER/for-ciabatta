# Commands

- !recipe — Link to a cookie recipe
- !bakeoff — Kick off mini-games
- !ovenstatus — Fun oven line
- !leaderboard — Link to leaderboard page
- !guess — Start Guess the Ingredient
- !oventrivia — Start Oven Timer Trivia
- !seasonal — Start a seasonal mini-game
- !setseason <name|off> — Broadcaster only, set current season
- !redeem <xp_boost|confetti|doublexp> — Spend tokens

Notes:
- Channel point redemptions can trigger the same rewards via EventSub; map titles in channel_point_map in bot/commands.py

Cooldowns:
- Commands: per-user 3s
- Participation XP: per-user 15s
- Rate limit: 8 messages per 10s per user
