/* Modspilsaftalerne (SPEC-modspilsaftaler.md, session 2): valget af metoder, fælles med Modspil i Fordelingstræneren,
   og udvælgelsen af quizspørgsmål. Logikken uden DOM, så den kan testes med node --test (tools/modspilsaftaler.test.mjs).

   Valget ligger i Modspils nøgle 'modspil:v1' (felterne profil og metoder). Konventionstræner skriver kun de to felter;
   alle andre felter bevares. Kan den gemte tilstand ikke læses som gyldig JSON med de to felter, skrives der ikke, og
   valget vises som Standard. Uden gemt tilstand gælder Standard, og et valg skriver en ny tilstand som Modspils
   standardtilstand (defaultMsSaved i Fordelingstræneren/src/modspil/storage.ts). */
(function (root) {
  var NOEGLE = 'modspil:v1';

  function isObj(x) { return x !== null && typeof x === 'object' && !Array.isArray(x); }
  function kopi(o) { var u = {}; Object.keys(o).forEach(function (k) { u[k] = o[k]; }); return u; }

  /** Profilens id, når metoderne svarer til en profil, ellers 'egen' (som profilId i Modspil). */
  function profilId(data, metoder) {
    var p = data.profiler.find(function (x) {
      return data.kategorier.every(function (k) { return x.valg[k.id] === metoder[k.id]; });
    });
    return p ? p.id : 'egen';
  }

  function profil(data, id) { return data.profiler.find(function (x) { return x.id === id; }); }
  function standard(data) { return kopi(profil(data, 'standard').valg); }

  /** Er metoderne gyldige: én kendt metode pr. kategori? */
  function gyldigeMetoder(data, m) {
    return isObj(m) && data.kategorier.every(function (k) {
      return typeof m[k.id] === 'string' && k.metoder.some(function (x) { return x.id === m[k.id]; });
    });
  }

  /** Læser den gemte tilstand: { status: 'tom' | 'gyldig' | 'ugyldig', obj }. */
  function laesTilstand(storage) {
    var tekst = null;
    try { tekst = storage.getItem(NOEGLE); } catch (e) { return { status: 'ugyldig' }; }
    if (tekst === null || tekst === undefined) return { status: 'tom' };
    var obj;
    try { obj = JSON.parse(tekst); } catch (e) { return { status: 'ugyldig' }; }
    if (!isObj(obj)) return { status: 'ugyldig' };
    return { status: 'gyldig', obj: obj };
  }

  /** Valget: { profil, metoder, kilde: 'standard' | 'gemt', note: true, når de gemte data ikke kunne læses }. */
  function laesValg(storage, data) {
    var t = laesTilstand(storage);
    if (t.status === 'gyldig' && typeof t.obj.profil === 'string' && gyldigeMetoder(data, t.obj.metoder)) {
      var m = {};
      data.kategorier.forEach(function (k) { m[k.id] = t.obj.metoder[k.id]; });
      return { profil: profilId(data, m), metoder: m, kilde: 'gemt', note: false };
    }
    return { profil: 'standard', metoder: standard(data), kilde: 'standard', note: t.status !== 'tom' };
  }

  /** Modspils standardtilstand med de valgte metoder. */
  function nyTilstand(data, metoder) {
    return { version: 1, settings: { dayStartsAtHour: 4 }, profil: profilId(data, metoder), metoder: kopi(metoder),
      level: 1, levelLog: [], items: {}, xp: 0, streak: { current: 0, best: 0, lastDay: '' }, sessions: [] };
  }

  /** Gemmer metoderne. Skriver kun profil og metoder; returnerer false, når intet blev skrevet. */
  function gemValg(storage, data, metoder) {
    if (!gyldigeMetoder(data, metoder)) return false;
    var t = laesTilstand(storage);
    var ud;
    if (t.status === 'tom') ud = nyTilstand(data, metoder);
    else if (t.status === 'gyldig' && typeof t.obj.profil === 'string' && gyldigeMetoder(data, t.obj.metoder)) {
      ud = t.obj;
      ud.profil = profilId(data, metoder);
      var m = kopi(t.obj.metoder);
      data.kategorier.forEach(function (k) { m[k.id] = metoder[k.id]; });
      ud.metoder = m;
    } else return false;
    try { storage.setItem(NOEGLE, JSON.stringify(ud)); return true; } catch (e) { return false; }
  }

  /** Metoderne for en profil. */
  function profilMetoder(data, id) { var p = profil(data, id); return p ? kopi(p.valg) : null; }

  /** Metoderne med én kategori skiftet. */
  function medMetode(metoder, kategori, id) { var m = kopi(metoder); m[kategori] = id; return m; }

  /** Kortets rækker (meldinger) delt i den valgte metodes gruppe og de andre: { valgt: [rækker], andre: [rækker] }.
      Grupperne hedder som metodernes navn (tekst) i metoder.json. */
  function delKort(meldinger, valgtNavn) {
    var valgt = [], andre = [], cur = null;
    (meldinger || []).forEach(function (r) {
      if (r.gruppe !== undefined && Object.keys(r).length === 1) cur = r.gruppe === valgtNavn ? valgt : andre;
      (cur || andre).push(r);
    });
    return { valgt: valgt, andre: andre };
  }

  /** Den valgte metode for kortet ms-<kategori>: { kategori, metode } eller null. */
  function valgtFor(data, kortId, metoder) {
    var kat = data.kategorier.find(function (k) { return 'ms-' + k.id === kortId; });
    if (!kat) return null;
    return { kategori: kat, metode: kat.metoder.find(function (x) { return x.id === metoder[kat.id]; }) };
  }

  /** Quizzens spørgsmål: de valgte metoders, eller alle ved alle = true; kun kortets kategori, når kategori er givet. */
  function spoergsmaal(quiz, metoder, alle, kategori) {
    return quiz.spoergsmaal.filter(function (s) {
      return (!kategori || s.kategori === kategori) && (alle || metoder[s.kategori] === s.metode);
    });
  }

  var API = { NOEGLE: NOEGLE, profilId: profilId, gyldigeMetoder: gyldigeMetoder, laesValg: laesValg, gemValg: gemValg,
    profilMetoder: profilMetoder, medMetode: medMetode, delKort: delKort, valgtFor: valgtFor, spoergsmaal: spoergsmaal };
  root.Modspilsaftaler = API;
  if (typeof module === 'object' && module.exports) module.exports = API;
})(typeof globalThis !== 'undefined' ? globalThis : this);
