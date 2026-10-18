# SPEC-konventionskort

17. oktober 2026 · Frank

Konventionerne og modspilsaftalerne får en fast beskrivelse: ét konventionskort pr. konvention efter skabelonen `konvention/2` i `docs/konventionskort-skabelon.md`. Skabelonen har to typer, `melding` og `modspil`, med de samme seks afsnit. Kortene er uafhængige af makker og ligger som data i `data/kort/`. Siden `viden/konventionskort.html` viser dem. Designgrundlaget er artifactet "Konventionskortet" (https://claude.ai/artifact/KjwqP8ZPqSzh3WzRZyq4fx).

Filerne i denne leverance er færdige og testet. Opgaven er at lægge dem ind, linke til siden og gøre arbejdsgangen fast.

## Afgrænsning

Før arbejdet starter:

1. Commit og tag den nuværende side, fx `v-foer-konventionskort`.
2. Arbejd på grenen `konventionskort`, og flet først ind efter godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `data/kort/` (ny) | kortene, `index.json` og `konvention.schema.json` fra leverancen | — |
| `docs/konventionskort-skabelon.md` (ny) | skabelonen fra leverancen | — |
| `tools/` | `tjek_konventionskort.py`, `build_konventionskort.py`, `konventionskort.src.html` og `konventionskort-shell.html` fra leverancen; `konventionskort-hint-shell.js` (ny, Afklaret 8) | ændre de eksisterende værktøjer |
| `viden/konventionskort.html` (ny) | genereres med `build_konventionskort.py` | rettes i hånden |
| `viden/index.html` | ét fælles felt "Konventionskort" over systemerne, der linker til siden | ændre listen over systemdokumenter |
| `CLAUDE.md` (ny) | arbejdsreglerne fra leverancen | — |
| `assets/konventionskort-hint.js` (ny) | genereres med `build_konventionskort.py` (Afklaret 8) | rettes i hånden |
| `traener.html`, `markering.html`, `multi-svar-traener.html` | ⓘ ved titlen (Afklaret 5) | ændre træningen |
| `data/konventioner.json`, puljerne | intet i denne omgang | alt |
| Sprog | sidens faste tekster forbliver på dansk; kortene er kun på dansk | engelske kort uden ny version af skabelonen |

Kræver noget alligevel en ændring ud over tabellen, skal Claude Code stoppe og spørge.

## Trin

1. Læg filerne fra leverancen ind i samme mapper som i leverancen.
2. Kør `pip install jsonschema` og derefter `python3 tools/tjek_konventionskort.py`. Den skal melde "5 konventionskort er i orden".
3. Kør `python3 tools/build_konventionskort.py` og kontrollér, at `viden/konventionskort.html` ikke ændrer sig i forhold til leverancen.
4. Tilføj feltet "Konventionskort" på `viden/index.html` med samme kortstil (`.tile`) som systemdokumenterne. Tekst: "Konventionerne beskrevet i én fast skabelon – uafhængigt af makker."
5. Åbn via lokal webserver: `viden/konventionskort.html`, `#truscott`, `#truscott-1klor`, `#multiforsvar`, `#lavinthal` og `#udspil`. Tjek fuld visning, kompakt og skabelon på computer og mobil.

## Afklaret

1. Kortet har samme `id` som træneren i `data/konventioner.json`, når der findes en (`multiforsvar`, `lavinthal`). Lavinthal-kortets eksempler er hentet fra `pools/lavinthal.json`. Et link fra træneren til kortet er næste skridt, ikke denne opgave.
2. Siden ligger i shadow DOM, så `site.css` og kortets egne klasser (`.wrap`, `.chip`, `.kort`) ikke påvirker hinanden. Topbjælke og sidefod er sitets egne.
3. Nye konventioner følger arbejdsgangen i `CLAUDE.md`: ny fil i `data/kort/`, tilføj i `index.json`, kør tjekket.
4. Udspilsaftalerne samles på ét kort, `udspil`. Markeringer (kald, antal, afkast) bliver næste modspilskort med `id` = `markeringer`, så det matcher træneren.

ⓘ i trænerne – Franks ønske og svar (17. oktober 2026):

5. **ⓘ i trænerne** (Franks valg: "ⓘ nu, kort løbende"): `traener.html`, `markering.html` og `multi-svar-traener.html` viser et ⓘ ved titlen, når `data/kort/index.json` har et kort med samme `id` som træneren. I dag gælder det Lavinthal (`markering.html?k=lavinthal`) og Multiforsvar (`traener.html?k=multiforsvar` og multitræneren). Trænere uden kort viser intet. Deres ⓘ kommer af sig selv, når kortet lægges ind. Dermed er "næste skridt" fra punkt 1 taget.
6. **Visningen** (Franks valg: "Fold ud under titlen"): et tryk folder kompaktvisningen ud under trænerens beskrivelse (i multitræneren under indledningen), og et nyt tryk lukker den. Kortet er lukket, når siden åbnes. "Hele konventionen →" fører til `viden/konventionskort.html#<id>`. Knappen har `aria-expanded` og `aria-label` "Om konventionen" / "About the convention (in Danish)". ⓘ og kortet vises ikke ved udskrift.
7. **Kun på trænerne** (Franks valg): Træn-siden får ingen ⓘ.
8. **Én kilde:** `assets/konventionskort-hint.js` genereres af `build_konventionskort.py`. Den bruger de samme visningsfunktioner i `konventionskort.src.html` som siden (fra `KATEGORI` til `vaelg`) og den nye skal `tools/konventionskort-hint-shell.js`. Kortet ligger i shadow DOM som på siden. Ret aldrig i hint-filen direkte.
9. **Engelsk:** kortene findes kun på dansk. På engelsk hedder knappen "About the convention (in Danish)", og øverst i kortet står "The convention card is in Danish.".
10. **Linjeskift:** `build_konventionskort.py` skriver med LF (`newline='\n'`), så siden bliver byte for byte som leverancen, også på Windows. Før gav Windows CRLF (Claude Codes fund ved trin 3).
11. **Centreret tekst i kompaktvisningen:** kildens regel `.ramme p` er ment for noten under kortet, men rammer også kortets egne afsnit. Derfor står undertitel, situation og kort fortalt centreret i en smal spalte. Rettet i kilden til `.ramme > p` og i artifactet (Franks valg, 17. oktober 2026), så siden og ⓘ viser det samme. Fra nu af er siden ikke længere byte for byte som leverancen; forskellen er kun denne regel (Claude Codes fund).
12. **Feltet på Viden** står øverst under overskriften "Alle konventioner" / "All conventions" med mærket "Opslag" / "Reference · in Danish". Siden SPEC-traen-side, Afklaret 26, står makkerskabernes systemer ikke længere på Viden, så "over systemerne" i trin 4 betyder øverst.
13. **Knappen står inde i overskriften**, så den følger titlen på alle skærmbredder. Overskriftens tekst (`textContent`) indeholder derfor også "i". Skriver variantvælgeren i `traener.html` titlen om, sætter komponenten knappen ind igen.

De øvrige kort – Franks svar (17. oktober 2026):

14. **Ét kort pr. træner** (Franks valg): kortet har trænerens `id`, også når samme konvention trænes i begge makkerskaber (fx `michaels` og `ff-michaels`). Kortets tekst nævner ikke makkerskabet; `id` er kun en nøgle.
15. **Ét emne ad gangen** (Franks valg): hvert emne skrives på sin egen gren (`kort-<emne>`), og Frank læser kortene igennem, før de flettes ind. Rækkefølgen begynder med Svar på 1NT. Trænerne fra Kampen om kontrakten får også kort, men til sidst (Franks valg).
16. **Kilder:** kortet skrives ud fra systemdokumentet, som træneren henviser til (feltet `viden` i `data/konventioner.json`), og ud fra trænerens pulje. Eksemplerne er hænder fra puljen med samme meldeforløb og samme svar. Tal, som hverken dokumentet eller puljen angiver, skrives ikke ind. Fx har overføringernes udgangsmeldinger ingen pointgrænse, fordi kilden kun siger "udgang".
17. **Svar på 1NT** (5 kort): `stayman`, `transfer`, `ff-ass`, `ff-overfoeringer` og `ff-gerber`. Bridgesystemet angiver ikke farvelængden ved transfer. "5+" i major og "6+" i minor svarer til trænerens hænder (5–6 og 6–7 kort) og til det andet systemdokument. Staymans 3NT med "10+ hp" følger af, at 2NT er 8–9 hp. Afsnit 3 bygger på Bridgesystem 8.3–8.4 og på 11a–11b i det andet dokument.
18. **Svar på 1NT er godkendt og flettet ind** (Frank, 17. oktober 2026).
19. **Modspil: Markeringer** (1 kort, `markeringer`, Afklaret 4): kortet er bygget ud fra Bridgesystem 9.1–9.2 og puljen. Grupperne følger systemets tabel: makker spiller ud eller skifter farve (kald), konge-udspil (antal), spilførers nye farve (Malmø) og første afkast mod farve og sans. De seks eksempler er kopieret uændret fra puljens opgaver, hvor du giver markeringen. Lavinthal står under Åbne spørgsmål, fordi den kan erstatte kald og antal i bestemte situationer.
20. **Puljefund (ikke rettet):** i 8 af 22 opgaver om første afkast mod sans i `pools/markeringer.json` mangler det laveste kort i afkastfarven både i `valg` og i forklaringen. Fx har hånd 182 ♥B632, men kortrækken og forklaringen viser ♥ B 6 3. Hånden står derfor med 12 kort. Bedømmelsen er rigtig, så det er en skønhedsfejl. Den rettes kun efter aftale med Frank.
21. **Markeringer er godkendt og flettet ind** (Frank, 17. oktober 2026). Puljefundet i punkt 20 er ikke rettet.
22. **Slem** (3 kort: `cuebids`, `1430`, `ff-1430`): Bridgesystemet angiver ikke svarene på 4NT. De står på 1430-kortet efter puljen (5♣ 1/4, 5♦ 0/3, 5♥/5♠ 2 uden/med dame), og kf-puljen har ingen hænder med 5 nøglekort. RKC-kortet har "2 eller 5" og kongespørgsmålets svar efter det andet dokument. Cuebids følger dokumentets regler; grænsen på 17 sp for slemambition over åbners tillæg står i puljen. Afsnit 3 (indmelding) er tomt på alle tre kort, fordi kilderne ikke beskriver det. 1430 og RKC 1430 er samme konvention og står derfor under "Spiller sammen med".
23. **Slem er godkendt og flettet ind** (Frank, 17. oktober 2026).
24. **Støtte** (5 kort: `omvendt-bergen`, `bekkasin`, `ff-revideret-omvendt-bergen`, `ff-trial-bids`, `ff-omvendt-minor`). Kilderne er uenige fire steder. Kortene følger trænerne og nævner uenigheden under Åbne spørgsmål, hvor det er relevant:
    - Bekkasin efter modpartens dobling: Bridgesystem 8.4 siger "gælder fortsat", det andet dokument siger "slået fra" og bruger Jordan 2NT.
    - Trial bids: skemaet og træneren regner 4 små kort som hjælp; dokumentets eksempel siger, at x-x-x-x uden honnør giver for mange tabere. Styrken for trial bid er 15–17 sp i dokumentet og 14–16 sp i træneren (4M direkte med 17+).
    - Omvendt Bergen: trænerens beskrivelse i `data/konventioner.json` siger "25-reglen", men puljen regner med 26. Kortet bruger 26.
    - Bonusspørgsmålene i tre puljer (`ff-omvendt-minor`, `ff-revideret-omvendt-bergen`, `ff-two-over-one`) nævner makkerskaberne, fx "hos Makker 2 & mig". Ikke rettet.
25. **Franks afgørelser om Støtte** (17. oktober 2026). Godkendt med disse rettelser:
    - **Bekkasin efter dobling:** Bridgesystemets regel gælder: Bekkasin gælder fortsat. Det andet systemdokument er rettet i afsnit 2 og i oversigten over indblanding; Jordan 2NT og noten "(Forslag — ikke afprøvet)" i samme afsnit er fjernet. Kortet viser reglen under afsnit 3.
    - **Trial bids:** 4 små kort uden honnør er ikke hjælp, som i dokumentets eksempel. Hjælp er honnør (E, K, D) eller korthed. Skemaet i afsnit 3, puljen (26 hænder ændret til 3M og bonusteksten) og kortet er rettet.
    - **Trial bids:** styrken er 15–17 sp. Med 17 sp og en svag sidefarve meldes trial bid (3 hænder ændret); 4M direkte er 18+ eller 17 uden svag sidefarve.
    - **Omvendt Bergen bruger 25-reglen:** udgang, når parret har mindst 25 støttepoint. Puljen er beregnet på ny (83 hænder fik nyt svar, 20 hænder med 18 sp efter makkers minimum er fjernet, fordi åbner da melder 4♠ direkte), og forklaringerne og bonusteksten siger "25-reglen". Kortet viser grænserne: efter 3♣ afmeld højst 13, spørg med 14, udgang med 15+; efter 1♠ – 3♦ afmeld højst 14, spørg 15–17, udgang 18+; efter 1♥ – 3♦ 4♥ med 16+.
26. **Støtte er godkendt og flettet ind** med rettelserne i punkt 25 (Frank, 17. oktober 2026).
27. **Videre meldeforløb** (6 kort: `xy-sans`, `fjerde-farve`, `ff-two-over-one`, `ff-fast-arrival`, `ff-staerke-genmeldinger`, `ff-revers`). Steder, hvor kilden selv siger, at noget ikke er afgjort, står neutralt under Åbne spørgsmål: XYZ efter ny farve på 1-trinnet, fjerde farve efter revers, og om ny højere farve på 2-trinnet er naturlig (12–18, ikke krav) eller revers (16+, rundekrav). Revers-kortet beskriver bilag G uden at kalde det et forslag. Puljetekster, der stadig nævner status eller makkerskab, er ikke rettet: `ff-staerke-genmeldinger` ("foreløbig – bekræftes"), `ff-revers` ("i forslaget") og `ff-two-over-one` ("hos Makker 2 & mig").
28. **Videre meldeforløb er flettet ind**, og resten laves på grenen `kort-resten` med én commit pr. emne (Frank: "fortsæt med resten", 17. oktober 2026). Grenen flettes først ind, når Frank har gennemset den.
29. **Åbninger** (4 kort: `ff-2kl`, `ff-ogust`, `ff-flannery`, `forslag-2kl-kontrolsvar`). `ff-multi-2ru` og `ff-muiderberg` har status "kommer" og ingen træner endnu, så de har intet kort. Ogust: kilden nævner 1-2-3-reglen for videre spærring, træneren bruger Loven (3 med 9 trumf, 4 med 10) – kortet følger træneren og nævner forskellen under Åbne spørgsmål. 2♣ waiting og 2♣ med kontrolsvar står som "Ikke at forveksle med" på hinanden. `tools/tjek_kort_eksempler.py` springer nu tal efter "under", "over", "mindst" og "højst" over, fordi de er grænser og ikke håndens point.
30. **Indmeldinger** (4 kort: `michaels`, `usaedvanlig-2nt`, `ff-michaels`, `ff-genaabning`). De to systemer har lidt forskellige tal, og hvert kort følger sin egen kilde: svarers cuebid er 10+ på `michaels`/`usaedvanlig-2nt` og 11+ på `ff-michaels`. **Rettet fejl i puljen** `ff-genaabning`: i situationerne `gen_hj` og `gen_sp` stod makkers pas som "Modstander", så træneren viste modstanderen to gange i træk. Rollen er rettet til "Makker"; svarene er uændrede. Ingen andre puljer har meldeforløb, hvor samme side melder to gange i træk.
31. **Doblinger og 1NT i konkurrence** (5 kort: `lebensohl`, `ff-lebensohl`, `ff-doblinger`, `ff-kravpas`, `ff-dont`). De to Lebensohl-kort følger hver sin kilde (invit 9–12 hp mod 8–11 hp, og cuebid udgangskrav kun i den ene). **Uafklaret:** afsnit 17 og træneren `ff-doblinger` lader 2NT efter modpartens dobling af vores 1M vise 10+ sp med støtte (trænerens beskrivelse kalder den Jordan 2NT). Det strider mod punkt 25, hvor Bekkasin gælder fortsat ved dobling (13+ sp, 4+ trumf). Kortet følger træneren og nævner konflikten under Åbne spørgsmål; dokument og pulje er ikke rettet, før Frank har afgjort det. Konkurrencedoblingens intervaller er markeret som ikke fastlagt i kilden og står også under Åbne spørgsmål.
32. **Kampen om kontrakten** (10 kort: `kamp-forsvar-1ut`, `kamp-stoette-def`, `kamp-stoette-off`, `kamp-stoette-minor`, `kamp-efter-od`, `kamp-gif`, `kamp-2020`, `kamp-doblinger`, `kamp-1ut-indmeldt`, `kamp-1ut-forsvar`). Kilden er `docs/kampen-om-kontrakten.md`. Dokumentets markering "(aftale)" er udeladt; hvor dokumentet siger, at bogen siger noget andet eller intet, står det under Åbne spørgsmål. Profilen Turnering (Stenberg 2NT og Lebensohl) er nævnt ved de meldinger, den ændrer. `kamp-forsvar-1ut` har ingen egen pulje, fordi træneren vælger mellem Landy, DONT og Multiforsvar; kortet beskriver Landy, henter eksemplerne fra `pools/kamp-landy.json` og henviser til DONT- og Multiforsvar-kortene. `kamp-landy` står ikke på Træn (intet system) og har derfor intet kort.
33. **Alle trænere på Træn har nu et konventionskort** (48 kort i alt, heraf 5 fra leverancen). Kun `ff-multi-2ru` og `ff-muiderberg` (status "kommer") mangler, fordi de ikke har en træner endnu.
34. **Franks afgørelser** (18. oktober 2026), godkendt med `kort-resten`:
    - **2NT efter modpartens dobling af vores åbning** er Truscott: 10+ sp med støtte. Afsnit 17 er rettet fra "Bekkasin" til "(Truscott)"; træneren er uændret. Doblinger-kortet siger det samme, og det åbne spørgsmål i punkt 31 er lukket.
    - **Ogust og svage åbninger:** videre spærring følger Loven (3 i farven med 9 trumf, 4 med 10). Afsnit 12 er rettet, også i linjen om svag 4/5 ("Videre spærring efter Loven: antal trumf tilsammen = antal stik"), og bilag B3 siger nu "Svag 2 med Ogust og Loven fungerer". Ogust-kortet er rettet.
    - **Neutrale trænertekster:** "hos Makker 2 & mig", "hos Makker 1 & mig" og "i forslaget" er fjernet fra bonusspørgsmål og forklaringer i `ff-two-over-one`, `ff-omvendt-minor`, `ff-revideret-omvendt-bergen` og `ff-revers` (dansk og engelsk). Om noget er et forslag, fremgår kun af feltet `system` i `data/konventioner.json`; Revers står fortsat som forslag dér.
    - **"foreløbig – bekræftes"** fjernes først, når Frank har set listen over stederne (data/konventioner.json, pools/ff-staerke-genmeldinger.json, viden/2-over-1-makker2.html og design/tegneflade/Main.dc.html).
35. **Åbent:** Frank har skrevet, at Bekkasin (13+ sp, 4 trumf) kun gælder uden indblanding. Det strider mod punkt 25, hvor Bekkasin gælder fortsat ved dobling: Bekkasin-kortet, afsnit 2 i det andet systemdokument og Bridgesystem 8.4 siger det. Ikke rettet, før Frank har afgjort det.

36. **Bekkasin gælder fortsat efter dobling** (Franks afgørelse, 18. oktober 2026). Afløser første punkt i punkt 34 og lukker punkt 35. Bekkasin-kortet, afsnit 2 i det andet systemdokument og Bridgesystem 8.4 gælder: 1M – (X) – 2NT er Bekkasin (13+ sp, 4+ trumf). Afsnit 17 er rettet tilbage fra "(Truscott)" til Bekkasin. Træneren `ff-doblinger` (redobling med 3 trumf og 10+ hp, 2NT kun med 4+ trumf og 13+ sp), dens beskrivelse ("Jordan 2NT" → "Bekkasin 2NT") og kortet er rettet; kortet har nye eksempler fra den nye pulje, og 10–12 sp med 4+ trumf efter dobling står under Åbne spørgsmål. Truscott findes kun som selvstændig træner, se `SPEC-truscott-traener.md`.
37. **"foreløbig – bekræftes" står fortsat** (Franks afgørelse, 18. oktober 2026). Aftalen om åbners nye højere farve på 2-trinnet (naturlig, 5-4, 12–18 hp, ikke krav) er ikke bekræftet; Frank afklarer den med Makker 2. Markeringen står alle steder på listen: 9 linjer i det andet systemdokument, beskrivelsen i `data/konventioner.json`, `dealer/ff_genmeld.py` og puljen `ff-staerke-genmeldinger` samt tegnefladen, og spørgsmålet i C1 er åbent. C1 nævner nu hullet: 12–18 ikke krav sammen med spring i ny farve fra 19+ efterlader 16–18 hp med 5-4 uden en krav-melding. Valget står mellem revers (16+ og rundekrav, Bilag G) og naturlig 12–15 ikke krav med en ændret springgrænse.
