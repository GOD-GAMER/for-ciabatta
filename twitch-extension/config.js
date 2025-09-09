(function(){
  const twitch = window.Twitch && window.Twitch.ext;
  const input = document.getElementById('base-url');
  const status = document.getElementById('status');

  function show(msg){ status.textContent = msg; }

  function loadCfg(){
    try {
      if (twitch && twitch.configuration && twitch.configuration.broadcaster && twitch.configuration.broadcaster.content) {
        const cfg = JSON.parse(twitch.configuration.broadcaster.content);
        input.value = cfg && cfg.publicBaseUrl || '';
        show('Loaded current config.');
      } else {
        show('No broadcaster config set yet.');
      }
    } catch(e){ show('Failed to read config.'); }
  }

  function saveCfg(){
    const v = input.value.trim();
    if(!v || !/^https?:\/\//i.test(v)) { show('Please enter a valid URL (must start with http or https).'); return; }
    const payload = JSON.stringify({ publicBaseUrl: v });
    try {
      twitch.configuration.set('broadcaster', '1', payload);
      show('Saved!');
    } catch(e){ show('Failed to save config.'); }
  }

  document.getElementById('save').addEventListener('click', saveCfg);
  document.getElementById('load').addEventListener('click', loadCfg);

  if (twitch) {
    twitch.onAuthorized(function(){ loadCfg(); });
    twitch.configuration.onChanged(function(){ loadCfg(); });
  } else {
    show('Twitch helper not available (local dev).');
  }
})();
