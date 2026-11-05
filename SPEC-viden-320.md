# SPEC-viden-320

5. november 2026 · Franks valg. Bygget på grenen `viden-320`; `main` før er tagget `v-foer-viden-320`. Frank godkender, før der flettes.

Siderne i `viden/` må ikke give vandret scroll ved 320 px. Punktet stod under Kendte forbehold i `../SYSTEM.md` for `viden/2-over-1.html`, hvor opgaverne stak 20 px ud. Målingen viste, at også andre sider i `viden/` stikker ud.

## Afgrænsning

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| Siderne i `viden/` under 360 px | layoutet tilpasses, så intet stikker ud, og intet skjules | indholdet ændres |
| Ved 390 og 1280 px | intet | noget flytter sig; siderne er pixel for pixel som før |
| `overflow` på `html` og `body` | intet | vandret scroll fjernes ved at skjule det, der stikker ud |

## Accepttest

- [ ] `node tools/tjek_viden_320.mjs`: ingen vandret scroll ved 320, 340, 360 og 375 px på alle sider i `viden/`, på dansk og engelsk, med `<details>` lukket og åbne.
- [ ] Samme tjek ved 320 og 375 px på alle konventionskort i deres visninger; kortene står i en shadow root, og målingen går også derind.
- [ ] Hverken `html` eller `body` skjuler noget med `overflow`.
- [ ] Ved 390 og 1280 px er alle sider og kort pixel for pixel som `v-foer-viden-320`.
- [ ] `tools/tjek_sidefod.mjs` måler igen hele siden ved 320 px på alle sine sider, også `viden/2-over-1.html`.
- [ ] Sprog, fagord, beskrivende form og skrifttyper er grønne.

Giv Frank udsnit ved 320 px før og efter. Frank godkender, før der flettes.

## Afklaret

Udfyldes, når årsagerne er rettet.
