# SPEC-viden-320

5. november 2026 · Franks valg. Bygget på grenen `viden-320`; `main` før er tagget `v-foer-viden-320`. Godkendt af Frank, flettet og udgivet 5. november 2026 (`e987ab4`); de udgivne sider er tjekket ved 320 px, og grenen er slettet.

Siderne i `viden/` må ikke give vandret scroll ved 320 px. Punktet stod under Kendte forbehold i `../SYSTEM.md` for `viden/2-over-1.html`, hvor opgaverne stak 20 px ud. Målingen viste, at også andre sider i `viden/` stikker ud.

## Afgrænsning

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| Siderne i `viden/` under 360 px | layoutet tilpasses, så intet stikker ud, og intet skjules | indholdet ændres |
| Ved 390 og 1280 px | intet | noget flytter sig; siderne er pixel for pixel som før |
| `overflow` på `html` og `body` | intet | vandret scroll fjernes ved at skjule det, der stikker ud |

## Accepttest

- [x] `node tools/tjek_viden_320.mjs`: ingen vandret scroll ved 320, 340, 360 og 375 px på alle sider i `viden/`, på dansk og engelsk, med `<details>` lukket og åbne.
- [x] Samme tjek ved 320 og 375 px på alle konventionskort i deres visninger; kortene står i en shadow root, og målingen går også derind.
- [x] Hverken `html` eller `body` skjuler noget med `overflow`.
- [x] Ved 390 og 1280 px er alle sider og kort pixel for pixel som `v-foer-viden-320`.
- [x] `tools/tjek_sidefod.mjs` måler igen hele siden ved 320 px på alle sine sider, også `viden/2-over-1.html`.
- [x] Sprog, fagord, beskrivende form og skrifttyper er grønne.

Kørt 5. nov. 2026 på grenen: `tjek_viden_320.mjs` 792 tjek i orden (ét forsøg med støj, se Afklaret 9), `tjek_sidefod.mjs`, `tjek_skrifttyper.mjs`, `tjek_bred_multi.mjs` og de ni Python-tjek (konventionskort, kort_eksempler, fagord, bydeform, sprog, skrifttyper, makker2_aftaler, makker2_bilag_c, crowhurst) i orden.

Giv Frank udsnit ved 320 px før og efter. Frank godkender, før der flettes.

## Afklaret

1. **Fire sider og kortene, ikke kun 2-over-1** (målt 5. nov. 2026 på `v-foer-viden-320`): `2-over-1` (opgaverne +20 px), `bridgesystem` (ordet "Konkurrencemeldinger" i overskriften +17 px), `forslag-2klor-kontrolsvar` (tabellen `table.abner` +2 px) og `konventionskort` (siden +3 px, og alle 49 kort stak ud i fuld visning, crowhurst og kamp-kortene mest).
2. **Rettelserne:**
   - `2-over-1`: opgaverne må blive smallere end 19rem (`minmax(min(19rem,100%),1fr)`), og afstanden mellem spillenes kolonner er mindre under 360 px (`.deal{ gap:.45rem .35rem }` i en `max-width:359px`-regel). Kompasset beholder målene fra reglen for 430 px (4.4rem). Første udgave gjorde det 3.4rem, og så ramte bogstaverne og ringen om giveren hinanden med op til 5 × 4 px. En måling af alle 7 spil ved 320, 340 og 359 px viste, at kompasset aldrig bestemmer kolonnens bredde (det gør Nords og Syds hånd), så det gav ingen plads at gøre det mindre. Med 4.4rem og den mindre afstand stikker intet ud. Kompasset er med på billederne ved 320 px før og efter (`320-2-over-1-spil-*.png`; Franks krav 5. nov. 2026).
   - `assets/doc-sg.css`: overskriften er 23 px under 360 px. Det gælder også `2-over-1-makker2` og `kampen-om-kontrakten`, der bruger samme stylesheet.
   - `forslag-2klor-kontrolsvar`: tabellens celler har mindre luft til siderne under 360 px.
   - Konventionskortet (`tools/konventionskort.src.html`, bygget med `tools/build_konventionskort.py`): chips og sidefod må brække under 390 px, og fanerne og overskriften er mindre under 360 px. Ved 320 px fordeler chippene sig anderledes på linjerne (fx står "Overføringer" ikke længere efter "Amerikansk Stayman (ASS)"). Chippene er lige brede før og efter, men før var chipfeltet 16–323 px, bredere end skærmen, fordi den lange chip "Åbners stærke genmeldinger og 3♣ checkback" ikke kunne brække. Nu er feltet 16–304 px, og den lange chip står på to linjer.
3. **Brudpunkterne** (Franks spørgsmål 5. nov. 2026): "under 390 px" er `max-width:389px`, og "under 360 px" er `max-width:359px`, så ingen regel gælder ved præcis 390 eller 360 px. `.quiz`-reglen står ikke i en `@media`-regel, men `min(19rem,100%)` er det samme som 19rem, så længe boksen er mindst 304 px bred. Boksen er skærmbredden minus 40 px (`.page` har 1.25rem luft i hver side), så reglen virker først under 344 px.
4. **Hint-vinduet** (Franks valg 5. nov. 2026: i orden): kortenes regler står også i `assets/konventionskort-hint.js`, som bygges fra samme kilde, så de gælder også i hint-vinduet i `traener.html`, `multi-svar-traener.html` og `markering.html` under 390 px.
5. **`doc-sg.css?v=2026-10-18` er uændret:** reglen virker kun under 360 px, og GitHub Pages lader browseren gemme filen i 10 minutter. De tre sider, der henter filen, og `tools/build_kamp_viden.py` er derfor ikke rørt.
6. **Testen hang** ved pixelsammenligningen ved 390 px. Den havde en fane til siden før og en til siden nu i samme vindue, og Chrome tegner ikke en fane, der ligger bagved, så skærmbilledet af den kom aldrig. Et svar fra browseren, der udebliver i 60 s, er nu en fejl i stedet for en test, der aldrig slutter.
7. **De 15 pixelfejl ved 390 og 1280 px** (første hele kørsel, med to faner, der blev bragt frem på skift): konventionskortsiden var 2902 px høj mod 5903 px før, og 14 sider og kort havde 1–3 pixels forskel. Sådan blev de prøvet: seks af dem (forslag-2klor ved 390 px på engelsk, konventionskortsiden ved 390 px, stayman kompakt og ff-michaels fuld ved 390 px, bridgesystem ved 1280 px og usaedvanlig-2nt kompakt ved 1280 px) blev taget tre gange fra tagget og tre gange fra grenen, efter hinanden i én fane med tom `localStorage`. Før mod før, nu mod nu og før mod nu var ens pixel for pixel i alle seks. Højden skyldtes, at kortsiden husker sidste kort og visning i `localStorage` (`kk-konv`, `kk-visning`) for hver adresse. Testen havde lige klikket alle kort igennem på grenens adresse, så siden nu åbnede på et andet kort end siden før. En kørsel med én fane og ryddet `localStorage` gav stadig 1–3 pixels på to tilfælde (2-over-1 ved 390 px på engelsk og stayman kompakt ved 390 px) og blev stoppet.
8. **Hvert skærmbillede i sin egen browserkontekst** (Franks krav 5. nov. 2026): testen åbner hver side i en ny browserkontekst (`Target.createBrowserContext`), som et nyt privat vindue med tom `localStorage` og kun én fane, og kasserer den bagefter. Der skiftes aldrig fane, og resultatet afhænger ikke af rækkefølgen. Det gælder siden før og siden nu i pixelsammenligningen, hver side og hvert sprog ved de smalle bredder og billederne til Frank. Ved de smalle bredder klikkes kortene igennem i én kontekst pr. sprog, fordi målingen kun ser på det kort, der står fremme. Er der en pixelforskel, siger fejlen, hvor den sidder, farven før og nu og elementet dér.
9. **Støj fra Chrome:** den første kørsel med nye kontekster gav 1 fejl af 792: én pixel i et ♥ på `2-over-1-makker2` ved 1280 px på engelsk, ved y = 54609 px, med en farveforskel på 6 i to kanaler. Samme sammenligning blev taget fem gange hver vej. Før mod nu var ens alle fem gange, men i én runde var både før mod før og nu mod nu én pixel forskellige (231 mod 232 i én kanal, ved y = 43680 px), selvom filerne var de samme. Chrome tegner altså en sjælden gang én pixel en anelse anderledes på meget lange sider. En ændring kommer igen hver gang, støj gør ikke. Derfor skal en forskel nu være der i tre forsøg i træk, hvert med nye kontekster, og hvert forsøg kræver stadig pixel for pixel. Et forsøg med støj står som en `NB`-linje i testens udskrift.

10. **De udgivne sider** (5. nov. 2026, efter GitHub Pages-udrulningen af `e987ab4`): `tools/tjek_viden_320.mjs ingen` mod www.kontraktbridge.dk/konventionstraener/ gav 568 tjek i orden, det samme antal som lokalt. Det var alle sider og alle 49 kort ved 320, 340, 360 og 375 px, på dansk og engelsk, lukket og foldet ud. Testen har ingen `--live`, så den blev kørt fra en kopi, hvor siden nu er sitets adresse. Pixelsammenligningen ved 390 og 1280 px blev ikke kørt mod sitet, fordi den sammenligner med tagget lokalt.

## Åbne punkter

- **Crowhurst-kortet ved 390–398 px** (Franks valg 5. nov. 2026: rettes ikke her; rettet med `SPEC-crowhurst-390.md`, godkendt af Frank og udgivet 6. nov. 2026): kortet giver vandret scroll i fuld visning, 9 px ved 390 px, 4 px ved 395 px og intet fra 399 px, også på `v-foer-viden-320` (målt 5. nov. 2026). Kompakt visning er i orden. Årsagen er chippen "Crowhurst (checkback efter åbners 1NT-genmelding)" i kortet: den er 343 px bred og må ikke brække over 389 px, så kortets kolonne bliver 383 px i en side, der har 358 px. Punktet rettes ikke her, fordi 390 px skal være pixel for pixel som før. Det tages på en egen gren bagefter og står under Kendte forbehold i `../SYSTEM.md`.
