import aiohttp
from aiohttp import web
import aiosqlite
import qrcode
import io
import logging
import json
from datetime import datetime

logger = logging.getLogger('BakeBot.Web')

async def ensure_schema(db_path: str):
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            'CREATE TABLE IF NOT EXISTS recipes ('
            ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
            ' title TEXT NOT NULL,'
            ' url TEXT DEFAULT "",'
            ' description TEXT DEFAULT "",'
            ' visible INTEGER DEFAULT 1,'
            ' ord INTEGER DEFAULT 0,'
            ' created_at INTEGER DEFAULT (strftime("%s","now"))'
            ')'
        )
        await db.commit()

async def create_app(db_path: str):
    app = web.Application()
    await ensure_schema(db_path)

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
        <h1> ?? Bake-Off Leaderboard ??</h1>
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
        async with aiosqlite.connect(db_path) as db:
            async with db.execute('SELECT title, url, description FROM recipes WHERE visible=1 ORDER BY ord ASC, id ASC') as cur:
                rows = await cur.fetchall()
        cards = []
        for title, url, desc in rows:
            title_html = f"<a href='{url}' target='_blank'>{title}</a>" if url else title
            desc_html = f"<p>{desc}</p>" if desc else ''
            cards.append(f"<div class='recipe'><h3>{title_html}</h3>{desc_html}</div>")
        items_html = "\n".join(cards) if cards else "<p>No recipes yet.</p>"
        html = f"""
        <!DOCTYPE html>
        <html><head>
        <title>Recipes</title>
        <meta charset="utf-8">
        <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #8b4513; text-align: center; }}
        .recipe {{ margin: 20px 0; padding: 15px; background: #fff3cd; border-radius: 5px; border-left: 4px solid #d4a574; }}
        a.btn {{ display:inline-block; padding:8px 12px; background:#d4a574; color:white; text-decoration:none; border-radius:6px }}
        </style>
        </head>
        <body>
        <div class="container">
        <h1> ?? Favorite Recipes ??</h1>
        {items_html}
        <p><a class='btn' href="/leaderboard">Back to Leaderboard</a></p>
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

    # Recipes API
    async def list_recipes(request):
        async with aiosqlite.connect(db_path) as db:
            async with db.execute('SELECT id, title, url, description, visible, ord, created_at FROM recipes ORDER BY ord ASC, id ASC') as cur:
                rows = await cur.fetchall()
        data = [
            {
                'id': r[0], 'title': r[1], 'url': r[2], 'description': r[3],
                'visible': bool(r[4]), 'ord': r[5], 'created_at': r[6]
            } for r in rows
        ]
        return web.json_response({'data': data})

    async def create_recipe(request):
        try:
            data = await request.json()
        except Exception:
            return web.json_response({'error': 'Invalid JSON'}, status=400)
        title = (data.get('title') or '').strip()
        if not title:
            return web.json_response({'error': 'title required'}, status=400)
        url = (data.get('url') or '').strip()
        desc = (data.get('description') or '').strip()
        visible = 1 if str(data.get('visible', '1')).lower() in ('1','true','yes','on') else 0
        ordv = int(data.get('ord', 0) or 0)
        async with aiosqlite.connect(db_path) as db:
            await db.execute('INSERT INTO recipes(title,url,description,visible,ord) VALUES(?,?,?,?,?)', (title, url, desc, visible, ordv))
            await db.commit()
        return web.json_response({'success': True})

    async def update_recipe(request):
        rid = request.match_info.get('rid')
        try:
            data = await request.json()
        except Exception:
            return web.json_response({'error': 'Invalid JSON'}, status=400)
        fields = []
        values = []
        for key in ('title','url','description','ord','visible'):
            if key in data:
                if key == 'visible':
                    values.append(1 if str(data['visible']).lower() in ('1','true','yes','on') else 0)
                else:
                    values.append(data[key])
                fields.append(f"{key}=?")
        if not fields:
            return web.json_response({'error': 'no fields'}, status=400)
        async with aiosqlite.connect(db_path) as db:
            await db.execute(f'UPDATE recipes SET {", ".join(fields)} WHERE id=?', (*values, rid))
            await db.commit()
        return web.json_response({'success': True})

    async def delete_recipe(request):
        rid = request.match_info.get('rid')
        async with aiosqlite.connect(db_path) as db:
            await db.execute('DELETE FROM recipes WHERE id=?', (rid,))
            await db.commit()
        return web.json_response({'success': True})

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
        web.get('/api/recipes', list_recipes),
        web.post('/api/recipes', create_recipe),
        web.put('/api/recipes/{rid}', update_recipe),
        web.delete('/api/recipes/{rid}', delete_recipe),
    ])

    return app
