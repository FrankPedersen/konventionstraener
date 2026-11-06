# SPEC-crowhurst-390

6. november 2026 · Franks valg. Bygges på grenen `crowhurst-390`; `main` før er tagget `v-foer-crowhurst-390`. Godkendt af Frank, flettet og udgivet 6. november 2026 (`e8d4fc2`); den udgivne side er tjekket, og grenen er slettet.

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

- [x] **Ingen vandret scroll** på crowhurst-kortet ved 390, 393, 395 og 398 px på dansk og engelsk, i fuld og kompakt visning og skabelonen, med alt foldet ud, og i hint-vinduet i `traener.html?k=crowhurst`.
- [x] **Ved 390 px** er de andre 48 kort i fuld og kompakt visning, crowhurst i kompakt visning og alle sider i `viden/` på begge sprog pixel for pixel som `v-foer-crowhurst-390`.
- [x] **Ved 399 og 1280 px** er alle sider i `viden/` på begge sprog og alle 49 kort i fuld og kompakt visning pixel for pixel som tagget.
- [x] **Billederne:** `--billeder=mappe` gemmer crowhurst-kortet i fuld visning ved 390 px før og efter på dansk og engelsk, med en rød streg, hvor skærmen slutter, når kortet stikker ud (`../skaermbilleder/crowhurst-390/`).

Desuden er `node tools/tjek_viden_320.mjs` og repoets øvrige tjek grønne.

## Afklaret

Kørt 6. nov. 2026 på grenen: `tjek_crowhurst_390.mjs` 418 tjek i orden (15 minutter; fem forsøg med støj, se Afklaret 6), `tjek_viden_320.mjs` 791 tjek i orden (ét færre end før, se Afklaret 5), `tjek_sidefod.mjs`, `tjek_skrifttyper.mjs`, `tjek_bred_multi.mjs` og de ni Python-tjek (konventionskort, kort_eksempler, fagord, bydeform, sprog, skrifttyper, makker2_aftaler, makker2_bilag_c, crowhurst) i orden.

1. **Årsagen er bekræftet** (målt på tagget med den nye test): fuld visning stak 9, 6, 4 og 1 px ud ved 390, 393, 395 og 398 px på begge sprog; kompakt visning, skabelonen og hint-vinduet var i orden (8 fejl ud af 80 tjek før rettelsen, 0 efter).
2. **Chippen brækker ved bindestregen:** "Crowhurst (checkback efter åbners 1NT-" / "genmelding)". Hele kortet bliver 564 px længere ved 390 px (13.369 mod 12.805 px), fordi kortets kolonne før var 25 px bredere end siden (383 mod 358 px), så tekst og tabeller brækkede mindre. Nu passer kolonnen til siden.
3. **Reglen er flyttet, ikke kopieret:** `.chip{white-space:normal}` står i `@media (max-width:398px)`, og `.fod{overflow-wrap:anywhere}` bliver i reglen med `max-width:389px`. Under 390 px er reglerne de samme som før.
4. **Intet andet ændrer sig:** ved 390 px er de andre 48 kort, crowhurst i kompakt visning og alle sider pixel for pixel som tagget, så alle andre chips kan stå på én linje. Ved 399 og 1280 px er alt som tagget.
5. **`tjek_viden_320.mjs`** sammenligner 390 px med `v-foer-viden-320`. Crowhurst i fuld visning er nu bevidst anderledes og står på testens liste `ÆNDRET`, så resten tjekkes som før; `tjek_crowhurst_390.mjs` tjekker crowhurst.
6. **Støj:** fem sammenligninger havde 1–2 pixels ét farvetrin forskellige i første forsøg og var ens i andet (som Afklaret 9 i `docs/specs/SPEC-viden-320.md`). Testen bruger samme kode som `tjek_viden_320.mjs`: hver side i sin egen browserkontekst, og en forskel skal være der i tre forsøg i træk.
7. **Billederne** (`../skaermbilleder/crowhurst-390/`): `390-<sprog>-crowhurst-fuld-<foer|efter>.png` er hele kortet med en rød streg ved 390 px, når det stikker ud, og `390-<sprog>-crowhurst-chip-<foer|efter>.png` udsnittet omkring chippen.
8. **Den udgivne side** (6. nov. 2026, efter GitHub Pages-udrulningen af `e8d4fc2`): `viden/konventionskort.html` og `assets/konventionskort-hint.js` på www.kontraktbridge.dk har reglen med `max-width:398px`, og testens tjek af vandret scroll (crowhurst i alle visninger og hint-vinduet ved 390, 393, 395 og 398 px på begge sprog) giver 80 tjek i orden mod sitet. Testen har ingen `--live`, så den blev kørt fra en kopi uden for repoet, hvor siden nu er www.kontraktbridge.dk/konventionstraener/.
