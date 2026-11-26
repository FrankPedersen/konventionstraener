// Accepttest, punkt 6 og 7 (SPEC-modspilsaftaler.md): indstillingen fælles med Modspil og udvælgelsen af quizspørgsmål.
// Kør fra repoets rod:  node --test tools/modspilsaftaler.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const M = require('../assets/modspilsaftaler.js');
const data = JSON.parse(readFileSync(new URL('../data/modspilsaftaler.json', import.meta.url), 'utf8'));
const quiz = JSON.parse(readFileSync(new URL('../data/modspilsaftaler-quiz.json', import.meta.url), 'utf8'));
const KEY = 'modspil:v1';

function lager(start) {
  const m = new Map(start === undefined ? [] : [[KEY, start]]);
  return { getItem: (k) => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)), m };
}

const kompendiet = () => ({ ...data.profiler.find((p) => p.id === 'kompendiet').valg });

// En tilstand, som Modspil selv gemmer den: niveau, Leitner-poster, svarlog, øvelse 8's post og eksportdatoen.
const MODSPIL = JSON.stringify({
  version: 1, settings: { dayStartsAtHour: 4 }, profil: 'standard',
  metoder: { ...data.profiler[0].valg }, level: 3, levelLog: [1, 1, 0, 1],
  items: { 'ovelse:regel11': { box: 3, due: '2026-11-28', seen: 7 }, 'ovelse:kald': { box: 1, due: '2026-11-26', seen: 2 } },
  xp: 1234.5, streak: { current: 4, best: 9, lastDay: '2026-11-25', jokerWeek: '2026-W47' },
  sessions: [{ day: '2026-11-25', ms: 312000, correct: 9, total: 10, xp: 120, level: 3 }],
  answers: [{ day: '2026-11-25', ovelse: 'regel11', level: 3, score: 1, ms: 8123 }],
  lastExport: '2026-11-20', findUdspil: { box: 2, due: '2026-11-27', seen: 5 },
});

const udenValg = (s) => { const o = JSON.parse(s); delete o.profil; delete o.metoder; return JSON.stringify(o); };

test('uden gemt tilstand vises Standard', () => {
  const v = M.laesValg(lager(), data);
  assert.equal(v.profil, 'standard');
  assert.deepEqual(v.metoder, data.profiler.find((p) => p.id === 'standard').valg);
  assert.equal(v.note, false);
});

test('et valg uden gemt tilstand skriver Modspils standardtilstand med valget', () => {
  const l = lager();
  assert.equal(M.gemValg(l, data, kompendiet()), true);
  const o = JSON.parse(l.m.get(KEY));
  assert.equal(o.version, 1);
  assert.equal(o.profil, 'kompendiet');
  assert.deepEqual(o.metoder, kompendiet());
  assert.equal(o.level, 1);
  assert.deepEqual(o.items, {});
});

test('et valg skriver kun profil og metoder og bevarer resten tegn for tegn', () => {
  const l = lager(MODSPIL);
  const m = M.medMetode(M.profilMetoder(data, 'standard'), 'kald', 'romersk-kald');
  assert.equal(M.gemValg(l, data, m), true);
  const ny = l.m.get(KEY);
  const o = JSON.parse(ny);
  assert.equal(o.profil, 'egen');
  assert.equal(o.metoder.kald, 'romersk-kald');
  assert.equal(udenValg(ny), udenValg(MODSPIL));
  assert.deepEqual(Object.keys(o), Object.keys(JSON.parse(MODSPIL)));
  assert.equal(M.laesValg(l, data).profil, 'egen');
});

test('ugyldige data overskrives ikke og vises som Standard med en note', () => {
  for (const tekst of ['{ikke json', '[1,2]', '"tekst"', JSON.stringify({ ...JSON.parse(MODSPIL), metoder: { kald: 'findes-ikke' } }),
    JSON.stringify({ ...JSON.parse(MODSPIL), profil: undefined })]) {
    const l = lager(tekst);
    const v = M.laesValg(l, data);
    assert.equal(v.profil, 'standard');
    assert.equal(v.note, true);
    assert.equal(M.gemValg(l, data, kompendiet()), false);
    assert.equal(l.m.get(KEY), tekst);
  }
});

test('en ugyldig metode skrives ikke', () => {
  const l = lager(MODSPIL);
  assert.equal(M.gemValg(l, data, { ...kompendiet(), kald: 'noget-andet' }), false);
  assert.equal(l.m.get(KEY), MODSPIL);
});

test('profilen regnes af metoderne', () => {
  for (const p of data.profiler) assert.equal(M.profilId(data, p.valg), p.id);
  assert.equal(M.profilId(data, M.medMetode(kompendiet(), 'laengde', 'hoejt-lavt-lige')), 'egen');
});

test('kortet viser den valgte metode øverst som Din aftale', () => {
  const kort = JSON.parse(readFileSync(new URL('../data/kort/ms-kald.json', import.meta.url), 'utf8'));
  const v = M.valgtFor(data, 'ms-kald', kompendiet());
  assert.equal(v.metode.id, 'romersk-kald');
  const d = M.delKort(kort.meldinger, v.metode.tekst);
  assert.deepEqual(d.valgt[0], { gruppe: 'romersk kald' });
  assert.ok(d.andre.some((r) => r.gruppe === 'højt = kald') && d.andre.some((r) => r.gruppe === 'lavt = kald'));
  assert.ok(!d.andre.some((r) => r.gruppe === 'romersk kald'));
  assert.equal(d.valgt.length + d.andre.length, kort.meldinger.length);
  const s = readFileSync(new URL('../tools/konventionskort.src.html', import.meta.url), 'utf8');
  assert.match(s, /Din aftale/);
  assert.match(s, /Andre varianter/);
});

test('quizzen tager kun de valgte metoders spørgsmål, og alle 34 ved Alle varianter', () => {
  assert.equal(quiz.spoergsmaal.length, 34);
  const valgte = M.spoergsmaal(quiz, kompendiet(), false);
  assert.equal(valgte.length, 14);
  assert.ok(valgte.every((s) => kompendiet()[s.kategori] === s.metode));
  assert.equal(M.spoergsmaal(quiz, kompendiet(), true).length, 34);
  assert.equal(M.spoergsmaal(quiz, kompendiet(), false, 'kald').length, 2);
  assert.equal(M.spoergsmaal(quiz, kompendiet(), true, 'kald').length, 6);
});
