import asyncio
import random
from typing import Dict, Any
import humanize
import time

class CommandHandler:
    def __init__(self, storage, games, cooldowns, rate_limiter, web_urls: Dict[str, str]):
        self.storage = storage
        self.games = games
        self.cooldowns = cooldowns
        self.rate_limiter = rate_limiter
        self.web_urls = web_urls
        # Simple mapping for channel point titles -> reward keys used by !redeem
        self.channel_point_map: Dict[str, str] = {
            'XP Boost': 'xp_boost',
            'Confetti': 'confetti',
            'Double XP (5 min)': 'doublexp'
        }

    async def handle(self, ctx, author: str, content: str):
        # Global per-user command cooldown to mitigate spam
        if not self.cooldowns.check(f"cmd:{author}", 3):
            return
        if not self.rate_limiter.allow(author):
            return
        parts = content.strip().split()
        if not parts:
            return
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd == '!recipe':
            await self.cmd_recipe(ctx)
        elif cmd == '!bakeoff':
            await self.cmd_bakeoff(ctx)
        elif cmd == '!ovenstatus':
            await self.cmd_ovenstatus(ctx)
        elif cmd == '!leaderboard':
            await self.cmd_leaderboard(ctx)
        elif cmd == '!guess':
            await self.games.start_guess_ingredient(ctx)
        elif cmd == '!oventrivia':
            await self.games.start_oven_timer_trivia(ctx)
        elif cmd == '!seasonal':
            await self.games.start_seasonal_event(ctx)
        elif cmd == '!setseason':
            await self.cmd_setseason(ctx, author, args)
        elif cmd == '!redeem':
            await self.cmd_redeem(ctx, author, args)

    async def cmd_recipe(self, ctx):
        await ctx.send('Try Chocolate Chip Cookies: https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/')

    async def cmd_bakeoff(self, ctx):
        await ctx.send('Bake-Off time! Try !seasonal, !guess or !oventrivia to start a mini-game!')

    async def cmd_ovenstatus(self, ctx):
        await ctx.send('Oven preheated to 350°F. Timer set. Mitts ready.')

    async def cmd_leaderboard(self, ctx):
        url = self.web_urls.get('leaderboard')
        await ctx.send(f'Leaderboard: {url}')

    async def cmd_setseason(self, ctx, author: str, args):
        # Simple auth: only broadcaster can change season
        target = getattr(ctx.ctx, 'channel', None)
        is_broadcaster = False
        try:
            is_broadcaster = getattr(ctx.ctx, 'author', None) and getattr(ctx.ctx.author, 'is_broadcaster', False)
        except Exception:
            pass
        if not is_broadcaster:
            await ctx.send('Only broadcaster can change the season.')
            return
        season = args[0].lower() if args else 'none'
        if season in ('none', 'off', 'disable'):
            self.games.set_season(None)
            await self.storage.set_metadata('season', '')
            await ctx.send('Seasonal events disabled.')
            return
        self.games.set_season(season)
        await self.storage.set_metadata('season', season)
        await ctx.send(f'Season set to: {season}')

    async def cmd_redeem(self, ctx, author: str, args):
        if not args:
            await ctx.send('Usage: !redeem <xp_boost|confetti|doublexp>')
            return
        await self.apply_reward(ctx, author, args[0].lower())

    async def apply_reward(self, ctx, author: str, choice: str):
        costs = {'xp_boost': 10, 'confetti': 5, 'doublexp': 20}
        rewards = {'xp_boost': 50, 'confetti': 0, 'doublexp': 0}
        if choice not in costs:
            await ctx.send('Unknown reward. Options: xp_boost, confetti, doublexp')
            return
        user = await self.storage.get_or_create_user(author)
        # Channel point redemptions do not deduct our internal tokens; only !redeem does
        # If invoked via !redeem, tokens must be sufficient; for EventSub, skip deduction
        if getattr(ctx, 'skip_token_check', False) is not True:
            if user['tokens'] < costs[choice]:
                await ctx.send(f"{author}, you need {costs[choice]} tokens. You have {user['tokens']}.")
                return
            await self.storage.add_tokens(author, -costs[choice])
        await self.storage.record_redemption(author, choice, costs[choice], int(time.time()))
        if choice == 'xp_boost':
            await self.storage.add_xp(author, rewards[choice])
            await ctx.send(f"{author} redeemed XP Boost! +{rewards[choice]} XP")
        elif choice == 'confetti':
            await ctx.send(f"{author} throws confetti everywhere! ??")
        elif choice == 'doublexp':
            await ctx.send(f"{author} activated Double XP for 5 minutes!")

    async def award_participation(self, author: str):
        await self.storage.add_xp(author, 1)

    async def award_win(self, author: str):
        await self.storage.add_xp(author, 25)
        await self.storage.add_tokens(author, 5)
        await self.storage.add_win(author)
