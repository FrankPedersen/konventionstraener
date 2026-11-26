# SPEC-modspilsaftaler

26. november 2026 · Rådgiverens spec, **godkendt af Frank 26. nov.** Opgave B i `PLAN-aabne-opgaver.md`. Bygges i Konventionstræner på grenen `modspilsaftaler`; `main` før tagges `v-foer-modspilsaftaler`.

## Formål

Modspilsaftalerne bliver konventionskort uden makker: hver aftale beskrives med alle de varianter, Modspil i Fordelingstræneren træner, og brugeren vælger sine varianter i en indstilling. Kortene, eksemplerne og quizzen følger valget. Der er intet overlap med Modspil (Franks valg 24. nov.): kortene beskriver aftalerne, og quizzen spørger kun til aftalernes indhold, ikke til aflæsning eller valg af kort. Hvert kort har linket "Træn i Modspil" til `/fordelingstraeneren/#modspil`.

## Beslutninger (26. nov.)

1. **Varianterne vælges i indstillingerne** (Franks ønske 26. nov.).
2. **Alle Modspils varianter kommer med.** Facit findes allerede: `Fordelingstræneren/src/modspil/content/metoder.json` har 7 kategorier med i alt 17 metoder og tre profiler. Specen tilføjer ingen variant, som ikke står dér.
3. **Indstillingen er den samme som Modspils profiler** (rådgiverens anbefaling, fulgt af Frank 26. nov.): profilerne Standard, Omvendt og Kompendiet plus "egen", hvor hver kategori vælges for sig, med de samme id'er og navne som i Modspil.
4. **Ét fælles valg for begge apper** (Franks valg 26. nov.): et skift i Konventionstræner ændrer også valget i Modspil (se Indstillingen).

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
- Session 1 undersøger, om `traener.html` kan vise et spørgsmål uden hånd. Hvis ikke, bygges den mindste ændring, der kan, og den beskrives under Afklaret.

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
