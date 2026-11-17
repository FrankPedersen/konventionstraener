# SPEC – Pixeltolerance i tjek_viden_320 og tjek_crowhurst_390

15. november 2026 · Konventionstræner · opgave S i `PLAN-aabne-opgaver.md` · gren `pixeltolerance`, tag før: `v-foer-pixeltolerance`. Godkendt af Frank og udgivet 17. november 2026 (`56e1613`); grenen er slettet.

## Formål

Pixelsammenligningen i `tools/tjek_viden_320.mjs` og `tools/tjek_crowhurst_390.mjs` fejler af og til på sider, der ikke er ændret. Det sker også på `main`. Chrome tegner 1–5 pixels en anelse forskelligt fra gang til gang, og de tre forsøg i `somFør` fanger ikke altid støjen. Testene skal kun fejle ved en ægte ændring.

## Afgrænsning

| Må ændres | Må ikke ændres |
| --- | --- |
| `tools/tjek_viden_320.mjs` og `tools/tjek_crowhurst_390.mjs` (sammenligningen og NB-linjen) | siderne, kortene og CSS'en |
| et nyt fælles modul `tools/pixelstoej.mjs` med loftet og afgørelsen | de øvrige tjek (vandret scroll, sidefod, `--live`) |
| en lille enhedstest af modulet, kørt med `node --test` | antallet af forsøg (tre) og tagget, der sammenlignes med |
| `CLAUDE.md` (én linje om loftet) og denne spec under Afklaret | |

## Reglen

1. **En pixel tæller kun, når den afviger mere end 5 farvetrin i mindst én kanal** (R, G eller B), og **højst 5 sådanne pixels** pr. skærmbillede regnes som støj (Franks valg (b) 15. nov. 2026 efter målingen i del 1; før stod der "loft over antal pixels, ikke over farvetrin" og højst 5 pixels i alt). Pixels, der afviger højst 5 trin, er altid støj, uanset hvor mange de er.
2. **Støj** giver en NB-linje som i dag, med antal, område og element, og testen består.
3. **Over loftet** gælder de tre forsøg i træk som nu. Er forskellen over loftet i alle tre forsøg, fejler testen med samme melding som i dag.
4. Begge grænser står ét sted, som `TRIN = 5` og `LOFT = 5` i `tools/pixelstoej.mjs`, og begge scripts bruger modulet.

## Del 1: måling (før koden ændres)

1. Kør sammenligningen "før mod før" (tagget mod sig selv) **10 runder** på alle sider og bredder i begge scripts, uden de tre forsøg.
2. Notér for hver forskel antal pixels og største farvetrin pr. kanal.
3. Rapportér en tabel med kolonnerne side, bredde, runde, pixels og trin. Skriv også det største antal pixels, der er målt.
4. **Er det største antal over 5, så stop og rapportér**, før koden ændres. Så skal loftet besluttes på ny.

## Accepttest (skrives først, røde)

1. **Enhedstest af `pixelstoej.mjs`:**
   - 0–5 tællende pixels er støj.
   - 6 tællende pixels er ikke støj.
   - 25 pixels med 1–5 trin er støj, og 6 pixels med 6 trin eller mere er ikke støj.
   - Loftet og trinnet læses kun fra modulet.
2. **Ægte ændring fanges:** I en midlertidig kopi af én side under `viden/` ændres ét ord i en overskrift. Begge scripts skal fejle ved 390 og 1280 px. Kopien rulles tilbage, og den kommer ikke i git.
3. **Ingen falske fejl:** Begge scripts køres 5 gange i træk på grenen, uden andre ændringer end denne. De må ikke give FEJL. NB-linjer for støj er tilladt og noteres.
4. **Uændret adfærd i øvrigt:** `--live` og `ingen` virker som før. Sammenligning af højde og vandret scroll fejler som før.

## Afklaret

### Efter Franks valg (b), 15.–17. nov. 2026

**Bygget og stoppet før merge.** Frank valgte (b) 15. nov.: en pixel tæller kun, når den afviger mere end 5 farvetrin i mindst én kanal, og højst 5 tællende pixels pr. skærmbillede er støj. `tjek_crowhurst_390.mjs` skulle have samme reference til Makker 2-dokumentet som `tjek_viden_320.mjs`. Reglen og accepttest 1 ovenfor er rettet.

1. **Commits på `pixeltolerance`:** `88d0971` (Reglen og enhedstesten, rød), `0d051bf` (modulet, de to scripts, referencen og én linje i `CLAUDE.md`) og denne Afklaret. Intet er pushet.
2. **Koden:** `tools/pixelstoej.mjs` har `TRIN = 5` og `LOFT = 5` og funktionerne `tæller(før, nu)`, `erStøj(pixels)` og `afgør(forskelle)`. I begge scripts tæller `forskel` alle forskellige pixels og de tællende (over `TRIN` i én kanal) i hele skærmbilledet (alle bidder), og `somFør` lader en forskel med højst `LOFT` tællende pixels passere med en NB-linje ("… N pixels over 5 trin, M forskellige i alt, i område (farve; element) – støj (højst 5 pixels over 5 trin)"). Over loftet gælder de tre forsøg som før, og en forskel i højden er aldrig støj. `tjek_crowhurst_390.mjs` har fået `NYERE`, så Makker 2-dokumentet sammenlignes med commit `bca7e0c` (tagget er det samme). Tal for loft og trin står kun i modulet.
3. **Accepttest 1 (enhedstesten):** `node --test tools/pixelstoej.test.mjs` var rød, før modulet fandtes, og gav derefter 1 fejl ("loftet og trinnet læses kun fra modulet"), til scripts brugte modulet. Nu er alle 7 tests grønne: grænserne er 5 og 5, en pixel tæller kun over 5 trin, 0–5 tællende pixels er støj, 6 og derover og en forskel i højden er ikke, 25 pixels med 1–5 trin er støj, 6 pixels med 6–229 trin er ikke støj (og 5 af dem sammen med 25 svage er), og loft og trin står kun i modulet.
4. **Accepttest 2 og 4 (ægte ændringer), 15. nov.:** tre sider blev ændret midlertidigt i arbejdsmappen: ét ord i en overskrift i `viden/bridgesystem.html` ("2.2 Sansåbninger" → "2.2 Sansmeldinger"), en ekstra linje i `viden/forslag-2klor-kontrolsvar.html` og en 700 px bred blok i `viden/kampen-om-kontrakten.html`. `tjek_viden_320.mjs` gav 28 FEJL og `tjek_crowhurst_390.mjs` 18:
   - ordet i overskriften: FEJL "som før" ved 390 og 1280 px (og 399 px i `tjek_crowhurst_390`) på dansk og engelsk, med 1472–1482 pixels over 5 trin;
   - den ekstra linje: FEJL "højden er …, før …" ved alle bredder;
   - den brede blok: FEJL "ingen vandret scroll" ved 320, 340, 360 og 375 px, lukket og foldet ud, og FEJL på højden ved 390 og 1280 px.
   Ændringerne er rullet tilbage med `git checkout`, og arbejdsmappen var ren bagefter; de kom aldrig i git.
5. **Accepttest 3 (ingen falske fejl):** 12 kørsler af begge scripts på en ren arbejdsmappe på `0d051bf`, de to scripts samtidig i hver kørsel.

   | Kørsel | `tjek_viden_320` | `tjek_crowhurst_390` |
   | --- | --- | --- |
   | 1 | i orden, 2 NB | i orden, 8 NB |
   | 2 | 1 FEJL: "Kortene kom ikke frem" (stoppet efter 611 af 791 tjek) | 1 FEJL: "Runtime.evaluate svarede ikke inden for 60 s" (183 af 418) |
   | 3 | i orden, 9 NB | i orden, 19 NB |
   | 4 | i orden, 4 NB | i orden, 17 NB |
   | 5 | i orden, 13 NB | i orden, 16 NB |
   | 6 | i orden, 9 NB | i orden, 21 NB |
   | 7 | 1 FEJL: "Emulation.setEmulatedMedia svarede ikke inden for 60 s" (588 af 791) | 1 FEJL: "Target.createTarget svarede ikke inden for 60 s" (133 af 418) |
   | 8 | i orden, 9 NB | i orden, 15 NB |
   | 9 | i orden, 7 NB | i orden, 13 NB |
   | 10 | i orden, 9 NB | i orden, 14 NB |
   | 11 | i orden, 3 NB | i orden, 7 NB |
   | 12 | i orden, 5 NB | i orden, 15 NB |

   - **Kørsel 8–12 er fem i træk uden FEJL** (17. nov. kl. 05:24–06:31 UTC på en stille maskine). Det opfylder accepttest 3.
   - **Ingen kørsel har haft FEJL på pixels.** De to afbrudte kørsler stoppede, fordi browseren ikke svarede inden for 60 s: kørsel 2, mens Modspil-agenten i Fordelingstræneren kørte tunge tests (15. nov. 17:41–17:48 UTC), og kørsel 7, mens maskinen sov (15. nov. 22:16 til 16. nov. 12:21 UTC). Begge stoppede, før de nåede alle tjek, og derfor står de som FEJL ("testen kørte færdig").
   - **NB-linjerne:** 221 i alle kørsler. 210 har 0 tællende pixels (kun forskelle på højst 5 trin), 10 har 1 tællende pixel og 1 har 2. Den største forskel i én NB-linje er 48 pixels i alt. Ingen sammenligning skulle prøves igen: al støj lå under loftet i første forsøg. De enkelte tællende pixels ligger mest i Makker 2-dokumentet ved 1280 px.
6. **Accepttest 4 (uændret adfærd i øvrigt):** `--live` gav 568 tjek i orden mod www.kontraktbridge.dk/konventionstraener/ i `tjek_viden_320` og 83 i `tjek_crowhurst_390` (223 og 335 pixeltjek sprunget over som før), og `ingen` gav 568 og 80 tjek i orden uden NB-linjer. Højden og vandret scroll fejler som før (punkt 4).
7. **Fundet undervejs:** de to scripts' egne tidsgrænser (60 s pr. kald til browseren) kan give FEJL, når maskinen er travl eller sover. Det er ikke en pixelforskel og er uændret af denne spec; testene bør køres alene.
8. **Tokenforbrug** (nye input, skrevet til cachen, læst fra cachen og output; fra Claude Codes logfil for sessionen; et svar hører til den opgave, der var i gang på dets tidspunkt):
   - Bygningen og starten af accepttestene efter Franks valg (15. nov. 15:52–17:33 UTC): 12 svar; nye input 22, skrevet til cachen 813.344, læst fra cachen 7.505.745, output 16.043; i alt 8.335.154
   - Koordineringen af kørslerne og status i `SYSTEM.md` for både pixeltolerance og Modspil (15. nov. 17:45 til 17. nov. 06:31 UTC; mest gentagelserne af accepttest 3): 20 svar; nye input 44, skrevet til cachen 915.218, læst fra cachen 15.560.184, output 14.493; i alt 16.489.939
   - Selve kørslerne brugte ingen tokens. Denne Afklaret er skrevet bagefter og er ikke med i tallene.
9. **Udgivet 17. nov. 2026:** Frank godkendte ændringen. Enhedstesten var grøn (7 tests) på grenen og igen på `main` efter fletningen. `pixeltolerance` er flettet til `main` med `--no-ff` (`56e1613`) og pushet sammen med tagget `v-foer-pixeltolerance`, og GitHub Pages har bygget `56e1613` (06:48 UTC). Live-tjekkene mod www.kontraktbridge.dk/konventionstraener/, kørt én ad gangen: `tjek_viden_320.mjs --live` gav "Alt i orden: 568 tjek" (223 pixeltjek sprunget over), og `tjek_crowhurst_390.mjs --live` gav "Alt i orden: 83 tjek" (335 pixeltjek sprunget over), begge uden FEJL og som før ændringen. Grenen `pixeltolerance` er slettet lokalt; den lå aldrig på GitHub.

### Del 1 (målingen, 15. nov. 2026)

**Målingen viser, at loftet på 5 pixels ikke holder. Arbejdet er stoppet efter del 1, før koden ændres (del 1, punkt 4); loftet skal besluttes på ny.** Grenen `pixeltolerance` (tag før: `v-foer-pixeltolerance`) har kun specen og enhedstesten, som er rød; `tools/pixelstoej.mjs` og ændringen i de to scripts er skrevet, men ikke lagt i repoet.

1. **Sådan er der målt (15. nov. 2026, 13:03–14:59 UTC):** hvert script er kopieret til en målekopi uden for repoet, der kun adskiller sig ved, at siden nu og siden før begge hentes fra scriptets reference (`v-foer-viden-320` med Makker 2-dokumentet fra `NYERE`, og `v-foer-crowhurst-390`), at vandret scroll springes over, og at hver sammenligning tages én gang pr. runde uden de tre forsøg. Skærmbillederne tages som i scripts (samme Chrome-flag, egne kontekster, bidder på 6000 px). For hver forskel er antallet af forskellige pixels talt i hele skærmbilledet (alle bidder) og det største farvetrin i én kanal (R, G eller B). 10 runder i hvert script: 2230 sammenligninger i `tjek_viden_320.mjs` (223 pr. runde ved 390 og 1280 px) og 3350 i `tjek_crowhurst_390.mjs` (335 pr. runde ved 390, 399 og 1280 px). De to målinger kørte samtidig (runde 1–10 i `tjek_viden_320` og runde 1–7 i `tjek_crowhurst_390`); runde 8–10 i `tjek_crowhurst_390` kørte alene og havde også forskelle over 5 pixels (8 og 6).
2. **Resultatet:**
   - **Største antal pixels:** 25 i `tjek_viden_320.mjs` og 42590 i `tjek_crowhurst_390.mjs`. Uden den ene udsvingning er det største 24.
   - **Over 5 pixels:** 7 af 2230 sammenligninger og 28 af 3350.
   - **Almindelig støj er svag i farven eller lille:** i `tjek_viden_320` har alle forskelle et farvetrin på højst 5, og de fleste 1. I `tjek_crowhurst_390` har 15 små forskelle (1–4 pixels) et trin på 6–57, og resten højst 5. Ud over udsvingningen nedenfor har ingen forskel både over 5 pixels og over 5 trin. Den største støj kommer igen samme sted: `viden/2-over-1.html` ved 390 px i boksen "12–15 minimum" (19–25 pixels, 1 trin, 10 gange i 8 af de 20 runder) og ved 399 px i "37+ storeslem" (16–20 pixels, 5 trin).
   - **Én stor udsvingning:** Makker 2-dokumentet på dansk ved 399 px i runde 1 af `tjek_crowhurst_390` gav 42590 pixels og 229 trin fra overskriften "De tre håndtyper" og nedefter, med samme højde. Siden var tegnet anderledes én gang ud af ti; de tre forsøg i `somFør` fanger det, men intet loft på pixels gør.
3. **Forslag til et nyt loft (Franks valg):**
   - **(a) Højere loft over pixels, som reglen er i dag:** fx 30 pixels i alt. Det dækker den målte støj (højst 25 og 24), men en lille ægte ændring, fx ét tal i en tabel med 13 px skrift, kan også give omkring 20–40 pixels (anslået, ikke målt) og gå under loftet.
   - **(b) Loft over pixels, der afviger mere end 5 trin:** pixels med en forskel på højst 5 trin i alle kanaler tæller ikke, og loftet på 5 pixels gælder resten. Al målt støj undtagen udsvingningen giver højst 4 pixels over 5 trin og ligger under loftet, og en ægte ændring af tekst (sort på hvidt er over 200 trin) tælles fuldt. Det bryder med reglen "loft over antal pixels, ikke over farvetrin" i specen, men målingen viser, at farvetrinnet er det, der skiller støj fra ændringer. Mit forslag er (b).
   - I begge tilfælde gælder de tre forsøg som i dag for forskelle over loftet, og udsvingningen på 42590 pixels fanges af dem.
4. **`tjek_crowhurst_390.mjs` og Makker 2-dokumentet:** scriptet sammenligner med `v-foer-crowhurst-390` (6. nov.), og Makker 2-dokumentet er ændret siden (markeringerne 15. nov.). Accepttest 3 (fem kørsler uden FEJL) vil derfor fejle på dokumentet ved 390, 399 og 1280 px af en ægte grund (udledt af ændringen; ikke kørt). Forslag: samme `NYERE` som i `tjek_viden_320.mjs` (dokumentet sammenlignes med commit `bca7e0c`), uden at tagget ændres. Det er ikke gjort.
5. **Enhedstesten** `tools/pixelstoej.test.mjs` er skrevet og rød (modulet findes ikke). Den kræver `LOFT = 5` og følger det nye loft, når det er besluttet.
6. **Tokenforbrug for sessionen** (fra Claude Codes logfil for sessionen; et svar hører til den opgave, der var i gang på dets tidspunkt; "cache læst" er samtalen, der genlæses fra cache ved hvert svar): pixeltolerance, hele opgaven til og med committen af rapporten (15. nov. 2026, 13:01–15:00 UTC): 25 svar; input 54, cache skrevet 790.881, cache læst 17.588.041, output 39.610; i alt 18.418.586 tokens. Cache skrevet er højt, fordi cachen udløb, mens målingen kørte, og samtalen blev skrevet til cachen igen. Hertil kommer de 4 svar, hvor begge specer blev læst, fælles med `SPEC-kontakt-ip-graense.md` (i alt 2.636.802 tokens). Selve målingen kørte i baggrunden og brugte ingen tokens.

#### Tabellen fra del 1

Kolonnerne er side, bredde, runde, pixels og trin (største farvetrin i én kanal); sidste kolonne er elementet ved den første forskel. Sammenligninger uden forskel er ikke med.

#### tjek_viden_320.mjs

2230 sammenligninger i 10 runder (223 pr. runde), 93 med forskel, 7 over 5 pixels, 0 med forskel i højden. Største antal pixels: 25; største farvetrin pr. kanal: 5.

Fordeling (pixels: antal forskelle): 1: 47, 2: 18, 3: 15, 4: 5, 5: 1, 6: 2, 7: 1, 19: 3, 25: 1

| Side | Bredde | Runde | Pixels | Trin | Første forskel |
| --- | --- | --- | --- | --- | --- |
| viden/2-over-1.html på da | 390 | 5 | 25 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/2-over-1.html på da | 390 | 2 | 19 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/2-over-1.html på en | 390 | 2 | 19 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/2-over-1.html på en | 390 | 10 | 19 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/bridgesystem.html på en | 390 | 10 | 7 | 1 | td "Svarer spørger efter kortfarve" ved 260,12620 |
| viden/2-over-1.html på da | 390 | 8 | 6 | 1 | div.felt.vew "NSVØ" ved 156,28369 |
| viden/bridgesystem.html på en | 390 | 1 | 6 | 1 | td "Svarer spørger efter kortfarve" ved 260,12620 |
| Kortet ff-doblinger, kompakt | 390 | 1 | 5 | 1 | button.chip.lnk "Negativ dobling, støttedobling" ved 147,799 |
| Kortet ff-2kl, kompakt | 390 | 5 | 4 | 1 | li.k-gul "Specialaftale, alertér" ved 234,2428 |
| Kortet ff-2kl, kompakt | 390 | 8 | 4 | 1 | li.k-gul "Specialaftale, alertér" ved 234,2428 |
| viden/bridgesystem.html på da | 390 | 2 | 4 | 1 | td "Minortransfer – klør" ved 165,6216 |
| viden/bridgesystem.html på da | 390 | 6 | 4 | 1 | td "Spørger efter trumfdamen" ved 240,18105 |
| viden/bridgesystem.html på da | 390 | 10 | 4 | 1 | td "Svarer spørger efter kortfarve" ved 260,12620 |
| Kortet ff-flannery, kompakt | 1280 | 5 | 3 | 1 | li.k-gron "Naturlig / støtte" ved 539,1695 |
| Kortet ff-flannery, kompakt | 1280 | 10 | 3 | 1 | li.k-gron "Naturlig / støtte" ved 539,1695 |
| Kortet usaedvanlig-2nt, kompakt | 1280 | 9 | 3 | 1 | li.k-gron "Naturlig / støtte" ved 539,1933 |
| Kortet usaedvanlig-2nt, kompakt | 1280 | 10 | 3 | 1 | li.k-gron "Naturlig / støtte" ved 539,1933 |
| viden/2-over-1-makker2.html på da | 390 | 3 | 3 | 5 | strong "Kommer indmeldingen først, eft" ved 270,31542 |
| viden/2-over-1-makker2.html på en | 390 | 9 | 3 | 5 | strong "Kommer indmeldingen først, eft" ved 270,31542 |
| viden/2-over-1.html på da | 390 | 3 | 3 | 1 | div.felt.vew "NSVØ" ved 156,28369 |
| viden/2-over-1.html på da | 390 | 10 | 3 | 1 | div.felt.vns "NSVØ" ved 158,18359 |
| viden/2-over-1.html på en | 390 | 3 | 3 | 1 | p "Genåbningen hører med til afta" ved 255,30499 |
| viden/2-over-1.html på en | 390 | 4 | 3 | 1 | div.felt.vew "NSVØ" ved 156,28369 |
| viden/2-over-1.html på en | 390 | 5 | 3 | 1 | div.felt.vew "NSVØ" ved 156,28369 |
| viden/2-over-1.html på en | 390 | 6 | 3 | 1 | p "Genåbningen hører med til afta" ved 255,30499 |
| viden/2-over-1.html på en | 390 | 7 | 3 | 1 | div.felt.vew "NSVØ" ved 156,28369 |
| viden/2-over-1.html på en | 390 | 9 | 3 | 1 | div.felt.vns "NSVØ" ved 158,18359 |
| viden/bridgesystem.html på da | 390 | 3 | 3 | 1 | strong "Sekvens" ved 69,25694 |
| Kortet 1430, kompakt | 390 | 4 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 108,1818 |
| Kortet 1430, kompakt | 390 | 6 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 108,1818 |
| Kortet ff-dont, kompakt | 1280 | 5 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 524,2436 |
| Kortet ff-dont, kompakt | 1280 | 8 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 524,2436 |
| Kortet ff-genaabning, kompakt | 1280 | 6 | 2 | 1 | p "Genåbn ca. 3 hp lettere end i " ved 713,813 |
| Kortet ff-gerber, kompakt | 1280 | 4 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 524,1370 |
| Kortet kamp-stoette-def, kompakt | 1280 | 10 | 2 | 1 | button.chip.lnk "Støtte efter makkers indmeldin" ved 242,431 |
| Kortet multiforsvar, kompakt | 390 | 4 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 108,2237 |
| Kortet multiforsvar, kompakt | 390 | 8 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 108,2237 |
| Kortet transfer, kompakt | 390 | 8 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 108,1753 |
| viden/2-over-1-makker2.html på da | 390 | 8 | 2 | 1 | strong "Kommer indmeldingen først, eft" ved 270,31542 |
| viden/2-over-1-makker2.html på en | 390 | 6 | 2 | 1 | strong "Kommer indmeldingen først, eft" ved 270,31542 |
| viden/2-over-1.html på da | 390 | 9 | 2 | 1 | p "Pas på med 3♠︎: efter åbners 2" ved 246,15270 |
| viden/forslag-2klor-kontrolsvar.html på da | 390 | 5 | 2 | 1 | th "Udgang i trumffarven" ved 78,6071 |
| viden/forslag-2klor-kontrolsvar.html på da | 390 | 6 | 2 | 1 | th "Udgang i trumffarven" ved 78,6071 |
| viden/forslag-2klor-kontrolsvar.html på da | 390 | 7 | 2 | 1 | th "Udgang i trumffarven" ved 78,6071 |
| viden/forslag-2klor-kontrolsvar.html på da | 390 | 9 | 2 | 1 | th "Udgang i trumffarven" ved 78,6071 |
| viden/forslag-2klor-kontrolsvar.html på da | 390 | 10 | 2 | 1 | th "Udgang i trumffarven" ved 78,6071 |
| Kortet ff-1430, fuld | 390 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2130 |
| Kortet ff-ass, kompakt | 390 | 8 | 1 | 1 | p "Bruges som hint i træneren: ku" ved 368,2201 |
| Kortet ff-doblinger, kompakt | 1280 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,2756 |
| Kortet ff-dont, kompakt | 390 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,3008 |
| Kortet ff-flannery, fuld | 390 | 1 | 1 | 1 | h2 "Flannery" ved 147,1207 |
| Kortet ff-flannery, fuld | 390 | 8 | 1 | 1 | h2 "Flannery" ved 147,1207 |
| Kortet ff-genaabning, kompakt | 390 | 3 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2193 |
| Kortet ff-gerber, fuld | 1280 | 9 | 1 | 1 | p "Formål At vælge det rigtige sa" ved 804,945 |
| Kortet ff-kravpas, kompakt | 390 | 8 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2157 |
| Kortet ff-lebensohl, fuld | 390 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2066 |
| Kortet ff-michaels, fuld | 390 | 2 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2114 |
| Kortet ff-michaels, fuld | 390 | 10 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2114 |
| Kortet ff-revers, fuld | 390 | 2 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 107,1953 |
| Kortet ff-revers, fuld | 390 | 3 | 1 | 1 | span "Kilde: 2 over 1 · Moderne majo" ved 207,6785 |
| Kortet ff-revers, fuld | 390 | 7 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 107,1953 |
| Kortet ff-revers, kompakt | 390 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,1903 |
| Kortet ff-revers, kompakt | 390 | 7 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,1903 |
| Kortet ff-staerke-genmeldinger, fuld | 390 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2144 |
| Kortet ff-staerke-genmeldinger, fuld | 390 | 9 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2144 |
| Kortet fjerde-farve, fuld | 390 | 7 | 1 | 1 | td.bud.k-gron "1. Støtte" ved 113,2832 |
| Kortet kamp-1ut-forsvar, fuld | 390 | 3 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1989 |
| Kortet kamp-1ut-indmeldt, fuld | 390 | 3 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1905 |
| Kortet kamp-1ut-indmeldt, fuld | 390 | 7 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1905 |
| Kortet kamp-2020, kompakt | 1280 | 6 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,1482 |
| Kortet kamp-forsvar-1ut, kompakt | 390 | 7 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2118 |
| Kortet kamp-gif, kompakt | 1280 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,1767 |
| Kortet kamp-gif, kompakt | 1280 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,1767 |
| Kortet kamp-gif, kompakt | 1280 | 7 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,1767 |
| Kortet kamp-gif, kompakt | 1280 | 8 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,1767 |
| Kortet kamp-stoette-minor, fuld | 390 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1962 |
| Kortet kamp-stoette-off, fuld | 390 | 8 | 1 | 1 | button.chip.lnk "Støtte efter makkers indmeldin" ved 71,5168 |
| Kortet kamp-stoette-off, fuld | 390 | 9 | 1 | 1 | button.chip.lnk "Støtte efter makkers indmeldin" ved 71,5168 |
| Kortet kamp-stoette-off, kompakt | 390 | 7 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2204 |
| Kortet lebensohl, kompakt | 390 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2124 |
| Kortet michaels, kompakt | 390 | 6 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2620 |
| Kortet michaels, kompakt | 1280 | 3 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,2023 |
| Kortet michaels, kompakt | 1280 | 9 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,2023 |
| viden/2-over-1-makker2.html på da | 390 | 1 | 1 | 1 | strong "Kommer indmeldingen først, eft" ved 270,31542 |
| viden/2-over-1-makker2.html på da | 390 | 5 | 1 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på da | 390 | 6 | 1 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på da | 390 | 7 | 1 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på da | 390 | 9 | 1 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på en | 390 | 5 | 1 | 1 | p "Nogle parturneringer scores ef" ved 265,83966 |
| viden/2-over-1-makker2.html på en | 390 | 8 | 1 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på en | 390 | 10 | 1 | 5 | span "♥" ved 222,39739 |
| viden/bridgesystem.html på da | 390 | 4 | 1 | 1 | td "Spørger efter trumfdamen" ved 240,18105 |
| viden/bridgesystem.html på en | 390 | 9 | 1 | 1 | td "Spørger efter trumfdamen" ved 240,18105 |

#### tjek_crowhurst_390.mjs

3350 sammenligninger i 10 runder (335 pr. runde), 184 med forskel, 28 over 5 pixels, 0 med forskel i højden. Største antal pixels: 42590; største farvetrin pr. kanal: 229.

Fordeling (pixels: antal forskelle): 1: 101, 2: 21, 3: 21, 4: 7, 5: 6, 6: 12, 7: 1, 8: 4, 16: 1, 18: 1, 19: 2, 20: 2, 22: 2, 24: 2, 42590: 1

| Side | Bredde | Runde | Pixels | Trin | Første forskel |
| --- | --- | --- | --- | --- | --- |
| viden/2-over-1-makker2.html på da | 399 | 1 | 42590 | 229 | h4 "De tre håndtyper — hvad bestem" ved 274,25884 |
| viden/2-over-1.html på en | 390 | 3 | 24 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/2-over-1.html på en | 390 | 6 | 24 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/2-over-1.html på da | 390 | 4 | 22 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/2-over-1.html på da | 390 | 5 | 22 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/2-over-1.html på da | 399 | 4 | 20 | 5 | span.z4 "37+storeslem" ved 36,6034 |
| viden/2-over-1.html på en | 399 | 4 | 20 | 5 | span.z4 "37+storeslem" ved 36,6034 |
| viden/2-over-1.html på da | 390 | 3 | 19 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/2-over-1.html på en | 390 | 7 | 19 | 1 | span.z1 "12–15minimum" ved 38,7606 |
| viden/2-over-1.html på en | 399 | 7 | 18 | 5 | span.z4 "37+storeslem" ved 36,6034 |
| viden/2-over-1.html på da | 399 | 2 | 16 | 5 | span.z4 "37+storeslem" ved 36,6034 |
| viden/2-over-1.html på da | 390 | 7 | 8 | 1 | p "Pas på med 3♠︎: efter åbners 2" ved 246,15270 |
| viden/bridgesystem.html på da | 399 | 10 | 8 | 1 | p "Svarers 2. melding: 4 i trumff" ved 234,12096 |
| viden/bridgesystem.html på en | 399 | 3 | 8 | 1 | p "Svarers 2. melding: 4 i trumff" ved 234,12096 |
| viden/bridgesystem.html på en | 399 | 4 | 8 | 1 | p "Svarers 2. melding: 4 i trumff" ved 234,12096 |
| viden/bridgesystem.html på da | 390 | 3 | 7 | 1 | td "Minortransfer – klør" ved 165,6216 |
| viden/2-over-1.html på da | 390 | 2 | 6 | 1 | div.felt.vew "NSVØ" ved 156,28369 |
| viden/2-over-1.html på da | 390 | 6 | 6 | 1 | div.felt.vew "NSVØ" ved 156,28369 |
| viden/2-over-1.html på en | 390 | 9 | 6 | 1 | div.felt.vns "NSVØ" ved 158,18359 |
| viden/bridgesystem.html på da | 390 | 5 | 6 | 1 | td "Svarer spørger efter kortfarve" ved 260,12620 |
| viden/bridgesystem.html på da | 399 | 1 | 6 | 1 | td "Spørger efter minorfarven" ved 240,24503 |
| viden/bridgesystem.html på da | 399 | 2 | 6 | 1 | td "Spørger efter minorfarven" ved 240,24503 |
| viden/bridgesystem.html på da | 399 | 4 | 6 | 1 | td "Spørger efter minorfarven" ved 240,24503 |
| viden/bridgesystem.html på da | 399 | 5 | 6 | 1 | td "Spørger efter minorfarven" ved 240,24503 |
| viden/bridgesystem.html på da | 399 | 9 | 6 | 1 | td "Spørger efter minorfarven" ved 240,24503 |
| viden/bridgesystem.html på en | 399 | 1 | 6 | 1 | td "Spørger efter minorfarven" ved 240,24503 |
| viden/bridgesystem.html på en | 399 | 6 | 6 | 1 | td "Spørger efter minorfarven" ved 240,24503 |
| viden/bridgesystem.html på en | 399 | 7 | 6 | 1 | td "Spørger efter minorfarven" ved 240,24503 |
| Kortet ff-doblinger, kompakt | 390 | 8 | 5 | 1 | button.chip.lnk "Negativ dobling, støttedobling" ved 147,799 |
| Kortet ff-doblinger, kompakt | 399 | 3 | 5 | 1 | button.chip.lnk "Negativ dobling, støttedobling" ved 147,799 |
| Kortet ff-flannery, kompakt | 390 | 2 | 5 | 1 | h2 "Flannery" ved 121,1206 |
| viden/2-over-1.html på da | 390 | 8 | 5 | 1 | p "Pas på med 3♠︎: efter åbners 2" ved 246,15270 |
| viden/2-over-1.html på en | 390 | 4 | 5 | 1 | p "Pas på med 3♠︎: efter åbners 2" ved 246,15270 |
| viden/2-over-1.html på en | 390 | 5 | 5 | 1 | p "Pas på med 3♠︎: efter åbners 2" ved 246,15270 |
| Kortet ff-2kl, kompakt | 390 | 3 | 4 | 1 | li.k-gul "Specialaftale, alertér" ved 234,2428 |
| Kortet ff-2kl, kompakt | 390 | 6 | 4 | 1 | li.k-gul "Specialaftale, alertér" ved 234,2428 |
| viden/2-over-1-makker2.html på da | 399 | 3 | 4 | 57 | em "Doblingen skifter altså karakt" ved 86,30639 |
| viden/2-over-1-makker2.html på da | 399 | 7 | 4 | 57 | em "Doblingen skifter altså karakt" ved 86,30639 |
| viden/2-over-1.html på da | 399 | 5 | 4 | 1 | div.felt.vns "NSVØ" ved 160,18058 |
| viden/2-over-1.html på en | 399 | 5 | 4 | 1 | div.felt.vns "NSVØ" ved 160,18058 |
| viden/bridgesystem.html på da | 390 | 9 | 4 | 1 | td "Spørger efter trumfdamen" ved 240,18105 |
| Kortet ff-2kl, kompakt | 399 | 3 | 3 | 1 | li.k-gul "Specialaftale, alertér" ved 234,2428 |
| Kortet ff-2kl, kompakt | 399 | 7 | 3 | 1 | li.k-gul "Specialaftale, alertér" ved 234,2428 |
| Kortet ff-flannery, kompakt | 1280 | 4 | 3 | 1 | li.k-gron "Naturlig / støtte" ved 539,1695 |
| Kortet ff-revideret-omvendt-bergen, kompakt | 390 | 3 | 3 | 1 | li.k-gron "Naturlig / støtte" ved 123,2321 |
| Kortet ff-revideret-omvendt-bergen, kompakt | 390 | 6 | 3 | 1 | li.k-gron "Naturlig / støtte" ved 123,2321 |
| Kortet ff-revideret-omvendt-bergen, kompakt | 399 | 2 | 3 | 1 | li.k-gron "Naturlig / støtte" ved 123,2321 |
| viden/2-over-1-makker2.html på da | 390 | 7 | 3 | 5 | em "Dobler modparten, ændrer det i" ved 86,17573 |
| viden/2-over-1-makker2.html på da | 390 | 8 | 3 | 1 | strong "Kommer indmeldingen først, eft" ved 270,31542 |
| viden/2-over-1-makker2.html på da | 399 | 4 | 3 | 28 | span "♥" ved 222,39178 |
| viden/2-over-1-makker2.html på da | 1280 | 10 | 3 | 6 | p "Når svarer har meldt på 1-trin" ved 715,5256 |
| viden/2-over-1-makker2.html på en | 390 | 10 | 3 | 5 | strong "Kommer indmeldingen først, eft" ved 270,31542 |
| viden/2-over-1-makker2.html på en | 399 | 10 | 3 | 32 | span "♥" ved 222,39178 |
| viden/2-over-1.html på en | 390 | 10 | 3 | 1 | div.felt.vns "NSVØ" ved 158,18359 |
| viden/bridgesystem.html på da | 390 | 1 | 3 | 1 | td "Minortransfer – klør" ved 165,6216 |
| viden/bridgesystem.html på da | 390 | 6 | 3 | 1 | td "Svarer spørger efter kortfarve" ved 260,12620 |
| viden/bridgesystem.html på da | 390 | 7 | 3 | 1 | td "Svarer spørger efter kortfarve" ved 260,12620 |
| viden/bridgesystem.html på da | 390 | 10 | 3 | 1 | td "Svarer spørger efter kortfarve" ved 260,12620 |
| viden/bridgesystem.html på en | 390 | 1 | 3 | 1 | strong "Sekvens" ved 69,25694 |
| viden/bridgesystem.html på en | 390 | 6 | 3 | 1 | td "Svarer spørger efter kortfarve" ved 260,12620 |
| viden/bridgesystem.html på en | 390 | 7 | 3 | 1 | strong "Sekvens" ved 69,25694 |
| viden/bridgesystem.html på en | 390 | 10 | 3 | 1 | td "Svarer spørger efter kortfarve" ved 260,12620 |
| Kortet ff-doblinger, fuld | 390 | 2 | 2 | 1 | button.chip.lnk "Negativ dobling, støttedobling" ved 147,799 |
| Kortet ff-doblinger, fuld | 390 | 9 | 2 | 1 | button.chip.lnk "Negativ dobling, støttedobling" ved 147,799 |
| Kortet ff-dont, kompakt | 1280 | 2 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 524,2436 |
| Kortet ff-genaabning, fuld | 399 | 7 | 2 | 1 | li.k-gron "Naturlig / støtte" ved 122,1901 |
| Kortet ff-genaabning, fuld | 399 | 9 | 2 | 1 | li.k-gron "Naturlig / støtte" ved 122,1901 |
| Kortet ff-genaabning, kompakt | 1280 | 3 | 2 | 1 | p "Genåbn ca. 3 hp lettere end i " ved 713,813 |
| Kortet kamp-1ut-forsvar, fuld | 399 | 4 | 2 | 1 | li.k-gron "Naturlig / støtte" ved 122,1961 |
| Kortet multiforsvar, kompakt | 390 | 2 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 108,2237 |
| Kortet transfer, kompakt | 390 | 6 | 2 | 1 | li.k-gul "Specialaftale, alertér" ved 108,1753 |
| viden/2-over-1-makker2.html på da | 399 | 6 | 2 | 28 | span "♥" ved 222,39178 |
| viden/2-over-1-makker2.html på da | 399 | 8 | 2 | 28 | span "♥" ved 222,39178 |
| viden/2-over-1-makker2.html på da | 399 | 9 | 2 | 28 | span "♥" ved 222,39178 |
| viden/2-over-1-makker2.html på da | 1280 | 9 | 2 | 6 | td "Omvendt minor: 10+ støttepoint" ved 981,43680 |
| viden/2-over-1-makker2.html på en | 390 | 2 | 2 | 1 | strong "Kommer indmeldingen først, eft" ved 270,31542 |
| viden/2-over-1-makker2.html på en | 390 | 6 | 2 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på en | 390 | 9 | 2 | 1 | p "Nogle parturneringer scores ef" ved 265,83966 |
| viden/2-over-1.html på da | 399 | 7 | 2 | 1 | div.felt.vew "NSVØ" ved 156,27925 |
| viden/2-over-1.html på en | 399 | 1 | 2 | 1 | div.felt.vew "NSVØ" ved 156,27925 |
| viden/2-over-1.html på en | 399 | 2 | 2 | 1 | div.felt.vew "NSVØ" ved 156,27925 |
| viden/2-over-1.html på en | 399 | 8 | 2 | 1 | div.felt.vew "NSVØ" ved 156,27925 |
| viden/bridgesystem.html på da | 399 | 6 | 2 | 1 | p "Svarers 2. melding: 4 i trumff" ved 234,12096 |
| Kortet cuebids, kompakt | 399 | 3 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2169 |
| Kortet cuebids, kompakt | 399 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2169 |
| Kortet ff-2kl, kompakt | 1280 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,1582 |
| Kortet ff-ass, kompakt | 390 | 2 | 1 | 1 | p "Bruges som hint i træneren: ku" ved 368,2201 |
| Kortet ff-ass, kompakt | 399 | 4 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 107,2075 |
| Kortet ff-ass, kompakt | 399 | 6 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 107,2075 |
| Kortet ff-doblinger, kompakt | 1280 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 539,2756 |
| Kortet ff-dont, kompakt | 390 | 2 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,3008 |
| Kortet ff-dont, kompakt | 390 | 3 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,3008 |
| Kortet ff-dont, kompakt | 390 | 6 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,3008 |
| Kortet ff-genaabning, fuld | 390 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1901 |
| Kortet ff-genaabning, kompakt | 390 | 2 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2193 |
| Kortet ff-genaabning, kompakt | 390 | 8 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2193 |
| Kortet ff-genaabning, kompakt | 399 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2193 |
| Kortet ff-genaabning, kompakt | 399 | 3 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2193 |
| Kortet ff-genaabning, kompakt | 399 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2193 |
| Kortet ff-gerber, kompakt | 399 | 4 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 107,1969 |
| Kortet ff-kravpas, kompakt | 390 | 2 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2157 |
| Kortet ff-kravpas, kompakt | 399 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2131 |
| Kortet ff-kravpas, kompakt | 399 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2131 |
| Kortet ff-lebensohl, fuld | 390 | 3 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2066 |
| Kortet ff-lebensohl, fuld | 390 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2066 |
| Kortet ff-lebensohl, fuld | 390 | 6 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2066 |
| Kortet ff-lebensohl, fuld | 399 | 2 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2034 |
| Kortet ff-michaels, kompakt | 390 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2937 |
| Kortet ff-michaels, kompakt | 390 | 6 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2937 |
| Kortet ff-omvendt-minor, fuld | 1280 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 350,1219 |
| Kortet ff-revers, fuld | 390 | 2 | 1 | 1 | span "Kilde: 2 over 1 · Moderne majo" ved 207,6785 |
| Kortet ff-revers, kompakt | 390 | 6 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,1903 |
| Kortet ff-revers, kompakt | 390 | 9 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,1903 |
| Kortet ff-revers, kompakt | 399 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,1903 |
| Kortet ff-revers, kompakt | 399 | 2 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,1903 |
| Kortet ff-revideret-omvendt-bergen, fuld | 399 | 7 | 1 | 1 | span "Kilde: 2 over 1 · Moderne majo" ved 199,5349 |
| Kortet ff-staerke-genmeldinger, fuld | 390 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2144 |
| Kortet ff-staerke-genmeldinger, kompakt | 399 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2743 |
| Kortet ff-trial-bids, fuld | 399 | 7 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1902 |
| Kortet ff-trial-bids, fuld | 399 | 10 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1902 |
| Kortet fjerde-farve, fuld | 390 | 6 | 1 | 1 | td.bud.k-gron "1. Støtte" ved 113,2832 |
| Kortet forslag-2kl-kontrolsvar, fuld | 390 | 6 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,2048 |
| Kortet kamp-1ut-forsvar, fuld | 390 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1989 |
| Kortet kamp-1ut-forsvar, kompakt | 390 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2260 |
| Kortet kamp-1ut-forsvar, kompakt | 390 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2260 |
| Kortet kamp-1ut-indmeldt, kompakt | 390 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2057 |
| Kortet kamp-1ut-indmeldt, kompakt | 390 | 2 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2057 |
| Kortet kamp-1ut-indmeldt, kompakt | 399 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2057 |
| Kortet kamp-forsvar-1ut, fuld | 390 | 4 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1957 |
| Kortet kamp-forsvar-1ut, fuld | 390 | 7 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1957 |
| Kortet kamp-forsvar-1ut, fuld | 399 | 7 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1957 |
| Kortet kamp-forsvar-1ut, kompakt | 399 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2118 |
| Kortet kamp-gif, fuld | 399 | 6 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1933 |
| Kortet kamp-gif, fuld | 399 | 8 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1933 |
| Kortet kamp-stoette-def, fuld | 399 | 2 | 1 | 1 | button.chip.lnk "Støtte efter indmelding over m" ved 71,5553 |
| Kortet kamp-stoette-def, fuld | 399 | 6 | 1 | 1 | button.chip.lnk "Støtte efter indmelding over m" ved 71,5553 |
| Kortet kamp-stoette-minor, fuld | 399 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1962 |
| Kortet kamp-stoette-minor, kompakt | 390 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2125 |
| Kortet kamp-stoette-minor, kompakt | 390 | 2 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2125 |
| Kortet kamp-stoette-minor, kompakt | 399 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2125 |
| Kortet kamp-stoette-minor, kompakt | 1280 | 1 | 1 | 1 | button.chip.lnk "Minorstøtte og negativ dobling" ved 803,431 |
| Kortet kamp-stoette-off, fuld | 390 | 4 | 1 | 1 | button.chip.lnk "Støtte efter makkers indmeldin" ved 71,5168 |
| Kortet kamp-stoette-off, kompakt | 390 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2204 |
| Kortet kamp-stoette-off, kompakt | 390 | 9 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2204 |
| Kortet lebensohl, kompakt | 399 | 5 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2124 |
| Kortet lebensohl, kompakt | 399 | 6 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2124 |
| Kortet michaels, kompakt | 390 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2620 |
| Kortet michaels, kompakt | 399 | 7 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2620 |
| Kortet michaels, kompakt | 399 | 10 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 123,2620 |
| Kortet stayman, fuld | 399 | 1 | 1 | 1 | li.k-gron "Naturlig / støtte" ved 122,1905 |
| Kortet stayman, kompakt | 390 | 1 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 108,1985 |
| Kortet stayman, kompakt | 390 | 5 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 108,1985 |
| Kortet stayman, kompakt | 390 | 6 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 108,1985 |
| Kortet transfer, kompakt | 399 | 3 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 275,1728 |
| Kortet transfer, kompakt | 399 | 6 | 1 | 1 | li.k-gul "Specialaftale, alertér" ved 275,1728 |
| viden/2-over-1-makker2.html på da | 390 | 3 | 1 | 1 | em "Ét hul er markeret ærligt: RKC" ved 231,86637 |
| viden/2-over-1-makker2.html på da | 390 | 4 | 1 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på da | 390 | 5 | 1 | 1 | p "Nogle parturneringer scores ef" ved 265,83966 |
| viden/2-over-1-makker2.html på da | 390 | 6 | 1 | 1 | p "Nogle parturneringer scores ef" ved 265,83966 |
| viden/2-over-1-makker2.html på da | 390 | 10 | 1 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på da | 399 | 2 | 1 | 32 | span "♥" ved 100,55572 |
| viden/2-over-1-makker2.html på da | 399 | 5 | 1 | 32 | span "♥" ved 100,55572 |
| viden/2-over-1-makker2.html på en | 390 | 1 | 1 | 1 | em "Ét hul er markeret ærligt: RKC" ved 231,86637 |
| viden/2-over-1-makker2.html på en | 390 | 3 | 1 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på en | 390 | 4 | 1 | 1 | em "Ét hul er markeret ærligt: RKC" ved 231,86637 |
| viden/2-over-1-makker2.html på en | 390 | 7 | 1 | 5 | span "♥" ved 222,39739 |
| viden/2-over-1-makker2.html på en | 390 | 8 | 1 | 1 | p "Nogle parturneringer scores ef" ved 265,83966 |
| viden/2-over-1-makker2.html på en | 399 | 3 | 1 | 32 | span "♥" ved 100,55572 |
| viden/2-over-1-makker2.html på en | 399 | 6 | 1 | 5 | span "♥" ved 303,47545 |
| viden/2-over-1-makker2.html på en | 399 | 7 | 1 | 32 | span "♥" ved 100,55572 |
| viden/2-over-1-makker2.html på en | 399 | 8 | 1 | 32 | span "♥" ved 100,55572 |
| viden/2-over-1-makker2.html på en | 399 | 9 | 1 | 5 | span "♥" ved 303,47545 |
| viden/2-over-1-makker2.html på en | 1280 | 7 | 1 | 6 | span "♥" ved 853,54609 |
| viden/2-over-1-makker2.html på en | 1280 | 10 | 1 | 1 | td "Omvendt minor: 10+ støttepoint" ved 981,43680 |
| viden/bridgesystem.html på da | 390 | 8 | 1 | 1 | td "Spørger efter trumfdamen" ved 240,18105 |
| viden/bridgesystem.html på da | 1280 | 8 | 1 | 1 | strong "Sekvens" ved 436,16680 |
| viden/bridgesystem.html på en | 1280 | 9 | 1 | 1 | strong "Sekvens" ved 436,16680 |
| viden/forslag-2klor-kontrolsvar.html på da | 399 | 2 | 1 | 1 | p "Kontrolsvar er aftalt i system" ved 112,9344 |
| viden/forslag-2klor-kontrolsvar.html på da | 399 | 6 | 1 | 1 | p "Kontrolsvar er aftalt i system" ved 112,9344 |
| viden/forslag-2klor-kontrolsvar.html på en | 399 | 1 | 1 | 1 | p "Kontrolsvar er aftalt i system" ved 112,9344 |
| viden/forslag-2klor-kontrolsvar.html på en | 399 | 2 | 1 | 1 | p "Kontrolsvar er aftalt i system" ved 112,9344 |
| viden/forslag-2klor-kontrolsvar.html på en | 399 | 4 | 1 | 1 | p "Kontrolsvar er aftalt i system" ved 112,9344 |
| viden/kampen-om-kontrakten.html på da | 1280 | 9 | 1 | 1 | p "Tre-trins-raketten gælder kun " ved 651,13551 |
| viden/kampen-om-kontrakten.html på en | 1280 | 8 | 1 | 1 | p "Tre-trins-raketten gælder kun " ved 651,13551 |



## Arbejdsgang

1. Tag `v-foer-pixeltolerance`, og opret grenen `pixeltolerance`.
2. Lav målingen (del 1), og skriv accepttestene, som skal være røde.
3. Byg ændringen.
4. Stop før merge til Franks gennemgang.
5. Efter "godkendt": flet, push og kør begge scripts med `--live`. Arkivér specen, og slet grenen lokalt og på GitHub.
