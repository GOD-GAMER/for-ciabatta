# Extending (Developers)

Add commands
- Edit bot/commands.py (handle method) and add a new elif branch
- Implement your handler method and call ctx.send

Add games
- Edit bot/games.py and create a new start_* method
- Wire it in commands via a new !command

Storage
- Use bot/storage.py for DB access (aiosqlite) and metadata

Web
- Edit bot/web.py to add endpoints

Seasonal features
- Use storage metadata key "season" and BakingGames.set_season
