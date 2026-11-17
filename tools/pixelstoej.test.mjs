// Enhedstest af tools/pixelstoej.mjs (SPEC-pixeltolerance.md, Franks valg (b) 15. november 2026): en pixel tæller kun,
// når den afviger mere end TRIN farvetrin i mindst én kanal, og højst LOFT tællende pixels pr. skærmbillede er støj.
//
//   node --test tools/pixelstoej.test.mjs
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';

import { LOFT, TRIN, afgør, erStøj, tæller } from './pixelstoej.mjs';

/** En pixel med en forskel på `trin` i én kanal: [før, nu] som [r, g, b]. */
const pixel = (trin) => [[200, 100, 50], [200 + trin, 100, 50]];

test('grænserne er 5 trin og 5 pixels', () => {
  assert.equal(TRIN, 5);
  assert.equal(LOFT, 5);
});

test('en pixel tæller kun, når den afviger mere end 5 trin i mindst én kanal', () => {
  for (let t = 0; t <= 5; t++) assert.equal(tæller(...pixel(t)), false, `${t} trin`);
  for (const t of [6, 28, 57, 229]) assert.equal(tæller(...pixel(t)), true, `${t} trin`);
  assert.equal(tæller([10, 10, 10], [15, 4, 15]), true, 'grøn afviger 6 trin');
  assert.equal(tæller([10, 10, 10], [15, 15, 5]), false, 'højst 5 trin i alle kanaler');
});

test('0–5 tællende pixels er støj', () => {
  for (let n = 0; n <= 5; n++) assert.equal(erStøj(n), true, `${n} pixels`);
});

test('6 tællende pixels og derover er ikke støj, heller ikke en forskel i højden', () => {
  for (const n of [6, 7, 50, 42590]) assert.equal(erStøj(n), false, `${n} pixels`);
  assert.equal(erStøj(Infinity), false, 'højden er forskellig');
});

test('25 pixels med 1–5 trin er støj', () => {
  const forskelle = Array.from({ length: 25 }, (_, i) => pixel(1 + (i % 5)));
  assert.deepEqual(afgør(forskelle), { pixels: 0, støj: true });
});

test('6 pixels med 6 trin eller mere er ikke støj', () => {
  const forskelle = [6, 7, 28, 57, 200, 229].map(pixel);
  assert.deepEqual(afgør(forskelle), { pixels: 6, støj: false });
  // 5 af dem er støj, også sammen med mange svage forskelle.
  assert.deepEqual(afgør([...forskelle.slice(0, 5), ...Array.from({ length: 25 }, () => pixel(1))]), { pixels: 5, støj: true });
});

test('loftet og trinnet læses kun fra modulet', () => {
  for (const script of ['tjek_viden_320.mjs', 'tjek_crowhurst_390.mjs']) {
    const kilde = readFileSync(new URL(`./${script}`, import.meta.url), 'utf-8');
    assert.match(kilde, /import \{[^}]*\berStøj\b[^}]*\} from '\.\/pixelstoej\.mjs';/, `${script} importerer erStøj fra modulet`);
    assert.match(kilde, /import \{[^}]*\bTRIN\b[^}]*\} from '\.\/pixelstoej\.mjs';/, `${script} importerer TRIN fra modulet`);
    assert.doesNotMatch(kilde, /\b(LOFT|TRIN)\s*=/, `${script} definerer ikke sit eget loft eller trin`);
    assert.doesNotMatch(kilde, /pixels?\s*(<=|<|>=|>)\s*\d/, `${script} sammenligner ikke antal pixels med et tal`);
    assert.doesNotMatch(kilde, /(trin|\bt|Math\.max\([^)]*\))\s*(<=|<|>=|>)\s*\d/, `${script} sammenligner ikke farvetrin med et tal`);
  }
});
