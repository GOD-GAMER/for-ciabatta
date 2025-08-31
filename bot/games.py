import asyncio
import random
import time
import math
from typing import Dict, Optional, List
from rapidfuzz import fuzz

class BreadFightGame:
    def __init__(self):
        self.active_fights: Dict[str, Dict] = {}
        self.pending_challenges: Dict[str, Dict] = {}
        
        # Bread knowledge questions for damage calculation
        self.fight_questions = [
            {"question": "What makes bread rise?", "answer": "yeast", "difficulty": 1},
            {"question": "What temperature kills yeast?", "answer": "140", "difficulty": 2},
            {"question": "What's the process of kneading called?", "answer": "gluten development", "difficulty": 3},
            {"question": "What's a starter culture called?", "answer": "sourdough", "difficulty": 2},
            {"question": "What flour has the highest protein?", "answer": "bread flour", "difficulty": 2},
            {"question": "What creates steam in bread?", "answer": "water", "difficulty": 1},
            {"question": "What's the Maillard reaction?", "answer": "browning", "difficulty": 3},
            {"question": "What's autolyse in bread making?", "answer": "flour water rest", "difficulty": 3},
            {"question": "What creates holes in bread?", "answer": "carbon dioxide", "difficulty": 2},
            {"question": "What's the ideal proofing temperature?", "answer": "75-80", "difficulty": 2}
        ]
    
    def calculate_level(self, xp: int) -> int:
        """Calculate level from XP (every 100 XP = 1 level)"""
        return max(1, xp // 100)
    
    def calculate_health(self, level: int) -> int:
        """Calculate max health based on level"""
        return 50 + (level * 10)
    
    def calculate_base_damage(self, level: int) -> int:
        """Calculate base damage based on level"""
        return 10 + (level * 2)

class BakingGames:
    def __init__(self, award_cb, win_cb):
        self.current_game: Optional[Dict] = None
        self.award_cb = award_cb
        self.win_cb = win_cb
        self.season: Optional[str] = None
        self.bread_fight = BreadFightGame()

    def set_season(self, season: Optional[str]):
        self.season = season

    def _normalize(self, s: str) -> str:
        return ''.join(ch.lower() for ch in s if ch.isalnum() or ch.isspace()).strip()

    async def start_bread_fight_challenge(self, ctx, challenger: str, target: str, storage):
        """Start a bread fight challenge between two players"""
        challenger = challenger.lower()
        target = target.lower()
        
        # Check if either player is already in a fight
        if challenger in self.bread_fight.active_fights or target in self.bread_fight.active_fights:
            await ctx.send(f"{challenger}, one of you is already in a bread fight!")
            return
        
        # Check if there's already a pending challenge
        if target in self.bread_fight.pending_challenges:
            await ctx.send(f"{target} already has a pending challenge!")
            return
            
        # Get player stats
        challenger_data = await storage.get_or_create_user(challenger)
        target_data = await storage.get_or_create_user(target)
        
        challenger_level = self.bread_fight.calculate_level(challenger_data['xp'])
        target_level = self.bread_fight.calculate_level(target_data['xp'])
        
        # Create challenge
        self.bread_fight.pending_challenges[target] = {
            'challenger': challenger,
            'challenger_level': challenger_level,
            'target_level': target_level,
            'expires': time.time() + 60  # 60 second timeout
        }
        
        await ctx.send(f"???? {challenger} (Level {challenger_level}) challenges {target} (Level {target_level}) to a BREAD FIGHT! "
                      f"{target}, type '!accept' within 60 seconds to accept the challenge!")
        
        # Set timeout to clean up pending challenge
        asyncio.create_task(self._cleanup_challenge(target, 60))

    async def accept_bread_fight(self, ctx, accepter: str, storage):
        """Accept a bread fight challenge"""
        accepter = accepter.lower()
        
        if accepter not in self.bread_fight.pending_challenges:
            await ctx.send(f"{accepter}, you don't have any pending challenges!")
            return
        
        challenge = self.bread_fight.pending_challenges.pop(accepter)
        
        if time.time() > challenge['expires']:
            await ctx.send(f"{accepter}, the challenge has expired!")
            return
        
        challenger = challenge['challenger']
        challenger_level = challenge['challenger_level']
        target_level = challenge['target_level']
        
        # Calculate health for both players
        challenger_health = self.bread_fight.calculate_health(challenger_level)
        target_health = self.bread_fight.calculate_health(target_level)
        
        # Create the fight
        fight_data = {
            'challenger': challenger,
            'target': accepter,
            'challenger_level': challenger_level,
            'target_level': target_level,
            'challenger_health': challenger_health,
            'target_health': target_health,
            'challenger_max_health': challenger_health,
            'target_max_health': target_health,
            'current_turn': challenger,  # Challenger goes first
            'question': None,
            'question_start': 0,
            'turn_timeout': 30,
            'round': 1
        }
        
        # Add both players to active fights
        self.bread_fight.active_fights[challenger] = fight_data
        self.bread_fight.active_fights[accepter] = fight_data
        
        await ctx.send(f"???? BREAD FIGHT BEGINS! {challenger} (Level {challenger_level}, {challenger_health}??) vs "
                      f"{accepter} (Level {target_level}, {target_health}??)")
        
        # Start first turn
        await self._start_fight_turn(ctx, fight_data)

    async def _start_fight_turn(self, ctx, fight_data):
        """Start a new turn in the bread fight"""
        current_player = fight_data['current_turn']
        other_player = fight_data['target'] if current_player == fight_data['challenger'] else fight_data['challenger']
        
        # Select a random question
        question_data = random.choice(self.bread_fight.fight_questions)
        fight_data['question'] = question_data
        fight_data['question_start'] = time.time()
        
        await ctx.send(f"?? Round {fight_data['round']}: {current_player}'s turn! "
                      f"Answer this bread question for damage: **{question_data['question']}** "
                      f"(Difficulty: {'?' * question_data['difficulty']}) - 15 seconds!")
        
        # Set timeout for question
        asyncio.create_task(self._question_timeout(ctx, fight_data, 15))

    async def handle_bread_fight_answer(self, ctx, author: str, message: str, storage):
        """Handle answers during bread fights"""
        author = author.lower()
        
        if author not in self.bread_fight.active_fights:
            return False
        
        fight_data = self.bread_fight.active_fights[author]
        
        # Check if it's this player's turn
        if fight_data['current_turn'] != author:
            return False
        
        # Check if there's an active question
        if not fight_data['question'] or time.time() > fight_data['question_start'] + 15:
            return False
        
        question_data = fight_data['question']
        
        # Check answer accuracy using fuzzy matching
        accuracy = fuzz.ratio(self._normalize(message), self._normalize(question_data['answer']))
        
        if accuracy >= 75:  # 75% accuracy required
            # Calculate damage based on accuracy and difficulty
            base_damage = self.bread_fight.calculate_base_damage(
                fight_data['challenger_level'] if author == fight_data['challenger'] else fight_data['target_level']
            )
            
            # Damage multipliers based on accuracy and difficulty
            accuracy_multiplier = 0.5 + (accuracy / 100)  # 0.75 to 1.5x
            difficulty_multiplier = question_data['difficulty'] * 0.3  # 0.3x to 0.9x
            
            total_damage = int(base_damage * accuracy_multiplier * (1 + difficulty_multiplier))
            
            # Apply damage to opponent
            other_player = fight_data['target'] if author == fight_data['challenger'] else fight_data['challenger']
            
            if other_player == fight_data['challenger']:
                fight_data['challenger_health'] = max(0, fight_data['challenger_health'] - total_damage)
                remaining_health = fight_data['challenger_health']
                max_health = fight_data['challenger_max_health']
            else:
                fight_data['target_health'] = max(0, fight_data['target_health'] - total_damage)
                remaining_health = fight_data['target_health']
                max_health = fight_data['target_max_health']
            
            await ctx.send(f"? Correct! {author} deals {total_damage} damage to {other_player}! "
                          f"{other_player} has {remaining_health}/{max_health}?? remaining!")
            
            # Check for victory
            if remaining_health <= 0:
                await self._end_bread_fight(ctx, author, other_player, fight_data, storage)
                return True
        else:
            await ctx.send(f"? Wrong answer, {author}! No damage dealt.")
        
        # Switch turns
        fight_data['current_turn'] = fight_data['target'] if author == fight_data['challenger'] else fight_data['challenger']
        fight_data['round'] += 1
        fight_data['question'] = None
        
        # Start next turn after a short delay
        await asyncio.sleep(2)
        await self._start_fight_turn(ctx, fight_data)
        
        return True

    async def _end_bread_fight(self, ctx, winner: str, loser: str, fight_data, storage):
        """End a bread fight and award rewards"""
        # Remove both players from active fights
        if winner in self.bread_fight.active_fights:
            del self.bread_fight.active_fights[winner]
        if loser in self.bread_fight.active_fights:
            del self.bread_fight.active_fights[loser]
        
        await ctx.send(f"?? BREAD FIGHT OVER! {winner} defeats {loser} in epic bread combat! "
                      f"{winner} gains XP and tokens!")
        
        # Award winner
        await self.win_cb(winner)
        
        # Small consolation for loser (participation XP)
        await self.award_cb(loser)

    async def _question_timeout(self, ctx, fight_data, timeout):
        """Handle question timeout in bread fights"""
        await asyncio.sleep(timeout)
        
        if fight_data['question'] and time.time() >= fight_data['question_start'] + timeout:
            current_player = fight_data['current_turn']
            other_player = fight_data['target'] if current_player == fight_data['challenger'] else fight_data['challenger']
            
            await ctx.send(f"? Time's up! {current_player} failed to answer. No damage dealt!")
            
            # Switch turns
            fight_data['current_turn'] = other_player
            fight_data['round'] += 1
            fight_data['question'] = None
            
            # Start next turn
            await asyncio.sleep(2)
            await self._start_fight_turn(ctx, fight_data)

    async def _cleanup_challenge(self, target: str, timeout: int):
        """Clean up expired challenges"""
        await asyncio.sleep(timeout)
        if target in self.bread_fight.pending_challenges:
            del self.bread_fight.pending_challenges[target]

    async def start_guess_ingredient(self, ctx, ingredients=None, answer=None, duration=30):
        if self.current_game:
            await ctx.send('Another game is already running. Please wait!')
            return
        ingredients = ingredients or ['flour', 'sugar', 'butter', 'eggs', 'vanilla', 'baking soda', 'salt', 'cocoa powder']
        answer = answer or random.choice(ingredients)
        self.current_game = {
            'type': 'guess', 'answer': answer, 'end': time.time() + duration,
            'hint': answer[0] + ('*' * (len(answer) - 1))
        }
        await ctx.send(f"Guess the Ingredient! Hint: {self.current_game['hint']} - You have {duration}s. Use chat to guess!")
        await asyncio.sleep(duration)
        if self.current_game and time.time() >= self.current_game['end']:
            await ctx.send(f"Time's up! The ingredient was: {answer}.")
            self.current_game = None

    async def start_oven_timer_trivia(self, ctx, question=None, answer=None, duration=25):
        if self.current_game:
            await ctx.send('Another game is already running. Please wait!')
            return
        qa = [
            ("What temp (F) is commonly used to bake cookies?", '350'),
            ("What ingredient makes bread rise?", 'yeast'),
            ("What does baking soda need to activate?", 'acid')
        ]
        if not question:
            question, answer = random.choice(qa)
        self.current_game = {'type': 'trivia', 'answer': answer, 'end': time.time() + duration}
        await ctx.send(f"Oven Timer Trivia: {question} - {duration}s to answer!")
        await asyncio.sleep(duration)
        if self.current_game:
            await ctx.send(f"Ding! Time's up. Correct answer: {answer}.")
            self.current_game = None

    async def start_seasonal_event(self, ctx, duration=25):
        if self.current_game:
            await ctx.send('Another game is already running. Please wait!')
            return
        # Simple seasonal placeholder: themed guess with narrower set
        if self.season == 'halloween':
            items = ['pumpkin', 'cinnamon', 'nutmeg', 'candy corn']
            name = 'Halloween Mystery Ingredient'
        elif self.season == 'holiday':
            items = ['ginger', 'peppermint', 'cranberry', 'eggnog']
            name = 'Holiday Secret Ingredient'
        else:
            items = ['honey', 'lemon', 'almond', 'oat']
            name = 'Seasonal Surprise Ingredient'
        answer = random.choice(items)
        self.current_game = {'type': 'seasonal', 'answer': answer, 'end': time.time() + duration}
        await ctx.send(f"{name}! Guess it in {duration}s!")
        await asyncio.sleep(duration)
        if self.current_game:
            await ctx.send(f"Seasonal round over! It was: {answer}.")
            self.current_game = None

    async def on_message(self, author: str, message: str, ctx=None, storage=None):
        # First check if this is a bread fight answer
        if storage and await self.handle_bread_fight_answer(ctx, author, message, storage):
            return None
        
        # Handle regular games
        if not self.current_game:
            return None
        g = self.current_game
        if g['type'] == 'guess':
            if fuzz.ratio(self._normalize(message), self._normalize(g['answer'])) >= 90:
                self.current_game = None
                await self.win_cb(author)
                return f"Correct, {author}! It was {g['answer']}!"
        elif g['type'] == 'trivia':
            if fuzz.ratio(self._normalize(message), self._normalize(g['answer'])) >= 90:
                self.current_game = None
                await self.win_cb(author)
                return f"Correct, {author}!"
        elif g['type'] == 'seasonal':
            if fuzz.ratio(self._normalize(message), self._normalize(g['answer'])) >= 90:
                self.current_game = None
                await self.win_cb(author)
                return f"You got it, {author}!"
        return None
