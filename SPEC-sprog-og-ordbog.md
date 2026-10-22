# SPEC-sprog-og-ordbog

22. oktober 2026 · Frank

Hele kontraktbridge.dk får en sprogkontrol og en bridgeordbog. Specen gælder tre repoer: `frankpedersen.github.io` (forsiden, Om mig og ordbogen), `fordelingstraeneren` og `konventionstraener`. Den lægges i roden af hvert repo, og Claude Code bygger kun den del, der hører til repoet.

1. **Ordbogen** får sin egen side, www.kontraktbridge.dk/ordbog/, bygget fra `Dansk_bridgeordbog.md` (version 1.1, 403 opslag).
2. **Sidefoden** får en ny kolonne, **Opslag**, med linket **Bridgeordbog** på alle sider og i begge apps.
3. **Stavefejl og fagord** rettes efter listen nedenfor.
4. **En varig kontrol** forhindrer, at fejlene og de forkerte fagord kommer igen.

## Husets fagord

Gælder i al dansk tekst på sitet og i ordbogen (Franks valg 22. oktober 2026). De andre ord må kun stå i ordbogen som alternative termer, der peger på husets ord.

| Husets ord | Ikke | Engelsk |
| --- | --- | --- |
| bordet | blindemand, den blinde | dummy |
| kipning, kippe, dobbelt kipning | knibning, snit, dobbeltknibning | finesse |
| forbindelser, indgang | broer | entries |
| slutspil om det generelle; indspil kun om den særlige form, hvor en modspiller sættes ind | — (begge ord er rigtige, se Afklaret 3) | endplay, throw-in |

Tre ord mere foreslås fastlagt (se Åbne punkter). De bygges først, når Frank har sagt ja:

| Forslag | I dag | Hvor |
| --- | --- | --- |
| T1: **hp** i dansk tekst, HCP kun på engelsk | "HCP" i danske tekster | ca. 28 steder i `src/haandevaluering/ui/texts.ts` (fx "HCP og Zar er uenige") og et par steder i konventionstræneren |
| T2: **dobbeltton** | "doubleton" | ca. 50 steder i konventionstræneren (`data/kort/`, `dealer/`, puljerne); Fordelingstræneren og MODEL.md skriver dobbeltton |
| T3: **fitten** | "fittet" | ca. 19 steder i konventionstræneren; Fordelingstræneren skriver fitten |

## Afgrænsning

Før arbejdet starter i hvert repo:

1. Commit og tag den nuværende udgave, fx `v-foer-sprog`.
2. Arbejd på grenen `sprog-og-ordbog`, og flet først ind efter godkendelse.
3. Kør de eksisterende tests før og efter.

| Repo og sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `frankpedersen.github.io`: `ordbog/Dansk_bridgeordbog.md` (ny) | ordbogen som kilde, som Frank leverer den | rettes af Claude Code; rettelser skrives som forslag til Frank |
| `frankpedersen.github.io`: `tools/build_ordbog.py` (ny), `ordbog/index.html` (genereres) | siden bygges fra markdown; `index.html` rettes aldrig i hånden | eksterne biblioteker i browseren |
| `frankpedersen.github.io`: `index.html`, `om-mig/index.html`, `sitemap.xml` | kolonnen Opslag i sidefoden; `/ordbog/` i sitemap | ændre kortene, menuen eller stilen i øvrigt |
| `fordelingstraeneren`: `src/ui/Footer.tsx` | kolonnen Opslag med linket til `/ordbog/` | ændre de andre kolonner |
| `konventionstraener`: `assets/footer.js` | kolonnen Opslag med linket til `/ordbog/` | ændre de andre kolonner |
| Alle tre: teksterne i rettelseslisten | rette præcis de ord, listen nævner | omskrive tekster i øvrigt |
| Alle tre: `tools/sprogtjek.py` eller `scripts/sprogtjek.ts` (ny), en fagordstest (ny) | den varige kontrol (se nedenfor) | gøre `npm test` afhængig af netværk |
| Lagring, tokens, data, løsere, puljernes indhold ud over ordene | intet | alt |

Kræver noget alligevel en ændring ud over tabellen, skal Claude Code stoppe og spørge.

Besked til Claude Code (samme i alle tre repoer):

> Læs CLAUDE.md og SPEC-sprog-og-ordbog.md. Byg den del af specen, der hører til dette repo, på grenen `sprog-og-ordbog`. Skriv accepttestene først, og stop, når testene er grønne, så jeg kan godkende. T1–T3 bygges først, når jeg har svaret på dem.

## Ordbogssiden

| Del | Indhold |
| --- | --- |
| Adresse | www.kontraktbridge.dk/ordbog/ med samme topbjælke, sidefod og stil (Subtle Gradient) som forsiden og Om mig |
| Overskrift | "Bridgeordbog" med undertekst "403 bridgeord på dansk med engelsk oversættelse." (tallet regnes af scriptet) |
| Søgning | ét felt øverst, der filtrerer på opslagsord, alternative termer og engelsk, mens man skriver; "Ingen opslag passer" ved nul |
| Filtre | kategori og niveau som knapper; A–Å-linje til spring |
| Opslag | opslagsord som overskrift med anker `#id`; Engelsk, Alternative termer, Forkortelse, Niveau, Kategori og Systemafhængig som en lille linje; Kort definition; Forklaring kun når den er forskellig fra definitionen; Relaterede begreber som links til deres anker |
| Indekser | Engelsk–dansk som foldbar liste nederst; Dansk–engelsk vises ikke, fordi hvert opslag allerede har det engelske ord |
| Sprog | siden er dansk; sidens faste tekster har `data-en` som forsiden, men opslagene er kun på dansk |
| Mobil | ingen vandret rulning ved 390 px |
| Byg | `python3 tools/build_ordbog.py` læser `ordbog/Dansk_bridgeordbog.md` og skriver `ordbog/index.html`. Scriptet stopper med en fejl ved døde henvisninger, dobbelte id'er eller et opslagsord, der er et af husets "Ikke"-ord |

## Sidefoden

Kolonnen kommer efter Trænere i alle sidefødder:

| Overskrift | Link | Engelsk |
| --- | --- | --- |
| Opslag | Bridgeordbog → `/ordbog/` | Reference · Bridge dictionary |

Det gælder forsiden, Om mig, ordbogssiden, Fordelingstrænerens `Footer.tsx` og konventionstrænerens `footer.js`, så sidefoden er ens på hele sitet.

## Rettelser

Fundet med en dansk stavekontrol (hunspell da_DK) af al synlig tekst i de tre repoer, 22. oktober 2026. De fleste ukendte ord var bridgeord og engelsk tekst; her er de rigtige fejl:

| Repo og fil | Står der | Rettes til |
| --- | --- | --- |
| konventionstraener `dealer/ff_trial.py` (og puljen `pools/ff-trial-bids.json`, der bygges igen) | "Støtte til en ny trumffarv" | "Støtte til en ny trumffarve" |
| konventionstraener `data/kort/ff-ogust.json` | "hvor gode trumfene er" | "hvor gode trumferne er" |
| konventionstraener `viden/2-over-1-makker2.html` | "bekræft especielt hvad …" | "bekræft især hvad …" |
| konventionstraener `viden/2-over-1-makker2.html` (2 steder) | "stærke hændertyper" | "stærke håndtyper" |
| konventionstraener `viden/kampen-om-kontrakten.html` | "stopmeldinger fra invitter" | "stopmeldinger fra invitationer" |

Er en side genereret (fx fra et systemdokument), rettes kilden, og siden bygges igen.

## Den varige kontrol

1. **Fagordstest i hvert repo:** en test, der læser al dansk synlig tekst (de danske tekstfiler, data og sider) og fejler, hvis et af husets "Ikke"-ord står der. "i snit" (gennemsnit) er tilladt. Når T1–T3 er godkendt, kommer de med i testen. Testen kører i `npm test` (Fordelingstræneren) og i `tools/tjek_*.py` (konventionstræneren og forsiden).
2. **Stavekontrol som værktøj:** `sprogtjek` kører hunspell-reglerne for dansk (fx Python-pakken `spylls` med `da_DK` fra `dictionary-da`) på al dansk synlig tekst og skriver en liste over ukendte ord. Bridgeord, der er rigtige, står i `ordliste.txt` (fx cuebid, sleminvit, Stayman, sidninger, kipning), og listen fyldes også med ordbogens opslagsord. Værktøjet køres med hånden før hver udgivelse og er ikke en del af `npm test`.

## Accepttest

- [x] www.kontraktbridge.dk/ordbog/ viser 403 opslag, og søgning på "finesse", "knibning" og "kipning" finder alle opslaget Kipning.
- [x] Søgning på "blindemand" finder Bordet. Søgning på "indspil" finder Indspil, og Slutspil og Indspil linker til hinanden.
- [x] Hvert opslags Relaterede begreber linker til et anker, der findes på siden.
- [x] Opslag, hvor Forklaring er den samme som Kort definition, viser kun definitionen.
- [x] `build_ordbog.py` fejler, hvis et opslagsord er "Knibning", "Snit" eller "Den blinde".
- [x] Sidefoden har kolonnen Opslag med Bridgeordbog på forsiden, Om mig, ordbogen, i Fordelingstræneren og i konventionstræneren, på dansk og engelsk.
- [x] Ved 390 px har ordbogssiden og forsiden ingen vandret rulning.
- [x] Alle ord i rettelseslisten er rettet, og puljerne er bygget igen med `build_pools.py` (puljen ff-trial-bids er kun rettet i teksten, se Afklaret 7).
- [x] Fagordstesten består i alle tre repoer og fejler, hvis man skriver "knibning" i en dansk tekst.
- [x] `sprogtjek` kører og giver højst de ord, der står i `ordliste.txt`, eller en liste, Frank har set.

## Afklaret

1. **Husets ord** gælder: bordet, kipning, forbindelser og slutspil. Ordbogen er rettet til dem i version 1.1: Kipning, Dobbelt kipning og Bordet er opslagsord, og Knibning, Snit, Den blinde og Blindemand står kun som alternative søgeord, der fører til dem.
2. **Ordbogen version 1.1** har 403 opslag. Tre dubletter er slået sammen: Adjusted score (AdjS) ind i Justeret score, Contract ind i Kontrakt og Screen ind i Skærm. Bordets forklaring er rettet: spilføreren vælger også bordets kort. Indekserne er bygget igen.
3. **Slutspil og indspil er to begreber** (Franks valg 22. oktober 2026): slutspil (endplay) er overbegrebet, hvor en modspiller tvinges til at give et stik; indspil (throw-in) er én form for slutspil, hvor en modspiller sættes ind og må spille ud til spilførerens fordel. Skvis og Morton's Fork er andre former. Ordbogen har et opslag for hver, og "indspil" er ikke et forbudt ord i fagordstesten.
4. **Placering:** egen side med overskriften Opslag i sidefoden (Franks valg 22. oktober 2026).
5. **T1–T3** (Franks svar 22. oktober 2026): husets ord i dansk tekst er **hp** (HCP kun på engelsk), **doubleton** (ikke dobbeltton) og **fittet** (ikke fitten). Det er de ord, konventionstræneren brugte i forvejen, så forslaget i tabellen ovenfor er vendt for T2 og T3. Ordbogen har også Doubleton som opslagsord med Dobbeltton som alternativ term.

Claude Codes valg i konventionstræneren (22. oktober 2026, grenen `sprog-og-ordbog`; appen før er tagget `v-foer-sprog`):

6. **Sidefoden:** kolonnen Opslag står i `assets/footer.js` mellem Trænere og Aftaler og notater, med Bridgeordbog → `/ordbog/` og Reference · Bridge dictionary på engelsk.
7. **Puljen ff-trial-bids er ikke bygget igen med `build_pools.py`.** Puljerne udtrækkes uden seed, så en ny bygning giver nye hænder. Desuden blev puljen og kortet rettet direkte 17. oktober 2026 (commit 7e7961b: "4 små kort er ikke hjælp", trial bid 15–17 sp), mens `dealer/ff_trial.py` stadig har den gamle regel. En ny bygning ville derfor rulle Franks rettelser tilbage, og kortets 5 meldeeksempler ville ikke længere findes i puljen. Ordet er rettet i `dealer/ff_trial.py` og i puljens tekst; hænderne er uændrede. `tools/tjek_sprog.py` tjekker, at puljens svarmuligheder er de samme som dealerens. **Til Frank:** `dealer/ff_trial.py` bør have reglerne fra 17. oktober, før puljen bygges igen.
8. **Kampen om kontrakten:** rettet i `docs/kampen-om-kontrakten.md` (kilden) og i `viden/kampen-om-kontrakten.html`. `tools/build_kamp_viden.py` virker ikke siden commit f0f70b0 (CSS-blokken i `tools/import_design.py` findes ikke længere), og siden er rettet i hånden efter det, så en ny bygning ville fjerne de rettelser.
9. **Makker 2-dokumentet** er genereret fra Claude Design-eksporten »2 over 1 - Moderne majorstotte.html«, som ligger uden for repoet (i Downloads, og `build_ff_page.py` findes ikke i repoet). Ordene er rettet i `viden/2-over-1-makker2.html`; **til Frank:** ret også "especielt" og "hændertyper" i eksporten, før siden genereres igen.
10. **Husets ord:** i konventionstræneren er kun "dobbeltton" rettet til "doubleton" i `viden/2-over-1.html` (2 steder). Alle HCP stod allerede i engelsk tekst (`data-en`, `en`-felter og det engelske argument til `T`).
11. **Fagordstesten** (`tools/tjek_fagord.py`) læser siderne, assets, data, puljerne, det danske argument til `tx` i `dealer/` og `docs/kampen-om-kontrakten.md`. Engelsk springes over: `data-en`, det engelske argument til `T`/`t`, `link` og `kolonne`, og `"en"`-felterne i JSON, også inde i sidernes scripts.
12. **Sprogtjek** (`tools/sprogtjek.py`) bruger samme tekst og `spylls` med da_DK fra npm-pakken dictionary-da, som hentes første gang og gemmes i brugerens cache (ikke i repoet). `tools/ordliste.txt` har bridgeord, navne, forkortelser, engelske fagtermer, felt- og klassenavne, som værktøjet ikke kan skille fra tekst, og ordbogens opslagsord, som hunspell ikke kender. Værktøjet giver i dag 4 ord til Franks liste: "trinene" (8 steder; retskrivningen er *trinnene*), "klørerne" og "11-pointshænder" (2 steder).

Åbne punkter:

1. **T1–T3:** besvaret, se Afklaret 5.
2. **Ordbogens kvalitet** (Franks arbejde, ikke Claude Codes): 173 af 403 opslagsord er engelske (fx Appeal, Average, Nine (9)); 356 står i kategorien Grundlæggende begreber og 374 på niveau begynder, så filtrene siger ikke meget endnu; i 363 opslag er Forklaring den samme som Kort definition. Siden virker, men ordbogen bliver bedre med danske opslagsord, rigtige kategorier og niveauer og egentlige forklaringer i en version 1.2.
