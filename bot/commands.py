import asyncio
import random
from typing import Dict, Any, Optional
import humanize
import time
import logging

class BakeryShop:
    """Baking-themed shop system for token economy"""
    
    def __init__(self):
        # Shop items with baking theme - organized by category
        self.shop_items = {
            # Boosts & Buffs
            'flour_power': {
                'name': 'Flour Power Boost',
                'description': 'Double XP gain for 10 minutes',
                'cost': 25,
                'category': 'boost',
                'effect': 'double_xp_10min'
            },
            'yeast_feast': {
                'name': 'Yeast Feast',
                'description': 'Instant +100 XP',
                'cost': 20,
                'category': 'boost', 
                'effect': 'instant_xp_100'
            },
            'sugar_rush': {
                'name': 'Sugar Rush',
                'description': 'Skip all cooldowns for 5 minutes',
                'cost': 30,
                'category': 'boost',
                'effect': 'no_cooldowns_5min'
            },
            
            # Cosmetics & Fun
            'golden_whisk': {
                'name': 'Golden Whisk',
                'description': 'Special chat title: [Master Baker]',
                'cost': 50,
                'category': 'cosmetic',
                'effect': 'title_master_baker'
            },
            'rainbow_sprinkles': {
                'name': 'Rainbow Sprinkles',
                'description': 'Colorful chat celebration effect',
                'cost': 15,
                'category': 'fun',
                'effect': 'rainbow_chat'
            },
            'cookie_jar': {
                'name': 'Cookie Jar',
                'description': 'Random goodie (XP, tokens, or surprise)',
                'cost': 12,
                'category': 'gamble',
                'effect': 'mystery_box'
            },
            
            # Combat & Games
            'sourdough_shield': {
                'name': 'Sourdough Shield',
                'description': 'Extra health in bread fights (+20 HP)',
                'cost': 40,
                'category': 'combat',
                'effect': 'bread_fight_health_20'
            },
            'mixing_mastery': {
                'name': 'Mixing Mastery',
                'description': 'Extra damage in bread fights (+5 damage)',
                'cost': 35,
                'category': 'combat',
                'effect': 'bread_fight_damage_5'
            },
            
            # Utilities
            'recipe_book': {
                'name': 'Personal Recipe Book',
                'description': 'Get 3 random baking recipes',
                'cost': 18,
                'category': 'utility',
                'effect': 'recipe_collection'
            },
            'timer_precision': {
                'name': 'Timer Precision',
                'description': 'Extra time for trivia questions (+5 seconds)',
                'cost': 22,
                'category': 'utility',
                'effect': 'trivia_time_bonus'
            }
        }
        
        # Daily/hourly earning opportunities
        self.earning_opportunities = {
            'daily_knead': {
                'name': 'Daily Knead',
                'description': 'Daily login bonus',
                'reward': 10,
                'cooldown': 86400  # 24 hours
            },
            'hourly_rise': {
                'name': 'Hourly Rise',
                'description': 'Check in every hour',
                'reward': 3,
                'cooldown': 3600  # 1 hour
            },
            'streak_baker': {
                'name': 'Streak Baker',
                'description': 'Bonus for consecutive days',
                'reward': 5,  # Additional per day
                'cooldown': 86400
            }
        }

class CommandHandler:
    def __init__(self, storage, games, cooldowns, rate_limiter, web_urls: Dict[str, str]):
        self.storage = storage
        self.games = games
        self.cooldowns = cooldowns
        self.rate_limiter = rate_limiter
        self.web_urls = web_urls
        self.logger = logging.getLogger('BakeBot.Commands')
        self.bakery_shop = BakeryShop()
        
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
        
        # Existing commands
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
        
        # New token economy commands
        elif cmd == '!shop':
            await self.cmd_shop(ctx, author, args)
        elif cmd == '!buy':
            await self.cmd_buy(ctx, author, args)
        elif cmd == '!daily':
            await self.cmd_daily(ctx, author)
        elif cmd == '!hourly':
            await self.cmd_hourly(ctx, author)
        elif cmd == '!tokens':
            await self.cmd_tokens(ctx, author, args)
        elif cmd == '!gift':
            await self.cmd_gift_tokens(ctx, author, args)
        elif cmd == '!work':
            await self.cmd_work(ctx, author)

    async def cmd_shop(self, ctx, author: str, args):
        """Display the bakery shop"""
        if args and args[0].lower() in ['boost', 'cosmetic', 'fun', 'combat', 'utility', 'gamble']:
            # Show specific category
            category = args[0].lower()
            items = {k: v for k, v in self.bakery_shop.shop_items.items() if v['category'] == category}
            await ctx.send(f"?? Bakery Shop - {category.title()} Items:")
            for item_id, item in items.items():
                await ctx.send(f"  {item['name']} - {item['cost']} tokens | {item['description']}")
        else:
            # Show all categories
            categories = {}
            for item_id, item in self.bakery_shop.shop_items.items():
                cat = item['category']
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(f"{item['name']} ({item['cost']}??)")
            
            await ctx.send("?? Welcome to the Bakery Shop! Categories:")
            for cat, items in categories.items():
                await ctx.send(f"  {cat.title()}: {', '.join(items[:3])}{'...' if len(items) > 3 else ''}")
            await ctx.send("Use !shop [category] for details, !buy [item] to purchase")

    async def cmd_buy(self, ctx, author: str, args):
        """Buy an item from the bakery shop"""
        if not args:
            await ctx.send(f"{author}, usage: !buy <item_name> - Check !shop first!")
            return
        
        # Find item by name (flexible matching)
        item_name = ' '.join(args).lower().replace(' ', '_')
        item = None
        item_id = None
        
        # Try exact match first
        if item_name in self.bakery_shop.shop_items:
            item_id = item_name
            item = self.bakery_shop.shop_items[item_name]
        else:
            # Try partial matching
            for iid, idata in self.bakery_shop.shop_items.items():
                if item_name in iid or item_name in idata['name'].lower():
                    item_id = iid
                    item = idata
                    break
        
        if not item:
            await ctx.send(f"{author}, item not found! Check !shop for available items.")
            return
        
        user_data = await self.storage.get_or_create_user(author)
        
        if user_data['tokens'] < item['cost']:
            await ctx.send(f"{author}, you need {item['cost']} tokens but have {user_data['tokens']}. "
                          f"Earn more with !daily, !hourly, !work, or win games!")
            return
        
        # Deduct tokens and apply effect
        await self.storage.add_tokens(author, -item['cost'])
        await self.storage.record_redemption(author, item_id, item['cost'], int(time.time()))
        
        # Apply the item's effect
        await self.apply_shop_effect(ctx, author, item['effect'], item)

    async def apply_shop_effect(self, ctx, author: str, effect: str, item: dict):
        """Apply the effect of a purchased shop item"""
        if effect == 'instant_xp_100':
            await self.storage.add_xp(author, 100)
            await ctx.send(f"?? {author} consumed {item['name']} and gained 100 XP!")
        
        elif effect == 'double_xp_10min':
            # Store a temporary effect (could be implemented with metadata)
            await self.storage.set_metadata(f"double_xp_{author}", str(int(time.time()) + 600))
            await ctx.send(f"? {author} activated {item['name']}! Double XP for 10 minutes!")
        
        elif effect == 'no_cooldowns_5min':
            await self.storage.set_metadata(f"no_cooldowns_{author}", str(int(time.time()) + 300))
            await ctx.send(f"?? {author} has {item['name']} active! No cooldowns for 5 minutes!");
        
        elif effect == 'rainbow_chat':
            await ctx.send(f"??? {author} throws rainbow sprinkles everywhere! ??? Chat sparkles with color! ????")
        
        elif effect == 'mystery_box':
            # Random reward from cookie jar
            rewards = [
                (50, lambda: self.storage.add_xp(author, 25)),  # 50% chance: 25 XP
                (30, lambda: self.storage.add_tokens(author, 8)),  # 30% chance: 8 tokens
                (15, lambda: self.storage.add_tokens(author, 20)),  # 15% chance: 20 tokens jackpot
                (5, lambda: self.storage.add_xp(author, 100))  # 5% chance: 100 XP jackpot
            ]
            
            roll = random.randint(1, 100)
            cumulative = 0
            for chance, reward_func in rewards:
                cumulative += chance
                if roll <= cumulative:
                    await reward_func()
                    if chance == 50:
                        await ctx.send(f"?? {author}'s cookie jar contained: 25 XP!")
                    elif chance == 30:
                        await ctx.send(f"?? {author}'s cookie jar contained: 8 tokens!")
                    elif chance == 15:
                        await ctx.send(f"?? JACKPOT! {author}'s cookie jar contained: 20 tokens!")
                    else:
                        await ctx.send(f"?? MEGA JACKPOT! {author}'s cookie jar contained: 100 XP!")
                    break
        
        elif effect == 'title_master_baker':
            await self.storage.set_metadata(f"title_{author}", "Master Baker")
            await ctx.send(f"?? {author} is now a [Master Baker]! Title will show in special events!")
        
        elif effect == 'recipe_collection':
            recipes = [
                "Classic Sourdough Bread", "French Croissants", "Chocolate Chip Cookies",
                "Banana Bread", "Apple Pie", "Cinnamon Rolls", "Red Velvet Cake",
                "Macarons", "Bagels", "Pretzels"
            ]
            user_recipes = random.sample(recipes, 3)
            await ctx.send(f"?? {author} received these recipes: {', '.join(user_recipes)}!")
        
        else:
            await ctx.send(f"? {author} purchased {item['name']}! Effect applied.")

    async def cmd_daily(self, ctx, author: str):
        """Claim daily token bonus"""
        last_daily = await self.storage.get_metadata(f"last_daily_{author}")
        now = int(time.time())
        
        if last_daily:
            time_since = now - int(last_daily)
            if time_since < 86400:  # 24 hours
                remaining = 86400 - time_since
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                await ctx.send(f"{author}, daily bonus available in {hours}h {minutes}m!")
                return
        
        # Check for streak bonus
        streak = 0
        streak_data = await self.storage.get_metadata(f"daily_streak_{author}")
        if streak_data:
            last_streak_day = int(streak_data.split(',')[0])
            streak_count = int(streak_data.split(',')[1])
            
            # If claimed yesterday, continue streak
            if now - last_streak_day <= 86400 + 3600:  # Allow 1 hour buffer
                streak = streak_count + 1
            else:
                streak = 1
        else:
            streak = 1
        
        # Calculate rewards
        base_reward = 10
        streak_bonus = min(streak * 2, 20)  # Cap at 20 bonus
        total_reward = base_reward + streak_bonus
        
        await self.storage.add_tokens(author, total_reward)
        await self.storage.set_metadata(f"last_daily_{author}", str(now))
        await self.storage.set_metadata(f"daily_streak_{author}", f"{now},{streak}")
        
        await ctx.send(f"?? {author} claimed daily bonus: {total_reward} tokens! "
                      f"(Streak day {streak}: +{streak_bonus} bonus)")

    async def cmd_hourly(self, ctx, author: str):
        """Claim hourly token bonus"""
        last_hourly = await self.storage.get_metadata(f"last_hourly_{author}")
        now = int(time.time())
        
        if last_hourly and now - int(last_hourly) < 3600:
            remaining = 3600 - (now - int(last_hourly))
            minutes = remaining // 60
            await ctx.send(f"{author}, hourly bonus available in {minutes} minutes!")
            return
        
        reward = 3
        await self.storage.add_tokens(author, reward)
        await self.storage.set_metadata(f"last_hourly_{author}", str(now))
        
        await ctx.send(f"? {author} claimed hourly bonus: {reward} tokens!")

    async def cmd_work(self, ctx, author: str):
        """Work in the bakery for tokens (mini-game)"""
        if not self.cooldowns.check(f"work:{author}", 300):  # 5 minute cooldown
            await ctx.send(f"{author}, you're already tired from work! Rest for a bit.")
            return
        
        jobs = [
            {"name": "kneading dough", "reward": (5, 8), "description": "You knead fresh bread dough"},
            {"name": "decorating cakes", "reward": (6, 10), "description": "You carefully decorate wedding cakes"},
            {"name": "managing the oven", "reward": (4, 7), "description": "You monitor perfect baking temperatures"},
            {"name": "serving customers", "reward": (7, 12), "description": "You serve happy bakery customers"},
            {"name": "cleaning equipment", "reward": (3, 5), "description": "You sanitize all baking tools"},
            {"name": "inventory counting", "reward": (4, 6), "description": "You organize ingredient supplies"}
        ]
        
        job = random.choice(jobs)
        reward = random.randint(job["reward"][0], job["reward"][1])
        
        await self.storage.add_tokens(author, reward)
        await ctx.send(f"????? {author} spent time {job['name']}. {job['description']} and earned {reward} tokens!")

    async def cmd_tokens(self, ctx, author: str, args):
        """Check token balance"""
        target = args[0].lstrip('@').lower() if args else author.lower()
        user_data = await self.storage.get_or_create_user(target)
        
        await ctx.send(f"?? {target} has {user_data['tokens']} tokens. "
                      f"Earn more with !daily, !hourly, !work, or games!")

    async def cmd_gift_tokens(self, ctx, author: str, args):
        """Gift tokens to another user"""
        if len(args) < 2:
            await ctx.send(f"{author}, usage: !gift @username amount")
            return
        
        target = args[0].lstrip('@').lower()
        try:
            amount = int(args[1])
        except ValueError:
            await ctx.send(f"{author}, please enter a valid number!")
            return
        
        if amount <= 0:
            await ctx.send(f"{author}, amount must be positive!")
            return
        
        if target == author.lower():
            await ctx.send(f"{author}, you cannot gift tokens to yourself!")
            return
        
        sender_data = await self.storage.get_or_create_user(author)
        
        if sender_data['tokens'] < amount:
            await ctx.send(f"{author}, you only have {sender_data['tokens']} tokens!")
            return
        
        # Apply small fee to prevent abuse (5% minimum 1 token)
        fee = max(1, amount // 20)
        net_amount = amount - fee
        
        await self.storage.add_tokens(author, -amount)
        await self.storage.add_tokens(target, net_amount)
        
        await ctx.send(f"?? {author} gifted {net_amount} tokens to {target}! "
                      f"(Transfer fee: {fee} tokens)")

    # Existing command methods...
    async def cmd_recipe(self, ctx):
        await ctx.send('Try Chocolate Chip Cookies: https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/')

    async def cmd_bakeoff(self, ctx):
        await ctx.send('Bake-Off time! Try !seasonal, !guess, !oventrivia, !fight, or check the !shop for power-ups!')

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
        
        # Check for special title
        title = await self.storage.get_metadata(f"title_{target}")
        title_display = f"[{title}] " if title else ""
        
        await ctx.send(f"?? {title_display}{target}: Level {level} | {user_data['xp']} XP | {user_data['tokens']} tokens | "
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

    async def award_participation(self, author: str):
        await self.storage.add_xp(author, 1)

    async def award_win(self, author: str):
        await self.storage.add_xp(author, 25)
        await self.storage.add_tokens(author, 5)
        await self.storage.add_win(author)
