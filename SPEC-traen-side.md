# SPEC-traen-side

17. oktober 2026 · Frank

Forsiden (`index.html`) får en ny struktur: alle trænere på én side, ordnet efter emne i stedet for system, med søgning og et filter pr. system. Henvisningen til aftalerne flyttes fra forsiden ned i en fælles sidefod. Alle sider får den samme sorte sidefod som www.kontraktbridge.dk. Designgrundlaget er tegnefladen "Ny struktur for trænerne" (https://claude.ai/artifact/Y9sKNd1KgmKQtHTVr2mMAw), skærmene "Konventionstræner · Træn (computer)" og "Konventionstræner · Træn (mobil)".

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
| `traener.html`, `markering.html` | gemme konventionen i "Senest trænet", når en runde starter; sidefoden | ændre træningen, hænderne eller bedømmelsen |
| `multi-svar-traener.html` | gemme `multiforsvar` i "Senest trænet", når en runde starter; sidefoden (Afklaret, punkt 2) | ændre træningen, hænderne eller bedømmelsen |
| `viden/` | sidefoden | ændre indholdet |
| `assets/site.css` | klasser til søgning, filter, kort og sidefod med eksisterende variabler | ændre værdien af eksisterende variabler |
| Lagring | ny nøgle `senest` (se nedenfor); `system` læses og skrives som i dag | ændre andre nøgler |
| Sprog | al ny tekst på dansk og engelsk med `T()`, `data-en` og `en`-felter | dansk tekst på den engelske side |

Kræver noget alligevel en ændring ud over tabellen, skal Claude Code stoppe og spørge.

Besked til Claude Code:

> Byg den nye forside efter SPEC-traen-side.md og skærmene "Konventionstræner · Træn" på tegnefladen. Trænerne, puljerne og hænderne er uændrede. Al ny tekst skal findes på dansk og engelsk. Vis mig siden lokalt, før du fletter ind.

## Opbygning af forsiden

Øverst til nederst:

1. **Topmenu** som i dag: Konventionstræner, Træn, Viden og sprogknappen.
2. **Indledning:** "45 trænere · 8 meldeforløb pr. runde" (tallet regnes ud fra data), overskriften "Træn konventionerne, til de sidder" og én linje: "Vælg en konvention og få 8 tilfældige meldeforløb. Nogle gange åbner eller melder du ind, andre gange svarer du makker." Linket til Viden i teksten fjernes.
3. **Find en træner:** en hvid boks med
   - et søgefelt ("Søg", pladsholder "Stayman, Bergen, 2♣ …"), der søger i titel og beskrivelse uden forskel på store og små bogstaver
   - filterknapper: Alle, Makker 1 & mig, Makker 2 & mig, Kampen om kontrakten og Forslag, hver med antal trænere. Den valgte er sort med hvid tekst og har `aria-pressed="true"`.
   - når et system er valgt, en linje: "Viser trænerne for Makker 2 & mig. Aftalerne for Makker 2 & mig →" med link til systemets dokument.
4. **Senest trænet:** en lys orange boks med op til tre knapper til de senest trænede konventioner (titel og system). Boksen vises ikke, før man har trænet noget.
5. **Gå til:** en række knapper, ét pr. emne, der springer ned til emnet. Kun emner med trænere efter søgning og filter vises.
6. **Delene** med emner og kort (tabellen nedenfor). Hver del har en stor overskrift og én linje under. Hvert emne har en mellemoverskrift og antal trænere ("6 trænere").
7. **Sidefoden** (se nedenfor).

Afsnittet "Viden" med kort nederst på forsiden fjernes. Viden findes stadig i topmenuen og i sidefoden.

### Kortene

- Hvidt kort med hjørner 24px: mærker for systemerne øverst, titlen, to linjer af beskrivelsen og nederst rollerne til venstre ("Åbner · Svarer") og "Træn 8 →" til højre.
- Mærkerne er "Makker 1", "Makker 2", "Kampen om kontrakten" og "Forslag". Forslag har gul baggrund, de andre grå. En konvention i flere systemer har et mærke for hvert.
- Kulørerne farves som i dag (`suits()`).
- En konvention med `status` "kommer" vises med tynd ramme, dæmpet tekst og "Kommer" i stedet for "Træn 8 →". Den er ikke et link.
- Kortet fører til samme adresse som i dag: `side` eller `traener.html`, med `?k=<id>`.
- Mobil: kortene vises som rækker i én hvid boks (titel, mærker og roller og en pil), som på mobilskærmen.

### Ingen træner fundet

Giver søgning og filter ingen trænere: "Ingen trænere passer. Prøv et andet ord, eller vælg Alle." og en knap "Vis alle trænere", der nulstiller begge.

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
- Feltet `gruppe` bevares, fordi `traener.html` viser det i overskriften.

## Filter og adresse

- Standard er Alle.
- `?system=kf` (eller ff, kamp, forslag) i adressen vælger systemet, så tilbage-linket fra træneren (`./?system=…#traen`) virker som i dag.
- Valget skrives i `system` i localStorage som i dag, men forsiden starter kun med det valgte system, når det står i adressen.
- Søgning og filter ændrer ikke adressen.

## Senest trænet

- Ny nøgle `senest` i localStorage: en liste med højst tre konvention-id'er, nyeste først, uden dubletter.
- `traener.html` og `markering.html` skriver id'et, når en runde starter. Al adgang til localStorage står i `try/catch` som i dag.
- Forsiden viser kun id'er, der findes og er klar. Systemet på knappen er konventionens første system.

## Sidefoden

Samme sorte sidefod nederst på alle sider: `index.html`, trænerne og siderne under `viden/`. Den bygges som en fælles komponent, fx `assets/footer.js`, der indsætter sidefoden i et element `<footer id="sidefod">`, så teksten kun står ét sted.

- **Venstre:** "Kontraktbridge" (orange, Manrope 800, link til https://www.kontraktbridge.dk/), mellemoverskriften "Om mig" og teksten: "Jeg er bridgeentusiast med forkærlighed for spillets kognitive udfordringer og det gode fællesskab omkring bordet. Jeg elsker at skabe og forbedre ting – og med AI som ny medspiller har jeg bygget et digitalt bridge-univers, der kombinerer logik, læring og spilleglæde."
- **Kolonnen Trænere:** Konventionstræner, Fordeling, Pointregnskab, Farvebehandling og Håndevaluering. De fire sidste fører til `/fordelingstraeneren/`.
- **Kolonnen Aftaler og notater:** Makker 1 & mig, Makker 2 & mig, Kampen om kontrakten, Forslag og Forskelle mellem systemerne (`viden/#forskelle`).
- **Kolonnen Kontakt:** "Har du fundet en fejl, eller har du en idé til en ny træner? Skriv til mig." og frank.steen.pedersen@gmail.com som `mailto:`-link i orange.
- **Nederst** under en streg: "© 2026 Frank Pedersen".
- Farver: baggrund `--sg-ink`, tekst `--sg-canvas-soft`, navn og mail `--sg-primary`, hjørner 24px, margen 48px × 24px.
- Engelsk: "About me", "Trainers", "Agreements and notes (in Danish)", "Contact" og en engelsk udgave af teksterne.
- Links til de andre trænere skrives med `/` foran (`/fordelingstraeneren/`), fordi siden ligger på www.kontraktbridge.dk. Alle andre links i siden forbliver relative.
- Sidefoden vises ikke ved udskrift (`@media print`), så systemdokumenterne udskrives som i dag.

## Accepttest

- [ ] Hvert kort fører til samme adresse som før (`traener.html?k=…` eller `markering.html?k=…`).
- [ ] Alle konventioner, der vises i dag, vises stadig, og ingen vises to gange.
- [ ] Hver konvention har et `emne`, og emnerne står i rækkefølgen i `data/emner.json`.
- [ ] Filteret viser det rigtige antal pr. system, og en konvention i to systemer tæller i begge.
- [ ] Søgning på "bergen" viser Omvendt Bergen og Revideret omvendt Bergen; søgning på "2♣" virker.
- [ ] `?system=ff` vælger Makker 2 & mig, og tilbage-linket fra træneren virker.
- [ ] "Senest trænet" viser de tre senest startede konventioner og vises ikke for en ny bruger.
- [ ] Siden virker uden localStorage (privat vindue).
- [ ] Sidefoden står ens på alle sider og vises ikke ved udskrift.
- [ ] På engelsk står der intet dansk på forsiden, bortset fra dokumenternes titler.
- [ ] Ingen vandret rulning på en 390 px bred skærm.

## Afklaret

Claude Codes gennemgang og Franks svar (17. oktober 2026):

1. **Tællingen:** indledningen tæller de konventioner, der er klar og har et system (45). Filterknapperne og emnernes antal tæller også dem med status "kommer" (Alle 47, Forslag 6, Åbninger 6), som på tegnefladen (Franks valg) (Opbygning af forsiden).
2. **Multitræneren** (`multi-svar-traener.html`) får sidefoden og skriver `multiforsvar` i `senest`, når en runde starter. På forsiden står den derfor som "Multiforsvar mod 1NT", og knappen åbner `traener.html?k=multiforsvar` (Franks valg). Siden er kun på dansk, så sidefoden står på dansk dér (Afgrænsning, Senest trænet).
3. **Sidefoden pr. app:** udseendet er det samme som på www.kontraktbridge.dk, men kolonnerne følger hver apps spec. Konventionstræneren har Trænere med fem links og Aftaler og notater; Fordelingstræneren har kolonnerne i SPEC-forside-spor.md (Franks valg) (Sidefoden).
4. **Tegnefladens mobilskærm:** sidefoden og den korte indledning dér er en ældre udgave. Computerskærmens sidefod og specens indledning gælder på begge skærme.
5. **Kortene** åbner i samme vindue. Tegnefladens nye faner skyldes kun tegnefladen (Kortene).
6. **Mobil:** rækkerne i én hvid boks bruges under 600 px, samme grænse som i `assets/site.css` (Kortene).
7. **`#traen`** står på boksen "Find en træner", så tilbage-linket fra træneren lander dér (Filter og adresse).
8. **Søgningen** søger i titel og beskrivelse på sidens sprog.
9. **Systemlinjen for Forslag:** "Viser trænerne for Forslag. Læs forslagene →" / "Showing the trainers for Proposals. Read the proposals →", fordi "Aftalerne for Forslag" lyder skævt.
10. **Sidefoden og Word-eksporten:** sidefoden står uden for `<main>`, så `doc-export.js` ikke tager den med i Word-filen (Sidefoden).
11. **Relative links i sidefoden:** `assets/footer.js` finder sitets rod ud fra sin egen adresse, så linkene til aftalerne virker både fra roden og fra `viden/` (Sidefoden).
12. **Data:** alle 47 viste konventioner står i emnetabellen præcis én gang; kun `kamp-landy` mangler og får `nt-konkurrence` som beskrevet (Dele og emner).
