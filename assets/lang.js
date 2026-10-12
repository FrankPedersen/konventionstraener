/* Sprog – dansk som standard, engelsk med knappen »English« på forsiden (som i Fordelingstræneren).
   Valget gemmes i localStorage ('lang') og kan også sættes med ?lang=en eller ?lang=da i adressen.
     T('dansk', 'English')  vælger teksten efter sproget
     L(obj)                 lægger objektets "en"-felt ovenpå (data/*.json og puljerne fra build_pools.py)
     W('Makker')            faste ord fra puljerne: pladser, roller, Pas
     youAre('Svarer')       »Du er svarer« / »You are the responder«
   Elementer med data-en (indhold) og data-en-title (title) får den engelske tekst, når siden vises på engelsk.
   Systemdokumenterne under Viden er kun på dansk. */
(function () {
  var lang = 'da';
  try { if (localStorage.getItem('lang') === 'en') lang = 'en'; } catch (e) {}
  var q = new URLSearchParams(location.search).get('lang');
  if (q === 'en' || q === 'da') { lang = q; try { localStorage.setItem('lang', q); } catch (e) {} }
  var EN = lang === 'en';
  document.documentElement.lang = lang;
  window.LANG = lang;
  window.T = function (da, en) { return EN ? en : da; };

  function isObj(x) { return x && typeof x === 'object' && !Array.isArray(x); }
  function merge(a, b) { Object.keys(b).forEach(function (k) { if (isObj(a[k]) && isObj(b[k])) merge(a[k], b[k]); else a[k] = b[k]; }); }
  window.L = function loc(o) {
    if (Array.isArray(o)) return o.map(loc);
    if (!isObj(o)) return o;
    var out = {};
    Object.keys(o).forEach(function (k) { if (k !== 'en') out[k] = loc(o[k]); });
    if (EN && isObj(o.en)) merge(out, o.en);
    return out;
  };

  var WORDS = { 'Makker': 'Partner', 'Modstander': 'Opponent', 'Dig': 'You', 'Pas': 'Pass',
    'Åbner': 'Opener', 'Svarer': 'Responder', 'Indmelder': 'Overcaller', 'Modspiller': 'Defender', 'Genåbner': 'Balancer',
    'Dobler': 'Doubler', 'Fortsætter': 'Advancer', 'Spørger': 'Asker', 'Fjerde hånd': 'Fourth seat', 'Anden hånd': 'Second seat',
    'Nord': 'North', 'Øst': 'East', 'Syd': 'South', 'Vest': 'West' };
  window.W = function (w) { return (EN && WORDS[w]) || w; };
  var SEAT_ROLE = { 'Fjerde hånd': 'in fourth seat', 'Anden hånd': 'in second seat' };
  window.youAre = function (role) {
    if (!EN) return 'Du er ' + role.toLowerCase();
    return 'You are ' + (SEAT_ROLE[role] || (WORDS[role] ? 'the ' + WORDS[role].toLowerCase() : role));
  };

  document.addEventListener('DOMContentLoaded', function () {
    if (EN) {
      document.querySelectorAll('[data-en]').forEach(function (el) { el.innerHTML = el.getAttribute('data-en'); });
      document.querySelectorAll('[data-en-title]').forEach(function (el) { el.title = el.getAttribute('data-en-title'); });
    }
    var btn = document.getElementById('langBtn');
    if (btn) {
      btn.textContent = EN ? 'Dansk' : 'English';
      btn.setAttribute('lang', EN ? 'da' : 'en');
      btn.addEventListener('click', function () {
        var u = new URL(location.href);
        u.searchParams.delete('lang');
        try { localStorage.setItem('lang', EN ? 'da' : 'en'); } catch (e) { u.searchParams.set('lang', EN ? 'da' : 'en'); }
        location.href = u.toString();
      });
    }
  });
})();
