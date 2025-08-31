import asyncio
import random
from typing import Dict, Any
import humanize
import time
import logging

class CommandHandler:
    def __init__(self, storage, games, cooldowns, rate_limiter, web_urls: Dict[str, str]):
        self.storage = storage
        self.games = games
        self.cooldowns = cooldowns
        self.rate_limiter = rate_limiter
        self.web_urls = web_urls
        self.logger = logging.getLogger('BakeBot.Commands')
        # Simple mapping for channel point titles -> reward keys used by !redeem
        self.channel_point_map: Dict[str, str] = {
            'XP Boost': 'xp_boost',
            'Confetti': 'confetti',
            'Double XP (5 min)': 'doublexp',
            'Bread Fight': 'breadfight'
        }

    async def handle(self, ctx, author: str, content: str):
        # Global per-user command cooldown to mitigate spam
        if not self.cooldowns.check(f"cmd:{author}", 3):
            self.logger.debug('Cooldown hit for user %s command %s', author, content)
            return
        if not self.rate_limiter.allow(author):
            self.logger.debug('Rate limit hit for user %s', author)
            return
        parts = content.strip().split()
        if not parts:
            return
        cmd = parts[0].lower()
        args = parts[1:]
        self.logger.info('Command %s by %s args=%s', cmd, author, args)
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
        elif cmd == '!fight':
            await self.cmd_fight(ctx, author, args)
        elif cmd == '!accept':
            await self.cmd_accept_fight(ctx, author)
        elif cmd == '!level':
            await self.cmd_level(ctx, author, args)

    async def cmd_recipe(self, ctx):
        await ctx.send('Try Chocolate Chip Cookies: https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/')

    async def cmd_bakeoff(self, ctx):
        await ctx.send('Bake-Off time! Try !seasonal, !guess, !oventrivia, or !fight @someone for bread combat!')

    async def cmd_ovenstatus(self, ctx):
        await ctx.send('Oven preheated to 350F. Timer set. Mitts ready.')

    async def cmd_leaderboard(self, ctx):
        url = self.web_urls.get('leaderboard')
        await ctx.send(f'Leaderboard: {url}')

    async def cmd_fight(self, ctx, author: str, args):
        """Start a bread fight challenge"""
        if not args:
            await ctx.send(f'{author}, usage: !fight @username - Challenge someone to bread combat!')
            return
        
        target = args[0].lstrip('@').lower()
        if target == author.lower():
            await ctx.send(f'{author}, you cannot fight yourself! Find a worthy opponent!')
            return
        
        await self.games.start_bread_fight_challenge(ctx, author, target, self.storage)

    async def cmd_accept_fight(self, ctx, author: str):
        """Accept a bread fight challenge"""
        await self.games.accept_bread_fight(ctx, author, self.storage)

    async def cmd_level(self, ctx, author: str, args):
        """Show player level and stats"""
        target = args[0].lstrip('@').lower() if args else author.lower()
        user_data = await self.storage.get_or_create_user(target)
        
        level = self.games.bread_fight.calculate_level(user_data['xp'])
        health = self.games.bread_fight.calculate_health(level)
        damage = self.games.bread_fight.calculate_base_damage(level)
        
        await ctx.send(f"?? {target}: Level {level} | {user_data['xp']} XP | {user_data['tokens']} tokens | "
                      f"{user_data['wins']} wins | Combat: {health}?? {damage}??")

    async def cmd_setseason(self, ctx, author: str, args):
        # Simple auth: only broadcaster can change season
        is_broadcaster = False
        try:
            is_broadcaster = getattr(ctx.ctx, 'author', None) and getattr(ctx.ctx.author, 'is_broadcaster', False)
        except Exception:
            pass
        if not is_broadcaster:
            await ctx.send('Only broadcaster can change the season.')
            self.logger.warning('Unauthorized setseason attempt by %s', author)
            return
        season = args[0].lower() if args else 'none'
        if season in ('none', 'off', 'disable'):
            self.games.set_season(None)
            await self.storage.set_metadata('season', '')
            await ctx.send('Seasonal events disabled.')
            self.logger.info('Season disabled by %s', author)
            return
        self.games.set_season(season)
        await self.storage.set_metadata('season', season)
        await ctx.send(f'Season set to: {season}')
        self.logger.info('Season set to %s by %s', season, author)

    async def cmd_redeem(self, ctx, author: str, args):
        if not args:
            await ctx.send('Usage: !redeem <xp_boost|confetti|doublexp|breadfight>')
            return
        await self.apply_reward(ctx, author, args[0].lower())

    async def apply_reward(self, ctx, author: str, choice: str):
        costs = {'xp_boost': 10, 'confetti': 5, 'doublexp': 20, 'breadfight': 15}
        rewards = {'xp_boost': 50, 'confetti': 0, 'doublexp': 0, 'breadfight': 0}
        
        if choice not in costs:
            await ctx.send('Unknown reward. Options: xp_boost, confetti, doublexp, breadfight')
            self.logger.warning('Unknown reward choice by %s: %s', author, choice)
            return
        
        user = await self.storage.get_or_create_user(author)
        
        # Channel point redemptions do not deduct our internal tokens; only !redeem does
        if getattr(ctx, 'skip_token_check', False) is not True:
            if user['tokens'] < costs[choice]:
                await ctx.send(f"{author}, you need {costs[choice]} tokens. You have {user['tokens']}.")
                self.logger.info('Insufficient tokens for %s: have=%s need=%s', author, user['tokens'], costs[choice])
                return
            await self.storage.add_tokens(author, -costs[choice])
            self.logger.debug('Deducted %s tokens from %s for %s', costs[choice], author, choice)
        
        await self.storage.record_redemption(author, choice, costs[choice], int(time.time()))
        self.logger.info('Redemption recorded: %s by %s cost=%s', choice, author, costs[choice])
        
        if choice == 'xp_boost':
            await self.storage.add_xp(author, rewards[choice])
            await ctx.send(f"{author} redeemed XP Boost! +{rewards[choice]} XP")
        elif choice == 'confetti':
            await ctx.send(f"{author} throws confetti everywhere!")
        elif choice == 'doublexp':
            await ctx.send(f"{author} activated Double XP for 5 minutes!")
        elif choice == 'breadfight':
            await ctx.send(f"?? {author} receives a BREAD FIGHT PASS! Challenge anyone with !fight @username for the next 10 minutes!")
            # Set a temporary flag for enhanced fight rewards (could be implemented)

    async def award_participation(self, author: str):
        await self.storage.add_xp(author, 1)

    async def award_win(self, author: str):
        await self.storage.add_xp(author, 25)
        await self.storage.add_tokens(author, 5)
        await self.storage.add_win(author)
