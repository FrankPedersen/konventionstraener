# SPEC-muiderberg

21. november 2026 · Frank · rettet 24. november 2026 (rådgiverens forslag, se Afklaret 8–11)

En ny træner for **Muiderberg (Bikini) 2♥ og 2♠**. Den bygges efter `SPEC-multi-2ru.md` er flettet ind og genbruger dens mønster: et modul i `dealer/`, en pulje i `pools/`, en post i `data/konventioner.json` og et konventionskort i `data/kort/`. Træningssiden er den fælles `traener.html?k=muiderberg`. Der kommer ingen nye skærmbilleder, så der laves ingen mock-up.

**Forudsætning:** Multi 2♦ (`multi-2ru`) er godkendt og udgivet. Opfyldt 24. november 2026 (fletning `9ce90ee`).

Muiderberg står i dag som "kommer" under Forslag (`ff-muiderberg`, kun 2♠, afsnit B4 i Makker 2-dokumentet). Den nye træner afløser den post (Afklaret, punkt 1).

## Kilderne

1. **Franks tekst af 21. november 2026 (F).** Den er hovedkilden og står i sin helhed nedenfor.
2. **Word-dokumentet "Ruder Multi" (W)** (`C:\Users\frank\Kontraktbridge\Ruder_Multi.docx`, afsnittet om Bikini). Det er enigt med F om åbningen, 3♣ og 2NT-relæet og tilføjer én regel: en ny farve fra en stærk svarhånd er naturlig og krav i én runde. Dokumentet må ikke lægges i repoet.

### Franks tekst (F)

Hvis makkerparret anvender Multi 2♦ til svage hænder med 6-farve i major, kan 2♥ og 2♠ anvendes som Muiderberg-åbninger.

**Åbningen viser:**
- ca. 5–10 hp;
- en 5-korts majorfarve;
- mindst en 4-korts minorfarve.

| Åbning | Betydning |
| --- | --- |
| 2♥ | 5+ hjerter og 4+ kort i en ukendt minor. |
| 2♠ | 5+ spar og 4+ kort i en ukendt minor. |

Mange par spiller ved ugunstig zonestilling, at minorfarven normalt skal være mindst 5 kort.

**Svar:**

| Svar | Betydning |
| --- | --- |
| Pas | Præference til åbners major. |
| 3♣ | Pas eller ret: ønske om at spille i åbners minor. Med klør passes, med ruder meldes 3♦. |
| 2NT | Kunstigt, stærkt spørgebud. |
| 3♥ / 3♠ | Enkeltløft i åbners major: spærrepræget og ikke krav (RONF). |
| 4♥ / 4♠ | Slutkontrakt. |

**2NT-relæet** spørger om både minorfarve og styrke:

| Svar | Betydning |
| --- | --- |
| 3♣ | Minimum med klør. |
| 3♦ | Minimum med ruder. |
| 3♥ | Maksimum med klør. |
| 3♠ | Maksimum med ruder. |

Efter svaret vælger makker mellem delkontrakt, udgang og slem.

**Eksempel:** ♠KBT75 ♥73 ♦98 ♣KD65 åbner 2♠. Hånden viser 5 spar, mindst 4 kort i en ukendt minor og en svag åbningshånd.

Muiderberg kaldes også Bikini, Lucas Two Bids eller Dutch Two Bids. Navnet Bikini henviser humoristisk til håndtypen: "lidt foroven og lidt forneden" (major + minor).

## Afgrænsning

Før arbejdet starter:

1. Commit og tag den nuværende side som `v-foer-muiderberg`.
2. Arbejd på grenen `muiderberg`, og flet først ind efter Franks godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `dealer/muiderberg.py` (ny) | Generator og bedømmelse efter reglerne nedenfor, med `export_pool(path)`. | — |
| `build_pools.py` | Tilføje `"muiderberg": muiderberg` i `CONVENTIONS`. | Ændre andre konventioner. |
| `pools/muiderberg.json` (ny) | Genereres med `python build_pools.py muiderberg`. | Rettes i hånden. |
| `data/konventioner.json` | Én ny post (se nedenfor), og posten `ff-muiderberg` fjernes. | Ændre de øvrige poster. |
| `data/kort/muiderberg.json` (ny), `data/kort/index.json` | Et nyt kort efter skabelonen, med `traener`-feltet. | Tal, som kilderne ikke angiver. |
| `data/kort/multi-2ru.json` | Under "Åbne spørgsmål" erstattes Bikini-linjen af en henvisning til Muiderberg-kortet. | Andre ændringer. |
| `viden/konventionskort.html`, `assets/konventionskort-hint.js` | Bygges med `python3 tools/build_konventionskort.py`. | Rettes i hånden. |
| `tools/tjek_muiderberg.py` (ny) | Accepttesten. | — |
| `tools/tjek_viden_320.mjs`, `tools/tjek_crowhurst_390.mjs` | Tallet for kortene rettes fra 50 til 51, og `muiderberg` tjekkes kun for vandret scroll. Siden før henter `data/kort/index.json` og `data/kort/multi-2ru.json` fra commit H, den sidste commit i session 1, der ændrer dem. H står i `NYERE` og under Afklaret. | Andre ændringer. Session 2 må ikke ændre de tre filer. |
| `../SYSTEM.md` (ikke i git) | En linje i beslutningsloggen for hver session og datoen øverst, som ved Multi 2♦. | Hemmeligheder. |
| `viden/2-over-1-makker2.html`, `dealer/multi_2ru.py`, `traener.html`, `dealer/core.py` | Intet. | Alt. |
| Sprog | Som i `SPEC-multi-2ru.md`: `tx('dansk', 'English')`, husets ord og beskrivende form. | Dansk tekst på den engelske side. |

## Situationer

| Situation | Rolle | Meldeforløb | Meldinger at vælge imellem |
| --- | --- | --- | --- |
| `aabning` | Åbner | – | Pas, 1♥, 1♠, 2♦, 2♥, 2♠ |
| `svar` | Svarer | 2♥ eller 2♠ – Pas – ? | Pas, 2♠ (efter 2♥), 2NT, 3♣, 3♦, 3♥, 3♠, 4♥, 4♠ |
| `ret` | Åbner | 2M – Pas – 3♣ – Pas – ? | Pas, 3♦, 3M |
| `spm` | Åbner | 2M – Pas – 2NT – Pas – ? | 3♣, 3♦, 3♥, 3♠, 3NT |

## Regler

### `aabning`
- **2♥ / 2♠:** Præcis fem kort i majoren, 4–5 kort i en minor, højst tre kort i den anden major og 5–10 hp.
- **2♦ (Multi):** Seks kort i en major efter `multi-2ru`'s regler. Hænderne er med, så brugeren skelner mellem 5-4 og en seksfarve.
- **1♥ / 1♠:** Samme fordeling som 2♥/2♠ med 11–15 hp.
- **Pas:** Samme fordeling med 0–4 hp.

### `ret`
Pas med klør og 3♦ med ruder. 3M er en forkert valgmulighed.

### `spm`
- 3♣ viser minimum med klør.
- 3♦ viser minimum med ruder.
- 3♥ viser maksimum med klør.
- 3♠ viser maksimum med ruder.

### `svar`
Reglerne prøves i rækkefølgen under Grænser. Den første regel, der passer, giver svaret.

## Grænser, som kilderne ikke giver tal for – ret dem her

```python
# --- Grænser, som kilderne ikke giver tal for – ret dem her ------------
MIN_HP, MAX_HP = (5, 7), (8, 10)            # åbners minimum og maksimum inden for 5–10

# svar: 2M – Pas – ?  (første regel, der passer)
UDGANG       = dict(stoette=3, hp=(13, 16))  # 4M: 3+ i åbners major, 13–16 hp
SPAER_UDGANG = dict(stoette=4, hp=(0, 10))   # 4M: 4+ i åbners major, højst 10 hp (spærrende)
SPOERG       = dict(hp=17)                   # 2NT: 17+ hp,
SPOERG_INVIT = dict(stoette=3, hp=(11, 12))  #      eller 3+ støtte og 11–12 hp
ENKELTLOEFT  = dict(stoette=3, hp=(6, 10))   # 3M: præcis 3 i åbners major, 6–10 hp (RONF)
MINOR_RET    = dict(major_max=1, minor=3, hp_max=10)  # 3♣: højst 1 i åbners major, 3+ i begge minorer, højst 10 hp
# Pas: 2+ i åbners major og højst 10 hp
# Ny farve (W: naturlig og krav) og 2♠ efter 2♥ genereres ikke (Afklaret, punkt 3)
# En svarhånd, der ikke rammer en regel, genereres ikke (Afklaret, punkt 9)
```

**Hænder uden regel:** Reglerne dækker ikke alle svarhænder, fx 11–16 hp med højst 2 kort i åbners major, eller en kort major uden 3+ i begge minorer og højst 10 hp. Sådanne hænder melder i praksis ny farve eller 2NT, som ikke trænes, og de genereres derfor ikke.

**Kontrol:** Franks eksempel ♠KBT75 ♥73 ♦98 ♣KD65 har 9 hp, fem spar og fire klør, så det giver 2♠.

## Post i data/konventioner.json

```json
{
  "id": "muiderberg",
  "titel": "Muiderberg (Bikini) 2♥/2♠",
  "gruppe": "Åbninger",
  "emne": "aabninger",
  "beskrivelse": "2♥/2♠ viser en femfarve i majoren og en firfarve i en ukendt minor, ca. 5–10 hp. Pas og løft er præference, 3♣ er pas eller ret til åbners minor, og 2NT spørger om minor og styrke.",
  "roller": ["Åbner", "Svarer"],
  "status": "klar",
  "system": "generel",
  "viden": "viden/konventionskort.html#muiderberg",
  "en": {
    "titel": "Muiderberg (Bikini) 2♥/2♠",
    "gruppe": "Openings",
    "beskrivelse": "2♥/2♠ show five cards in the major and four in an unknown minor, about 5–10 HCP. Pass and raises are preference, 3♣ is pass-or-correct to opener's minor, and 2NT asks for the minor and strength."
  }
}
```

## Konventionskortet

`data/kort/muiderberg.json` følger skabelonen (`type: "melding"`) og har tal kun fra kilderne.

1. **Meldinger:** Åbningen og svarene.
2. **Fortsættelser:** 2NT-relæet og åbners svar på 3♣.
3. **Indmelding:** Kilderne siger intet. Afsnittet henviser til "Åbne spørgsmål".
4. **Eksempler:** Franks eksempel og hænder fra puljen.
5. **Faldgruber:**
   - 3♣ er pas eller ret, ikke egen farve.
   - 3M er spærrende og ikke krav.
   - Med seks kort i majoren åbnes 2♦ (Multi).
6. **Åbne spørgsmål:**
   - Minorfarven ved ugunstig zone (mindst 5 kort).
   - Ny farve fra en stærk svarhånd (W: naturlig og krav).
   - Meldingerne efter modpartens dobling og indmelding.

Kortet nævner, at Muiderberg forudsætter Multi 2♦, og henviser til `multi-2ru`.

**Tekster til gennemgang:** Alle forklaringer, faldgruber og bonusspørgsmål står i en tabel under Afklaret med kilden (F, W eller "(tilføjelse)"). Står der intet i F, ser agenten i W, før den spørger. Agentens egne begrundelser markeres "(tilføjelse)". Frank godkender tabellen før fletning.

## Accepttest

`python3 tools/tjek_muiderberg.py` skrives først og skal være rød. Den tjekker syv ting:

1. Franks eksempel giver 2♠.
2. `ret` og `spm` giver tabellens svar for alle kombinationer af major, minor og minimum eller maksimum.
3. Puljen har alle fire situationer. Hver melding, der genereres, har mindst 7 hænder, og `build_pools.py` skriver ingen "Advarsel: kun …".
4. For hver hånd er `correct` det svar, reglerne giver. Hver svarhånd i `svar` rammer en regel. Alle åbnerhænder i `svar`, `ret` og `spm` er gyldige Muiderberg-åbninger.
5. Posten `muiderberg` findes, og `ff-muiderberg` er væk.
6. `tjek_konventionskort.py`, `tjek_kort_eksempler.py muiderberg`, `tjek_fagord.py`, `tjek_bydeform.py` og `tjek_sprog.py` melder "i orden".
7. Tabellen "Tekster til gennemgang" findes under Afklaret og har en kilde i hver række.

Desuden åbnes `traener.html?k=muiderberg` på dansk og engelsk ved 1280, 390 og 320 px. Skærmbillederne gemmes i `C:\Users\frank\Kontraktbridge\skaermbilleder\muiderberg\`. De skal vise:
- `svar` med forklaring;
- `spm`;
- ⓘ med kortet åbent;
- 320 px uden vandret scroll.

## Trin

To korte sessioner (Styring, punkt 7–11). Frank sender `/usage` (5 timer og uge) før og efter hver session.

1. **Session 1 (Opus, high effort):**
   - Tag og gren.
   - Skriv accepttesten (rød), kortet, generatoren og puljen.
   - Ret posterne, og byg kortsiden.
   - Kør testen, til den er grøn.
   - Stop og rapportér med H og tabellen "Tekster til gennemgang". Hvis en grænse ikke kan give nok hænder, stopper sessionen og spørger.
   - Bliver sessionen lang, stopper den efter den røde accepttest og kortet, og generatoren tages i en ny session (1b, Opus, high effort).
2. **Session 2 (Sonnet, medium effort, `/model`):** Hele testsuiten én gang i forgrunden, i en ny session. Tag skærmbillederne, stop før fletning, og rapportér med tokenforbruget.

Efter Franks "godkendt" (Sonnet, medium effort): flet, push, live-tjek, arkivér specen i `docs/specs/` med en linje i `README.md`, og slet grenen.

## Afklaret

1. **Ny generel træner i stedet for `ff-muiderberg`.** Ligesom Multi bliver Muiderberg en generel træner med system "generel", og posten "kommer" fjernes. Frank har bedt om den (21. november 2026).
2. **F gælder, og W udfylder hullerne.** B4 i Makker 2-dokumentet (kun 2♠, ny farve naturlig og ikke krav, 2NT viser minoren billigst) står uændret som Makker 2's forslag.
3. **Ny farve og 2♠ efter 2♥ trænes ikke.** F nævner dem ikke. W siger, at en ny farve er naturlig og krav, men giver ingen grænser. Meldingerne står som valgmuligheder, men er aldrig det rigtige svar.
4. **Zonestilling trænes ikke.** Træneren giver ingen zone, og minoren er 4–5 kort.
5. **Grænserne er antagelser.** Tallene er rådgiverens forslag. Frank kan rette dem før session 1.
6. **To kørsler** (Franks spørgsmål 21. november 2026). Multi og Muiderberg rører de samme filer, og planen siger én opgave pr. repo ad gangen. Muiderberg starter derfor først, når Multi er udgivet.

7. **Omfanget** (Franks valg 21. november 2026): håndtypen for 2♥/2♠; svarene pas, 3♣ (pas eller ret), løft af major og 2NT-relæet; og svarene på 2NT. Åbners pas/3♦ efter 3♣ hører med til 3♣, og Multi 2♦ er med som valgmulighed i `aabning` (rådgiverens anbefaling; Frank kan fjerne dem).

8. **Spærreløftet til 10 hp** (rådgiverens forslag 24. november 2026): med 4 trumf og 10 hp er 4M bedre end pas, så `SPAER_UDGANG` går til 10 hp. Frank kan rette det før session 1.
9. **Hænder uden regel genereres ikke** (rådgiverens forslag 24. november 2026). Se "Hænder uden regel" under Grænser.
10. **Pixeltestene** (som Multi 2♦, Franks svar 24. november 2026): kortene bliver 51, `muiderberg` tjekkes for vandret scroll, og de andre sammenlignes med siden før, der henter de ændrede filer fra H.
11. **Forsidens tal:** Muiderberg erstatter en "kommer"-post med en træner med status "klar", så tallet i forsidens topbånd bliver 47. Det rettes på næste gren i Forside sammen med sidefoden, ikke i denne opgave.

**Tokenforbrug** (nye input · skrevet til cachen · læst fra cachen · output):
- Session 1: 144 · 289.555 · 13.654.337 · 92.176; i alt 14.036.212
- Session 2:
- Efter godkendelsen:

### Session 1 (24. nov. 2026)

**Status:** Tag og gren er lavet. Accepttesten blev skrevet først og var rød (7 af 7 punkter). Generatoren, puljen, kortet, posten og pixeltestene er lavet, og `tools/tjek_muiderberg.py` er grøn på 7 af 7 punkter. Hele suiten, de fulde pixeltests og skærmbillederne hører til session 2. Intet er flettet eller pushet.

**Tag og commits:** `main` (`f539056`, lig med `origin/main`) er tagget `v-foer-muiderberg`. Grenen `muiderberg` har:
- `77017a3`: specen, som Frank rettede 24. november;
- `a1324d2`: accepttesten, rød;
- `32ff995`: `dealer/muiderberg.py`, modulet i `build_pools.py` og puljen;
- `2d411fe`: kortet, `data/kort/index.json` og Bikini-linjen på multi-2ru-kortet (= H);
- `4441c28`: posten `muiderberg`, og `ff-muiderberg` er fjernet;
- `5e2033b`: de to pixeltests (51 kort og H);
- derefter dette afsnit og tokenforbruget.

**H = `2d411fe`** (`2d411fec58314ae1f5b2e792b69c5d794aa20a21`) er den sidste commit, der ændrer `assets/footer.js`, `data/kort/index.json`, `data/kort/multi-2ru.json` eller `data/kort/muiderberg.json`. `assets/footer.js` er ikke ændret på grenen, så den er den samme som i `e4e3936`.
- Begge pixeltests henter de fire filer fra H via `NYERE`. Resten af siden før kommer stadig fra testens tag, så siden før har knapperne "Multi 2♦" og "Muiderberg (Bikini) 2♥/2♠" og 51 kort.
- `NYE_KORT` er `['muiderberg']`. Det nye kort tjekkes kun for vandret scroll, og de 50 andre kort sammenlignes med siden før, nu også multi-2ru.
- Tallene er rettet fra 50 til 51 kort, og fra 49 til 50 i meddelelsen om de kort, der sammenlignes.
- `node --check` på begge scripts er i orden. De fulde pixeltests er ikke kørt (session 2), og session 2 må ikke ændre de fire filer.

**Puljen** (`python build_pools.py muiderberg`) har 296 hænder fordelt på 28 meldinger i 7 situationer, 10–11 hænder pr. melding og ingen advarsler:

| Situation | Meldeforløb | Hænder pr. melding |
| --- | --- | --- |
| `aabning` | ? | Pas 11, 1♥ 11, 1♠ 11, 2♦ 11, 2♥ 11, 2♠ 11 |
| `svar_2h` | 2♥ – pas – ? | Pas 11, 2NT 11, 3♣ 11, 3♥ 11, 4♥ 11 |
| `svar_2s` | 2♠ – pas – ? | Pas 10, 2NT 10, 3♣ 10, 3♠ 10, 4♠ 10 |
| `ret_2h` | 2♥ – pas – 3♣ – pas – ? | Pas 11, 3♦ 11 |
| `ret_2s` | 2♠ – pas – 3♣ – pas – ? | Pas 10, 3♦ 10 |
| `spm_2h` | 2♥ – pas – 2NT – pas – ? | 3♣ 11, 3♦ 11, 3♥ 11, 3♠ 10 |
| `spm_2s` | 2♠ – pas – 2NT – pas – ? | 3♣ 10, 3♦ 10, 3♥ 10, 3♠ 10 |

Alle grænser giver nok hænder, også `SPAER_UDGANG`, `SPOERG_INVIT` og `MINOR_RET`. `PER_CALL` er 7, og `build_pool` lægger 100 hænder oveni, fordelt efter antallet.

**Kortet** (`data/kort/muiderberg.json`, type `melding`, kategori `aabning`, nøgle `gul`) står i `index.json` efter multi-2ru:
- **Meldinger:** 2♥ og 2♠ (5–10 hp, 5+ i majoren og 4+ kort i en ukendt minor) og svarene pas, 2NT, 3♣, 3♥/3♠ og 4♥/4♠ efter F.
- **Fortsættelser:** åbners svar på 2NT med F's note om delkontrakt, udgang og slem, og åbner efter 3♣ (pas med klør og 3♦ med ruder).
- **Indmelding:** én række, der siger, at kilderne intet siger, og henviser til Åbne spørgsmål.
- **Eksempler:** Franks eksempel og fire hænder fra puljen (3♣ efter 2♠, 2NT med 17 hp efter 2♥, 3♥ efter 2♠ – 2NT og 3♦ efter 2♥ – 3♣) med puljens forklaring.
- **Faldgruber og Åbne spørgsmål:** de tre og de tre fra specen.
- **Fod:** "Spiller sammen med" er Multi 2♦ (et link til multi-2ru-kortet), og situationsteksten siger, at Muiderberg forudsætter Multi 2♦.
- Kortet har tal kun fra kilderne (5–10 hp og F's "mindst 5 kort" ved ugunstig zone). Grænserne fra generatoren står ikke på kortet.

**Multi-2ru-kortet:** i den sidste linje under Åbne spørgsmål er Bikini-delen "Bikini (2♥/2♠ 5–10 hp …)" erstattet af "Muiderberg (Bikini), som har sit eget kort "Muiderberg (Bikini) 2♥/2♠"". Good/Bad Multi og Ekren står uændret, og resten af kortet er som i tagget (punkt 6 tjekker det).

**Kortsiden** er bygget med `tools/build_konventionskort.py`. De byggede filer er uændrede, fordi siden henter kortene fra `data/kort/`.

#### Tekster til gennemgang

Alle forklaringer og bonusspørgsmål i `dealer/muiderberg.py`, som de står i puljen `pools/muiderberg.json` i `32ff995`, og kortets faldgruber. Dansk og engelsk står side om side, med én række pr. situation og melding (28), én række med bonusspørgsmålet pr. situation (7) og én række pr. faldgrube (3), i alt 38 rækker.
- Tallene er håndens tal fra ét eksempel i puljen. Har en melding flere udgaver af teksten, står de under hinanden.
- **Kilde:** F er Franks tekst, W er Ruder_Multi.docx, og F/W betyder, at de er enige. **(tilføjelse)** markerer Claude Codes egen begrundelse. Noterne under tabellen siger, hvor en tekst bygger på en grænse fra specen. To rækker har en tilføjelse: 4♥ og 4♠ i den spærrende udgave.

| Situation | Melding | Dansk | Engelsk | Kilde |
| --- | --- | --- | --- | --- |
| `aabning`<br>? | Pas | 5 spar, 4 klør og kun 2 hp: pas – Muiderberg kræver ca. 5–10 hp. | 5 spades, 4 clubs and only 2 HCP: pass – Muiderberg needs about 5–10 HCP. | F (note 1) |
| `aabning`<br>? | 1♥ | 5 hjerter, 5 ruder og 14 hp: 1♥ – med 11–15 hp er hånden for stærk til Muiderberg (ca. 5–10 hp). | 5 hearts, 5 diamonds and 14 HCP: 1♥ – with 11–15 HCP the hand is too strong for Muiderberg (about 5–10 HCP). | F (note 1) |
| `aabning`<br>? | 1♠ | 5 spar, 5 ruder og 15 hp: 1♠ – med 11–15 hp er hånden for stærk til Muiderberg (ca. 5–10 hp). | 5 spades, 5 diamonds and 15 HCP: 1♠ – with 11–15 HCP the hand is too strong for Muiderberg (about 5–10 HCP). | F (note 1) |
| `aabning`<br>? | 2♦ | 6 spar, 8 hp og ét es: 2♦ – med en seksfarve i majoren åbnes Multi 2♦. Muiderberg 2♥/2♠ viser en femfarve. | 6 spades, 8 HCP and one ace: 2♦ – with a six-card major the opening is Multi 2♦. Muiderberg 2♥/2♠ shows a five-card suit. | F |
| `aabning`<br>? | 2♥ | 5 hjerter, 5 ruder og 10 hp: 2♥ – Muiderberg: en femfarve i hjerter og mindst fire kort i en ukendt minor med ca. 5–10 hp. | 5 hearts, 5 diamonds and 10 HCP: 2♥ – Muiderberg: a five-card heart suit and at least four cards in an unknown minor with about 5–10 HCP. | F |
| `aabning`<br>? | 2♠ | 5 spar, 4 klør og 9 hp: 2♠ – Muiderberg: en femfarve i spar og mindst fire kort i en ukendt minor med ca. 5–10 hp. | 5 spades, 4 clubs and 9 HCP: 2♠ – Muiderberg: a five-card spade suit and at least four cards in an unknown minor with about 5–10 HCP. | F |
| `aabning`<br>? | Bonusspørgsmål | Hvad viser en Muiderberg-åbning på 2♥ eller 2♠?<br>Rigtigt: En femfarve i majoren, mindst fire kort i en ukendt minor og ca. 5–10 hp<br>Forkert: En seksfarve i majoren og ca. 5–10 hp; En femfarve i majoren, mindst fire kort i en ukendt minor og 11–15 hp<br>Forklaring: 2♥/2♠ viser en femfarve i majoren og mindst fire kort i en ukendt minor med ca. 5–10 hp. Med en seksfarve i majoren åbnes Multi 2♦. | What does a Muiderberg opening of 2♥ or 2♠ show?<br>Rigtigt: A five-card major, at least four cards in an unknown minor and about 5–10 HCP<br>Forkert: A six-card major and about 5–10 HCP; A five-card major, at least four cards in an unknown minor and 11–15 HCP<br>Forklaring: 2♥/2♠ shows a five-card major and at least four cards in an unknown minor with about 5–10 HCP. With a six-card major the opening is Multi 2♦. | F (note 5) |
| `svar_2h`<br>2♥ – pas – ? | Pas | 2 hjerter og 6 hp: pas – præference til åbners major.<br>3 hjerter og 3 hp: pas – præference til åbners major. Hånden er for svag til enkeltløftet. | 2 hearts and 6 HCP: pass – preference for opener's major.<br>3 hearts and 3 HCP: pass – preference for opener's major. The hand is too weak for the single raise. | F<br>F (note 3) |
| `svar_2h`<br>2♥ – pas – ? | 2NT | 5 hjerter og 11 hp: 2NT – kunstigt, stærkt spørgebud. Efter åbners svar vælger svarer mellem delkontrakt og udgang.<br>19 hp: 2NT – kunstigt, stærkt spørgebud. Åbner viser minor og styrke: 3♣ minimum med klør, 3♦ minimum med ruder, 3♥ maksimum med klør og 3♠ maksimum med ruder. | 5 hearts and 11 HCP: 2NT – artificial, strong enquiry. After opener's answer responder chooses between a partscore and game.<br>19 HCP: 2NT – artificial, strong enquiry. Opener shows the minor and strength: 3♣ a minimum with clubs, 3♦ a minimum with diamonds, 3♥ a maximum with clubs and 3♠ a maximum with diamonds. | F |
| `svar_2h`<br>2♥ – pas – ? | 3♣ | 1 hjerter, 5 klør, 3 ruder og 5 hp: 3♣ – pas eller ret: ønske om at spille i åbners minor. Åbner passer med klør og melder 3♦ med ruder. | 1 heart, 5 clubs, 3 diamonds and 5 HCP: 3♣ – pass or correct: to play in opener's minor. Opener passes with clubs and bids 3♦ with diamonds. | F/W |
| `svar_2h`<br>2♥ – pas – ? | 3♥ | 3 hjerter og 8 hp: 3♥ – enkeltløft i åbners major: spærrepræget og ikke krav. | 3 hearts and 8 HCP: 3♥ – a single raise in opener's major: preemptive and non-forcing. | F |
| `svar_2h`<br>2♥ – pas – ? | 4♥ | 5 hjerter og 5 hp: 4♥ – slutkontrakt i åbners major. Med mindst fire trumf er udgangen spærrende.<br>3 hjerter og 16 hp: 4♥ – slutkontrakt i åbners major. | 5 hearts and 5 HCP: 4♥ – sign-off in opener's major. With at least four trumps the game bid is preemptive.<br>3 hearts and 16 HCP: 4♥ – sign-off in opener's major. | F; sætningen om fire trumf er (tilføjelse) (note 2)<br>F |
| `svar_2h`<br>2♥ – pas – ? | Bonusspørgsmål | Hvad betyder 3♣ som svar på Muiderberg?<br>Rigtigt: Pas eller ret: ønske om at spille i åbners minor<br>Forkert: Naturligt med egen klørfarve; Kunstigt, stærkt spørgebud<br>Forklaring: 3♣ er pas eller ret: svarer vil spille i åbners minor. Åbner passer med klør og melder 3♦ med ruder. Det stærke spørgebud er 2NT. | What does 3♣ mean in response to Muiderberg?<br>Rigtigt: Pass or correct: to play in opener's minor<br>Forkert: Natural with responder's own club suit; Artificial, strong enquiry<br>Forklaring: 3♣ is pass or correct: responder wants to play in opener's minor. Opener passes with clubs and bids 3♦ with diamonds. The strong enquiry is 2NT. | F/W (note 5) |
| `ret_2h`<br>2♥ – pas – 3♣ – pas – ? | Pas | 5 hjerter og 5 klør: pas – 3♣ er pas eller ret, og med klør passer åbner. | 5 hearts and 5 clubs: pass – 3♣ is pass or correct, and with clubs opener passes. | F/W |
| `ret_2h`<br>2♥ – pas – 3♣ – pas – ? | 3♦ | 5 hjerter og 5 ruder: 3♦ – 3♣ er pas eller ret, og med ruder retter åbner til 3♦. | 5 hearts and 5 diamonds: 3♦ – 3♣ is pass or correct, and with diamonds opener corrects to 3♦. | F/W |
| `ret_2h`<br>2♥ – pas – 3♣ – pas – ? | Bonusspørgsmål | Hvad melder åbner med ruder efter 2♥ – 3♣?<br>Rigtigt: 3♦, fordi 3♣ er pas eller ret<br>Forkert: Pas, fordi 3♣ er svarers egen farve; 3♥, åbners egen major<br>Forklaring: 3♣ er pas eller ret: svarer vil spille i åbners minor. Åbner passer med klør og melder 3♦ med ruder. | What does opener bid with diamonds after 2♥ – 3♣?<br>Rigtigt: 3♦, because 3♣ is pass or correct<br>Forkert: Pass, because 3♣ is responder's own suit; 3♥, opener's own major<br>Forklaring: 3♣ is pass or correct: responder wants to play in opener's minor. Opener passes with clubs and bids 3♦ with diamonds. | F/W (note 5) |
| `spm_2h`<br>2♥ – pas – 2NT – pas – ? | 3♣ | 5 hjerter, 5 klør og 7 hp (minimum): 3♣ – minimum med klør. | 5 hearts, 5 clubs and 7 HCP (a minimum): 3♣ – a minimum with clubs. | F/W (note 4) |
| `spm_2h`<br>2♥ – pas – 2NT – pas – ? | 3♦ | 5 hjerter, 5 ruder og 5 hp (minimum): 3♦ – minimum med ruder. | 5 hearts, 5 diamonds and 5 HCP (a minimum): 3♦ – a minimum with diamonds. | F/W (note 4) |
| `spm_2h`<br>2♥ – pas – 2NT – pas – ? | 3♥ | 5 hjerter, 5 klør og 10 hp (maksimum): 3♥ – maksimum med klør. | 5 hearts, 5 clubs and 10 HCP (a maximum): 3♥ – a maximum with clubs. | F/W (note 4) |
| `spm_2h`<br>2♥ – pas – 2NT – pas – ? | 3♠ | 5 hjerter, 5 ruder og 9 hp (maksimum): 3♠ – maksimum med ruder. | 5 hearts, 5 diamonds and 9 HCP (a maximum): 3♠ – a maximum with diamonds. | F/W (note 4) |
| `spm_2h`<br>2♥ – pas – 2NT – pas – ? | Bonusspørgsmål | Hvad viser åbners 3♥ efter 2♥ – 2NT?<br>Rigtigt: Maksimum med klør<br>Forkert: Minimum med klør; Maksimum med ruder<br>Forklaring: Efter 2NT viser 3♣ minimum med klør, 3♦ minimum med ruder, 3♥ maksimum med klør og 3♠ maksimum med ruder. | What does opener's 3♥ show after 2♥ – 2NT?<br>Rigtigt: A maximum with clubs<br>Forkert: A minimum with clubs; A maximum with diamonds<br>Forklaring: After 2NT, 3♣ shows a minimum with clubs, 3♦ a minimum with diamonds, 3♥ a maximum with clubs and 3♠ a maximum with diamonds. | F/W (note 5) |
| `svar_2s`<br>2♠ – pas – ? | Pas | 2 spar og 9 hp: pas – præference til åbners major.<br>3 spar og 5 hp: pas – præference til åbners major. Hånden er for svag til enkeltløftet. | 2 spades and 9 HCP: pass – preference for opener's major.<br>3 spades and 5 HCP: pass – preference for opener's major. The hand is too weak for the single raise. | F<br>F (note 3) |
| `svar_2s`<br>2♠ – pas – ? | 2NT | 17 hp: 2NT – kunstigt, stærkt spørgebud. Åbner viser minor og styrke: 3♣ minimum med klør, 3♦ minimum med ruder, 3♥ maksimum med klør og 3♠ maksimum med ruder.<br>4 spar og 12 hp: 2NT – kunstigt, stærkt spørgebud. Efter åbners svar vælger svarer mellem delkontrakt og udgang. | 17 HCP: 2NT – artificial, strong enquiry. Opener shows the minor and strength: 3♣ a minimum with clubs, 3♦ a minimum with diamonds, 3♥ a maximum with clubs and 3♠ a maximum with diamonds.<br>4 spades and 12 HCP: 2NT – artificial, strong enquiry. After opener's answer responder chooses between a partscore and game. | F |
| `svar_2s`<br>2♠ – pas – ? | 3♣ | 1 spar, 3 klør, 6 ruder og 6 hp: 3♣ – pas eller ret: ønske om at spille i åbners minor. Åbner passer med klør og melder 3♦ med ruder. | 1 spade, 3 clubs, 6 diamonds and 6 HCP: 3♣ – pass or correct: to play in opener's minor. Opener passes with clubs and bids 3♦ with diamonds. | F/W |
| `svar_2s`<br>2♠ – pas – ? | 3♠ | 3 spar og 10 hp: 3♠ – enkeltløft i åbners major: spærrepræget og ikke krav. | 3 spades and 10 HCP: 3♠ – a single raise in opener's major: preemptive and non-forcing. | F |
| `svar_2s`<br>2♠ – pas – ? | 4♠ | 4 spar og 7 hp: 4♠ – slutkontrakt i åbners major. Med mindst fire trumf er udgangen spærrende.<br>4 spar og 13 hp: 4♠ – slutkontrakt i åbners major. | 4 spades and 7 HCP: 4♠ – sign-off in opener's major. With at least four trumps the game bid is preemptive.<br>4 spades and 13 HCP: 4♠ – sign-off in opener's major. | F; sætningen om fire trumf er (tilføjelse) (note 2)<br>F |
| `svar_2s`<br>2♠ – pas – ? | Bonusspørgsmål | Hvad betyder 3♠ efter 2♠ – pas?<br>Rigtigt: Enkeltløft: spærrepræget og ikke krav<br>Forkert: Invit til udgang; Kunstigt, stærkt spørgebud<br>Forklaring: 3♥/3♠ er et enkeltløft i åbners major: spærrepræget og ikke krav (RONF). Det stærke spørgebud er 2NT. | What does 3♠ mean after 2♠ – pass?<br>Rigtigt: A single raise: preemptive and non-forcing<br>Forkert: An invitation to game; Artificial, strong enquiry<br>Forklaring: 3♥/3♠ is a single raise in opener's major: preemptive and non-forcing (RONF). The strong enquiry is 2NT. | F (note 5) |
| `ret_2s`<br>2♠ – pas – 3♣ – pas – ? | Pas | 5 spar og 5 klør: pas – 3♣ er pas eller ret, og med klør passer åbner. | 5 spades and 5 clubs: pass – 3♣ is pass or correct, and with clubs opener passes. | F/W |
| `ret_2s`<br>2♠ – pas – 3♣ – pas – ? | 3♦ | 5 spar og 4 ruder: 3♦ – 3♣ er pas eller ret, og med ruder retter åbner til 3♦. | 5 spades and 4 diamonds: 3♦ – 3♣ is pass or correct, and with diamonds opener corrects to 3♦. | F/W |
| `ret_2s`<br>2♠ – pas – 3♣ – pas – ? | Bonusspørgsmål | Hvad melder åbner med ruder efter 2♠ – 3♣?<br>Rigtigt: 3♦, fordi 3♣ er pas eller ret<br>Forkert: Pas, fordi 3♣ er svarers egen farve; 3♠, åbners egen major<br>Forklaring: 3♣ er pas eller ret: svarer vil spille i åbners minor. Åbner passer med klør og melder 3♦ med ruder. | What does opener bid with diamonds after 2♠ – 3♣?<br>Rigtigt: 3♦, because 3♣ is pass or correct<br>Forkert: Pass, because 3♣ is responder's own suit; 3♠, opener's own major<br>Forklaring: 3♣ is pass or correct: responder wants to play in opener's minor. Opener passes with clubs and bids 3♦ with diamonds. | F/W (note 5) |
| `spm_2s`<br>2♠ – pas – 2NT – pas – ? | 3♣ | 5 spar, 5 klør og 5 hp (minimum): 3♣ – minimum med klør. | 5 spades, 5 clubs and 5 HCP (a minimum): 3♣ – a minimum with clubs. | F/W (note 4) |
| `spm_2s`<br>2♠ – pas – 2NT – pas – ? | 3♦ | 5 spar, 5 ruder og 5 hp (minimum): 3♦ – minimum med ruder. | 5 spades, 5 diamonds and 5 HCP (a minimum): 3♦ – a minimum with diamonds. | F/W (note 4) |
| `spm_2s`<br>2♠ – pas – 2NT – pas – ? | 3♥ | 5 spar, 4 klør og 8 hp (maksimum): 3♥ – maksimum med klør. | 5 spades, 4 clubs and 8 HCP (a maximum): 3♥ – a maximum with clubs. | F/W (note 4) |
| `spm_2s`<br>2♠ – pas – 2NT – pas – ? | 3♠ | 5 spar, 5 ruder og 10 hp (maksimum): 3♠ – maksimum med ruder. | 5 spades, 5 diamonds and 10 HCP (a maximum): 3♠ – a maximum with diamonds. | F/W (note 4) |
| `spm_2s`<br>2♠ – pas – 2NT – pas – ? | Bonusspørgsmål | Hvad viser åbners 3♦ efter 2♠ – 2NT?<br>Rigtigt: Minimum med ruder<br>Forkert: Maksimum med ruder; Minimum med klør<br>Forklaring: Efter 2NT viser 3♣ minimum med klør, 3♦ minimum med ruder, 3♥ maksimum med klør og 3♠ maksimum med ruder. | What does opener's 3♦ show after 2♠ – 2NT?<br>Rigtigt: A minimum with diamonds<br>Forkert: A maximum with diamonds; A minimum with clubs<br>Forklaring: After 2NT, 3♣ shows a minimum with clubs, 3♦ a minimum with diamonds, 3♥ a maximum with clubs and 3♠ a maximum with diamonds. | F/W (note 5) |
| kortet<br>Faldgruber | Faldgrube | 3♣ er pas eller ret, ikke svarers egen farve: åbner passer med klør og melder 3♦ med ruder. | 3♣ is pass or correct, not responder's own suit: opener passes with clubs and bids 3♦ with diamonds. | F/W (note 6) |
| kortet<br>Faldgruber | Faldgrube | 3♥/3♠ er et spærrepræget enkeltløft og ikke krav; det stærke spørgebud er 2NT. | 3♥/3♠ is a preemptive single raise and non-forcing; the strong enquiry is 2NT. | F (note 6) |
| kortet<br>Faldgruber | Faldgrube | Med seks kort i majoren åbnes Multi 2♦, ikke 2♥/2♠. | With six cards in the major the opening is Multi 2♦, not 2♥/2♠. | F (note 6) |

**Noter:**
1. **Pas og 1♥/1♠ ved åbningen:** 0–4 hp og 11–15 hp er specens regel (Regler, `aabning`). F giver kun "ca. 5–10 hp" for 2♥/2♠, og "kræver ca. 5–10 hp" og "for stærk til Muiderberg" bygger på den.
2. **4♥/4♠ med højst 10 hp:** F siger kun "Slutkontrakt". Sætningen "Med mindst fire trumf er udgangen spærrende." er Claude Codes begrundelse for grænsen `SPAER_UDGANG` (rådgiverens forslag, Afklaret 8) og markeret som tilføjelse.
3. **Pas med tre kort i åbners major og under 6 hp:** "Hånden er for svag til enkeltløftet" bygger på grænsen `ENKELTLOEFT` (6–10 hp) fra specen. F siger kun "Præference til åbners major".
4. **Minimum og maksimum efter 2NT** er specens grænser `MIN_HP` og `MAX_HP` (5–7 og 8–10 hp). F og W siger kun minimum og maksimum.
5. **Bonusspørgsmålene:** spørgsmålet, det rigtige svar og forklaringen bygger på kilderne. De to forkerte svar er Claude Codes, og de er ikke påstande om konventionen.
6. **Faldgruberne** står kun på kortet, som er på dansk. Den engelske tekst er en oversættelse til gennemgang og bruges ikke på siden.

**Testresultater:**
- `tjek_muiderberg.py`: i orden (7 af 7 punkter);
- `tjek_konventionskort.py`: "51 konventionskort er i orden";
- `tjek_kort_eksempler.py muiderberg`: "5 meldeeksempler er i orden (0 advarsler)", og for alle kort: "228 meldeeksempler er i orden (0 advarsler)";
- `tjek_fagord.py` og `tjek_bydeform.py`: i orden, og `tjek_sprog.py`: OK (10 tests);
- `sprogtjek.py`: ingen ukendte ord;
- `node --check` på `tjek_viden_320.mjs` og `tjek_crowhurst_390.mjs`: i orden;
- `tjek_multi_2ru.py`: **rød på punkt 6** (7 af 8 punkter i orden). Punktet sammenligner de øvrige poster i `data/konventioner.json` med tagget `v-foer-multi-2ru` og melder "de øvrige poster er ændret: ff-muiderberg, muiderberg". Det er netop den ændring, specen beder om, men Afgrænsningen tillader ikke at rette `tools/tjek_multi_2ru.py` (spørgsmål 1).

**Valg, specen ikke afgør:**
1. **Én situation pr. åbning:** `svar`, `ret` og `spm` har hver to situationer, én efter 2♥ og én efter 2♠, fordi `traener.html` tager meldeforløbet fra situationen. "Alle fire situationer" er de fire familier med i alt 7 meldeforløb.
2. **Håndtypen:** "4–5 kort i en minor" er læst som én minor med 4–5 kort, mens den anden minor har højst tre. En hånd med to minorer på 4+ kort (fx 5-0-4-4) har ingen entydig minor efter 3♣ og 2NT, så den genereres ikke (spørgsmål 3).
3. **Åbningen:** 1♥/1♠ og pas har samme fordeling som 2♥/2♠. 2♦ er en gyldig Multi-åbning efter multi-2ru's regel (`gyldig` og samplerne importeres fra `dealer/multi_2ru.py`, som er urørt). Seksfarver med 0–4 eller 11–15 hp genereres ikke.
4. **Enkeltløftet** kræver præcis tre kort i åbners major, som kommentaren i kodeblokken siger. Fire kort med højst 10 hp er allerede 4M efter `SPAER_UDGANG`.
5. **Svarhænderne:** puljen har som Multi kun svarers hånd, ikke åbners. Punkt 4 tjekker åbners hånd i `svar`, hvis puljen en dag får den. I `ret` og `spm` er hånden åbners, og den er altid en gyldig 2♥- eller 2♠-åbning.
6. **Franks eksempel i puljen:** samplerne til 2♠ i `aabning` giver først Franks hånd og derefter tilfældige hænder (`Foerst` i modulet). Så står kortets eksempel i puljen, og `tjek_kort_eksempler.py` giver 0 advarsler. `export_pool` tjekker desuden, at hånden giver 2♠.
7. **Bonusspørgsmålene:** specen nævner ingen bestemte. Hver situation har ét med tre svarmuligheder på begge sprog, og svarene er skrevet som tekst, der er forskellig på de to sprog, som i Multi.
8. **Kortet:**
   - Fortsættelserne viser forløbet efter 2♥, og titlen siger "det samme efter 2♠".
   - 3♦ efter 3♣ har nøglen `gron` (naturlig), og pas har `gra`.
   - Kortet har intet `alert`-felt, fordi kilderne ikke siger noget om alertering (spørgsmål 2).
   - Kilden står som "Franks tekst om Muiderberg (21. november 2026) · hullerne udfyldt efter dokumentet Ruder Multi".
9. **Posten** står sidst i `data/konventioner.json` efter multi-2ru, og `ff-muiderberg` er fjernet. Ingen anden fil bruger `ff-muiderberg` (kun det gamle udkast i `_design/`, som ikke udgives).
10. **Pixeltestene:** multi-2ru er ikke længere i `NYE_KORT`, fordi kortet nu findes i siden før via H. Det sammenlignes derfor som de andre kort (opgavens "de 50 andre"), og session 2 ser, om det er pixel for pixel som før.
11. **W** er læst i denne session (afsnittet om Bikini). Det bekræfter 2NT-svarene, 3♣ (pas med klør, ret til ruder) og ny farve som naturlig og krav i én runde, som står under Åbne spørgsmål.

**Spørgsmål til Frank:**
1. **`tjek_multi_2ru.py` punkt 6:** må testen se bort fra `muiderberg` og `ff-muiderberg`, når den sammenligner de øvrige poster med tagget `v-foer-multi-2ru`? Ellers er den rød i session 2's suite.
2. **Alertering:** skal kortet have feltet `alert`, fx "2♥/2♠ alerteres", som Multi-kortet ("2♦ alerteres")?
3. **To minorer på 4+ kort:** er det rigtigt, at 5-4-4-0 og lignende ikke trænes, eller skal de åbne 2♥/2♠ og have en regel for 3♣ og 2NT?
4. **Teksterne:** tabellen "Tekster til gennemgang" venter på Franks godkendelse før fletningen, også tilføjelsen om fire trumf.

**Til session 2 (Sonnet):**
- svaret på spørgsmål 1, før suiten køres;
- hele suiten og de fulde pixeltests (`node tools/tjek_viden_320.mjs` og `node tools/tjek_crowhurst_390.mjs`) én gang hver i forgrunden;
- skærmbillederne af `traener.html?k=muiderberg` (specen, Accepttest) i `C:\Users\frank\Kontraktbridge\skaermbilleder\muiderberg\`;
- `assets/footer.js`, `data/kort/index.json`, `data/kort/multi-2ru.json` og `data/kort/muiderberg.json` må ikke ændres, for så passer H ikke længere;
- stop før fletning og en rapport med tokenforbruget.

**Tokenforbrug i session 1** (72 svar, 17:39–17:54 UTC, målt før den sidste commit): nye input 144 · skrevet til cachen 289.555 · læst fra cachen 13.654.337 · output 92.176; i alt 14.036.212.
