# SPEC-crowhurst-390

6. november 2026 · Franks valg. Bygges på grenen `crowhurst-390`; `main` før er tagget `v-foer-crowhurst-390`. Frank godkender, før der flettes.

**Problemet:** crowhurst-kortet på `viden/konventionskort.html` giver vandret scroll ved 390–398 px i fuld visning: 9 px ved 390 px, 4 px ved 395 px og intet fra 399 px. Det står som forbehold i `../SYSTEM.md` (afsnit 8) og som åbent punkt i `docs/specs/SPEC-viden-320.md`. Årsagen er chippen "Crowhurst (checkback efter åbners 1NT-genmelding)" blandt kortets relaterede konventioner. Chips har `white-space:nowrap` og må kun brække under 390 px (`@media (max-width:389px)` fra viden-320). Chippen er 343 px bred, så kortets kolonne bliver bredere end siden.

**Ændringen:** chips må også brække ved 390–398 px. `.chip{white-space:normal}` flyttes fra reglen med `max-width:389px` til en ny regel med `max-width:398px` i `tools/konventionskort.src.html`, og siden og hint-komponenten bygges igen med `python3 tools/build_konventionskort.py`. En chip, der kan stå på én linje, er uændret; kun en chip, der er bredere end kortet, brækker. Under 390 px er reglerne de samme som før.

## Afgrænsning

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `tools/konventionskort.src.html` | `.chip{white-space:normal}` i en `@media (max-width:398px)` | andre regler ændres |
| `viden/konventionskort.html`, `assets/konventionskort-hint.js` | bygget igen fra kilden | rettet direkte |
| Crowhurst-kortet ved 390–398 px | chippen brækker, så kortet ikke stikker ud | |
| De andre 48 kort og siderne ved 390 px, alt ved 399 og 1280 px | intet | en pixel ændres |
| Kortenes indhold i `data/kort/` | intet | |

## Accepttest

`node tools/tjek_crowhurst_390.mjs` (ny) tjekker:

- [ ] **Ingen vandret scroll** på crowhurst-kortet ved 390, 393, 395 og 398 px på dansk og engelsk, i fuld og kompakt visning og skabelonen, med alt foldet ud, og i hint-vinduet i `traener.html?k=crowhurst`.
- [ ] **Ved 390 px** er de andre 48 kort i fuld og kompakt visning, crowhurst i kompakt visning og alle sider i `viden/` på begge sprog pixel for pixel som `v-foer-crowhurst-390`.
- [ ] **Ved 399 og 1280 px** er alle sider i `viden/` på begge sprog og alle 49 kort i fuld og kompakt visning pixel for pixel som tagget.
- [ ] **Billederne:** `--billeder=mappe` gemmer crowhurst-kortet i fuld visning ved 390 px før og efter på dansk og engelsk, med en rød streg, hvor skærmen slutter, når kortet stikker ud (`../skaermbilleder/crowhurst-390/`).

Desuden er `node tools/tjek_viden_320.mjs` og repoets øvrige tjek grønne.

## Afklaret

Udfyldes, når ændringen er bygget.
