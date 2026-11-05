# SPEC-sidefod

4. november 2026 · Franks valg. Bygget på grenen `sidefod`; `main` før er tagget `v-foer-sidefod`. Godkendt af Frank og udgivet 5. november 2026, efter `ny-forside`.

Sidefoden laves ens med forsidens nye, kompakte sidefod efter målene under Afklaret i `../Forside/docs/specs/SPEC-ny-forside.md`.

## Afgrænsning

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `assets/footer.js` | ny tekst og stil efter målene | ændre sidernes eget indhold |
| Topbjælken og siderne | intet | |

## Indhold

- Logo og "Om mig og kontakt".
- Kolonnen Trænere: Konventionstræner, Fordeling, Pointregnskab, Farvebehandling, Håndevaluering.
- Kolonnen Opslag: Analyse, Bridgeordbog, Scoring i bridge.
- ©-linjen.
- På mobil står logo og knappen på én række. Engelsk følger med.

## Accepttest

- [x] `node tools/tjek_sidefod.mjs`: målene, kolonnerne og rækkefølgen ved 1280 og 390 px på forsiden, en træner, multi-svar-træneren, Viden, makkeraftalerne og et systemdokument; intet stikker ud ved 320 px; engelsk.
- [x] `python tools/tjek_sprog.py`, `python tools/tjek_fagord.py` og `python tools/tjek_bydeform.py` består.

Giv Frank skærmbilleder ved 1280 og 390 px af sidefoden. Frank godkender, før der flettes.

## Afklaret

1. **Kolonnen "Aftaler og notater" udgår,** fordi sidefoden skal være ens med forsidens, og Frank har nævnt præcis to kolonner. Siderne kan stadig nås: Mine makkeraftaler står i topbjælken på alle sider, og Viden har Kampen om kontrakten, Forslag og notaterne.
2. **Stilen står kun i `assets/footer.js`** som før, med `#sidefod` foran, så systemdokumenternes egne regler for h2, p, ul, li og a ikke slår igennem. Grænsen er 1000 px som på forsiden.
3. **Linkene** til Fordelingstræneren går direkte til sporet (`/fordelingstraeneren/#fordeling` osv.) som på forsiden. Konventionstræner er en relativ adresse, så den også virker i en lokal kopi.
4. **Bredden:** sidefoden står stadig i sidens kolonne på højst 64rem; målene inde i den er forsidens.
5. **Knappens tekst må brække,** som på forsiden (Franks valg 5. november 2026): ved 360 px står "Om mig og kontakt" på to linjer og ved 320 px på tre, og på engelsk er den på to linjer allerede ved 390 px. `tools/tjek_sidefod.mjs` tjekker, at knappen står inden for polstringen ved 390, 360 og 320 px på begge sprog.
