/* Topbjælken – den samme sorte bjælke øverst på alle sider i Konventionstræneren (SPEC-traen-side.md, Topbjælken).
   Siden har et tomt <header id="topbjaelke"> som første element i <body> og henter dette script lige efter:
     data-aktiv="traen" | "viden"   hvilket menupunkt der er den aktive side
     data-sprog                     sprogknappen vises (kun sider, der findes på engelsk; lang.js giver den sin funktion)
     data-traen="#traen"            adressen på Træn, når siden selv er forsiden
   Al tekst og stil står kun her. Adresserne regnes relativt ud fra scriptets egen adresse som i footer.js. */
(function () {
  var el = document.getElementById('topbjaelke');
  var me = document.currentScript;
  if (!el || !me) return;
  var EN = window.LANG === 'en';
  function t(da, en) { return EN ? en : da; }
  var root = (me.getAttribute('src') || '').replace(/assets\/topbar\.js.*$/, '');
  var aktiv = el.getAttribute('data-aktiv');

  var css = ''
    + '#topbjaelke{display:block;margin:0;padding:0;border:0;background:#1a1a1a}'
    + '#topbjaelke .kb-bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 20px;box-sizing:border-box;width:100%;'
    + 'margin:0;padding:12px 20px;background:#1a1a1a;color:#f2f3f4;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;'
    + 'font-size:14px;line-height:20px;font-weight:600;letter-spacing:normal;text-align:left}'
    + '#topbjaelke .kb-venstre{display:inline-flex;align-items:center;min-width:0}'
    + '#topbjaelke .kb-brand{display:inline-flex;align-items:center;gap:10px;color:#fff;text-decoration:none}'
    + '#topbjaelke .kb-logo{display:inline-flex;align-items:center;justify-content:center;flex:none;width:36px;height:36px;border-radius:9px;'
    + 'background:#ff9f4a;color:#1a1a1a;font-family:Manrope,Inter,system-ui,sans-serif;font-weight:800;font-size:13px;line-height:1;letter-spacing:-.02em}'
    + '#topbjaelke .kb-name{font-family:Manrope,Inter,system-ui,sans-serif;font-weight:800;font-size:19px;line-height:1;letter-spacing:-.01em}'
    + '#topbjaelke .kb-app{font-weight:600;color:#c9cdd2;white-space:nowrap}'
    + '#topbjaelke .kb-app::before{content:"\\00B7";margin:0 8px 0 10px;color:#8a8a8a}'
    + '#topbjaelke .kb-links{display:flex;flex-wrap:wrap;align-items:center;gap:4px}'
    + '#topbjaelke .kb-links a{padding:8px 14px;border-radius:9999px;color:#f2f3f4;text-decoration:none;font-weight:600}'
    + '#topbjaelke .kb-links a:hover{background:rgba(255,255,255,.08);color:#fff}'
    + '#topbjaelke .kb-links a[aria-current="page"]{background:rgba(255,255,255,.12);color:#fff}'
    + '#topbjaelke .kb-lang{margin-left:6px;min-height:36px;padding:0 14px;border:0;border-radius:9999px;background:transparent;'
    + 'box-shadow:inset 0 0 0 1px rgba(255,255,255,.3);color:#f2f3f4;font:inherit;cursor:pointer}'
    + '#topbjaelke .kb-lang:hover{background:rgba(255,255,255,.08)}'
    + '#topbjaelke a:focus-visible,#topbjaelke button:focus-visible{outline:2px solid #ff9f4a;outline-offset:2px}'
    + '@media (max-width:600px){#topbjaelke .kb-bar{padding:8px 12px;gap:8px}'
    + '#topbjaelke .kb-logo{width:30px;height:30px;border-radius:8px;font-size:11px}#topbjaelke .kb-name{font-size:16px}'
    + '#topbjaelke .kb-app::before{margin:0 6px 0 8px}#topbjaelke .kb-links a{padding:8px 12px}}'
    + '@media print{#topbjaelke{display:none}}';
  var style = document.createElement('style');
  style.id = 'topbjaelke-stil';
  style.textContent = css;
  document.head.appendChild(style);

  var traen = el.getAttribute('data-traen') || (root || './') + '#traen';
  function punkt(id, href, da, en) {
    return '<a href="' + href + '"' + (aktiv === id ? ' aria-current="page"' : '') + '>' + t(da, en) + '</a>';
  }
  el.innerHTML = '<nav class="kb-bar" aria-label="' + t('Hovedmenu', 'Main menu') + '">'
    + '<span class="kb-venstre"><a class="kb-brand" href="https://www.kontraktbridge.dk/">'
    +   '<span class="kb-logo" aria-hidden="true">7NT</span><span class="kb-name">Kontraktbridge</span></a>'
    +   '<span class="kb-app">Konventionstræner</span></span>'
    + '<div class="kb-links">'
    +   punkt('traen', traen, 'Træn', 'Train')
    +   punkt('viden', root + 'viden/', 'Viden', 'Reference')
    +   (el.hasAttribute('data-sprog') ? '<button class="kb-lang" id="langBtn" type="button">' + t('English', 'Dansk') + '</button>' : '')
    + '</div></nav>';
})();
