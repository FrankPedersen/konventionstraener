/* Sidefoden – den samme sorte sidefod som på www.kontraktbridge.dk (med 7NT-logoet), nederst på forsiden, trænerne og Viden.
   Siden har et tomt <footer id="sidefod"> uden for <main> (så doc-export.js ikke tager den med i Word-filen)
   og henter dette script lige efter. Al tekst og stil står kun her.
   Om mig og kontakt har sin egen side på www.kontraktbridge.dk/om-mig/; sidefoden har kun knappen dertil (SPEC-om-mig.md).
   Den er ens med forsidens kompakte sidefod (SPEC-sidefod.md): kolonnerne Trænere og Opslag og ©-linjen, med målene fra SPEC-ny-forside.md.
   Sproget følger lang.js; sider uden lang.js (systemdokumenterne) er på dansk.
   Linket til Konventionstræner regnes relativt ud fra scriptets egen adresse (assets/footer.js eller ../assets/footer.js),
   links til de andre trænere skrives med / foran, fordi siderne ligger på www.kontraktbridge.dk. */
(function () {
  var el = document.getElementById('sidefod');
  var me = document.currentScript;
  if (!el || !me) return;
  var EN = window.LANG === 'en';
  function t(da, en) { return EN ? en : da; }
  var root = (me.getAttribute('src') || '').replace(/assets\/footer\.js.*$/, '');

  // Reglerne har #sidefod foran, så systemdokumenternes egne regler for h2, p, ul, li og a ikke slår igennem.
  // Målene er forsidens (SPEC-ny-forside.md, Afklaret); grænsen er 1000 px.
  var css = ''
    + '#sidefod{box-sizing:border-box;max-width:64rem;margin:var(--sg-space-3xl,48px) auto var(--sg-space-xl,24px);padding:0 var(--sg-space-xl,24px);'
    + 'font-family:var(--sg-sans,Inter,system-ui,sans-serif);font-size:14px;line-height:20px;letter-spacing:normal;text-align:left}'
    + '#sidefod .sf{display:flex;flex-direction:column;gap:16px;padding:24px 28px 18px;'
    + 'background:var(--sg-ink,#1a1a1a);color:var(--sg-canvas-soft,#f2f3f4);border-radius:20px}'
    + '#sidefod .sf-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-start;gap:20px 48px}'
    + '#sidefod .sf-om{display:flex;flex-direction:column;align-items:flex-start;gap:10px;max-width:320px}'
    + '#sidefod .sf-navn{display:inline-flex;align-items:center;gap:10px;font-family:var(--sg-display,Manrope,Inter,system-ui,sans-serif);'
    + 'font-weight:800;font-size:18px;line-height:1;letter-spacing:-.01em;color:#fff;text-decoration:none}'
    + '#sidefod .sf-logo{display:inline-flex;align-items:center;justify-content:center;flex:none;width:32px;height:32px;border-radius:8px;'
    + 'background:var(--sg-primary,#ff9f4a);color:var(--sg-ink,#1a1a1a);font-size:12px;line-height:1;letter-spacing:-.02em}'
    + '#sidefod p{margin:0;max-width:none;font-size:14px;line-height:20px;color:#c9cdd2}'
    + '#sidefod .sf-kolonner{display:flex;gap:48px}'
    + '#sidefod .sf-kol{display:flex;flex-direction:column;gap:4px}'
    + '#sidefod h2.kb-foot-title{margin:0 0 2px;padding:0;border:0;font-family:inherit;font-size:11px;line-height:16px;font-weight:600;'
    + 'letter-spacing:.08em;text-transform:uppercase;color:#9aa0a6}'
    + '#sidefod h2::before,#sidefod h2::after,#sidefod li::before,#sidefod li::after{content:none}'
    + '#sidefod ul{display:flex;flex-direction:column;gap:4px;margin:0;padding:0;list-style:none}'
    + '#sidefod li{margin:0;padding:0;font-size:14px;line-height:20px}'
    + '#sidefod a{color:#fff;font-weight:400;text-decoration:underline;text-decoration-color:rgba(255,255,255,.35);text-underline-offset:4px}'
    + '#sidefod a:hover{color:var(--sg-primary-active,#ffc48f);text-decoration-color:currentColor}'
    + '#sidefod a.sf-navn{text-decoration:none;font-weight:800}'
    + '#sidefod a.sf-knap{display:inline-flex;align-items:center;gap:8px;min-height:36px;padding:0 14px;border-radius:9999px;'
    + 'background:var(--sg-primary,#ff9f4a);color:var(--sg-ink,#1a1a1a);font-weight:600;text-decoration:none}'
    + '#sidefod a.sf-knap:hover{background:#ffb46e;color:var(--sg-ink,#1a1a1a)}'
    + '#sidefod a:focus-visible{outline:2px solid var(--sg-primary,#ff9f4a);outline-offset:2px;border-radius:4px}'
    + '#sidefod .sf-legal{padding-top:12px;border-top:1px solid var(--sg-body,#4a4a4a);font-size:12px;line-height:16px;color:#9aa0a6}'
    + '#sidefod .sf-legal-extra{display:none}'
    + '@media (max-width:999px){#sidefod{padding:0 var(--sg-space-lg,16px)}'
    + '#sidefod .sf{gap:12px;padding:18px 18px 14px}'
    + '#sidefod .sf-top{flex-direction:column;align-items:stretch;gap:12px}'
    + '#sidefod .sf-om{flex-direction:row;align-items:center;justify-content:space-between;gap:12px;max-width:none}'
    + '#sidefod .sf-om p{display:none}'
    + '#sidefod .sf-navn{gap:8px;font-size:16px}'
    + '#sidefod .sf-logo{width:30px;height:30px;font-size:11px}'
    + '#sidefod a.sf-knap{min-height:44px;font-size:13px}'
    + '#sidefod .sf-pil{display:none}'
    + '#sidefod .sf-kolonner{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}'
    + '#sidefod .sf-kol,#sidefod ul{gap:2px}'
    + '#sidefod li a{display:block;padding:3px 0}'
    + '#sidefod .sf-legal{padding-top:10px}'
    + '#sidefod .sf-legal-extra{display:inline}}'
    + '@media print{#sidefod{display:none}}';
  var style = document.createElement('style');
  style.id = 'sidefod-stil';
  style.textContent = css;
  document.head.appendChild(style);

  function link(href, da, en) { return '<li><a href="' + href + '">' + t(da, en) + '</a></li>'; }
  function kolonne(id, da, en, links) {
    return '<nav class="sf-kol" aria-labelledby="sf-' + id + '"><h2 class="kb-foot-title" id="sf-' + id + '">' + t(da, en) + '</h2>'
      + '<ul>' + links + '</ul></nav>';
  }
  el.innerHTML = '<div class="sf"><div class="sf-top">'
    + '<div class="sf-om">'
    +   '<a class="sf-navn" href="https://www.kontraktbridge.dk/"><span class="sf-logo" aria-hidden="true">7NT</span>Kontraktbridge</a>'
    +   '<p>' + t('Gratis bridgetræning i browseren. Lavet af Frank Pedersen.', 'Free bridge training in the browser. Made by Frank Pedersen.') + '</p>'
    +   '<a class="sf-knap" href="https://www.kontraktbridge.dk/om-mig/">' + t('Om mig og kontakt', 'About me and contact') + ' <span class="sf-pil" aria-hidden="true">→</span></a>'
    + '</div>'
    + '<div class="sf-kolonner">'
    +   kolonne('traenere', 'Trænere', 'Trainers',
          link(root || './', 'Konventionstræner', 'Convention trainer')
        + link('/fordelingstraeneren/#fordeling', 'Fordeling', 'Distribution')
        + link('/fordelingstraeneren/#pointregnskab', 'Pointregnskab', 'Point count')
        + link('/fordelingstraeneren/#farvebehandling', 'Farvebehandling', 'Suit combinations')
        + link('/fordelingstraeneren/#haandevaluering', 'Håndevaluering', 'Hand evaluation'))
    +   kolonne('opslag', 'Opslag', 'Reference',
          link('/fordelingstraeneren/#analyse', 'Analyse', 'Analysis')
        + link('/ordbog/', 'Bridgeordbog', 'Bridge dictionary')
        + link('/scoring/', 'Scoring i bridge', 'Scoring in bridge'))
    + '</div></div>'
    + '<div class="sf-legal">© 2026 Frank Pedersen<span class="sf-legal-extra"> · ' + t('Gratis bridgetræning i browseren', 'Free bridge training in the browser') + '</span></div></div>';
})();
