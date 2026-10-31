# SPEC-bred-layout (konventionstræneren)

31. oktober 2026 · Franks valg, skrevet ud af Claude Code

Fordelingstræneren får et bredt layout fra 1000 px efter **bud A · Bordet til venstre, opgaven til højre** (Franks valg 31. oktober 2026; `SPEC-bred-layout.md` i Fordelingstræneren). Afsnittet Konventionstræneren i den spec gælder her: `multi-svar-traener.html` står i dag i højst 620 px. Fra 1000 px bruger den samme regel som Fordelingstræneren: højst 1120 px; hånden i en venstre spalte på 420 px, der står fast; meldingerne, svarknapperne og forklaringen i højre spalte. Under 1000 px er den uændret. De andre sider står allerede i 64rem og ændres ikke.

## Afgrænsning

`main` er tagget `v-foer-bred-layout`, og arbejdet sker på grenen `bred-layout`. Der flettes først efter Franks godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `multi-svar-traener.html` | brede regler i `@media (min-width: 1000px)` i sidens egen `<style>` | ændre noget under 1000 px; ændre HTML, tekst, logik eller rækkefølgen for skærmlæser og tastatur; nye farver |
| `tools/tjek_bred_multi.mjs` | ny accepttest i en rigtig browser | |
| De andre sider | | ændres ikke |

## Fra 1000 px

1. **Bredden:** siden er højst 1120 px bred i midten med 32 px sidemargen, som Fordelingstræneren.
2. **Over begge spalter:** navnet, overskriften, teksten under den og fremdriften.
3. **Venstre spalte (420 px):** hånden. Den står fast (`position: sticky; top: 16px`), så den kan ses, mens man scroller i højre spalte.
4. **Højre spalte (mindst 400 px):** meldingerne, bonusspørgsmålet, "Hvad melder du?" med pæren, meldekassen, forklaringen og Næste hånd. Slutresultatet står over begge spalter.
5. **HTML** er uændret: rækken med hånden og bonusspørgsmålet (`.toprow`) er usynlig fra 1000 px (`display: contents`), og hånden placeres i venstre spalte med grid.

## Accepttest

`node tools/tjek_bred_multi.mjs` (Chrome uden vindue; siden før vises fra tagget med `git show`):

- [ ] Ved 1280 px står hånden til venstre og meldingerne til højre for den, og toppene flugter; hånden er 420 px.
- [ ] Ved 1280 px står meldekassen og forklaringen i højre spalte, og indholdet er højst 1120 px bredt i midten.
- [ ] Ved 1280 px står hånden fast, når der rulles.
- [ ] Ved 1000 px er højre spalte mindst 400 px bred.
- [ ] Ved 999 og 390 px er siden pixel for pixel som før, både ved første hånd og efter et svar.
- [ ] `tjek_fagord.py`, `tjek_sprog.py`, `tjek_bydeform.py`, `tjek_konventionskort.py`, `tjek_skrifttyper.py` og `tjek_skrifttyper.mjs` består.

## Afklaret

1. **Valget** er Franks, 31. oktober 2026 (bud A i mockuppen "Træning på computer").
2. **Meldingerne** (modstanderens åbning og makkers indmelding) står i højre spalte over bonusspørgsmålet, som specen siger; hånden står alene til venstre.
3. **Hånden** fylder venstre spalte (den var højst 260 px bred ved siden af bonusspørgsmålet); skrift og farver er uændrede.
