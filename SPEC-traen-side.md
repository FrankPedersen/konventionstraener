# SPEC-traen-side

17. oktober 2026 · Frank

Forsiden (`index.html`) får en ny struktur: alle trænere på én side, ordnet efter emne i stedet for system, med søgning. (Filteret pr. system er fjernet igen; makkerskaberne står på Mine makkeraftaler, Afklaret, punkt 24–25.) Henvisningen til aftalerne flyttes fra forsiden ned i en fælles sidefod. Alle sider får den samme sorte sidefod som www.kontraktbridge.dk. Designgrundlaget er tegnefladen "Ny struktur for trænerne" (https://claude.ai/artifact/Y9sKNd1KgmKQtHTVr2mMAw), skærmene "Konventionstræner · Træn (computer)" og "Konventionstræner · Træn (mobil)".

Trænerne (`traener.html`, `markering.html`, `multi-svar-traener.html`), puljerne og hændernes data ændres ikke, bortset fra sidefoden og registreringen af "Senest trænet".

## Afgrænsning

Før arbejdet starter:

1. Commit og tag den nuværende side, fx `v-foer-traen-side`.
2. Arbejd på grenen `traen-side`, og flet først ind efter godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `index.html` | ny opbygning som beskrevet nedenfor | fjerne en træner eller ændre, hvor et kort fører hen |
| `data/konventioner.json` | nyt felt `emne` på hver konvention (tabellen nedenfor) | ændre de eksisterende felter |
| `data/emner.json` (ny) | dele, emner og deres rækkefølge på dansk og engelsk | — |
| `traener.html`, `markering.html` | gemme konventionen i "Senest trænet", når en runde starter; topbjælken og sidefoden | ændre træningen, hænderne eller bedømmelsen |
| `multi-svar-traener.html` | gemme `multiforsvar` i "Senest trænet", når en runde starter; topbjælken og sidefoden (Afklaret, punkt 2 og 15) | ændre træningen, hænderne eller bedømmelsen |
| `viden/` | topbjælken og sidefoden | ændre indholdet |
| `assets/topbar.js` (ny) | topbjælken som fælles komponent (Topbjælken) | — |
| `assets/site.css` | klasser til søgning, filter, kort og sidefod med eksisterende variabler | ændre værdien af eksisterende variabler |
| Lagring | ny nøgle `senest` (se nedenfor); `system` bruges ikke længere (Afklaret, punkt 24) | ændre andre nøgler |
| Sprog | al ny tekst på dansk og engelsk med `T()`, `data-en` og `en`-felter | dansk tekst på den engelske side |

Kræver noget alligevel en ændring ud over tabellen, skal Claude Code stoppe og spørge.

Besked til Claude Code:

> Byg den nye forside efter SPEC-traen-side.md og skærmene "Konventionstræner · Træn" på tegnefladen. Trænerne, puljerne og hænderne er uændrede. Al ny tekst skal findes på dansk og engelsk. Vis mig siden lokalt, før du fletter ind.

## Opbygning af forsiden

Øverst til nederst:

1. **Topbjælke** (se "Topbjælken" nedenfor): 7NT-logoet, "Kontraktbridge · Konventionstræner", Træn, Viden, Mine makkeraftaler og English.
2. **Indledning:** "45 trænere · 8 meldeforløb pr. runde" (tallet regnes ud fra data), overskriften "Træn konventionerne, til de sidder" og én linje: "Vælg en konvention og få 8 tilfældige meldeforløb. Nogle gange åbner eller melder du ind, andre gange svarer du makker." Linket til Viden i teksten fjernes.
3. **Find en træner:** en hvid boks med
   - et søgefelt ("Søg", pladsholder "Stayman, Bergen, 2♣ …"), der søger i titel og beskrivelse uden forskel på store og små bogstaver
   - ingen filterknapper og ingen systemlinje: Træn er neutral, og makkerskaberne står på Mine makkeraftaler (Afklaret, punkt 24–25).
4. **Senest trænet:** en lys orange boks med op til tre knapper til de senest trænede konventioner (titlen). Boksen vises ikke, før man har trænet noget.
5. **Gå til:** en række knapper, ét pr. emne, der springer ned til emnet. Kun emner med trænere efter søgningen vises.
6. **Delene** med emner og kort (tabellen nedenfor). Hver del har en stor overskrift og én linje under. Hvert emne har en mellemoverskrift og antal trænere ("6 trænere").
7. **Sidefoden** (se nedenfor).

Afsnittet "Viden" med kort nederst på forsiden fjernes. Viden findes stadig i topmenuen og i sidefoden.

### Kortene

- Hvidt kort med hjørner 24px: titlen, to linjer af beskrivelsen og nederst rollerne til venstre ("Åbner · Svarer") og "Træn 8 →" til højre.
- Kortene har ingen systemmærker (Afklaret, punkt 24).
- Kulørerne farves som i dag (`suits()`).
- En konvention med `status` "kommer" vises med tynd ramme, dæmpet tekst og "Kommer" i stedet for "Træn 8 →". Den er ikke et link.
- Kortet fører til samme adresse som i dag: `side` eller `traener.html`, med `?k=<id>`.
- Mobil: kortene vises som rækker i én hvid boks (titel og roller og en pil), som på mobilskærmen.

### Ingen træner fundet

Giver søgningen ingen trænere: "Ingen trænere passer. Prøv et andet ord." og en knap "Vis alle trænere", der nulstiller søgningen.

## Dele og emner

Ny fil `data/emner.json` med delene og emnerne i den rækkefølge, de står på siden:

| Del (dansk / engelsk) | Linje under | Emner (`id`: dansk / engelsk) |
| --- | --- | --- |
| Åbninger og svar / Openings and responses | Åbninger, svar, støtte og videre meldeforløb – flere af trænerne tager også modpartens indmeldinger med. | `aabninger`: Åbninger / Openings · `svar-1nt`: Svar på 1NT / Responses to 1NT · `stoette`: Støtte / Raises · `videre`: Videre meldeforløb / Continuations |
| Konkurrence / Competition | Når modparten melder med – før eller efter os. | `nt-konkurrence`: 1NT i konkurrence / 1NT in competition · `indmeldinger`: Indmeldinger og genåbning / Overcalls and balancing · `doblinger`: Doblinger / Doubles · `stoette-konkurrence`: Støtte i konkurrence / Raises in competition |
| Slem og modspil / Slam and defence | Nøglekort, kontroller og markeringer. | `slem`: Slem / Slam · `modspil`: Modspil / Defence |

Hver konvention i `data/konventioner.json` får feltet `emne`:

| Emne | Konventioner (`id`) |
| --- | --- |
| `aabninger` | ff-2kl, ff-ogust, forslag-2kl-kontrolsvar, ff-flannery, ff-multi-2ru, ff-muiderberg |
| `svar-1nt` | stayman, transfer, ff-ass, ff-overfoeringer, ff-gerber |
| `stoette` | omvendt-bergen, ff-revideret-omvendt-bergen, bekkasin, ff-trial-bids, ff-omvendt-minor |
| `videre` | ff-two-over-one, ff-fast-arrival, ff-staerke-genmeldinger, xy-sans, fjerde-farve, ff-revers |
| `nt-konkurrence` | multiforsvar, ff-dont, kamp-forsvar-1ut, kamp-1ut-indmeldt, kamp-1ut-forsvar |
| `indmeldinger` | michaels, ff-michaels, usaedvanlig-2nt, ff-genaabning, kamp-gif, kamp-2020 |
| `doblinger` | ff-doblinger, kamp-doblinger, lebensohl, ff-lebensohl, ff-kravpas |
| `stoette-konkurrence` | kamp-stoette-def, kamp-stoette-off, kamp-stoette-minor, kamp-efter-od |
| `slem` | cuebids, 1430, ff-1430 |
| `modspil` | markeringer, lavinthal |

- Inden for et emne står konventionerne i samme rækkefølge som i `konventioner.json`.
- `kamp-landy` har intet system og vises ikke, som i dag. Den får `emne` `nt-konkurrence`, så den står rigtigt, hvis den senere får et system.
- En ny konvention uden `emne` vises under en sidste del "Andet" / "Other", så den aldrig forsvinder.
- Feltet `gruppe` bevares, fordi `traener.html` viser det i overskriften (uden system, Afklaret, punkt 27).

## Adresse

- Tilbage-linket fra trænerne er `./#traen`. Et gammelt `?system=…` i adressen ignoreres, så gemte links stadig virker (Afklaret, punkt 24).
- Nøglen `system` i localStorage læses og skrives ikke længere.
- Søgningen ændrer ikke adressen.

## Senest trænet

- Ny nøgle `senest` i localStorage: en liste med højst tre konvention-id'er, nyeste først, uden dubletter.
- `traener.html` og `markering.html` skriver id'et, når en runde starter. Al adgang til localStorage står i `try/catch` som i dag.
- Forsiden viser kun id'er, der findes og er klar. Knappen viser kun titlen (Afklaret, punkt 24).

## Topbjælken

Den samme sorte topbjælke øverst på alle sider: `index.html`, trænerne og siderne under `viden/`. Den bygges som en fælles komponent, fx `assets/topbar.js`, ligesom sidefoden.

- **Fuld bredde** og helt oppe i toppen, uden afrundede hjørner og uden luft omkring. Indholdet under har sin egen margen og maks. bredde 1200 px. (På tegnefladen hedder klassen `kb-bar` uden `round`.)
- **Venstre:** 7NT-logoet (orange meldekort, 36 × 36 px, hjørner 9 px, Manrope 800, tekst `--sg-ink`) og "Kontraktbridge" (Manrope 800, 19 px, hvid) som ét link til https://www.kontraktbridge.dk/. Derefter "· Konventionstræner" i lysegrå (#c9cdd2), som ikke er et link.
- **Højre:** Træn, Viden og Mine makkeraftaler som pille-links; den aktive side har `aria-current="page"` og en lys flade. Til sidst sprogknappen ("English" / "Dansk") med tynd hvid kant.
- Farver: baggrund #1a1a1a, tekst #f2f3f4, fokusring 2 px #ff9f4a.
- **Mobil** (under 600 px): samme bjælke i den smalle udgave (`slim`): logo 30 px, navn 16 px, mindre luft. Links og sprogknap brydes ned på en ny linje, hvis der ikke er plads. Stadig fuld bredde.
- Topbjælken vises ikke ved udskrift.

## Fælles regler for alle sider på www.kontraktbridge.dk

- **Topbjælke:** I appsene (Konventionstræner og Fordelingstræneren) er den fuld bredde øverst. På hubsiden www.kontraktbridge.dk står menuen i stedet inde i det sorte hero-felt, fordi feltet selv er sort. Det er bevidst.
- **Sprogknap:** På alle sider, der findes på engelsk: hubsiden, Konventionstræneren og Fordelingstræneren. Kun Konventionstrænerens systemdokumenter er på dansk og har ingen sprogknap (Franks beslutning 17. oktober 2026). På hubsiden og i Konventionstræneren gemmes valget under `lang` på www.kontraktbridge.dk, så det følger med mellem dem.
- **Sidefod:** 7NT-logoet, linjen "Gratis bridgetræning i browseren. Lavet af Frank Pedersen.", knappen "Om mig og kontakt →" og kolonnen Trænere (de 5 links nedenfor) på alle sider. Om mig og kontakt har sin egen side, https://www.kontraktbridge.dk/om-mig/ (SPEC-om-mig.md). Kun Konventionstrænerens sider har desuden kolonnen "Aftaler og notater".

## Sidefoden

Samme sorte sidefod nederst på alle sider: `index.html`, trænerne og siderne under `viden/`. Den bygges som en fælles komponent, fx `assets/footer.js`, der indsætter sidefoden i et element `<footer id="sidefod">`, så teksten kun står ét sted.

- **Venstre:** 7NT-logoet og "Kontraktbridge" som link til https://www.kontraktbridge.dk/, linjen "Gratis bridgetræning i browseren. Lavet af Frank Pedersen." og en orange knap "Om mig og kontakt →", der fører til https://www.kontraktbridge.dk/om-mig/. Teksten om mig og mailadressen står ikke længere i sidefoden (Afklaret, punkt 31).
- **Kolonnen Trænere:** Konventionstræner, Fordeling, Pointregnskab, Farvebehandling og Håndevaluering. De fire sidste fører til `/fordelingstraeneren/`.
- **Kolonnen Aftaler og notater:** Makker 1 & mig (`makkeraftaler.html#kf`), Makker 2 & mig (`makkeraftaler.html#ff`), Kampen om kontrakten, Forslag og Forskelle mellem systemerne (`makkeraftaler.html#forskelle`) (Afklaret, punkt 31).
- **Overskrift og link skal kunne skelnes:** kolonneoverskrifterne er `<h2 class="kb-foot-title">` i små grå versaler (12 px, 600, bogstavafstand 0,08em, #9aa0a6). Linkene står i en `<ul>` og er hvide, 15 px og altid understregede (stregen rgba(255,255,255,.35), afstand 4 px, orange #ffc48f ved hover).
- **Nederst** under en streg: "© 2026 Frank Pedersen" i grå.
- Farver: baggrund `--sg-ink`, tekst `--sg-canvas-soft`, knappen `--sg-primary`, navnet hvidt som på www.kontraktbridge.dk, hjørner 24px, margen 48px × 24px.
- Engelsk: "Trainers", "Agreements and notes (in Danish)", "About me and contact →", "Free bridge training in your browser. Made by Frank Pedersen." og "Partner 1 & me" / "Partner 2 & me".
- Links til de andre trænere skrives med `/` foran (`/fordelingstraeneren/`), fordi siden ligger på www.kontraktbridge.dk. Alle andre links i siden forbliver relative.
- Sidefoden vises ikke ved udskrift (`@media print`), så systemdokumenterne udskrives som i dag.

## Accepttest

Afkrydset 27. oktober 2026 efter et tjek af den udgivne side i Chrome (390 og 1200 px): 47 klar-kort og 2 "Kommer" af 49, ingen dubletter, emnerne i rækkefølgen fra `data/emner.json`, søgningerne, `?system=ff`, Senest trænet, siden uden localStorage, samme sidefod på 10 sider, topbjælke og sidefod skjult ved udskrift og intet dansk på den engelske forside ud over navnet Konventionstræner.

- [x] Hvert kort fører til samme adresse som før (`traener.html?k=…` eller `markering.html?k=…`).
- [x] Alle konventioner, der vises i dag, vises stadig, og ingen vises to gange.
- [x] Hver konvention har et `emne`, og emnerne står i rækkefølgen i `data/emner.json`.
- [x] Træn har intet filter og ingen systemmærker; Mine makkeraftaler linker til alle klar-trænere i hvert makkerskab.
- [x] Søgning på "bergen" viser Omvendt Bergen og Revideret omvendt Bergen; søgning på "2♣" virker.
- [x] Tilbage-linket fra træneren fører til `./#traen`, og et gammelt `?system=ff` giver den almindelige side.
- [x] "Senest trænet" viser de tre senest startede konventioner og vises ikke for en ny bruger.
- [x] Siden virker uden localStorage (privat vindue).
- [x] Sidefoden står ens på alle sider og vises ikke ved udskrift.
- [x] Sidefoden har ingen Om mig-tekst og ingen mailadresse, og knappen "Om mig og kontakt →" fører til https://www.kontraktbridge.dk/om-mig/.
- [x] Topbjælken går i fuld bredde på alle sider, også på mobil, og vises ikke ved udskrift.
- [x] På engelsk står der intet dansk på forsiden, bortset fra dokumenternes titler.
- [x] Ingen vandret rulning på en 390 px bred skærm.

## Afklaret

Claude Codes gennemgang og Franks svar (17. oktober 2026):

1. **Tællingen:** indledningen tæller de konventioner, der er klar og har et system (45). Filterknapperne og emnernes antal tæller også dem med status "kommer" (Alle 47, Forslag 6, Åbninger 6), som på tegnefladen (Franks valg) (Opbygning af forsiden). Filterknapperne er fjernet igen (punkt 24); emnernes antal tæller stadig sådan.
2. **Multitræneren** (`multi-svar-traener.html`) får sidefoden og skriver `multiforsvar` i `senest`, når en runde starter. På forsiden står den derfor som "Multiforsvar mod 1NT", og knappen åbner `traener.html?k=multiforsvar` (Franks valg). Siden er kun på dansk, så sidefoden står på dansk dér (Afgrænsning, Senest trænet).
3. **Sidefoden pr. app:** udseendet er det samme som på www.kontraktbridge.dk, men kolonnerne følger hver apps spec. Konventionstræneren har Trænere med fem links og Aftaler og notater; Fordelingstræneren har kolonnerne i SPEC-forside-spor.md (Franks valg) (Sidefoden).
4. **Tegnefladens mobilskærm:** sidefoden og den korte indledning dér er en ældre udgave. Computerskærmens sidefod og specens indledning gælder på begge skærme.
5. **Kortene** åbner i samme vindue. Tegnefladens nye faner skyldes kun tegnefladen (Kortene).
6. **Mobil:** rækkerne i én hvid boks bruges under 600 px, samme grænse som i `assets/site.css` (Kortene).
7. **`#traen`** står på boksen "Find en træner", så tilbage-linket fra træneren lander dér (Adresse).
8. **Søgningen** søger i titel og beskrivelse på sidens sprog.
9. **Systemlinjen for Forslag:** "Viser trænerne for Forslag. Læs forslagene →" / "Showing the trainers for Proposals. Read the proposals (in Danish) →", fordi "Aftalerne for Forslag" lyder skævt. På engelsk får alle links til aftalerne "(in Danish)" som i dag. Systemlinjen er fjernet igen (punkt 24).
10. **Sidefoden og Word-eksporten:** sidefoden står uden for `<main>`, så `doc-export.js` ikke tager den med i Word-filen (Sidefoden).
11. **Relative links i sidefoden:** `assets/footer.js` finder sitets rod ud fra sin egen adresse, så linkene til aftalerne virker både fra roden og fra `viden/` (Sidefoden).
12. **Data:** alle 47 viste konventioner står i emnetabellen præcis én gang; kun `kamp-landy` mangler og får `nt-konkurrence` som beskrevet (Dele og emner).
13. **Sidefodens stil** står i `assets/footer.js` og ikke i `assets/site.css`, fordi Viden-dokumenterne ikke indlæser `site.css`. Reglerne har `#sidefod` foran, så dokumenternes egne regler for `h2`, `p` og `a` ikke slår igennem (Claude Codes valg ved bygningen) (Sidefoden).
14. **Navnene Konventionstræner og Kontraktbridge** oversættes ikke på engelsk, ligesom navnet i topmenuen. Det er den eneste danske tekst på den engelske forside.

Topbjælken – Claude Codes gennemgang og Franks svar (17. oktober 2026):

15. **Tabellen under Afgrænsning** havde kun sidefoden for trænerne og `viden/`. Topbjælken er tilføjet i de rækker, fordi afsnittet Topbjælken gælder alle sider. Multitræneren får den også, ligesom sidefoden (Afgrænsning).
16. **Sprogknappen** står kun på sider, der findes på engelsk: forsiden, `traener.html` og `markering.html` (fra 17. oktober også `viden/index.html` og multitræneren, punkt 22). Systemdokumenterne har ingen sprogknap. Tegnefladens English på Viden og Systemdokument gælder ikke (Franks valg) (Topbjælken, Fælles regler).
17. **Bredden:** forsiden og trænerne beholder deres 64rem (1024 px), og systemdokumenterne deres egne bredder. "Maks. bredde 1200 px" betyder, at bjælken ikke rammer indholdet ind; kun topbjælken ændres (Franks valg) (Topbjælken).
18. **Logo i sidefoden:** sidefoden får 7NT-logoet foran "Kontraktbridge" som på www.kontraktbridge.dk og tegnefladen (Franks valg) (Sidefoden).
19. **De tre slags topmenu i dag** – `site-head` (forsiden, trænerne, `viden/index.html`, `2-over-1.html`, `forslag-2klor-kontrolsvar.html`), `header.top` i de tre systemdokumenter og navnepladen i multitræneren – erstattes af topbjælken. Multitrænerens navneplade "Bridgesystem · Multiforsvar · version 1.7" bliver stående under bjælken, fordi den er sidens titel. Sprogknappen beholder sin funktion fra `lang.js` (Topbjælken).
20. **Multitrænerens sidefod** stod ved siden af træneren i stedet for under den, fordi siden er en vandret flex-boks. Rettet i sidens eget stilark med en kolonne under topbjælken; testen tjekker nu sidefodens placering på alle sider (Claude Codes fund ved bygningen).
21. **Makker 2-dokumentet** (`viden/2-over-1-makker2.html`) ruller vandret på 390 px (413 px), fordi nogle tabeller er bredere end skærmen. Det var sådan før topbjælken, og indholdet under `viden/` må ikke ændres i denne opgave. Det kan tages i en senere opgave.

Engelsk på de sidste sider – Franks beslutning (17. oktober 2026):

22. **Viden-oversigten og multitræneren findes nu på engelsk** med sprogknap i topbjælken. Systemdokumenterne (ca. 32.000 ord) forbliver på dansk og står med "in Danish" i Viden-oversigten og "(in Danish)" ved links til aftalerne. Multitrænerens spørgsmål har `en`-felter i samme ordlyd som puljen `pools/multiforsvar.json` (HCP, support points, pass or correct, suggests penalty); meldingerne har et `data-call`, så knappen kan hedde "Pass" på engelsk.
23. **Konventionstræneren hedder "Convention trainer"** i sidefodens link på engelsk, som på hubsiden og i Fordelingstræneren. I topbjælken står navnet "Konventionstræner" som appens navn på begge sprog (punkt 14).

Neutral Træn-side og Mine makkeraftaler – Franks beslutning (17. oktober 2026):

24. **Træn er neutral** og kan bruges af alle: ingen filterknapper, ingen systemlinje og ingen systemmærker på kortene. Alle 47 trænere står stadig under deres emner, også dem, der var forslag (Flannery, Revers, 2♣ med kontrolsvar, Lavinthal). "Senest trænet" viser kun titlen. Forsiden bruger ikke længere `system` i localStorage, og et `?system=` i adressen ignoreres (Franks valg: "Fjern filteret og mærket").
25. **Mine makkeraftaler** (`makkeraftaler.html`) er en ny side og det tredje punkt i topmenuen ("My partnerships" på engelsk, med sprogknap). For hvert makkerskab (Makker 1 & mig, Makker 2 & mig) står navnet og kendetegnene fra `data/systemer.json`. Under "Aftaler og notater" står dokumenterne fra `data/viden.json`. Under "Trænere" står links til alle systemets trænere, grupperet efter emne; trænere med status "kommer" står uden link. Tabellen "Forskelle mellem systemerne" er flyttet hertil fra Viden (`#forskelle`) (Franks valg: "Egen side i topmenuen").
26. **Viden** hedder nu "Referencer og notater" og viser Kampen om kontrakten, Forslag og Notater med et link til Mine makkeraftaler. Makkerskabernes systemdokumenter står kun på Mine makkeraftaler. Notatet "Standard 2 over 1 i dansk version" står begge steder. Kampen om kontrakten har ingen filtre på Træn (Franks valg: "Nej, ingen filtre"). Linket "Træn emnerne →" i dokumentet fører til `../#traen`.
27. **Trænersiderne** viser kun gruppen øverst, fx "Modspil" i stedet for "Makker 1 & mig · Forslag · Modspil". Kildelinjen nederst ("Aftalerne står i systemet for Makker 2 & mig") bliver stående, fordi den fortæller, hvor reglerne kommer fra. Tilbage-linket er `./#traen` (Claude Codes valg, så trænerne også er neutrale).
28. **Data:** tekster i `data/konventioner.json`, der nævnte makkerskab eller forslag, er gjort neutrale på dansk og engelsk. `gruppe` "2♦-åbninger (Makker 2 & mig, bilag B)" er blevet til "2♦-åbninger" og "Forslag (Makker 2 & mig, bilag G)" til "Videre meldeforløb". Beskrivelserne af Two over One udgangskrav ("– ikke 10+ som hos Makker 1 & mig"), Lavinthal ("Forslag – trænes, før det skrives ind i systemkortet.") og Revers ("Diskussionsoplæg, ikke vedtaget:") har mistet de dele. Sammenligningen står i Forskelle-tabellen. Feltet `system` er uændret, fordi Mine makkeraftaler og Viden bruger det (Claude Codes valg).
29. **Systemdokumenterne** `viden/bridgesystem.html` og `viden/2-over-1-makker2.html` markerer Mine makkeraftaler som aktivt punkt i topbjælken. De øvrige dokumenter under `viden/` markerer Viden.
30. **Mobil:** under 600 px har topbjælkens links og sprogknap lidt mindre luft, så de står på én linje ved 390 px på begge sprog. Under ca. 380 px brydes sprogknappen ned på en ny linje. Lange trænertitler på Mine makkeraftaler må bryde linjen, så intet ruller vandret ved 320 px.

Om mig og kontakt får sin egen side – Franks beslutning (18. oktober 2026):

31. **Sidefoden uden Om mig og Kontakt.** Teksten om mig, kolonnen Kontakt og mailadressen er flyttet til siden https://www.kontraktbridge.dk/om-mig/ (SPEC-om-mig.md).
    - **Ny venstre del:** linjen "Gratis bridgetræning i browseren. Lavet af Frank Pedersen." og den orange knap "Om mig og kontakt →".
    - **Aftaler og notater** har nu Makker 1 & mig og Makker 2 & mig hver for sig (`makkeraftaler.html#kf` og `#ff`) i stedet for Mine makkeraftaler. Forskelle mellem systemerne peger stadig på `makkeraftaler.html#forskelle`, hvor tabellen står. Det afløser sidefodens del af punkt 25 (Franks valg).
    - **Udseendet** er det samme som på www.kontraktbridge.dk: kolonneoverskrifterne er små grå versaler, og linkene står i lister og er hvide og understregede.
    - **Topbjælken** er uændret (Franks valg).
    - **`makkeraftaler.html`** springer til ankeret (`#kf`, `#ff` eller `#forskelle`), når afsnittene er bygget. Ellers lander sidefodens links forkert, fordi afsnittene først tegnes efter indlæsningen (Claude Codes fund ved bygningen).
    - **Ikke rettet:** Makker 2-dokumentet ruller stadig vandret på 390 px (punkt 21).

Makker 2-dokumentet på mobil – Franks opgave (18. oktober 2026):

32. **Ingen vandret rulning i Makker 2-dokumentet.** Årsagen var ikke tabellerne, der ruller i deres egen boks, men tre h2-overskrifter med `font-size:40px` inline: "Del III · Spærremeldinger", "Bilag A · Alerteringsoversigt" og "Bilag E · Scoringsmetoder". Deres lange ord kunne ikke brydes.
    - `assets/doc-sg.css` giver nu h2–h4 i dokumenterne `overflow-wrap:anywhere` og `hyphens:auto`. Under 480 px er eksportens h2 30 px (`!important` på grund af inline-stilen).
    - `scrollWidth` er nu lig med skærmbredden ved 320, 360, 375 og 390 px. Det afløser punkt 21.
    - Versionen på stylesheetet er hævet til `?v=2026-10-18` i de tre dokumenter og i `tools/import_design.py`.
    - Bridgesystemet er 337 px bredt ved 320 px, ligesom før ændringen. Ved 360 px og derover passer det.
