# SPEC-multi-2ru

21. november 2026 · Frank

En ny træner for **Multi 2♦**. Den bygger på to kilder uden for repoerne:

1. **Jyderup Bridgeklubs ark "Multi 2ru"** (`C:\Users\frank\Kontraktbridge\Multi_2ru_Jyderup.pdf`). Det er hovedkilden, og den gælder, når kilderne er uenige (Franks valg 21. november 2026).
2. **Franks dokument "Ruder Multi"** (`C:\Users\frank\Kontraktbridge\Ruder_Multi.docx`). Det udfylder de huller, som arket ikke dækker, og giver eksemplerne.

Alt, hvad træneren skal bruge fra kilderne, står i denne spec. Kilderne skal ikke læses, og de må ikke lægges i repoet.

Træneren følger samme opbygning som de øvrige meldetrænere:
- et modul i `dealer/`;
- en pulje i `pools/`;
- en post i `data/konventioner.json`;
- et konventionskort i `data/kort/`.

Træningssiden er den fælles `traener.html?k=multi-2ru`. Der kommer ingen nye skærmbilleder, så der laves ingen mock-up.

Multi står i dag som "kommer" under Forslag (`ff-multi-2ru`, der peger på afsnit B2 i Makker 2-dokumentet). Den nye træner afløser den post (Afklaret, punkt 1).

## Afgrænsning

Før arbejdet starter:

1. Commit og tag den nuværende side som `v-foer-multi-2ru`.
2. Arbejd på grenen `multi-2ru`, og flet først ind efter Franks godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `dealer/multi_2ru.py` (ny) | Generator og bedømmelse efter reglerne nedenfor, med `export_pool(path)`. | — |
| `build_pools.py` | Importere `multi_2ru` og tilføje `"multi-2ru": multi_2ru` i `CONVENTIONS`. | Ændre andre konventioner. |
| `pools/multi-2ru.json` (ny) | Genereres med `python build_pools.py multi-2ru`. | Rettes i hånden. |
| `data/konventioner.json` | Én ny post (se nedenfor), og posten `ff-multi-2ru` fjernes. | Ændre de øvrige poster, heller ikke `ff-muiderberg` og `crowhurst`. |
| `data/kort/multi-2ru.json` (ny) og `data/kort/index.json` | Et nyt kort efter `docs/konventionskort-skabelon.md`, med `traener`-feltet. | Tal, som kilderne ikke angiver (se Grænser). |
| `viden/konventionskort.html`, `assets/konventionskort-hint.js` | Bygges med `python3 tools/build_konventionskort.py`. | Rettes i hånden. |
| `tools/tjek_multi_2ru.py` (ny) | Accepttesten (se nedenfor). | — |
| `viden/2-over-1-makker2.html` (afsnit B2 og B4) | Intet. | Alt. Afsnittene er Makker 2's forslag og står uændret (Afklaret, punkt 2). |
| `traener.html`, `dealer/core.py`, `dealer/crowhurst.py` | Intet. | Alt. |
| Sprog | Al tekst i træneren skrives med `tx('dansk', 'English')`, og posten får et `en`-felt. Husets ord (`../CLAUDE.md`) gælder, og teksterne står i beskrivende form. | Dansk tekst på den engelske side. |

## Kilderne

Mærkningen i tabellerne viser, hvor hver regel kommer fra: **J** er Jyderup-arket, **W** er Word-dokumentet, og **J/W** betyder, at de er enige.

### Åbningen (J)

2♦ viser en seksfarve i hjerter eller spar og 5–10 hp. Hånden har ingen firfarve i den anden major og højst ét es. Formålet er at frigøre 2♥ og 2♠.

### Svar på 2♦ (2♦ – Pas – ?)

| Svar | Betydning | Kilde |
| --- | --- | --- |
| 2♥ | Søger farven: åbner passer med hjerter og melder 2♠ med spar. | J/W |
| 2♠ | Invit med hjerter: åbner passer med spar. Med hjerter melder han 3♥ med minimum og 4♥ med maksimum. | J (W: pas eller ret) |
| 2NT | Spørger om styrken. | J/W |
| 3♣ / 3♦ | Krav med egen farve. | J/W |
| 3♥ / 3♠ | Pas eller ret: spærremelding i makkers farve. | J/W |
| 3NT | For at spille. | W |
| 4♣ | Transfer: åbner melder farven under sin egen, 4♦ med hjerter og 4♥ med spar. | J/W |
| 4♦ | Åbner melder sin farve. | W |
| 4♥ / 4♠ | Svarers egen farve. | J/W |

### Efter 2NT

**Åbners svar (2♦ – Pas – 2NT – Pas – ?), J/W:**

| Svar | Betydning |
| --- | --- |
| 3♣ | Maksimum. |
| 3♦ | Minimum og hjerter. |
| 3♥ | Minimum og spar. |

**Svarers melding efter 3♣ (2♦ – Pas – 2NT – Pas – 3♣ – Pas – ?):**
- 3♦ søger farven, og åbner viser den med en krydsmelding: 3♥ = spar og 3♠ = hjerter (J/W).
- 3♥/3♠ er krav med egen farve (J).

### Når modparten dobler (2♦ – X – ?), J

| Svar | Betydning |
| --- | --- |
| Pas | Svag hånd med ruder, for at spille. |
| XX | Styrke med interesse for straf. |
| 2♥ | Svag hånd med fit i begge majorer: pas eller ret. |
| Resten | Doblingen ignoreres, og der meldes som uden dobling. |

### Når modparten melder ind

**Over 2♠ (2♦ – 2♠ – ?), J:** X viser styrke (negativ dobling) og beder åbner strafpasse med spar.

**Over andre indmeldinger (2♦ – 3♣, 3♦ eller 4♥ – ?), W (arket siger intet):**

| Svar | Betydning |
| --- | --- |
| Pas | Intet at tilføje. |
| X | Straf. |
| ♥ / ♠ | Pas eller ret. |
| Minor | Naturligt og ikke krav. |

### Varianter i W, som ikke trænes nu

Word-dokumentet beskriver tre måder at bruge de frigjorte 2♥ og 2♠ på:
- **Good/Bad Multi:** 2♦ 3–7 hp, og 2♥/2♠ 8–11 hp med en seksfarve.
- **Bikini:** 2♥/2♠ 5–10 hp med femfarve og en firfarve i en minor, og 2NT-spørgsmålet giver 3♣/3♦ minimum og 3♥/3♠ maksimum.
- **Ekrens:** 2♥ 55 i major og 2♠ 55 i minor.

De står på kortet under "Åbne spørgsmål" (Afklaret, punkt 3).

## Eksemplerne (facit)

E = es, B = bonde og T = 10. Syd svarer, og Nord har åbnet 2♦. Eksemplerne kommer fra W.

**Facit med uændret svar:**

| # | Meldeforløb | ♠ | ♥ | ♦ | ♣ | Svar | Begrundelse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2♦ – Pas – ? | E72 | 984 | KD743 | 86 | 3♥ | Spærremelding: pas eller ret. |
| 3 | 2♦ – Pas – ? | – | KDBT874 | KD92 | E4 | 4♥ | Egen farve, som åbner passer. |
| 4 | 2♦ – Pas – ? | DBT | EK4 | 942 | EKD2 | 2NT | Spørger. |
| 5 | 2♦ – X – ? | 8 | D743 | EDT9742 | B | Pas | Svag med ruder, for at spille. |
| 7 | 2♦ – 3♣ – ? | 9 | KB93 | EK86 | KDT8 | X | Straf. |
| 8 | 2♦ – 3♦ – ? | 2 | KB3 | DT3 | EK7542 | Pas | Klør kan kun meldes på 4-trinnet, og spar mangler. |
| 9 | 2♦ – 4♥ – ? | KT72 | 862 | KD952 | 8 | 4♠ | Pas eller ret. Makker har sikkert spar. |

**To eksempler udgår, fordi Jyderup-reglerne giver dem et andet eller uklart svar:**
- **Eksempel 1** (♠E983 ♥T ♦KD7 ♣KB632, W: 2♠): hos J er 2♠ invit med hjerter, og hånden har single hjerter.
- **Eksempel 6** (♠K6 ♥K6 ♦832 ♣DT876 efter X, W: XX): hos J er XX styrke, og hånden er svag uden fit og uden ruder (Afklaret, punkt 4).

**Åbningshænder:**

| Hånd | W | Med J |
| --- | --- | --- |
| ♠KD9653 ♥7 ♦D76 ♣863 | 2♦ | 2♦ (7 hp) |
| ♠KBT975 ♥8 ♦873 ♣985 | 2♦ ("minimum") | **Pas** (4 hp, under 5) |
| ♠95 ♥KDB973 ♦KB ♣874 | 2♦ | 2♦ (10 hp) |
| ♠3 ♥KDBT8 ♦742 ♣9873 | 2♦ (femfarve) | Ikke med i træneren |

## Situationer

| Situation | Rolle | Meldeforløb | Meldinger at vælge imellem |
| --- | --- | --- | --- |
| `aabning` | Åbner | – | Pas, 1♥, 1♠, 2♦ |
| `svar` | Svarer | 2♦ – Pas – ? | Pas, 2♥, 2♠, 2NT, 3♣, 3♦, 3♥, 3♠, 3NT, 4♣, 4♦, 4♥, 4♠ |
| `ret` | Åbner | 2♦ – Pas – (2♥, 2♠, 3♥, 3♠, 4♣ eller 4♦) – Pas – ? | Pas, 2♠, 3♥, 3♠, 4♦, 4♥, 4♠ |
| `spm` | Åbner | 2♦ – Pas – 2NT – Pas – ? | 3♣, 3♦, 3♥, 3♠, 3NT |
| `spm2` | Åbner | 2♦ – Pas – 2NT – Pas – 3♣ – Pas – 3♦ – Pas – ? | 3♥, 3♠, 3NT |
| `dobling` | Svarer | 2♦ – X – ? | Pas, XX, 2♥, 2♠, 2NT, 3♣, 3♦, 3♥, 3♠, 4♣, 4♦, 4♥, 4♠ |
| `indmelding` | Svarer | 2♦ – (2♠, 3♣, 3♦ eller 4♥) – ? | Pas, X og de meldinger på næste trin, der kan bruges: ♥/♠ og minorer. |

## Regler

### `aabning`
- **2♦:** Præcis seks kort i én major, højst tre i den anden major, 5–10 hp og højst ét es.
- **1♥ / 1♠:** Seks kort i en major og 11–15 hp.
- **Pas:** Seks kort i en major og 0–4 hp.
- Hænder med 5–10 hp og to esser genereres ikke, fordi kilderne ikke siger, hvad man så melder. Bonusspørgsmålet spørger om es-grænsen.

### `ret`

| Svar | Åbners melding |
| --- | --- |
| 2♥ | Pas med hjerter, 2♠ med spar. |
| 2♠ | Pas med spar. Med hjerter 3♥ med minimum og 4♥ med maksimum. |
| 3♥ | Pas med hjerter, 3♠ med spar. |
| 3♠ | Pas med spar, 4♥ med hjerter. |
| 4♣ | 4♦ med hjerter, 4♥ med spar. |
| 4♦ | 4♥ med hjerter, 4♠ med spar. |

### `spm` og `spm2`
- 3♣ viser maksimum med begge majorer.
- 3♦ viser minimum med hjerter.
- 3♥ viser minimum med spar.
- Efter 3♣ – 3♦ viser 3♥ spar og 3♠ hjerter.

Svarers 3♥/3♠ efter 3♣ (krav med egen farve) står på kortet og i et bonusspørgsmål, men er ikke en situation.

### `svar`, `dobling` og `indmelding`
Reglerne prøves i den rækkefølge, der står under Grænser. Den første regel, der passer, giver svaret.

## Grænser, som kilderne ikke giver tal for – ret dem her

Tallene står som konstanter øverst i `dealer/multi_2ru.py` med denne overskrift. De bruges kun i generatoren og står ikke på kortet. Facit-eksemplerne giver kildens svar med disse grænser, og den kontrol står i accepttesten.

```python
# --- Grænser, som kilderne ikke giver tal for – ret dem her ------------
MIN_HP, MAX_HP = (5, 7), (8, 10)   # åbners minimum og maksimum inden for 5–10

# svar: 2♦ – Pas – ?  (første regel, der passer)
EGEN_MAJOR   = dict(laengde=7, top=2, hp=10)    # 4♥/4♠: 7+ i majoren, 2 af de 3 øverste, 10+ hp
EGEN_MINOR   = dict(laengde=6, top=2, hp=13)    # 3♣/3♦ krav: 6+ i minoren, 2 af de 3 øverste, 13+ hp, ikke 3+ i begge majorer
SPOERG_HP    = 16                               # 2NT: 16+ hp
UDGANG_HP    = (13, 15)                         # 4♦: 3+ i begge majorer og 13–15 hp
INVIT_HJ     = dict(hjerter=3, hp=(11, 12))     # 2♠: 3+ hjerter og 11–12 hp
SPAER_TRE_SP = dict(begge=4, hp=(6, 10))        # 3♠: 4+ i begge majorer, 6–10 hp
SPAER_TRE_HJ = dict(begge=3, hp=(6, 10))        # 3♥: 3+ i begge majorer, 6–10 hp
# 2♥: resten under 16 hp
# 4♣ og 3NT: kun som forkerte valgmuligheder (Afklaret, punkt 5)

# dobling: 2♦ – X – ?  (første regel, der passer)
PAS_RUDER    = dict(laengde=6, hp_max=10)       # Pas: 6+ ruder, højst 10 hp
STRAF_XX     = dict(hp=12, major_max=2)         # XX: 12+ hp og højst 2 kort i hver major
SVAG_FIT_X   = dict(begge=3, hp_max=5)          # 2♥: 3+ i begge majorer, højst 5 hp
# derefter som under svar (2♠, 2NT, 3♣/3♦, 3♥/3♠, 4♦, 4♥/4♠ med samme grænser)
# svage hænder uden ruder og uden fit i begge majorer genereres ikke (Afklaret, punkt 4)

# indmelding over 2♠: 2♦ – (2♠) – ?
NEGATIV_X    = dict(hp=10)                      # X: 10+ hp
STOETTE_HJ   = dict(hjerter=3, hp=(6, 9))       # 3♥: 3+ hjerter, 6–9 hp
# Pas: resten

# indmelding over 3♣, 3♦ og 4♥ (W)
STRAF        = dict(laengde=4, top4=2, hp=12)   # X: 4+ i modpartens farve, 2 af de 4 øverste, 12+ hp
PAS_RET      = dict(hp=7)                       # billigste major: 3+ i begge majorer (over 4♥: 4+ spar), 7+ hp
MINOR_NAT    = dict(laengde=6, top=2, hp=8)     # minor: god 6+ farve, kun på 3-trinnet
# Pas: resten
```

**Kontrol af facit mod grænserne:**
- **Eksempel 2:** 3-3 i majorerne og 9 hp, men ikke 4-4 → 3♥.
- **Eksempel 3:** Syv hjerter med K-D-B og 15 hp → 4♥.
- **Eksempel 4:** 19 hp → 2NT.
- **Eksempel 5:** Syv ruder og 9 hp efter X → Pas.
- **Eksempel 7:** ♣KDT8 og 16 hp over 3♣ → X.
- **Eksempel 8:** ♠2, og klør kun på 4-trinnet over 3♦ → Pas.
- **Eksempel 9:** Fire spar, tre hjerter og 8 hp over 4♥ → 4♠.
- **Åbningshænderne:** 7 og 10 hp uden es → 2♦; 4 hp → Pas.

## Forklaringer og bonusspørgsmål

Hver situation får et bonusspørgsmål med tre svarmuligheder. Forklaringen nævner kildens regel og de tal, der afgjorde svaret, som i `dealer/ff_flannery.py`. Claude Code foreslår teksterne, og Frank godkender dem, før der flettes. Mindst disse spørgsmål kommer med:
- `aabning`: "Hvilke krav stiller Multi 2♦ til hånden?" (5–10 hp, seksfarve, ingen firfarve i den anden major, højst ét es).
- `svar`: "Hvad betyder 2♠ som svar på Multi?" (invit med hjerter).
- `ret`: "Hvad melder åbner efter 4♣?"
- `spm2`: "Hvad betyder svarers 3♥ efter 2♦ – 2NT – 3♣?" (krav med egen farve).
- `dobling`: "Hvad viser redobling, når modparten dobler 2♦?" (styrke med interesse for straf).
- `indmelding`: "Hvad betyder dobling efter 2♦ – (2♠)?" (styrke; åbner strafpasser med spar).

## Post i data/konventioner.json

```json
{
  "id": "multi-2ru",
  "titel": "Multi 2♦",
  "gruppe": "Åbninger",
  "emne": "aabninger",
  "beskrivelse": "2♦ viser en svag 2 i hjerter eller spar (5–10 hp, seksfarve, højst ét es). 2♥ søger farven, 2♠ er invit med hjerter, 2NT spørger om styrken, og 3♥/3♠ spærrer i makkers farve – også når modparten dobler eller melder ind.",
  "roller": ["Åbner", "Svarer"],
  "status": "klar",
  "system": "generel",
  "viden": "viden/konventionskort.html#multi-2ru",
  "en": {
    "titel": "Multi 2♦",
    "gruppe": "Openings",
    "beskrivelse": "2♦ shows a weak two in hearts or spades (5–10 HCP, a six-card suit, at most one ace). 2♥ asks for the suit, 2♠ is an invitation in hearts, 2NT asks about strength, and 3♥/3♠ preempt in partner's suit – also when the opponents double or overcall."
  }
}
```

## Konventionskortet

`data/kort/multi-2ru.json` følger skabelonen og har `type: "melding"`. Det har de seks afsnit og tal kun fra kilderne.

1. **Meldinger:** Åbningen med Jyderups krav og svarene på 2♦.
2. **Fortsættelser:** Åbners svar på 2NT, krydsmeldingen, svarers 3♥/3♠ efter 3♣ og åbners svar på 2♠.
3. **Indmelding:** Meldingerne efter modpartens dobling og indmelding.
4. **Eksempler:** Hentes fra puljen med samme meldeforløb og svar som eksempel 3, 4, 5 og 9. `tools/tjek_kort_eksempler.py multi-2ru` giver ingen advarsler.
5. **Faldgruber:**
   - 2♥ er pas eller ret, men 2♠ er invit med hjerter.
   - Efter dobling er pas ruder, XX er styrke, og 2♥ er svag med fit i begge majorer.
   - 3♣ på 2NT er maksimum, og farven vises med en krydsmelding.
6. **Åbne spørgsmål:**
   - Hvornår svarer vælger 4♣ frem for 4♦.
   - Hvad 3NT kræver.
   - Hvad en svag hånd uden ruder og uden fit melder efter dobling.
   - Hvad en hånd med 5–10 hp, seksfarve og to esser åbner.
   - Hvad 2♥ og 2♠ bruges til (Good/Bad Multi, Bikini eller Ekrens, med tallene fra W).

`traener`-feltet er `{"url": "traener.html?k=multi-2ru", "pool": "pools/multi-2ru.json"}`.

## Accepttest

`python3 tools/tjek_multi_2ru.py` skrives først og skal være rød, før generatoren skrives. Den tjekker otte ting:

1. Facit-eksemplerne 2, 3, 4, 5, 7, 8 og 9 og de tre første åbningshænder giver svaret i tabellerne med `dealer/multi_2ru.py`'s bedømmelse.
2. `ret`, `spm` og `spm2` giver tabellens svar for alle kombinationer af svar, åbners major og minimum eller maksimum.
3. Puljen har alle syv situationer. Hver melding, der genereres, har mindst 7 hænder (`PER_CALL`), og `build_pools.py` skriver ingen "Advarsel: kun …".
4. For hver hånd i puljen er `correct` det svar, reglerne giver, og ingen hånd ligger uden for de regler, situationen har.
5. Alle åbnerhænder er gyldige 2♦-åbninger efter J: præcis seks kort i én major, højst tre i den anden, 5–10 hp og højst ét es. Når der genereres hele spil, gælder det også Nords hånd.
6. Posten `multi-2ru` findes, og `ff-multi-2ru` er væk.
7. `python3 tools/tjek_konventionskort.py` melder "i orden", og `tools/tjek_kort_eksempler.py multi-2ru` giver ingen advarsler.
8. `python3 tools/tjek_fagord.py`, `python3 tools/tjek_bydeform.py` og `python3 tools/tjek_sprog.py` melder "i orden".

Desuden åbnes `traener.html?k=multi-2ru` via en lokal webserver på dansk og engelsk ved 1280, 390 og 320 px, og der spilles en runde i hver situation. Skærmbillederne gemmes i `C:\Users\frank\Kontraktbridge\skaermbilleder\multi-2ru\`. De skal vise:
- et svar i `svar` med forklaring;
- `ret` efter 2♠;
- `dobling`;
- ⓘ med kortet åbent;
- 320 px uden vandret scroll.

## Trin

Arbejdet deles i tre korte sessioner (Styring, punkt 7 og 8 i `PLAN-aabne-opgaver.md`). Ingen session venter på en anden.

1. **Session 1 (Opus):** Tag og gren. Skriv `tools/tjek_multi_2ru.py`, og vis, at den er rød. Skriv konventionskortet, og kør kortets tjek. Stop og rapportér.
2. **Session 2 (Opus):**
   - Skriv `dealer/multi_2ru.py` efter reglerne og grænserne.
   - Tilføj modulet i `build_pools.py`.
   - Kør `python build_pools.py multi-2ru`.
   - Ret `data/konventioner.json`.
   - Byg kortsiden.
   - Kør `tools/tjek_multi_2ru.py`, til den er grøn.
   - Stop og rapportér. Hvis en grænse ikke kan give nok hænder, eller et eksempel kræver en anden grænse, stopper sessionen og spørger i stedet for at vælge selv.
3. **Session 3 (Sonnet, `/model`):** Hele testsuiten én gang i forgrunden, i en ny session. Tag skærmbillederne, stop før fletning, og rapportér med tokenforbruget.

Efter Franks "godkendt" (Sonnet): flet, push, live-tjek af `www.kontraktbridge.dk/konventionstraener/traener.html?k=multi-2ru`, arkivér specen i `docs/specs/` med en linje i `README.md`, og slet grenen.

## Afklaret

1. **Ny generel træner i stedet for `ff-multi-2ru`.** Makker 2 spiller Flannery på 2♦ (aftalt 3. november 2026), og konventionskortene er uafhængige af makker. Multi bliver derfor en træner med system "generel" ligesom Truscott og Crowhurst. Den står på Træn og har ⓘ med konventionskortet. Posten "kommer" under Forslag fjernes. *(Rådgiverens forslag, bekræftet af Frank 21. november 2026.)*
2. **Jyderup gælder, og W udfylder hullerne** (Franks valg 21. november 2026). Åbningen er 5–10 hp med højst ét es (Franks valg). Afsnit B2/B4 i Makker 2-dokumentet står uændret som Makker 2's forslag. Jyderups XX som styrke svarer til B2. Hvis Makker 2 en dag vælger Multi, rettes B2 i en egen spec.
3. **Kun Multi i denne udgave.** Good/Bad Multi, Bikini og Ekrens står på kortet under "Åbne spørgsmål". Muiderberg (Bikini) 2♥/2♠ får sin egen træner efter denne (`SPEC-muiderberg.md`, to kørsler efter Franks spørgsmål 21. november 2026). Den afløser `ff-muiderberg` og retter Bikini-linjen på dette kort.
4. **Et hul efter dobling.** J giver ingen melding til en svag hånd uden ruder og uden fit i begge majorer (W's XX = "meld din farve" er netop den hånd, men J bruger XX til styrke). Sådanne hænder genereres ikke, og spørgsmålet står på kortet.
5. **4♣, 3NT og pas uden indblanding trænes ikke.** Kilderne siger ikke, hvornår svarer selv vil være spilfører (4♣ frem for 4♦), eller hvad 3NT kræver. Begge står som valgmuligheder, men er aldrig det rigtige svar. Pas uden indblanding nævnes ikke.
6. **Grænserne er antagelser.** Tallene under Grænser er rådgiverens forslag, valgt så facit-eksemplerne giver kildens svar. Frank kan rette dem før session 2. *(Bekræftet af Frank 21. november 2026.)*
7. **Kilderne ligger uden for repoet** (`Kontraktbridge\Multi_2ru_Jyderup.pdf` og `Kontraktbridge\Ruder_Multi.docx`). Repoet er offentligt på GitHub, og kortet og specen gengiver reglerne med egne ord.

### Session 1 (21. nov. 2026)

**Status:** Tag og gren er lavet, accepttesten er skrevet og rød, og konventionskortet er skrevet. Sessionen stoppede før generatoren. Intet er flettet eller pushet.

**Tag og commits:** `main` (`02cc549`, lig med `origin/main`) er tagget `v-foer-multi-2ru`. Grenen `multi-2ru` har:
- `75c7be6`: specen;
- `04a3d73`: Afklaret, punkt 1 og 6 bekræftet;
- `acb1c74`: accepttesten, rød;
- `5d4fb40`: kortet;
- derefter dette afsnit og tokenforbruget.

**Accepttesten** `tools/tjek_multi_2ru.py` skriver hvert af de otte punkter som "i orden" eller "RØD" med fejlene:
- Reglerne er skrevet igen fra specen. Tallene læses fra kodeblokken under Grænser og sammenlignes med modulets konstanter og overskriften (punkt 1), så et tal rettes i specen og i modulet.
- Situationerne findes ud fra meldeforløbet, ikke ud fra navnene.
- Punkt 3 kører modulets `export_pool` til en midlertidig fil og fanger "Advarsel: kun …" uden at røre `pools/`.
- Testen er prøvet mod en attrap (modul og pulje lavet af testens egne regler i en midlertidig worktree uden for grenen, nu slettet). Med attrappen var 8 af 8 punkter grønne, og fire indbyggede fejl gjorde punkt 1, 3, 4 og 5 røde.

**Resultat:**
- **Før kortet:** 7 af 8 punkter var røde. Punkt 1–5 var røde, fordi modulet og puljen mangler, punkt 6, fordi posten mangler, og punkt 7, fordi kortet mangler. Punkt 8 var grønt.
- **Efter kortet:** stadig 7 af 8 røde. I punkt 7 er kortfilen, typen, `traener`-feltet, fem af seks afsnit og `tjek_konventionskort.py` ("50 konventionskort er i orden") grønne. Kun eksemplerne og `tjek_kort_eksempler.py multi-2ru` er røde, fordi de kræver puljen. Punkt 1–6 hører til session 2.

**Kortet** (`data/kort/multi-2ru.json`, type `melding`, kategori `aabning`, nøgle `gul`) står i `index.json` efter crowhurst:
- **Meldinger:** 2♦ med Jyderups krav og svarene på 2♦ i ni rækker som i specens tabel.
- **Fortsættelser:** fire grene: åbners svar på 2NT, svarer efter 3♣, krydsmeldingen og åbner efter 2♠.
- **Indmelding:** tre rækker: dobling, 2♠ og 3♣/3♦/4♥.
- **Eksempler:** tomt, se valg 7.
- **Faldgruber:** de tre fra specen.
- **Åbne spørgsmål:** de fem fra specen, med W's tal for Good/Bad Multi, Bikini og Ekrens.

Tal står kun, når kilderne giver dem: 5–10 hp og W's tal. Grænserne fra generatoren står ikke på kortet.

**Øvrige tjek:**
- `tjek_konventionskort.py`, `tjek_fagord.py` og `tjek_bydeform.py` melder "i orden", og `tjek_sprog.py` er OK (10 tests).
- `sprogtjek.py` finder ingen ukendte ord, efter at "ekrens" og "good" (Good/Bad Multi) er kommet i `tools/ordliste.txt`.
- Pixeltestene er ikke kørt (session 3).

**Valg, specen ikke afgør:**
1. **Én situation pr. meldeforløb:** `ret` og `indmelding` har én situation pr. svar og pr. indmelding (6 + 4), fordi `traener.html` tager meldeforløbet fra situationen. "Alle syv situationer" er de syv familier med i alt 15 meldeforløb.
2. **Meldingerne i `ret`:** de lovlige af Pas, 2♠, 3♥, 3♠, 4♦, 4♥ og 4♠, fx efter 4♦ kun Pas, 4♥ og 4♠.
3. **Meldingerne i `indmelding`:** Pas, X og det billigste bud i hver af de tre andre farver: over 2♠ 3♣ 3♦ 3♥, over 3♣ 3♦ 3♥ 3♠, over 3♦ 3♥ 3♠ 4♣ og over 4♥ 4♠ 5♣ 5♦. En situation med X eller XX har `allowX` eller `allowXX`.
4. **Svarene i puljen:** puljen har netop de svar, reglerne kan give, hvert med mindst 7 hænder. Fx har `svar` ikke Pas, 3NT og 4♣ (Afklaret, punkt 5), og `dobling` har ikke 4♣.
5. **Fortolkninger af reglerne:**
   - Over 4♥ kræver 4♠ 4+ spar og 7+ hp, men intet i hjerter.
   - Efter dobling kommer 2♥ kun fra `SVAG_FIT_X`. Svar-reglens "resten" gælder ikke dér, så de hænder genereres ikke.
   - 1♥/1♠ og pas ved åbningen kræver præcis seks kort i én major, men intet om den anden major.
   - `spm2` med minimum ligger uden for reglerne, og modulet giver dér ingen melding.
   - To lige lange gode minorer under `svar` ligger uden for reglerne.
6. **Bonusspørgsmålene og de fredede filer:**
   - Specens seks bonusspørgsmål står ordret i mindst én situation i hver familie.
   - Alle situationer har tre svarmuligheder på begge sprog.
   - Punkt 6 tjekker også, at de øvrige poster og de fire fredede filer (`viden/2-over-1-makker2.html`, `traener.html`, `dealer/core.py`, `dealer/crowhurst.py`) er som i tagget.
7. **Kortets eksempler:** afsnittet er tomt indtil session 2, fordi eksemplerne hentes fra puljen. Testen kræver eksempler med samme meldeforløb og svar som eksempel 3, 4, 5 og 9.
8. **Kortets fod og forveksling:**
   - `forveksles` er "Forsvar mod Multi 2♦ (Crowhurst)" og "Multiforsvar", og `relaterede` er tom.
   - Der er ingen `alert`-linje.
   - Kilden står som "Jyderup Bridgeklub: Multi 2ru · hullerne udfyldt efter dokumentet Ruder Multi".
9. **Ordlisten:** "ekrens" og "good" står i `tools/ordliste.txt`. Afgrænsningen nævner ikke filen, men efter `CLAUDE.md` står rigtige ord dér.

**Spørgsmål til Frank:**
1. **Pixeltestene:** `tools/tjek_viden_320.mjs` og `tools/tjek_crowhurst_390.mjs` forventer præcis 49 kort (`ider.length === 49`). Med multi-2ru er der 50, og Afgrænsningen tillader ikke at rette dem. Må tallet rettes til 50? Og hvordan skal det nye kort sammenlignes med tagget, som ikke har det? Session 3 kører dem.
2. **Over 4♥:** er 4♠ rigtigt forstået (4+ spar og 7+ hp, uden krav til hjerter)?
3. **Ekrens:** kortet skriver "Ekrens" som specen, mens crowhurst-kortet kalder 2♦ med begge majorer "Ekren". Er det i orden?
4. **Alert:** skal kortet have en `alert`-linje, fx "2♦ alerteres"?

**Tilbage til session 2:**
- `dealer/multi_2ru.py`: grænserne ordret fra specen under overskriften, `SITUATIONS`, `CLASSIFIERS`, `PER_CALL` (mindst 7) og `export_pool`.
- Modulet i `build_pools.py`, og puljen bygget med `python build_pools.py multi-2ru`.
- Posten i `data/konventioner.json` ordret fra specen, og `ff-multi-2ru` fjernet.
- Fire eksempler på kortet fra puljen med forklaring, så `tjek_kort_eksempler.py multi-2ru` giver 0 advarsler. Indtil da fejler `tjek_kort_eksempler.py` for alle kort, fordi `pools/multi-2ru.json` mangler.
- Kortsiden bygget, og `tjek_multi_2ru.py` grøn.

**Session 3** kører hele testsuiten og tager skærmbillederne, og spørgsmål 1 skal være afklaret før da.

**Tokenforbrug i session 1** (75 svar, 11:01–11:23 UTC, målt før den sidste commit): nye input 150 · skrevet til cachen 240.132 · læst fra cachen 11.994.692 · output 109.409; i alt 12.344.383.

**Tokenforbrug** (udfyldes af hver session: nye input · skrevet til cachen · læst fra cachen · output):
- Session 1: 150 · 240.132 · 11.994.692 · 109.409; i alt 12.344.383
- Session 2:
- Session 3:
- Efter godkendelsen:

### Franks svar, 21. nov. 2026

Ordret fra Franks besked til session 2:

> "Læs SPEC-multi-2ru.md, og lav session 2. Svar på dine fire spørgsmål (Franks valg): (1) tjek_viden_320.mjs og tjek_crowhurst_390.mjs må rettes fra 49 til 50 kort; det nye kort multi-2ru tjekkes kun for vandret scroll, og de 49 andre sammenlignes med tagget som før. (2) Ja: over modpartens 4♥ er 4♠ 4+ spar og 7+ hp uden krav til hjerter. (3) Skriv 'Ekren' som på Crowhurst-kortet, og fjern 'ekrens' fra ordlisten. (4) Kortet får linjen '2♦ er kunstig og alerteres.' under Meldinger. Tag desuden én småting med: i assets/footer.js kommer Modspil med under 'Trænere' lige efter Håndevaluering, med link('/fordelingstraeneren/#modspil', 'Modspil', 'Defence'); kør node tools/tjek_sidefod.mjs bagefter. Stop derefter, og rapportér med tokenforbruget i fire tal."
