# SPEC-makker2-markeringer

15. november 2026 · Franks afgørelse 15. november 2026. Bygges på grenen `makker2-markeringer`; `main` før er tagget `v-foer-makker2-markeringer`. Stop før merge.

Makker 2-dokumentet (`viden/2-over-1-makker2.html`) har markeringerne forkert. Makker 2 spiller som Bridgesystem og Kompendium over modspilsaftaler: lavt kort = kald, højt kort = afvisning, og lavt kort = lige antal, højt kort = ulige (lavt-højt = lige, højt-lavt = ulige). Lavinthal er uændret.

## Ændringen

- **Afsnit 19, Attitude:** reglen bliver "Lavt kort = kald (»fortsæt«), højt kort = afvisning (»skift«)". I tabellen med eksemplet 8-3-2 er 2'eren nu kald og 8'eren afvisning; rækkernes farver (grøn for kald, rød for afvisning) følger betydningen. Noten om, at højt og lavt er relativt, får eksemplet vendt: en 6'er er en afvisning fra 6-4-3 og et kald fra 9-8-6.
- **Afsnit 19, Rangorden:** count-linjen bliver "lavt kort = lige antal (lavt-højt), højt kort = ulige antal (højt-lavt)".
- **Resten af dokumentet** er gennemsøgt for "højt kort", "lavt kort", "højt-lavt", "lavt-højt", "kald" og "afvisning"; retningen står kun i afsnit 19. Lavinthal (afsnit 20) er uændret.
- **Tre rettelser mere i dokumentet** (Franks tillæg samme dag):
  - **B2, svarskemaet til Multi:** 2♠ bliver "Pas eller ret den anden vej, med hjertertolerance: pas med spar, ret til 3♥ med hjerter."
  - **Bilag E2:** "vejer tungere end fire overstik (1 imp)" bliver "vejer tungere end et overstik (1 imp)".
  - **Afsnit 19, grundreglen:** "2. højeste fra en svag farve uden honnør (»top af intet«)" bliver "2. højeste fra en svag farve uden honnør; fra to kort spilles det højeste (»top af intet«)".
- **Mine makkeraftaler** (`makkeraftaler.html`), tabellen Forskelle mellem systemerne: rækken Markering byggede på den gamle retning (Makker 2: "Højt kort = kald"). Begge makkerskaber spiller nu lavt kort = kald, så rækken viser den forskel, der er tilbage: hvornår der markeres antal (Makker 1 efter konge-udspil og ved ny farve; Makker 2, når attitude er kendt, eller spilfører angriber farven), på dansk og engelsk.

## Afgrænsning

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `viden/2-over-1-makker2.html` | afsnit 19: Attitude (reglen, tabellen og noten), count-linjen i Rangorden og grundreglen for udspil; Multi-svaret 2♠ i B2; sætningen i Bilag E2 | andre afsnit, Lavinthal, layout og stil |
| `makkeraftaler.html` | rækken Markering i Forskelle mellem systemerne (dansk og engelsk) | andre rækker |
| `tools/tjek_makker2_markeringer.py` | ny accepttest | |
| `tools/ordliste.txt` | ordet hjertertolerance (fra B2), som hunspell ikke kender | andre ord |
| Konventionskortene, puljerne, `dealer/`, `markering.html`, Bridgesystem | intet: de følger Bridgesystem og bygger ikke på Makker 2's gamle retning | |

## Accepttest

`python3 tools/tjek_makker2_markeringer.py`:

- [x] Afsnit 19 siger lavt kort = kald og højt kort = afvisning; tabellen har "Lavt kort (fx 2 fra 8-3-2)" som kald og "Højt kort (fx 8 fra 8-3-2)" som afvisning; noten siger afvisning fra 6-4-3 og kald fra 9-8-6.
- [x] Count-linjen siger lavt kort = lige antal (lavt-højt) og højt kort = ulige antal (højt-lavt).
- [x] Ingen steder i dokumentet står "højt kort = kald", "lavt kort = afvisning", "højt-lavt = lige" eller "lavt-højt = ulige".
- [x] B2 har det nye Multi-svar 2♠, Bilag E2 siger "et overstik", og grundreglen siger, at det højeste spilles fra to kort.
- [x] Dokumentet er tagget med præcis de aftalte rettelser og intet andet; afsnit 20 (Lavinthal) og B4 er tegn for tegn som i tagget.
- [x] Rækken Markering på Mine makkeraftaler siger lavt kort = kald for begge makkerskaber, på dansk og engelsk, og de andre rækker er uændrede.
- [x] De øvrige tjek er i orden: `tjek_konventionskort.py`, `tjek_fagord.py`, `tjek_bydeform.py`, `tjek_sprog.py`, `tjek_makker2_aftaler.py`, `tjek_makker2_bilag_c.py`, `tjek_sidefod.mjs` og `tjek_viden_320.mjs`; og stavekontrollen har ingen nye stavefejl.

## Afklaret

Kørt 15. nov. 2026 på grenen: `python3 tools/tjek_makker2_markeringer.py`, `tjek_konventionskort.py` (49 kort), `tjek_fagord.py`, `tjek_bydeform.py`, `tjek_sprog.py`, `tjek_makker2_aftaler.py`, `tjek_makker2_bilag_c.py`, `tjek_crowhurst.py`, `tjek_skrifttyper.py`, `node tools/tjek_sidefod.mjs` og `node tools/tjek_viden_320.mjs ingen` (568 tjek) er i orden, og stavekontrollen har ingen ukendte ord. Ikke flettet.

1. **Accepttesten** `tools/tjek_makker2_markeringer.py` blev skrevet før ændringen (`5fd706e`) og var rød (20 fejl). Efter ændringen fejlede den først på count-linjen, fordi "Reglen om 11" også står tidligere i afsnit 19, så testens udsnit for Rangorden blev tomt; testen søger nu efter Reglen om 11 efter overskriften Rangorden og tjekker, at Rangorden findes. Med Franks tre ekstra rettelser tjekker den, at dokumentet er tagget med præcis de aftalte rettelser og intet andet.
2. **Rettet i afsnit 19, Attitude:** reglen siger "Lavt kort = kald (»fortsæt«), højt kort = afvisning (»skift«)". Tabellen har nu "Lavt kort (fx 2 fra 8-3-2)" på den grønne række med Kald og "Højt kort (fx 8 fra 8-3-2)" på den røde række med Afvisning; teksterne om kald og afvisning og rækken Ligegyldigt kort er uændrede. Noten om, at højt og lavt er relativt, havde eksemplet efter den gamle retning og siger nu "En 6'er kan være en afvisning fra 6-4-3 og et kald fra 9-8-6."
3. **Rettet i afsnit 19, Rangorden:** count-linjen siger "lavt kort = lige antal (lavt-højt), højt kort = ulige antal (højt-lavt)". Resten af rækken (når attitude er kendt eller irrelevant, eller når spilfører angriber farven) er uændret.
4. **Resten af dokumentet** er gennemsøgt for højt kort, lavt kort, højt-lavt, lavt-højt, kald, afvisning, count, antal og markering. Retningen står ingen andre steder; Lavinthal (afsnit 20, højt kort = den højeste farve) er uændret, og noten "Har du hverken noget at kalde eller afvise med" er neutral.
5. **Mine makkeraftaler** (`makkeraftaler.html`) byggede på den gamle retning: rækken Markering i Forskelle mellem systemerne sagde "Lavt kort = kald" for Makker 1 og "Højt kort = kald" for Makker 2. Begge spiller nu lavt kort = kald, så rækken ville ikke længere vise en forskel. Mit valg: rækken viser nu den forskel, der er tilbage, nemlig hvornår der markeres antal: Makker 1 "Lavt kort = kald; antal efter konge-udspil og ved ny farve" og Makker 2 "Lavt kort = kald; antal, når attitude er kendt, eller spilfører angriber farven", også på engelsk. Alternativet er at fjerne rækken; det er Franks valg.
6. **Det, der ikke bygger på Makker 2's gamle retning, og som ikke er ændret:** konventionskortene Markeringer, Lavinthal og Udspil (efter Bridgesystem: lavt = kald, Malmø lavt = lige; kortene nævner ikke makkerskaber), markeringstræneren (`markering.html` og `dealer/markering.py`, system `kf`, lavt = kald), puljerne (der er ingen pulje eller træner for Makker 2's markeringer) og testene (ingen test tjekkede retningen).
7. **Franks tre ekstra rettelser (15. nov. 2026):** B2, svarskemaet til Multi: 2♠ siger nu "Pas eller ret den anden vej, med hjertertolerance: pas med spar, ret til 3♥ med hjerter." Bilag E2: "vejer tungere end et overstik (1 imp)". Afsnit 19, grundreglen: "2. højeste fra en svag farve uden honnør; fra to kort spilles det højeste (»top af intet«)".
8. **B4 har samme Multi-række:** B4 (samlet pakke med Multi 2♦) har stadig "Pas-eller-ret den anden vej — bruges med længere spar end hjerter" for 2♠, ordret som B2 havde det. Den er ikke rettet, fordi rettelsen gjaldt B2; Frank afgør, om B4 skal have samme tekst.
9. **Stavekontrollen** kendte ikke hjertertolerance, som står i B2-teksten. Ordet er rigtigt og står nu i `tools/ordliste.txt` ved de andre hjerter-ord.
10. **`tjek_viden_320.mjs` med pixelsammenligning** fejler for Makker 2-dokumentet ved 390 og 1280 px på dansk og engelsk, fordi teksten er ændret: forskellen ligger om de rettede linjer (fx "Lavt kort = kald"). Uden pixelsammenligning (`ingen`) er alle 568 tjek i orden, så der er ingen vandret scroll ved 320 px. Siderne i øvrigt og kortene var ens med tagget i den del, der nåede at køre.

