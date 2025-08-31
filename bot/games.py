import asyncio
import random
import time
from typing import Dict, Optional
from rapidfuzz import fuzz

class BakingGames:
    def __init__(self, award_cb, win_cb):
        self.current_game: Optional[Dict] = None
        self.award_cb = award_cb
        self.win_cb = win_cb
        self.season: Optional[str] = None  # e.g., 'halloween', 'holiday'

    def set_season(self, season: Optional[str]):
        self.season = season

    def _normalize(self, s: str) -> str:
        return ''.join(ch.lower() for ch in s if ch.isalnum() or ch.isspace()).strip()

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
        await ctx.send(f"Guess the Ingredient! Hint: {self.current_game['hint']} — You have {duration}s. Use chat to guess!")
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
        await ctx.send(f"Oven Timer Trivia: {question} — {duration}s to answer!")
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

    async def on_message(self, author: str, message: str):
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
