# SPEC-modspilsaftaler

26. november 2026 · Rådgiverens spec, **godkendt af Frank 26. nov.** Opgave B i `PLAN-aabne-opgaver.md`. Bygges i Konventionstræner på grenen `modspilsaftaler`; `main` før tagges `v-foer-modspilsaftaler`.

## Formål

Modspilsaftalerne bliver konventionskort uden makker: hver aftale beskrives med alle de varianter, Modspil i Fordelingstræneren træner, og brugeren vælger sine varianter i en indstilling. Kortene, eksemplerne og quizzen følger valget. Der er intet overlap med Modspil (Franks valg 24. nov.): kortene beskriver aftalerne, og quizzen spørger kun til aftalernes indhold, ikke til aflæsning eller valg af kort. Hvert kort har linket "Træn i Modspil" til `/fordelingstraeneren/#modspil`.

## Beslutninger (26. nov.)

1. **Varianterne vælges i indstillingerne** (Franks ønske 26. nov.).
2. **Alle Modspils varianter kommer med.** Facit findes allerede: `Fordelingstræneren/src/modspil/content/metoder.json` har 7 kategorier med i alt 17 metoder og tre profiler. Specen tilføjer ingen variant, som ikke står dér.
3. **Indstillingen er den samme som Modspils profiler** (rådgiverens anbefaling, fulgt af Frank 26. nov.): profilerne Standard, Omvendt og Kompendiet plus "egen", hvor hver kategori vælges for sig, med de samme id'er og navne som i Modspil.
4. **Ét fælles valg for begge apper** (Franks valg 26. nov.): et skift i Konventionstræner ændrer også valget i Modspil (se Indstillingen).

5. **Quizzen og indstillingen får sin egen side** `modspilsaftaler.html` (Franks valg 26. nov., session 2), som Markeringer har `markering.html`; `traener.html` ændres ikke.
6. **De tre udspilskort beholdes** (Franks valg 26. nov., session 2): ét kort pr. kategori som i Modspil, selv om skabelonen samler udspilsaftaler på ét kort.

Rådgiverens anbefaling om at dele B i B1 og B2 er trukket tilbage: med `metoder.json` som facit er alle 17 metoder ikke meget mere arbejde end de 6, der var tænkt til B1. Opgaven deles i stedet i sessioner (se Trin).

## Kilderne

- **Facit:** `metoder.json` (kategorier, metoder, `aftale`/`aftaleEn` og profiler). Teksterne derfra bruges ordret som kortets regel for metoden.
- **Kompendium over modspilsaftaler** (`C:\Users\frank\Kontraktbridge\Kompendium over modspilsaftaler.pdf`, ikke i repoet) til forklaringer, formål og faldgruber. Siderne står i `metoder.json` (romersk kald s. 25–26, O/E s. 24, omvendt forsinket kald s. 26).
- **ALA-tabellen** (planens beslutning 2) står allerede i `metoder.json` under `ala-mod-sans`.
- Står der intet i kilderne, er teksten agentens og markeres "(tilføjelse)".

## Kategorierne og kortene

Ét nyt kort pr. kategori, `type: "modspil"`, `system: "generel"`, id'et `ms-<kategori>`:

| Kort | Kategori i `metoder.json` | Metoder |
| --- | --- | --- |
| `ms-udspil-sans` | Udspil mod sans, lavt kort | 4.-højeste · 3. og 5. højeste · Kompendiets udspil |
| `ms-udspil-farve` | Udspil mod farve, lavt kort | 4.-højeste · 3. og 5. højeste |
| `ms-honnoerudspil` | Honnørudspil | top af sekvens · ALA mod sans |
| `ms-kald` | Kald eller afvisning på makkers udspil | højt = kald · lavt = kald · romersk kald |
| `ms-laengde` | Længdemarkering | højt-lavt = lige · lavt-højt = lige |
| `ms-afkast` | Første afkast | som kald eller afvisning · O/E · Lavinthal |
| `ms-forsinket` | Forsinket kald i spilførers første farve | intet forsinket kald · omvendt forsinket kald |

Hvert kort har:

1. **Formål og situation:** hvornår aftalen gælder (mod sans, mod farve, hvilken modspiller).
2. **Metoderne:** én blok pr. metode med navnet, reglen fra `aftale` og kilden. Den valgte metode står øverst og er mærket "Din aftale"; de andre står under "Andre varianter".
3. **Eksempler:** for hver metode 1–2 farver med det kort, metoden giver, fx "8 6 3 2 → 2 (lavt = kald)". Eksemplerne viser kun, hvad aftalen siger; de spørger ikke brugeren.
4. **Faldgruber** fra Kompendiet, fx at romersk kald mod sans falder tilbage til lavt = kald.
5. **Relaterede:** de eksisterende kort `markeringer`, `udspil` og `lavinthal` (Bridgesystem). `ms-afkast` henviser til `lavinthal` i stedet for at gentage det.
6. **Linket "Træn i Modspil"** til `/fordelingstraeneren/#modspil`.

De eksisterende kort `markeringer`, `udspil` og `lavinthal` følger Bridgesystem og ændres ikke.

## Indstillingen

- **Fælles med Modspil:** Konventionstræner og Fordelingstræneren ligger på samme domæne og deler derfor `localStorage`. Konventionstræner læser Modspils nøgle `modspil:v1` (felterne `profil` og `metoder`).
- **Skrivning:** ændrer brugeren valget i Konventionstræner, skrives kun `profil` og `metoder`; alle andre felter i `modspil:v1` (niveau, svarlog, Leitner-poster osv.) bevares tegn for tegn. Kan den gemte tilstand ikke læses som gyldig JSON med de to felter, skriver Konventionstræner ikke, men viser valget som Standard og en kort note.
- **Uden gemt tilstand:** profilen Standard, som i Modspil.
- **Placering:** en indstilling "Modspilsaftaler" med profilvalget og under den et valg pr. kategori. Vælges en anden metode end profilens, bliver profilen "egen".

**Ét fælles valg** (Franks valg 26. nov., (a)): Konventionstræner læser og skriver Modspils valg som beskrevet ovenfor. Alternativet, et eget valg under en egen nøgle, er fravalgt, fordi de to apper så kunne vise forskellige aftaler.

## Quizzen

- 2 spørgsmål pr. metode (34 i alt) med det rigtige svar, to forkerte og en forklaring, på dansk og engelsk.
- Spørgsmålene handler kun om aftalens indhold, fx "Hvad betyder en lille lige ved romersk kald?" De viser ingen hånd og beder ikke brugeren vælge kort.
- Quizzen bruger de valgte metoder; et valg "Alle varianter" tager alle 34.
- De forkerte svar er Claude Codes og ikke påstande om aftalen (som bonusspørgsmålene i Muiderberg).
- Afklaret i session 1: quizzen og indstillingen har egen side, modspilsaftaler.html (Beslutning 5); traener.html ændres ikke.

## Afgrænsning

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `data/modspilsaftaler.json` (ny) | En kopi af `metoder.json` (kategorier, metoder, profiler). | Rettes i hånden uden at rette `metoder.json` først. |
| `data/kort/ms-*.json` (7 nye), `data/kort/index.json` | De nye kort efter skabelonen. | Tal eller regler, som ikke står i kilderne. |
| `data/konventioner.json` | 7 nye poster (`system: "generel"`, gruppen Modspil). | Ændre de øvrige poster. |
| Indstillingen og quizzen (filerne vælges i session 1) | Som beskrevet ovenfor. | Andre indstillinger. |
| `viden/konventionskort.html`, `assets/konventionskort-hint.js` | Bygges med `python3 tools/build_konventionskort.py`. | Rettes i hånden. |
| `tools/tjek_modspilsaftaler.py` (ny) | Accepttesten. | — |
| `tools/tjek_viden_320.mjs`, `tools/tjek_crowhurst_390.mjs` | Tallet for kortene rettes fra 51 til 58, og de nye kort tjekkes kun for vandret scroll. Siden før henter `data/kort/index.json` fra commit H (den sidste commit i session 1, der ændrer den). H står i `NYERE` og under Afklaret. | Andre ændringer. Senere sessioner må ikke ændre de filer. |
| `data/kort/markeringer.json`, `udspil.json`, `lavinthal.json` | Intet. | Alt. |
| `../Fordelingstræneren` | Kun læsning (`metoder.json` og modellen til kontrol af eksempler). | Ændringer. |
| `../SYSTEM.md` (ikke i git) | En linje i beslutningsloggen pr. session og datoen øverst. | Hemmeligheder. |
| Sprog | `tx('dansk', 'English')`, husets ord, beskrivende form. | Dansk tekst på den engelske side. |

## Accepttest

`python3 tools/tjek_modspilsaftaler.py` skrives først og skal være rød. Den tjekker:

1. `data/modspilsaftaler.json` er indholdsmæssigt lig `../Fordelingstræneren/src/modspil/content/metoder.json` (kategorier, metoder, `aftale`/`aftaleEn` og profiler).
2. Der er 7 kort `ms-*`, ét pr. kategori, og hvert kort har alle kategoriens metoder med reglen ordret fra `aftale` (dansk) og `aftaleEn` (engelsk).
3. Hvert kort har linket til `/fordelingstraeneren/#modspil` og henviser til `markeringer`, `udspil` eller `lavinthal`, hvor det passer.
4. Hver metode har 2 quizspørgsmål med ét rigtigt og to forkerte svar og en forklaring på begge sprog; ingen spørgsmål har en hånd.
5. Eksemplerne giver det kort, metoden giver. Hvor modellen i `../Fordelingstræneren/src/modspil/model` kan kaldes for farven, kontrolleres de mod den; de øvrige står som "(tilføjelse)" i "Tekster til gennemgang".
6. Indstillingen: uden gemt tilstand vises Standard; et valg skriver kun `profil` og `metoder` i `modspil:v1` og bevarer resten; ugyldige data overskrives ikke (testet med en fil med Modspil-tilstand, svarlog og Leitner-poster).
7. Kortene viser den valgte metode øverst som "Din aftale", og quizzen tager kun de valgte metoders spørgsmål (og alle 34 ved "Alle varianter").
8. `tjek_konventionskort.py`, `tjek_kort_eksempler.py`, `tjek_fagord.py`, `tjek_bydeform.py` og `tjek_sprog.py` melder "i orden"; stavekontrollen har ingen nye fejl.
9. Tabellen "Tekster til gennemgang" findes under Afklaret og har en kilde i hver række (metoder.json, Kompendiet med side, eller "(tilføjelse)").

Desuden åbnes kortsiden og quizzen på dansk og engelsk ved 1280, 390 og 320 px. Skærmbillederne gemmes i `C:\Users\frank\Kontraktbridge\skaermbilleder\modspilsaftaler\` og skal vise:
- `ms-kald` med romersk kald som "Din aftale";
- indstillingen med profilen "egen";
- et quizspørgsmål med forklaring;
- 320 px uden vandret scroll.

## Trin

Tre korte sessioner (Styring, punkt 7–11). Frank sender `/usage` (5 timer og uge) før og efter hver session.

1. **Session 1 (Opus, high effort):** tag og gren; accepttesten (rød); kopien af `metoder.json`; de 7 kort med eksempler; posterne; byg kortsiden. Stop med H og et kig på, hvordan `traener.html` kan vise spørgsmål uden hånd.
2. **Session 2 (Opus, high effort):** indstillingen, quizzen og linket; testen grøn; tabellen "Tekster til gennemgang". Stop og rapportér.
3. **Session 3 (Sonnet, medium effort):** hele testsuiten én gang i forgrunden og skærmbillederne. Stop før fletning, og rapportér med tokenforbruget.

Efter Franks "godkendt" (Sonnet, medium effort): flet, push, live-tjek (`tjek_sidefod.mjs --live`, `tjek_viden_320.mjs --live`), arkivér specen i `docs/specs/` med en linje i `README.md`, og slet grenen.

## Afklaret

(Udfyldes af Claude Code. Tokenforbruget i fire tal pr. session: nye input, skrevet til cachen, læst fra cachen og output.)

### Session 1 (26. nov. 2026)

Kørt i rådgiverchatten på Franks ønske (Opus 5.5) via skallen på Franks computer, ikke i Claude Code. Grenen `modspilsaftaler`, tagget `v-foer-modspilsaftaler` på `aeecc28`.

1. **Accepttesten** `tools/tjek_modspilsaftaler.py` blev skrevet først og var rød med 28 fejl (`8e47b40`). Punkt 5 kontrollerer udspilseksemplerne mod Fordelingstrænerens model med `tools/kontrol_modspilsaftaler.mjs`; Node 22 fjerner selv typerne, og `tools/ts-hooks.mjs` giver importerne uden endelse `.ts` og indlæser JSON. Fordelingstræneren læses kun.
2. **Kopien** `data/modspilsaftaler.json` er en byte-kopi af `metoder.json`. Punkt 1 sammenligner kategorier og profiler.
3. **Kortene** (`a1b7cb4` = H): 7 kort `ms-<kategori>`, `type` og `kategori` modspil. Skabelonen og skemaet er uændrede: hver metode er en mellemoverskrift i Kortene med rækken "Aftalen" (aftalen ordret fra `metoder.json`) og metodens eksempler som rækker (holding → kort). Afsnittet Eksempler (fuld hånd) er tomt, fordi specens eksempler er farver og ikke hænder. Kortene er på dansk som alle andre kort; den engelske aftale bruges i indstillingen og quizzen (session 2). Skriptet, der skriver kortene, ligger i `_lab\modspilsaftaler\lav_kort.py` (uden for repoet).
4. **Skabelonen siger** "Udspilsaftaler samles på ét kort, `udspil`". De tre udspilskort `ms-udspil-sans`, `ms-udspil-farve` og `ms-honnoerudspil` følger specen i stedet (ét kort pr. kategori); `udspil` (Bridgesystem) er uændret. Hvis Frank vil holde skabelonens regel, kan de tre slås sammen til ét kort `ms-udspil` i session 2.
5. **Posterne** i `data/konventioner.json`: 7 poster efter `lavinthal`, gruppen Modspil, `system: "generel"`, `status: "klar"`; filen er ellers byte for byte som før. Posterne har endnu ingen træner, så `traener.html?k=ms-…` virker først efter session 2.
6. **Pixeltestene** `tjek_viden_320.mjs` og `tjek_crowhurst_390.mjs` (`d52114b`): 58 kort, de 7 kort `ms-*` står i `NYE_KORT` og tjekkes kun for vandret scroll, og siden før henter `data/kort/index.json` og de 7 kort fra H = `a1b7cb4`. Testene kræver Chrome og er ikke kørt her (session 3).
7. **Quizzen kan ikke ligge i `traener.html`:** træneren bygger hver runde af hænder fra `pools/<id>.json` med en melding og et bonusspørgsmål til hver hånd, så et spørgsmål uden hånd kræver en ny tilstand i hele træneren. Forslag til session 2: en lille side `modspilsaftaler.html` (quiz og indstilling), og posterne får `"side": "modspilsaftaler.html?k=ms-…"` som `markeringer` og `lavinthal` (`markering.html`). Spørgsmålene ligger i `data/modspilsaftaler-quiz.json`, og logikken i `assets/modspilsaftaler.js`, så den kan testes med `node --test`.
8. **Status efter session 1:** `python3 tools/tjek_modspilsaftaler.py` har punkt 1, 2, 5 og 8 i orden; punkt 3 (linket "Træn i Modspil"), 4 (quizzen), 6–7 (indstillingen og "Din aftale") hører til session 2, og punkt 9 bliver grønt med tabellen nedenfor. `tjek_konventionskort.py` (58 kort), `tjek_kort_eksempler.py`, `tjek_fagord.py`, `tjek_bydeform.py` og `tjek_sprog.py` er i orden.
9. **Tokenforbrug:** sessionen kørte i rådgiverchatten, så de fire tal fra Claude Code findes ikke. Frank kan tage `/usage` (5 timer og uge), når han er ved pc'en.

#### Tekster til gennemgang

Alle kortenes tekster ud over aftalerne (som er ordret fra `metoder.json`). Eksemplerne til udspil er kontrolleret mod modellen; de øvrige eksempler og "(tilføjelse)" er rådgiverens og skal godkendes af Frank.

| Kort | Felt | Tekst | Kilde |
| --- | --- | --- | --- |
| `ms-udspil-sans` | Formål | At vise makker farvens længde og om der er en honnør, så makker kan regne farven ud. | (tilføjelse) |
| `ms-udspil-sans` | Situation | Første udspil mod en sanskontrakt fra en farve uden honnørsekvens. · Udspil mod sans, lavt kort | (tilføjelse) |
| `ms-udspil-sans` | Eksempel (4.-højeste) | K 9 6 3 2 → 3 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-sans` | Eksempel (4.-højeste) | 8 6 3 2 → 2 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-sans` | Eksempel (3. og 5. højeste) | K 9 6 3 2 → 2 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-sans` | Eksempel (3. og 5. højeste) | K 9 6 3 → 6 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-sans` | Eksempel (Kompendiets udspil) | K 9 6 3 2 → 3 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-sans` | Eksempel (Kompendiets udspil) | 8 6 3 2 → 6 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-sans` | Forrang og undtagelser | Honnørsekvens: Honnørudspillet følger kortet Honnørudspil, ikke reglen for det lave kort. | (tilføjelse) |
| `ms-udspil-sans` | Forrang og undtagelser | Doubleton: Fra doubleton spilles det højeste kort. | Kompendiet s. 23 |
| `ms-udspil-sans` | Faldgrube | Med Kompendiets udspil viser et lavt kort ikke altid en honnør: fra fire småkort spilles det næsthøjeste. | metoder.json (Kompendiets udspil); Kompendiet s. 23 |
| `ms-udspil-farve` | Formål | At vise makker farvens længde, så makker kan regne ud, hvor mange stik farven kan give. | (tilføjelse) |
| `ms-udspil-farve` | Situation | Første udspil mod en farvekontrakt fra en farve uden honnørsekvens. · Udspil mod farve, lavt kort | (tilføjelse) |
| `ms-udspil-farve` | Eksempel (4.-højeste) | D 9 6 3 2 → 3 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-farve` | Eksempel (4.-højeste) | 9 6 3 → 9 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-farve` | Eksempel (3. og 5. højeste) | D 9 6 3 2 → 2 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-farve` | Eksempel (3. og 5. højeste) | D 9 6 3 → 6 | modellen i Fordelingstræneren (accepttest 5) |
| `ms-udspil-farve` | Forrang og undtagelser | Honnørsekvens: Mod farve spilles toppen af sekvensen (kortet Honnørudspil). | metoder.json (top af sekvens) |
| `ms-udspil-farve` | Forrang og undtagelser | Doubleton: Fra doubleton spilles det højeste kort. | (tilføjelse) |
| `ms-udspil-farve` | Faldgrube | Med 3. og 5. højeste kan et højt kort fra tre kort ligne en doubleton. | (tilføjelse) |
| `ms-honnoerudspil` | Formål | At vise makker sekvensen og bede om den markering, der hjælper mest. | (tilføjelse) |
| `ms-honnoerudspil` | Situation | Første udspil fra en farve med en honnørsekvens. · Honnørudspil mod sans og farve | (tilføjelse) |
| `ms-honnoerudspil` | Eksempel (top af sekvens) | Mod farve: E K 7 5 → E | modellen i Fordelingstræneren (accepttest 5) |
| `ms-honnoerudspil` | Eksempel (top af sekvens) | Mod sans: K D B 4 → K | modellen i Fordelingstræneren (accepttest 5) |
| `ms-honnoerudspil` | Eksempel (ALA mod sans) | Mod sans: E K 7 5 3 → K | modellen i Fordelingstræneren (accepttest 5) |
| `ms-honnoerudspil` | Eksempel (ALA mod sans) | Mod sans: K D 7 5 → D | modellen i Fordelingstræneren (accepttest 5) |
| `ms-honnoerudspil` | Eksempel (ALA mod sans) | Mod farve: E K 7 5 3 → E | modellen i Fordelingstræneren (accepttest 5) |
| `ms-honnoerudspil` | Makkers læsning | Makker efter ALA-udspil mod sans: Es eller dame = Kald eller afvisning; Konge = Længdemarkering | Kompendiet s. 24 (ALA) |
| `ms-honnoerudspil` | Forrang og undtagelser | ALA mod farve: Mod farve spilles toppen af sekvensen; Kompendiet bruger romersk kald mod farve og derfor ikke ALA. | Kompendiet s. 24 |
| `ms-honnoerudspil` | Forrang og undtagelser | To honnørkort i træk med små kort mod sans: Med top af sekvens afgør "table feeling", om honnøren eller det lave kort spilles. | metoder.json (top af sekvens); Kompendiet s. 23 |
| `ms-honnoerudspil` | Faldgrube | Med ALA beder kongen om længdemarkering og ikke om kald: E K x x x(+) spilles ud med kongen. | metoder.json (ALA-tabellen) |
| `ms-kald` | Formål | At fortælle udspilleren, om udspilsfarven skal fortsættes. | (tilføjelse) |
| `ms-kald` | Situation | Makker spiller ud, og du lægger til. · Tilspil på makkers udspil | (tilføjelse) |
| `ms-kald` | Eksempel (højt = kald) | Makker spiller E ud; du har D 8 3 → 8 (kald) | (tilføjelse) |
| `ms-kald` | Eksempel (højt = kald) | Makker spiller E ud; du har 8 6 3 → 3 (afvisning) | (tilføjelse) |
| `ms-kald` | Eksempel (lavt = kald) | Makker spiller E ud; du har D 8 3 → 3 (kald) | (tilføjelse) |
| `ms-kald` | Eksempel (lavt = kald) | Makker spiller E ud; du har 8 6 3 → 8 (afvisning) | (tilføjelse) |
| `ms-kald` | Eksempel (romersk kald) | Mod farve; du har D 7 3 → 3 (mindste ulige: kald) | (tilføjelse) |
| `ms-kald` | Eksempel (romersk kald) | Mod farve; du har 8 6 3 → 6 (lille lige: skift til den laveste af de to andre farver) | (tilføjelse) |
| `ms-kald` | Eksempel (romersk kald) | Mod farve; du har 8 6 3 → 8 (høj lige: skift til den højeste af de to andre farver) | (tilføjelse) |
| `ms-kald` | Makkers læsning | Udspilleren læser et romersk kald: Ulige kort = Kald til udspilsfarven; Lille lige = Skift til den laveste af de to andre farver; Høj lige = Skift til den højeste af de to andre farver. Trumf tæller ikke med. En lav lige er sædvanligvis et af de to laveste lige kort, udspilleren ikke kan se. | Kompendiet s. 25–26 |
| `ms-kald` | Forrang og undtagelser | Romersk kald mod sans: Mod sans gælder lavt = kald. | metoder.json (romersk kald) |
| `ms-kald` | Forrang og undtagelser | Romersk kald, når et kort stikkes: Romersk kald gælder kun, når hverken udspillets kort eller bordets kort stikkes. | metoder.json; Kompendiet s. 25 |
| `ms-kald` | Forrang og undtagelser | Romersk kald uden lige kort: En høj ulige (9 og op) kan vise ønske om skift. | metoder.json; Kompendiet s. 25 |
| `ms-kald` | Faldgrube | Tolkningen af et romersk kald må ikke erstatte sund fornuft: makkers kort kan være en singleton, og makker kan have kun lige eller kun ulige kort. | Kompendiet s. 25–26 |
| `ms-kald` | Faldgrube | Jo længere udspilsfarven er, og jo flere kort bordet har i den, jo færre muligheder har makker for at vise det ønskede. | Kompendiet s. 25 |
| `ms-laengde` | Formål | At fortælle makker, hvor mange kort du har i farven. | (tilføjelse) |
| `ms-laengde` | Situation | Når kald ikke er det vigtige, fx efter et konge-udspil med ALA, eller når spilfører spiller en farve. · Længdemarkering | (tilføjelse) |
| `ms-laengde` | Eksempel (højt-lavt = lige) | 8 3 → 8, derefter 3 (lige) | (tilføjelse) |
| `ms-laengde` | Eksempel (højt-lavt = lige) | 8 6 3 → 3, derefter 6 (ulige) | (tilføjelse) |
| `ms-laengde` | Eksempel (lavt-højt = lige) | 8 3 → 3, derefter 8 (lige) | (tilføjelse) |
| `ms-laengde` | Eksempel (lavt-højt = lige) | 8 6 3 → 8, derefter 6 (ulige) | (tilføjelse) |
| `ms-laengde` | Faldgrube | Det første kort kan kun aflæses ud fra de kort, makker ikke selv kan se. | (tilføjelse) |
| `ms-afkast` | Formål | At vise makker, hvilken farve du vil have spillet. | (tilføjelse) |
| `ms-afkast` | Situation | Første gang en modspiller ikke kan bekende. · Første afkast mod farve og sans | (tilføjelse) |
| `ms-afkast` | Eksempel (som kald eller afvisning) | Med lavt = kald: ♦2 fra ♦K D 7 2 → Kald til ruder | (tilføjelse) |
| `ms-afkast` | Eksempel (som kald eller afvisning) | Med lavt = kald: ♦9 fra ♦9 7 4 → Afvisning af ruder | (tilføjelse) |
| `ms-afkast` | Eksempel (O/E) | Spilfører spiller ♥; afkast ♦7 → Ulige: kald til ruder | (tilføjelse) |
| `ms-afkast` | Eksempel (O/E) | Spilfører spiller ♥; afkast ♦2 → Lille lige: styrke i klør | (tilføjelse) |
| `ms-afkast` | Eksempel (O/E) | Spilfører spiller ♥; afkast ♦8 → Stor lige: styrke i spar | (tilføjelse) |
| `ms-afkast` | Eksempel (Lavinthal) | Spilfører spiller ♥; afkast ♦2 → Lavt: beder om klør | (tilføjelse) |
| `ms-afkast` | Eksempel (Lavinthal) | Spilfører spiller ♥; afkast ♦9 → Højt: beder om spar | (tilføjelse) |
| `ms-afkast` | Forrang og undtagelser | O/E og Lavinthal: farverne: Klør er lavest. Afkastet viser en af de to farver, der hverken er afkastfarven eller den farve, der spilles. | Kompendiet s. 24 (klør er lavest); Lavinthal (tilføjelse) |
| `ms-afkast` | Forrang og undtagelser | Som kald eller afvisning med romersk kald mod farve: Afkastet læses som O/E. | metoder.json (som kald eller afvisning) |
| `ms-afkast` | Faldgrube | Aftalen gælder kun første gang, en modspiller ikke kan bekende. | Kompendiet s. 24 |
| `ms-forsinket` | Formål | At fortælle makker, om modspillet skal være passivt eller aktivt, og om et kald var ægte. | (tilføjelse) |
| `ms-forsinket` | Situation | I den første farve, spilfører spiller, efter udspillet. · Udspiller og tilspiller | (tilføjelse) |
| `ms-forsinket` | Eksempel (intet forsinket kald) | 3, derefter 7 → Ingen særlig betydning | (tilføjelse) |
| `ms-forsinket` | Eksempel (omvendt forsinket kald) | 3, derefter 7 (lav-høj) → Fortsæt i udspilsfarven, intet vigtigere at fortælle (passivt) | (tilføjelse) |
| `ms-forsinket` | Eksempel (omvendt forsinket kald) | 7, derefter 3 (høj-lav) → Skift farve, spil aktivt | (tilføjelse) |
| `ms-forsinket` | Forrang og undtagelser | Makker har brug for en markering: Der ses bort fra signalet, når det er tydeligt, at makker har brug for en længdemarkering. | Kompendiet s. 25 |
| `ms-forsinket` | Faldgrube | Lægger begge modspillere lav-høj, er modspillet passivt; lægger begge høj-lav, skal der angribes. | Kompendiet s. 26 |
| `modspilsaftaler.html` | Undertekst | Alle de varianter, Modspil træner. Valget af aftaler deles med Modspil i Fordelingstræneren, og quizzen spørger kun til, hvad aftalerne siger. | (tilføjelse) |
| `modspilsaftaler.html` | Note ved ugyldige data | De gemte data fra Modspil kunne ikke læses. Standard vises, og valget gemmes ikke, så Modspils data ikke overskrives. | Specen, Indstillingen |
| `modspilsaftaler.html` | Kilde | Kilde: aftalerne i Modspil (metoder.json) og Kompendium over modspilsaftaler. De forkerte svar i quizzen er ikke påstande om aftalerne. | Specen, Quizzen |
| Kortsiden, `ms-*` | Linjen under Formål | Din aftale følger profilen <navn>, som deles med Modspil. | (tilføjelse) |
| `data/modspilsaftaler-quiz.json` | 34 spørgsmål med rigtigt svar og forklaring (dansk og engelsk) | Spørgsmålene, de rigtige svar og forklaringerne gengiver metodens aftale. | metoder.json |
| `data/modspilsaftaler-quiz.json` | De forkerte svar (68 pr. sprog) | Rådgiverens; de er ikke påstande om aftalerne. | (tilføjelse) |
| `data/modspilsaftaler-quiz.json` | `afkast/ulige-lige/2`: forklaringen | "I farvernes rækkefølge er klør lavest" er hentet fra aftalens parentes. | metoder.json |

### Session 2 (26. nov. 2026)

Kørt i en ny rådgiverchat (Opus 5.5, high effort) via skallen på Franks computer, ikke i Claude Code. Grenen `modspilsaftaler`.

1. **Franks to valg** står under Beslutninger, punkt 5 og 6: quizzen og indstillingen får siden `modspilsaftaler.html`, og de tre udspilskort beholdes.
2. **Indstillingen** ligger i `assets/modspilsaftaler.js` (uden DOM; testes med `node --test tools/modspilsaftaler.test.mjs`, 8 tests). Den læser `modspil:v1` og skriver kun `profil` og `metoder`, med nøglernes rækkefølge og alle andre felter uændrede. Uden gemt tilstand vises Standard, og et valg skriver Modspils standardtilstand (som `defaultMsSaved`) med valget. Er de gemte data ikke gyldig JSON, eller mangler `profil` eller en gyldig metode i en kategori, vises Standard med en note, og intet skrives. Profilen regnes altid af metoderne, så en ændret metode giver "Egen" som i Modspil.
3. **Siden `modspilsaftaler.html`**: profilerne Standard, Omvendt, Kompendiet og Egen (kan ikke vælges, men markeres), en rulleliste pr. kategori med aftalen under, og quizzen med runder på op til 8 spørgsmål, emnevalg og "Alle varianter". `?k=ms-<kategori>` vælger emnet. Siden har links til Modspil og konventionskortene. Er `localStorage` spærret, gælder valget kun, mens siden er åben.
4. **Quizzen** `data/modspilsaftaler-quiz.json`: 34 spørgsmål (2 pr. metode) med felterne `q`, `correct`, `wrong`, `why` og `…En`. Spørgsmålene skrives af `_lab\modspilsaftaler\lav_quiz.py` (uden for repoet).
5. **Kortsiden** (`tools/konventionskort.src.html`, bygget): på kortene `ms-*` står den valgte metode øverst med mærket "Din aftale" og de andre under "Andre varianter", og under Formål står linkene "Træn i Modspil" (`/fordelingstraeneren/#modspil`) og "Quiz og indstilling" samt profilens navn. Andre kort er uændrede. `tools/konventionskort-shell.html` henter `../assets/modspilsaftaler.js`; i trænernes ⓘ findes den ikke, og kortene vises som før.
6. **Posterne** `ms-*` i `data/konventioner.json` har fået `"side": "modspilsaftaler.html"`, så forsidens kort åbner siden med emnet valgt.
7. **Ændringer i testværktøjerne**, uden for Afgrænsningen (godkendt af Frank 26. nov.): `tjek_fagord.py` springer felter over, hvis navn ender på `En` (ellers læste fagords-, bydeforms- og stavetestene den engelske aftale i `data/modspilsaftaler.json` som dansk, og stavekontrollen meldte 71 ukendte ord fra session 1); `tjek_bydeform.py` har linket "Træn i Modspil" under `UNDTAGELSER`; `tools/ordliste.txt` har ordet `feeling` ("table feeling").
8. **Testene:** `python3 tools/tjek_modspilsaftaler.py` melder "Alle punkter er i orden". Stavekontrollen melder ingen ukendte ord. Siden og kortsiden er prøvet i jsdom (dansk og engelsk, gyldig og ugyldig `modspil:v1`, skift af metode, Din aftale på `ms-kald`). Pixeltestene, `tjek_sidefod.mjs` og skærmbillederne kræver Chrome og hører til session 3; `modspilsaftaler.html` er en ny side, som `tjek_sidefod.mjs` og `tjek_viden_320.mjs` måske skal have på listen (session 3 undersøger det).
9. **Tokenforbrug:** sessionen kørte i rådgiverchatten, så de fire tal fra Claude Code findes ikke.

### Session 3 (26. nov. 2026)

Kørt i Claude Code (Sonnet 5.5, medium effort) på grenen `modspilsaftaler`. Ingen testfil og intet andet i repoet er ændret; kun denne Afklaret er skrevet. Intet er committet, flettet eller pushet.

1. **Accepttesterne:** `python tools/tjek_modspilsaftaler.py` melder "Alle punkter er i orden" (punkt 1–9), og `node --test tools/modspilsaftaler.test.mjs` har 8 af 8 grønne. (`python3` er på denne pc kun en Microsoft Store-genvej; `python` virker.)
2. **Hele suiten, én gang i forgrunden:** `tjek_viden_320.mjs` alt i orden (965 tjek), `tjek_crowhurst_390.mjs` alt i orden (712 tjek), `tjek_sidefod.mjs` alt i orden. Pixeltestene viser kun støj under loftet (NB-linjer med 1–3 pixels, også på ældre kort). Desuden i orden: `tjek_konventionskort.py` (58 kort), `tjek_kort_eksempler.py` (228), `tjek_fagord.py`, `tjek_bydeform.py`, `tjek_sprog.py` og `pixelstoej.test.mjs` (7 af 7).
3. **Skal `modspilsaftaler.html` på listerne?** Ikke ændret; til Franks beslutning.
   - `tjek_viden_320.mjs` henter kun `viden/*.html` og kortene, så siden dækkes ikke, og der er ingen grund til at udvide den: pixelsammenligningen har ingen "før" for en ny side.
   - `tjek_sidefod.mjs` har en fast liste `SIDER` uden `markering.html` og `modspilsaftaler.html`; sidens sidefod er den fælles `assets/footer.js`. Anbefaling: tilføj `modspilsaftaler.html` (og gerne `markering.html`) til `SIDER`.
   - Et tjek af vandret scroll for den nye side ved 390 og 320 px mangler i alle testene, og ville have fundet fejlen i punkt 5.
4. **Skærmbillederne** (18 stk. i `C:\Users\frank\Kontraktbridge\skaermbilleder\modspilsaftaler\`): `ms-kald-`, `indstilling-` og `quiz-` × da/en × 1280/390/320 px. `ms-kald` viser romersk kald øverst med "Din aftale" og profilen Egen, indstillingen viser profilen Egen (romersk kald, Kompendiets udspil mod sans, 3. og 5. højeste mod farve), og quizzen viser et spørgsmål med forklaring efter svaret. Kortsiden er dansk på den engelske side; det er som aftalt (kortene er på dansk, session 1 punkt 3).
5. **Fund, ikke rettet: vandret scroll på `modspilsaftaler.html` under 399 px.** Rullelisten "Emne" i quizzen (`select#emne` og dens `label`) er for bred: siden er 8 px for bred ved 390 px på dansk (4 px på engelsk) og 78 px (74 px) for bred ved 320 px. Det bryder specens krav "320 px uden vandret scroll". Kortsiden `ms-*` har ingen vandret scroll ved nogen bredde. Forslag til en mindste rettelse til en ny session: `#emne { max-width: 100%; min-width: 0 }` og `flex-wrap`/`flex-direction: column` på rækken med emnet under 399 px. Skærmbillederne `indstilling-*` og `quiz-*` ved 390 og 320 px viser fejlen og skal tages igen efter rettelsen.
6. **Kortsiden ved 390 og 320 px:** tabellerne på kortene (også de ældre, fx Truscott) klippes i højre kant uden vandret scroll på siden. Det er eksisterende opførsel og ikke ændret her.
7. **Tokenforbrug (nye input, skrevet til cachen, læst fra cachen, output):** de fire tal kan ikke læses inde fra sessionen. Frank tager `/usage` (5 timer og uge) efter sessionen, som ved session 1 og 2.

### Rettelse efter session 3 (26. nov. 2026)

Frank sagde ja til begge forslag fra session 3 (Claude Code, Sonnet 5.5, medium effort).

1. **Vandret scroll rettet** i `modspilsaftaler.html`: `.omfang label { max-width:100%; min-width:0 }`, `#emne { max-width:100%; min-width:0 }` og `@media (max-width:398px) { .omfang label { flex-wrap:wrap } }`, så rækken med Emne brækker. Rullelisterne i indstillingen (`.metode select`, `width:100%; max-width:100%`) holdt sig allerede inden for siden. Målt ved 1280, 390 og 320 px på dansk og engelsk: vandret scroll er 0 på kortsiden, indstillingen og quizzen. Reglerne ændrer ikke noget over 398 px (`max-width:100%` og `min-width:0` har ingen virkning, når indholdet er smallere end rækken); en pixelsammenligning ved 1280 px er ikke kørt, siden er ny og har intet "før".
2. **`tools/tjek_sidefod.mjs`:** `modspilsaftaler.html` er tilføjet til `SIDER` (`markering.html` er ikke med). Testen melder alt i orden, 120 tjek, og siden er med ved 1280, 390 og 320 px på begge sprog.
3. **Specen:** under session 2, punkt 7, står nu "(godkendt af Frank 26. nov.)", og sidste punkt i Quizzen er erstattet med afklaringen om `modspilsaftaler.html` (Beslutning 5).
4. **Skærmbillederne** `indstilling-` og `quiz-` ved 390 og 320 px er taget igen; de viser Emne-listen inden for siden. De øvrige 14 billeder er genskabt med samme indhold som før.
5. **Tests:** `tjek_modspilsaftaler.py` melder "Alle punkter er i orden". Scriptets tjek af teksten "Din aftale" på kortsiden melder fejlagtigt FEJL (fejl i selve scriptet); romersk kald øverst med "Din aftale" er set på skærmbillederne.
6. **Tokenforbrug:** de fire tal kan ikke læses inde fra sessionen; Frank tager `/usage`.
