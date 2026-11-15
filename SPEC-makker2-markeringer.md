# SPEC-makker2-markeringer

15. november 2026 · Franks afgørelse 15. november 2026. Bygges på grenen `makker2-markeringer`; `main` før er tagget `v-foer-makker2-markeringer`. Stop før merge.

Makker 2-dokumentet (`viden/2-over-1-makker2.html`) har markeringerne forkert. Makker 2 spiller som Bridgesystem og Kompendium over modspilsaftaler: lavt kort = kald, højt kort = afvisning, og lavt kort = lige antal, højt kort = ulige (lavt-højt = lige, højt-lavt = ulige). Lavinthal er uændret.

## Ændringen

- **Afsnit 19, Attitude:** reglen bliver "Lavt kort = kald (»fortsæt«), højt kort = afvisning (»skift«)". I tabellen med eksemplet 8-3-2 er 2'eren nu kald og 8'eren afvisning; rækkernes farver (grøn for kald, rød for afvisning) følger betydningen. Noten om, at højt og lavt er relativt, får eksemplet vendt: en 6'er er en afvisning fra 6-4-3 og et kald fra 9-8-6.
- **Afsnit 19, Rangorden:** count-linjen bliver "lavt kort = lige antal (lavt-højt), højt kort = ulige antal (højt-lavt)".
- **Resten af dokumentet** er gennemsøgt for "højt kort", "lavt kort", "højt-lavt", "lavt-højt", "kald" og "afvisning"; retningen står kun i afsnit 19. Lavinthal (afsnit 20) er uændret.
- **Mine makkeraftaler** (`makkeraftaler.html`), tabellen Forskelle mellem systemerne: rækken Markering byggede på den gamle retning (Makker 2: "Højt kort = kald"). Begge makkerskaber spiller nu lavt kort = kald, så rækken viser den forskel, der er tilbage: hvornår der markeres antal (Makker 1 efter konge-udspil og ved ny farve; Makker 2, når attitude er kendt, eller spilfører angriber farven), på dansk og engelsk.

## Afgrænsning

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `viden/2-over-1-makker2.html` | afsnit 19: Attitude (reglen, tabellen og noten) og count-linjen i Rangorden | andre afsnit, Lavinthal, layout og stil |
| `makkeraftaler.html` | rækken Markering i Forskelle mellem systemerne (dansk og engelsk) | andre rækker |
| `tools/tjek_makker2_markeringer.py` | ny accepttest | |
| Konventionskortene, puljerne, `dealer/`, `markering.html`, Bridgesystem | intet: de følger Bridgesystem og bygger ikke på Makker 2's gamle retning | |

## Accepttest

`python3 tools/tjek_makker2_markeringer.py`:

- [ ] Afsnit 19 siger lavt kort = kald og højt kort = afvisning; tabellen har "Lavt kort (fx 2 fra 8-3-2)" som kald og "Højt kort (fx 8 fra 8-3-2)" som afvisning; noten siger afvisning fra 6-4-3 og kald fra 9-8-6.
- [ ] Count-linjen siger lavt kort = lige antal (lavt-højt) og højt kort = ulige antal (højt-lavt).
- [ ] Ingen steder i dokumentet står "højt kort = kald", "lavt kort = afvisning", "højt-lavt = lige" eller "lavt-højt = ulige".
- [ ] Dokumentet er uændret uden for afsnit 19, og afsnit 20 (Lavinthal) er tegn for tegn som i tagget.
- [ ] Rækken Markering på Mine makkeraftaler siger lavt kort = kald for begge makkerskaber, på dansk og engelsk, og de andre rækker er uændrede.
- [ ] De øvrige tjek er i orden: `tjek_konventionskort.py`, `tjek_fagord.py`, `tjek_bydeform.py`, `tjek_sprog.py`, `tjek_makker2_aftaler.py`, `tjek_makker2_bilag_c.py`, `tjek_sidefod.mjs` og `tjek_viden_320.mjs`; og stavekontrollen har ingen nye stavefejl.

## Afklaret

(Udfyldes, når ændringen er bygget.)
