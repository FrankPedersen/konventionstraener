# SPEC-skrifttyper-fast

28. oktober 2026 · Frank

`tools/tjek_skrifttyper.mjs` var accepttesten for skrifttyperne på sitet selv: den sammenlignede siderne med udgaven i tagget `v-foer-skrifttyper` (med Google Fonts), både skrifttype for skrifttype og pixel for pixel. Den er bestået. Siden er der flettet godkendte ændringer ind (fx linket Scoring i bridge i sidefoden og nyt indhold i Makker 2 og Truscott), så pixelsammenligningen fejler nu, uden at noget er galt. Testen bliver en fast test af skrifttyperne.

## Afgrænsning

Arbejd på grenen `skrifttyper-fast`; `main` er tagget `v-foer-skrifttyper-fast`. Claude Code stopper før fletning.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `tools/tjek_skrifttyper.mjs` | fjerne pixelsammenligningen og udgaven fra tagget; beholde skrifttypedelen | tjekke færre sider |
| `tools/tjek_skrifttyper.py` | rette henvisningen til `.mjs` i beskrivelsen | ændre testen |
| `CLAUDE.md` | intet: testen er ikke nævnt der | |
| siderne, `assets/`, data | intet | alt |

## Testen fremover

På de samme sider ved 390 og 1280 px: intet hentes fra Google, skrifttyperne hentes fra `assets/fonts/`, og Chrome tegner overskriften og Manrope-elementet med Manrope, brødteksten med Inter og spillefarverne ♠♥♦♣ med Noto Sans Symbols 2, hvor siden beder om den, alle fra sitet og ikke fra systemet. Spillefarver i sidens almindelige skrift (fx i Multi-træneren og Makker 2, der ikke henter symbolskriften) tegnes med systemets tegn, som før skrifttyperne kom på sitet, og tjekkes ikke; det gælder 4 af de 12 sider.

## Accepttest

- [x] `node tools/tjek_skrifttyper.mjs` er grøn to gange i træk; trænerne trækker tilfældige hænder, så det viser, at testen ikke afhænger af hænderne.
- [x] Testen bruger hverken git, tagget `v-foer-skrifttyper` eller skærmbilleder.
- [x] `python3 tools/tjek_skrifttyper.py`, `python3 tools/tjek_konventionskort.py` og repoets øvrige tjek er grønne.

## Afklaret

1. **Kun skrifttypedelen** (Franks opgave 28. oktober 2026): pixelsammenligningen med `v-foer-skrifttyper` var accepttesten for skrifttypeændringen og er bestået.
2. **Uden tagget:** skrifttypedelen sammenlignede også med de skrifttyper, udgaven i tagget tegnede med. Det kræver tagget, og på markering.html fejlede den tilfældigt, når den ene udgaves hånd havde en spillefarve i første afsnit og den andens ikke. Den faste test tjekker i stedet, at hvert element tegnes med den skrifttype, det skal have, fra sitet.
3. **Spillefarverne** tjekkes på et element, der beder om Noto Sans Symbols 2. Det første element med en spillefarve kan stå i sidens almindelige skrift, og så tegner Chrome tegnet med Segoe UI fra systemet; sådan var det også med Google Fonts.
