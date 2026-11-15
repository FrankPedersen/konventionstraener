// Enhedstest af tools/pixelstoej.mjs (SPEC-pixeltolerance.md): loftet over støj i pixelsammenligningen.
//
//   node --test tools/pixelstoej.test.mjs
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';

import { LOFT, erStøj } from './pixelstoej.mjs';

test('loftet er 5 pixels', () => {
  assert.equal(LOFT, 5);
});

test('0–5 pixels er støj', () => {
  for (let n = 0; n <= 5; n++) assert.equal(erStøj(n), true, `${n} pixels`);
});

test('6 pixels og derover er ikke støj, heller ikke en forskel i højden', () => {
  for (const n of [6, 7, 50, 22212]) assert.equal(erStøj(n), false, `${n} pixels`);
  assert.equal(erStøj(Infinity), false, 'højden er forskellig');
});

test('loftet læses kun fra modulet', () => {
  for (const script of ['tjek_viden_320.mjs', 'tjek_crowhurst_390.mjs']) {
    const kilde = readFileSync(new URL(`./${script}`, import.meta.url), 'utf-8');
    assert.match(kilde, /import \{[^}]*\berStøj\b[^}]*\} from '\.\/pixelstoej\.mjs';/, `${script} importerer erStøj fra modulet`);
    assert.doesNotMatch(kilde, /\bLOFT\s*=/, `${script} definerer ikke sit eget loft`);
    assert.doesNotMatch(kilde, /pixels?\s*(<=|<|>=|>)\s*\d/, `${script} sammenligner ikke antal pixels med et tal`);
  }
});
