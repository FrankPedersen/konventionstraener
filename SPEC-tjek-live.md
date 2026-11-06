# SPEC-tjek-live

6. november 2026 · Franks opgave. Bygges på grenen `tjek-live`; `main` før er tagget `v-foer-tjek-live`. Frank godkender, før der flettes.

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

- [ ] Uden `--live` giver testene samme antal tjek som i dag, alle i orden: `tjek_viden_320.mjs` 791 og `tjek_crowhurst_390.mjs` 418 (og `tjek_sidefod.mjs` som i dag).
- [ ] Med `--live` er alle tjek af vandret scroll i orden mod sitet; antallet og antallet af sprungne pixeltjek står under Afklaret.
- [ ] Kun `tools/` og dokumentationen er ændret; `git diff v-foer-tjek-live` rører ingen side.
- [ ] Repoets øvrige tjek er grønne.

## Afklaret

Udfyldes, når ændringen er bygget.
