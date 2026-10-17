/* Sidefoden – den samme sorte sidefod som på www.kontraktbridge.dk, nederst på forsiden, trænerne og Viden.
   Siden har et tomt <footer id="sidefod"> uden for <main> (så doc-export.js ikke tager den med i Word-filen)
   og henter dette script lige efter. Al tekst og stil står kun her.
   Sproget følger lang.js; sider uden lang.js (Viden og multitræneren) er på dansk.
   Links til aftalerne regnes relativt ud fra scriptets egen adresse (assets/footer.js eller ../assets/footer.js),
   links til de andre trænere skrives med / foran, fordi siderne ligger på www.kontraktbridge.dk. */
(function () {
  var el = document.getElementById('sidefod');
  var me = document.currentScript;
  if (!el || !me) return;
  var EN = window.LANG === 'en';
  function t(da, en) { return EN ? en : da; }
  var root = (me.getAttribute('src') || '').replace(/assets\/footer\.js.*$/, '');

  var css = ''
    + '#sidefod{box-sizing:border-box;max-width:64rem;margin:var(--sg-space-3xl,48px) auto var(--sg-space-xl,24px);padding:0 var(--sg-space-xl,24px);'
    + 'font-family:var(--sg-sans,Inter,system-ui,sans-serif);font-size:14px;line-height:20px;letter-spacing:normal;text-align:left}'
    + '#sidefod .sf{display:flex;flex-direction:column;gap:var(--sg-space-2xl,32px);padding:var(--sg-space-3xl,48px) var(--sg-space-xl,24px);'
    + 'background:var(--sg-ink,#1a1a1a);color:var(--sg-canvas-soft,#f2f3f4);border-radius:var(--sg-radius-xl,24px)}'
    + '#sidefod .sf-top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:var(--sg-space-2xl,32px)}'
    + '#sidefod .sf-om{display:flex;flex-direction:column;gap:var(--sg-space-md,12px);max-width:420px}'
    + '#sidefod .sf-navn{font-family:var(--sg-display,Manrope,Inter,system-ui,sans-serif);font-weight:800;font-size:24px;line-height:28px;'
    + 'color:var(--sg-primary,#ff9f4a);text-decoration:none;align-self:flex-start}'
    + '#sidefod h2{margin:0;padding:0;border:0;font-family:inherit;font-size:14px;line-height:20px;font-weight:600;letter-spacing:normal;color:inherit;text-transform:none}'
    + '#sidefod .sf-om h2{margin-top:var(--sg-space-sm,8px);font-size:18px;line-height:24px}'
    + '#sidefod h2::before,#sidefod h2::after{content:none}'
    + '#sidefod p{margin:0;max-width:none;font-size:16px;line-height:24px;color:inherit}'
    + '#sidefod .sf-kolonner{display:flex;flex-wrap:wrap;gap:var(--sg-space-3xl,48px)}'
    + '#sidefod .sf-kol{display:flex;flex-direction:column;gap:var(--sg-space-sm,8px);max-width:240px}'
    + '#sidefod .sf-kol p{font-size:14px;line-height:20px}'
    + '#sidefod a{color:var(--sg-canvas-soft,#f2f3f4);text-decoration:none;font-weight:400}'
    + '#sidefod a:hover{color:var(--sg-primary-active,#ffc48f);text-decoration:underline}'
    + '#sidefod a:focus-visible{outline:2px solid var(--sg-primary,#ff9f4a);outline-offset:2px;border-radius:4px}'
    + '#sidefod a.sf-navn,#sidefod a.sf-mail{color:var(--sg-primary,#ff9f4a)}'
    + '#sidefod a.sf-mail{font-weight:600;overflow-wrap:anywhere}'
    + '#sidefod .sf-legal{padding-top:var(--sg-space-xl,24px);border-top:1px solid var(--sg-body,#4a4a4a);font-size:12px;line-height:16px}'
    + '@media (max-width:600px){#sidefod{padding:0 var(--sg-space-lg,16px)}#sidefod .sf{padding:var(--sg-space-2xl,32px) 20px}}'
    + '@media print{#sidefod{display:none}}';
  var style = document.createElement('style');
  style.id = 'sidefod-stil';
  style.textContent = css;
  document.head.appendChild(style);

  function link(href, da, en) { return '<a href="' + href + '">' + t(da, en) + '</a>'; }
  el.innerHTML = '<div class="sf"><div class="sf-top">'
    + '<div class="sf-om">'
    +   '<a class="sf-navn" href="https://www.kontraktbridge.dk/">Kontraktbridge</a>'
    +   '<h2>' + t('Om mig', 'About me') + '</h2>'
    +   '<p>' + t('Jeg er bridgeentusiast med forkærlighed for spillets kognitive udfordringer og det gode fællesskab omkring bordet. Jeg elsker at skabe og forbedre ting – og med AI som ny medspiller har jeg bygget et digitalt bridge-univers, der kombinerer logik, læring og spilleglæde.',
               'I am a bridge enthusiast with a soft spot for the cognitive challenges of the game and the good company around the table. I love creating and improving things – and with AI as a new partner, I have built a digital bridge universe that combines logic, learning and the joy of playing.') + '</p>'
    + '</div>'
    + '<div class="sf-kolonner">'
    +   '<div class="sf-kol"><h2>' + t('Trænere', 'Trainers') + '</h2>'
    +     link(root || './', 'Konventionstræner', 'Konventionstræner')
    +     link('/fordelingstraeneren/', 'Fordeling', 'Distribution')
    +     link('/fordelingstraeneren/', 'Pointregnskab', 'Point count')
    +     link('/fordelingstraeneren/', 'Farvebehandling', 'Suit combinations')
    +     link('/fordelingstraeneren/', 'Håndevaluering', 'Hand evaluation')
    +   '</div>'
    +   '<div class="sf-kol"><h2>' + t('Aftaler og notater', 'Agreements and notes (in Danish)') + '</h2>'
    +     link(root + 'viden/bridgesystem.html', 'Makker 1 &amp; mig', 'Partner 1 &amp; me')
    +     link(root + 'viden/2-over-1-makker2.html', 'Makker 2 &amp; mig', 'Partner 2 &amp; me')
    +     link(root + 'viden/kampen-om-kontrakten.html', 'Kampen om kontrakten', 'The battle for the contract')
    +     link(root + 'viden/#forslag', 'Forslag', 'Proposals')
    +     link(root + 'viden/#forskelle', 'Forskelle mellem systemerne', 'Differences between the systems')
    +   '</div>'
    +   '<div class="sf-kol"><h2>' + t('Kontakt', 'Contact') + '</h2>'
    +     '<p>' + t('Har du fundet en fejl, eller har du en idé til en ny træner? Skriv til mig.',
                    'Have you found a mistake, or do you have an idea for a new trainer? Write to me.') + '</p>'
    +     '<a class="sf-mail" href="mailto:frank.steen.pedersen@gmail.com">frank.steen.pedersen@gmail.com</a>'
    +   '</div>'
    + '</div></div>'
    + '<div class="sf-legal">© 2026 Frank Pedersen</div></div>';
})();
