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
- Session 1:
- Session 2:
- Efter godkendelsen:
