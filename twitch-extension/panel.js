(function(){
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(b => b.addEventListener('click', () => {
    tabs.forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    const id = b.dataset.tab; 
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(id).classList.add('active');
  }));

  let channelId = null;
  let authToken = null;
  let baseUrl = null;

  // Pull config via Twitch Extension helper
  const twitch = window.Twitch && window.Twitch.ext;
  if (twitch) {
    twitch.onAuthorized(function(auth) {
      channelId = auth.channelId;
      authToken = auth.token;
      twitch.configuration.onChanged(function(){
        try {
          if (twitch.configuration && twitch.configuration.broadcaster && twitch.configuration.broadcaster.content) {
            const cfg = JSON.parse(twitch.configuration.broadcaster.content);
            baseUrl = (cfg && cfg.publicBaseUrl) || '';
          }
        } catch (e) {
          baseUrl = '';
        }
        refresh();
      });
    });
  } else {
    // Fallback for local testing
    try { baseUrl = localStorage.getItem('bakebot_base_url') || ''; } catch {}
    refresh();
  }

  function refresh(){
    loadLeaderboard();
    loadRecipes();
  }

  async function loadLeaderboard(){
    const status = document.getElementById('lb-status');
    const list = document.getElementById('lb-list');
    list.innerHTML = '';
    status.textContent = 'Loading leaderboard...';
    const url = (baseUrl||'').replace(/\/$/,'') + '/ext/leaderboard';
    if(!baseUrl){ status.textContent = 'Not configured. Ask the broadcaster to set the extension config.'; return; }
    try{
      const r = await fetch(url, { headers: { 'Content-Type':'application/json' } });
      const d = await r.json();
      status.textContent = '';
      (d.data||[]).forEach((u,i) => {
        const li = document.createElement('li');
        li.innerHTML = `<span>#${i+1} ${u.username}</span><span class="meta">${u.xp} XP · ${u.wins} wins</span>`;
        list.appendChild(li);
      });
      if(list.children.length===0){ status.textContent = 'No data yet.'; }
    }catch(e){ status.textContent = 'Failed to load.'; }
  }

  async function loadRecipes(){
    const status = document.getElementById('rc-status');
    const list = document.getElementById('rc-list');
    list.innerHTML = '';
    status.textContent = 'Loading recipes...';
    const url = (baseUrl||'').replace(/\/$/,'') + '/ext/recipes';
    if(!baseUrl){ status.textContent = 'Not configured.'; return; }
    try{
      const r = await fetch(url, { headers: { 'Content-Type':'application/json' } });
      const d = await r.json();
      status.textContent = '';
      (d.data||[]).forEach((r) => {
        const li = document.createElement('li');
        const link = r.url ? `<a href="${r.url}" target="_blank">${r.title}</a>` : r.title;
        const desc = r.description ? `<div class="meta">${r.description}</div>` : '';
        li.innerHTML = `${link}${desc}`;
        list.appendChild(li);
      });
      if(list.children.length===0){ status.textContent = 'No recipes yet.'; }
    }catch(e){ status.textContent = 'Failed to load recipes.'; }
  }
})();
