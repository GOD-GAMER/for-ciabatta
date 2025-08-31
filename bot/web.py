import aiohttp
from aiohttp import web
import aiosqlite
import qrcode
import io
import logging

logger = logging.getLogger('BakeBot.Web')

async def create_app(db_path: str):
    app = web.Application()

    async def leaderboard(request):
        logger.debug('GET /leaderboard')
        async with aiosqlite.connect(db_path) as db:
            async with db.execute('SELECT username, xp, wins FROM users ORDER BY xp DESC LIMIT 20') as cur:
                rows = await cur.fetchall()
        items = ''.join(f"<li>{u} - {xp} XP - {w} wins</li>" for u, xp, w in rows)
        html = f"""
        <html><head><title>Leaderboard</title></head>
        <body>
        <h1>Bake-Off Leaderboard</h1>
        <ul>{items}</ul>
        </body></html>
        """
        return web.Response(text=html, content_type='text/html')

    async def recipe(request):
        logger.debug('GET /recipes')
        html = """
        <html><head><title>Recipes</title></head>
        <body>
        <h1>Favorite Recipes</h1>
        <ul>
          <li><a href='https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/'>Chocolate Chip Cookies</a></li>
        </ul>
        </body></html>
        """
        return web.Response(text=html, content_type='text/html')

    async def qr(request):
        url = request.query.get('url', 'https://twitch.tv')
        logger.debug('GET /qr url=%s', url)
        img = qrcode.make(url)
        bio = io.BytesIO()
        img.save(bio, format='PNG')
        return web.Response(body=bio.getvalue(), content_type='image/png')

    app.add_routes([
        web.get('/leaderboard', leaderboard),
        web.get('/recipes', recipe),
        web.get('/qr', qr),
    ])

    return app
