/* ⓘ i trænerne: et tryk folder konventionskortets kompaktvisning ud under titlen (SPEC-konventionskort, Afklaret 5–9).
   Genereret af tools/build_konventionskort.py fra tools/konventionskort.src.html og tools/konventionskort-hint-shell.js – ret dér, ikke her.
   Brug: konventionskortHint(id, titel, efter) – knappen sættes i titel-elementet og kortet efter elementet efter.
   Findes der intet kort med det id i data/kort/index.json, sker der ingenting. */
(function () {
  var me = document.currentScript;
  var root = (me && me.getAttribute('src') || '').replace(/assets\/konventionskort-hint\.js.*$/, '');
  var t = function (da, en) { return typeof T === 'function' ? T(da, en) : da; };

  // Visningsfunktionerne fra tools/konventionskort.src.html (de samme som på viden/konventionskort.html)
/*SCRIPT*/

  var CSS = `/*CSS*/`;
  // Kortet står til venstre under titlen i stedet for centreret som på Viden. Kildens .ramme p er ment for noten under
  // kortet, men rammer også kortets egne afsnit; her står de til venstre i fuld bredde.
  var HINT_CSS = '.kk-body{padding:0}.ramme{justify-items:start}.ramme > p{display:none}.kompakt{justify-self:start;max-width:40rem}'
    + '.kompakt p{text-align:left;max-width:none}'
    + '.kk-sprog{margin:0 0 8px;font-size:.85rem;color:var(--mute)}';

  var style = document.createElement('style');
  style.textContent = '.kk-i{position:relative;display:inline-flex;align-items:center;justify-content:center;width:1.75rem;height:1.75rem;'
    + 'margin-left:.35em;padding:0;border:2px solid currentColor;border-radius:50%;background:transparent;color:var(--sg-body,#55554f);'
    + 'font:italic 700 1.05rem/1 Georgia,"Times New Roman",serif;vertical-align:middle;cursor:pointer}'
    + '.kk-i::before{content:"";position:absolute;inset:-8px}'
    + '.kk-i:hover{color:var(--sg-ink,#1c1c1b)}'
    + '.kk-i[aria-expanded="true"]{background:var(--sg-ink,#1c1c1b);border-color:var(--sg-ink,#1c1c1b);color:#fff}'
    + '.kk-i:focus-visible{outline:2px solid #ff9f4a;outline-offset:2px}'
    + '.kk-hint{margin:16px 0 0}'
    + '@media print{.kk-i,.kk-hint{display:none}}';
  document.head.appendChild(style);

  function panel(k) {
    var ydre = document.createElement('div');
    ydre.className = 'kk-hint';
    ydre.id = 'kk-hint-' + k.id;
    ydre.hidden = true;
    var vaert = document.createElement('div');
    ydre.appendChild(vaert);
    var R = vaert.attachShadow({ mode: 'open' });
    R.innerHTML = '<style>' + CSS + HINT_CSS + '</style><div class="kk-body">'
      + (document.documentElement.lang === 'en' ? '<p class="kk-sprog">The convention card is in Danish.</p>' : '') + kompakt(k) + '</div>';
    var mere = R.querySelector('.mere');
    mere.removeAttribute('data-goto');
    mere.href = root + 'viden/konventionskort.html#' + encodeURIComponent(k.id);
    mere.textContent = 'Hele konventionen →';
    return ydre;
  }

  window.konventionskortHint = function (id, titel, efter) {
    if (!id || !titel || !efter) return;
    fetch(root + 'data/kort/index.json').then(function (r) { return r.json(); })
      .then(function (idx) { return idx.indexOf(id + '.json') < 0 ? null : fetch(root + 'data/kort/' + id + '.json').then(function (r) { return r.json(); }); })
      .then(function (k) {
        if (!k) return;
        var ydre = panel(k);
        efter.insertAdjacentElement('afterend', ydre);
        var knap = document.createElement('button');
        knap.type = 'button';
        knap.className = 'kk-i';
        knap.setAttribute('aria-expanded', 'false');
        knap.setAttribute('aria-controls', ydre.id);
        knap.setAttribute('aria-label', t('Om konventionen', 'About the convention (in Danish)'));
        knap.title = knap.getAttribute('aria-label');
        knap.innerHTML = '<span aria-hidden="true">i</span>';
        knap.addEventListener('click', function () {
          var aaben = ydre.hidden;
          ydre.hidden = !aaben;
          knap.setAttribute('aria-expanded', String(aaben));
        });
        titel.appendChild(knap);
        // Variantvælgeren i traener.html skriver titlen om; så sættes knappen ind igen
        new MutationObserver(function () { if (!titel.contains(knap)) titel.appendChild(knap); }).observe(titel, { childList: true });
      })
      .catch(function () {});
  };
})();
