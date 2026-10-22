/* Sidefoden – den samme sorte sidefod som på www.kontraktbridge.dk (med 7NT-logoet), nederst på forsiden, trænerne og Viden.
   Siden har et tomt <footer id="sidefod"> uden for <main> (så doc-export.js ikke tager den med i Word-filen)
   og henter dette script lige efter. Al tekst og stil står kun her.
   Om mig og kontakt har sin egen side på www.kontraktbridge.dk/om-mig/; sidefoden har kun knappen dertil (SPEC-om-mig.md).
   Kolonnen Opslag med Bridgeordbog (www.kontraktbridge.dk/ordbog/) står efter Trænere som på hele sitet (SPEC-sprog-og-ordbog.md).
   Sproget følger lang.js; sider uden lang.js (systemdokumenterne) er på dansk.
   Links til aftalerne regnes relativt ud fra scriptets egen adresse (assets/footer.js eller ../assets/footer.js),
   links til de andre trænere skrives med / foran, fordi siderne ligger på www.kontraktbridge.dk. */
(function () {
  var el = document.getElementById('sidefod');
  var me = document.currentScript;
  if (!el || !me) return;
  var EN = window.LANG === 'en';
  function t(da, en) { return EN ? en : da; }
  var root = (me.getAttribute('src') || '').replace(/assets\/footer\.js.*$/, '');

  // Reglerne har #sidefod foran, så systemdokumenternes egne regler for h2, p, ul, li og a ikke slår igennem.
  var css = ''
    + '#sidefod{box-sizing:border-box;max-width:64rem;margin:var(--sg-space-3xl,48px) auto var(--sg-space-xl,24px);padding:0 var(--sg-space-xl,24px);'
    + 'font-family:var(--sg-sans,Inter,system-ui,sans-serif);font-size:15px;line-height:22px;letter-spacing:normal;text-align:left}'
    + '#sidefod .sf{display:flex;flex-direction:column;gap:28px;padding:var(--sg-space-3xl,48px) var(--sg-space-xl,24px);'
    + 'background:var(--sg-ink,#1a1a1a);color:var(--sg-canvas-soft,#f2f3f4);border-radius:var(--sg-radius-xl,24px)}'
    + '#sidefod .sf-top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:32px 56px}'
    + '#sidefod .sf-om{display:flex;flex-direction:column;align-items:flex-start;gap:12px;max-width:340px}'
    + '#sidefod .sf-navn{display:inline-flex;align-items:center;gap:10px;font-family:var(--sg-display,Manrope,Inter,system-ui,sans-serif);'
    + 'font-weight:800;font-size:19px;line-height:1;letter-spacing:-.01em;color:#fff;text-decoration:none}'
    + '#sidefod .sf-logo{display:inline-flex;align-items:center;justify-content:center;flex:none;width:36px;height:36px;border-radius:9px;'
    + 'background:var(--sg-primary,#ff9f4a);color:var(--sg-ink,#1a1a1a);font-size:13px;line-height:1;letter-spacing:-.02em}'
    + '#sidefod p{margin:0;max-width:none;font-size:15px;line-height:22px;color:#c9cdd2}'
    + '#sidefod .sf-kolonner{display:flex;flex-wrap:wrap;gap:32px 56px}'
    + '#sidefod .sf-kol{display:flex;flex-direction:column;gap:10px;min-width:150px}'
    + '#sidefod h2.kb-foot-title{margin:0 0 2px;padding:0;border:0;font-family:inherit;font-size:12px;line-height:16px;font-weight:600;'
    + 'letter-spacing:.08em;text-transform:uppercase;color:#9aa0a6}'
    + '#sidefod h2::before,#sidefod h2::after,#sidefod li::before,#sidefod li::after{content:none}'
    + '#sidefod ul{display:flex;flex-direction:column;gap:10px;margin:0;padding:0;list-style:none}'
    + '#sidefod li{margin:0;padding:0;font-size:15px;line-height:22px}'
    + '#sidefod a{color:#fff;font-weight:400;text-decoration:underline;text-decoration-color:rgba(255,255,255,.35);text-underline-offset:4px}'
    + '#sidefod a:hover{color:var(--sg-primary-active,#ffc48f);text-decoration-color:currentColor}'
    + '#sidefod a.sf-navn{text-decoration:none}'
    + '#sidefod a.sf-knap{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 18px;border-radius:9999px;'
    + 'background:var(--sg-primary,#ff9f4a);color:var(--sg-ink,#1a1a1a);font-weight:600;text-decoration:none}'
    + '#sidefod a.sf-knap:hover{background:#ffb46e;color:var(--sg-ink,#1a1a1a)}'
    + '#sidefod a:focus-visible{outline:2px solid var(--sg-primary,#ff9f4a);outline-offset:2px;border-radius:4px}'
    + '#sidefod .sf-legal{padding-top:20px;border-top:1px solid var(--sg-body,#4a4a4a);font-size:12px;line-height:16px;color:#9aa0a6}'
    + '@media (max-width:600px){#sidefod{padding:0 var(--sg-space-lg,16px)}#sidefod .sf{padding:var(--sg-space-2xl,32px) 20px}}'
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
    +   '<p>' + t('Gratis bridgetræning i browseren. Lavet af Frank Pedersen.', 'Free bridge training in your browser. Made by Frank Pedersen.') + '</p>'
    +   '<a class="sf-knap" href="https://www.kontraktbridge.dk/om-mig/">' + t('Om mig og kontakt', 'About me and contact') + ' <span aria-hidden="true">→</span></a>'
    + '</div>'
    + '<div class="sf-kolonner">'
    +   kolonne('traenere', 'Trænere', 'Trainers',
          link(root || './', 'Konventionstræner', 'Convention trainer')
        + link('/fordelingstraeneren/', 'Fordeling', 'Distribution')
        + link('/fordelingstraeneren/', 'Pointregnskab', 'Point count')
        + link('/fordelingstraeneren/', 'Farvebehandling', 'Suit combinations')
        + link('/fordelingstraeneren/', 'Håndevaluering', 'Hand evaluation'))
    +   kolonne('opslag', 'Opslag', 'Reference',
          link('/ordbog/', 'Bridgeordbog', 'Bridge dictionary'))
    +   kolonne('aftaler', 'Aftaler og notater', 'Agreements and notes (in Danish)',
          link(root + 'makkeraftaler.html#kf', 'Makker 1 & mig', 'Partner 1 & me')
        + link(root + 'makkeraftaler.html#ff', 'Makker 2 & mig', 'Partner 2 & me')
        + link(root + 'viden/kampen-om-kontrakten.html', 'Kampen om kontrakten', 'The battle for the contract')
        + link(root + 'viden/#forslag', 'Forslag', 'Proposals')
        + link(root + 'makkeraftaler.html#forskelle', 'Forskelle mellem systemerne', 'Differences between the systems'))
    + '</div></div>'
    + '<div class="sf-legal">© 2026 Frank Pedersen</div></div>';
})();
