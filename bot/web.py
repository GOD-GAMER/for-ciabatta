import aiohttp
from aiohttp import web
import aiosqlite
import qrcode
import io
import logging
import json
from datetime import datetime

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
        <!DOCTYPE html>
        <html><head>
        <title>Leaderboard</title>
        <meta charset="utf-8">
        <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #8b4513; text-align: center; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ padding: 10px; margin: 5px 0; background: #fff3cd; border-left: 4px solid #d4a574; }}
        .refresh {{ text-align: center; margin: 20px; }}
        </style>
        </head>
        <body>
        <div class="container">
        <h1>?? Bake-Off Leaderboard ??</h1>
        <ul>{items}</ul>
        <div class="refresh">
        <button onclick="location.reload()">Refresh</button>
        <a href="/recipes">View Recipes</a>
        </div>
        </div>
        </body></html>
        """
        return web.Response(text=html, content_type='text/html')

    async def recipe(request):
        logger.debug('GET /recipes')
        html = """
        <!DOCTYPE html>
        <html><head>
        <title>Recipes</title>
        <meta charset="utf-8">
        <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #8b4513; text-align: center; }
        .recipe { margin: 20px 0; padding: 15px; background: #fff3cd; border-radius: 5px; }
        </style>
        </head>
        <body>
        <div class="container">
        <h1>?? Favorite Recipes ??</h1>
        <div class="recipe">
          <h3><a href='https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/'>Classic Chocolate Chip Cookies</a></h3>
          <p>The ultimate comfort cookie that never fails!</p>
        </div>
        <div class="recipe">
          <h3><a href='https://www.kingarthurbaking.com/recipes/238-original-pancakes'>Fluffy Pancakes</a></h3>
          <p>Perfect weekend breakfast treat.</p>
        </div>
        <p><a href="/leaderboard">Back to Leaderboard</a></p>
        </div>
        </body></html>
        """
        return web.Response(text=html, content_type='text/html')

    async def users_api(request):
        logger.debug('GET /api/users')
        async with aiosqlite.connect(db_path) as db:
            async with db.execute('SELECT username, xp, tokens, wins, last_seen, notes, is_banned FROM users ORDER BY xp DESC') as cur:
                rows = await cur.fetchall()
        
        users = []
        for row in rows:
            users.append({
                'username': row[0],
                'xp': row[1],
                'tokens': row[2],
                'wins': row[3],
                'last_seen': datetime.fromtimestamp(row[4]).strftime('%Y-%m-%d %H:%M') if row[4] else 'Never',
                'notes': row[5] or '',
                'is_banned': bool(row[6])
            })
        
        return web.json_response(users)

    async def update_user_api(request):
        if request.method == 'POST':
            data = await request.json()
            username = data.get('username')
            if not username:
                return web.json_response({'error': 'Username required'}, status=400)
            
            logger.info('Updating user %s via web API', username)
            async with aiosqlite.connect(db_path) as db:
                updates = []
                values = []
                
                for field in ['xp', 'tokens', 'wins', 'notes', 'is_banned']:
                    if field in data:
                        updates.append(f'{field} = ?')
                        values.append(data[field])
                
                if updates:
                    values.append(username.lower())
                    await db.execute(f'UPDATE users SET {", ".join(updates)} WHERE username = ?', values)
                    await db.commit()
            
            return web.json_response({'success': True})
        
        return web.json_response({'error': 'Method not allowed'}, status=405)

    async def chat_logs_api(request):
        username = request.query.get('username', '').lower()
        limit = int(request.query.get('limit', 100))
        
        logger.debug('GET /api/chat_logs username=%s limit=%d', username, limit)
        
        async with aiosqlite.connect(db_path) as db:
            if username:
                query = 'SELECT username, message, timestamp, channel FROM chat_logs WHERE username = ? ORDER BY timestamp DESC LIMIT ?'
                params = (username, limit)
            else:
                query = 'SELECT username, message, timestamp, channel FROM chat_logs ORDER BY timestamp DESC LIMIT ?'
                params = (limit,)
                
            async with db.execute(query, params) as cur:
                rows = await cur.fetchall()
        
        logs = []
        for row in rows:
            logs.append({
                'username': row[0],
                'message': row[1],
                'timestamp': datetime.fromtimestamp(row[2]).strftime('%Y-%m-%d %H:%M:%S'),
                'channel': row[3]
            })
        
        return web.json_response(logs)

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
        web.get('/api/users', users_api),
        web.post('/api/users/update', update_user_api),
        web.get('/api/chat_logs', chat_logs_api),
    ])

    return app
