# SPEC-tjek-live

6. november 2026 · Franks opgave. Bygges på grenen `tjek-live`; `main` før er tagget `v-foer-tjek-live`. Godkendt af Frank, flettet og udgivet 6. november 2026 (`f85d61b`); de tre tjek er kørt med `--live` efter udrulningen, og grenen er slettet. Forslaget om tolerance i pixeltesten står som åbent punkt til en egen opgave.

`tools/tjek_viden_320.mjs` og `tools/tjek_crowhurst_390.mjs` får `--live`, som Forsidens `tools/tjek_om_mig.mjs` og `tools/tjek_kun_siden.mjs`, så de kan køre mod www.kontraktbridge.dk uden en kopi. Efter udgivelserne 5. og 6. november blev de kørt fra en kopi uden for repoet, hvor siden nu var sitet (`docs/specs/SPEC-viden-320.md`, Afklaret 10; `docs/specs/SPEC-crowhurst-390.md`, Afklaret 8).

## Ændringen

- **`--live`:** siderne og kortene åbnes på https://www.kontraktbridge.dk/konventionstraener/. Uden `--live` er alt som i dag.
- **Tjekkene af vandret scroll** (og hint-vinduet i træneren) kører live.
- **Pixelsammenligningen med tagget** giver kun mening lokalt. Med `--live` springes den over, og testen skriver tydeligt, at den er sprunget over, og hvor mange tjek det er.
- **`tools/tjek_sidefod.mjs`** får samme `--live`, hvis det kan gøres uden ekstra arbejde; ellers står det under Afklaret.
- **Brugen** står øverst i hver fil, og `CLAUDE.md` nævner `--live` efter en udgivelse.

## Afgrænsning

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `tools/tjek_viden_320.mjs`, `tools/tjek_crowhurst_390.mjs`, `tools/tjek_sidefod.mjs` | `--live` og brugen øverst | tjekkene ændres ellers |
| `CLAUDE.md`, `../SYSTEM.md`, specen | `--live` nævnes | |
| Siderne, kortene, `assets/`, `data/` og alt andet, der udgives | intet | |

## Accepttest

- [x] Uden `--live` giver testene samme antal tjek som i dag, alle i orden: `tjek_viden_320.mjs` 791 og `tjek_crowhurst_390.mjs` 418 (og `tjek_sidefod.mjs` som i dag).
- [x] Med `--live` er alle tjek af vandret scroll i orden mod sitet; antallet og antallet af sprungne pixeltjek står under Afklaret.
- [x] Kun `tools/` og dokumentationen er ændret; `git diff v-foer-tjek-live` rører ingen side.
- [x] Repoets øvrige tjek er grønne.

## Åbent punkt

1. **Støj i pixelsammenligningen** (Franks valg 6. nov. 2026: løsnes ikke på denne gren; står åbent til en egen opgave, der først måler den største forskel i hver sammenligning, også i `../SYSTEM.md` afsnit 8). Chrome tegner en sjælden gang få pixels ét farvetrin anderledes, også på sider, der er byte for byte ens, og det sker nu tit nok til, at en forskel kan komme igen i tre forsøg i træk (Afklaret 4–6). Forslag: en forskel på højst 5 pixels med højst 2 trin pr. farvekanal tæller som ens. I de 12 fejl, der er set (Afklaret 4 og 5), var forskellen 1–5 pixels, og den første forskellige pixel var 1 trin forskellig, undtagen én: et ♥ på `2-over-1-makker2` ved 390 px på engelsk var 5 trin forskellig (103.128.106 mod 103.133.109). Den ville stadig fejle med 2 trin. Testene skriver kun den første forskellige pixel, så den egne opgave bør først måle den største forskel pr. farvekanal i hver sammenligning og derefter sætte grænsen; et alternativ er flere forsøg end tre.

## Afklaret

Kørt 6. nov. 2026 på grenen: uden `--live` `tjek_viden_320.mjs` 791 tjek og `tjek_crowhurst_390.mjs` 418 tjek i orden (Chrome 157, Afklaret 5) og `tjek_sidefod.mjs` 104 tjek i orden; med `--live` alle tjek i orden mod sitet (Afklaret 1); de ni Python-tjek (konventionskort, kort_eksempler, fagord, bydeform, sprog, skrifttyper, makker2_aftaler, makker2_bilag_c, crowhurst), `tjek_skrifttyper.mjs` og `tjek_bred_multi.mjs` i orden.

1. **Med `--live`** mod https://www.kontraktbridge.dk/konventionstraener/: `tjek_viden_320.mjs` 568 tjek af vandret scroll i orden og 223 pixeltjek sprunget over (568 + 223 = 791); `tjek_crowhurst_390.mjs` 83 tjek i orden (crowhurst i alle visninger og hint-vinduet ved 390–398 px, siderne og kortlisten) og 335 pixeltjek sprunget over (83 + 335 = 418). Testene skriver "SPRUNGET OVER med --live: …" med antallet og slutter med "Alt i orden: N tjek på https://www.kontraktbridge.dk/konventionstraener/; M pixeltjek sprunget over".
2. **`tjek_sidefod.mjs`** fik `--live` uden ekstra arbejde: den åbner siderne fra én adresse og læser `href` som attributter, så kun adressen skifter. Fra sitet venter den også på `document.readyState`, for en side kan være længere end de 900 ms om at komme. 104 tjek i orden både lokalt og med `--live`.
3. **Uden `--live`** er alt som før: siden nu kommer fra arbejdsmappen, og pixelsammenligningen kører. Siden før kommer altid fra tagget, også med `--live` (kortlisten, som de sprungne pixeltjek tælles efter).
4. **Støj i de første lokale kørsler** (Chrome 156.0.8078.80, 13:30–14:16): antallet af tjek var rigtigt (791 og 418), men 10 pixelsammenligninger var forskellige i tre forsøg i træk: `2-over-1-makker2`, `2-over-1`, `bridgesystem` og `kampen-om-kontrakten` ved 390, 399 eller 1280 px, 1–5 pixels hver, den første forskellige pixel 1 trin forskellig (et ♥ 5 trin). Siderne er byte for byte ens med begge tags (`git diff --quiet`), og grenen ændrer kun `tools/` og `CLAUDE.md`. Om morgenen gav de samme test 0 fejl.
5. **Samme sammenligninger på `main` uden ændringen** (Franks krav; en `git worktree` fra `v-foer-tjek-live`, Chrome 157.0.8103.39): `tjek_viden_320.mjs` 1 fejl ud af 791 (`2-over-1-makker2` ved 1280 px på engelsk, 1 pixel) og `tjek_crowhurst_390.mjs` 1 fejl ud af 418 (`2-over-1` ved 390 px på dansk, 3 pixels). Støjen kommer altså ikke fra grenen. Lige bagefter, med samme Chrome, gav grenen 791 og 418 tjek i orden (5 og 11 forsøg med støj, der var væk i næste forsøg).
6. **Chrome-versionen** (Franks krav): nu 157.0.8103.39 (`/json/version` fra en Chrome uden vindue, som testene starter). Mappen `157.0.8103.39` under `C:\Program Files\Google\Chrome\Application` blev oprettet 6. nov. 2026 kl. 14:20:16; før det var versionen 156.0.8078.80 (mappen fra 3. nov. 2026, `chrome.exe` fra 29. okt. 2026). Morgenens kørsler uden fejl (12:34–13:05) og de første kørsler med fejl (13:30–14:16) brugte altså begge 156; Chrome blev opdateret bagefter, og støjen findes i begge versioner.
7. **Pixeltesten er ikke løsnet** på denne gren (Franks valg); se Åbent punkt 1.
8. **Efter udrulningen** (6. nov. 2026, GitHub Pages-udrulningen af `f85d61b`): fra `main` giver `node tools/tjek_sidefod.mjs --live` 104 tjek i orden, `node tools/tjek_viden_320.mjs --live` 568 tjek i orden (223 pixeltjek sprunget over) og `node tools/tjek_crowhurst_390.mjs --live` 83 tjek i orden (335 sprunget over) mod www.kontraktbridge.dk/konventionstraener/.
