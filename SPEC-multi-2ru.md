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
- **Ekren:** 2♥ 55 i major og 2♠ 55 i minor.

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
   - Hvad 2♥ og 2♠ bruges til (Good/Bad Multi, Bikini eller Ekren, med tallene fra W).

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
3. **Kun Multi i denne udgave.** Good/Bad Multi, Bikini og Ekren står på kortet under "Åbne spørgsmål". Muiderberg (Bikini) 2♥/2♠ får sin egen træner efter denne (`SPEC-muiderberg.md`, to kørsler efter Franks spørgsmål 21. november 2026). Den afløser `ff-muiderberg` og retter Bikini-linjen på dette kort.
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
- Session 2: 194 · 309.681 · 19.760.828 · 116.651; i alt 20.187.354
- Session 3:
- Efter godkendelsen:

### Franks svar, 21. nov. 2026

Ordret fra Franks besked til session 2:

> "Læs SPEC-multi-2ru.md, og lav session 2. Svar på dine fire spørgsmål (Franks valg): (1) tjek_viden_320.mjs og tjek_crowhurst_390.mjs må rettes fra 49 til 50 kort; det nye kort multi-2ru tjekkes kun for vandret scroll, og de 49 andre sammenlignes med tagget som før. (2) Ja: over modpartens 4♥ er 4♠ 4+ spar og 7+ hp uden krav til hjerter. (3) Skriv 'Ekren' som på Crowhurst-kortet, og fjern 'ekrens' fra ordlisten. (4) Kortet får linjen '2♦ er kunstig og alerteres.' under Meldinger. Tag desuden én småting med: i assets/footer.js kommer Modspil med under 'Trænere' lige efter Håndevaluering, med link('/fordelingstraeneren/#modspil', 'Modspil', 'Defence'); kør node tools/tjek_sidefod.mjs bagefter. Stop derefter, og rapportér med tokenforbruget i fire tal."

### Session 2 (21. nov. 2026)

**Status:** Generatoren, puljen, posten, kortets eksempler, linjen om alertering, Ekren, Modspil i sidefoden og rettelserne af de to pixeltests er lavet, og accepttesten er grøn på 8 af 8 punkter. Sessionen stoppede før testsuiten og skærmbillederne (session 3). Intet er flettet eller pushet.

**Commits på `multi-2ru`:**
- `1c8bdec`: modellerne under Trin (Opus og Sonnet), som stod urettet i arbejdskopien;
- `f170a22`: Franks svar ordret;
- `3e1ac7e`: `dealer/multi_2ru.py`, `build_pools.py`, puljen og posten;
- `97add44`: kortets eksempler, linjen om alertering, Ekren og ordlisten;
- `425462f`: Modspil i sidefoden og `tjek_sidefod.mjs`;
- `7357134`: de to pixeltests;
- derefter dette afsnit og tokenforbruget.

**Bygget:**
- **Modulet** `dealer/multi_2ru.py` har grænserne ordret fra specen under overskriften og 15 situationer: `aabning`, `svar`, seks `ret_*` (efter 2♥, 2♠, 3♥, 3♠, 4♣ og 4♦), `spm`, `spm2`, `dobling` og fire `ind_*` (over 2♠, 3♣, 3♦ og 4♥). `PER_CALL` er 7 for hver situation, og `export_pool` tjekker først specens ti facit-hænder.
- **Puljen** `pools/multi-2ru.json` er bygget med `python build_pools.py multi-2ru`: 499 hænder fordelt på 57 meldinger, 8–9 pr. melding (7 plus andelen af de 100 ekstra) og ingen "Advarsel: kun …".
- **Posten** `multi-2ru` står ordret fra specen sidst i `data/konventioner.json`, og `ff-multi-2ru` er fjernet. De øvrige poster er uændrede.
- **Kortets eksempler** kommer fra puljen med samme meldeforløb og svar som eksempel 3, 4, 5 og 9 og med puljens forklaring:
  - 2♦ – pas – ?: ♠– ♥EKDT832 ♦D86 ♣KB7 (15 hp) → 4♥;
  - 2♦ – pas – ?: ♠D76 ♥EKD5 ♦E743 ♣KB (19 hp) → 2NT;
  - 2♦ – X – ?: ♠DB6 ♥97 ♦E976543 ♣9 (7 hp) → pas;
  - 2♦ – (4♥) – ?: ♠T542 ♥T643 ♦EKT94 ♣– (7 hp) → 4♠.
- **Kortsiden** er bygget med `tools/build_konventionskort.py`. Siden henter kortene fra `data/kort/`, så de byggede filer er uændrede.
- **Svar 2 (4♠ over 4♥):** reglen er 4+ spar og 7+ hp uden krav til hjerter. Accepttesten tolkede det allerede sådan og er ikke rettet.
- **Svar 3 (Ekren):** "Ekren" står på kortet og i specens tekst (Kilderne, Konventionskortet og Afklaret, punkt 3). Referatet fra session 1 og Franks svar står, som de blev skrevet. "ekrens" er fjernet fra `tools/ordliste.txt`.
- **Svar 4 (alertering):** linjen står i 2♦-rækken under Meldinger (valg 2).

**Rettelser af tests (Franks svar 1 og opgaven med sidefoden):**
1. `tools/tjek_sidefod.mjs`: før forventede testen fem links under Trænere (til og med Håndevaluering), nu seks med Modspil (`/fordelingstraeneren/#modspil`) og "Defence" på engelsk. Før rettelsen fejlede kun de 13 tjek af listen over links (12 på dansk og 1 på engelsk); alle mål var i orden.
2. `tools/tjek_viden_320.mjs`: før `ider.length === 49` på siden nu, nu 50. Nyt: `NYE_KORT = ['multi-2ru']` tjekkes for vandret scroll ved 390 og 1280 px (fuld og kompakt, dansk og engelsk) ud over 320 og 375 px, hvor alle kort tjekkes, og pixelsløjfen over tagets kort springer `NYE_KORT` over. De 49 kort sammenlignes med tagget som før.
3. `tools/tjek_crowhurst_390.mjs`: før `ider.length === 49` på siden fra tagget, som altid har 49 kort, så 50 dér ville altid fejle. Nu tjekkes det, at siden nu har 50 kort, tagget 49, og at alle tagets kort findes på siden nu. Nyt afsnit 1b: `multi-2ru` tjekkes for vandret scroll ved 390, 393, 395, 398, 399 og 1280 px (fuld og kompakt, dansk og engelsk), og pixelsløjfen springer `NYE_KORT` over.

`tools/tjek_multi_2ru.py` er ikke rettet. Pixeltestene er kun tjekket for syntaks (`node --check`): de kan ikke køre ét kort alene, så de køres i session 3.

**Testresultater:**
- `tjek_multi_2ru.py`: i orden (8 af 8 punkter);
- `tjek_konventionskort.py`: "50 konventionskort er i orden";
- `tjek_kort_eksempler.py multi-2ru`: "4 meldeeksempler er i orden (0 advarsler)", og for alle kort 223 i orden (0 advarsler);
- `tjek_fagord.py` og `tjek_bydeform.py`: i orden; `tjek_sprog.py`: OK (10 tests);
- `sprogtjek.py`: ingen ukendte ord;
- `tjek_sidefod.mjs`: alt i orden.

**Sidefoden:** Modspil står under Trænere lige efter Håndevaluering i `assets/footer.js`. Forsidens sidefod har ikke Modspil, så de to sidefødder er ikke længere ens (`SPEC-sidefod.md`); se spørgsmål 3.

**Sidefoden og kortlisten rammer pixeltestene i session 3.** Begge tests viser siden før fra tagget med alle dens filer (kun Makker 2-dokumentet kommer fra en nyere commit, `NYERE`), og skærmbilledet tager hele siden med:
- Sidefoden står på alle sider i `viden/` og på kortsiden. Med Modspil bliver Trænere én linje længere, så siderne bliver højere, og alle sammenligninger af sider og kort ved 390, 399 og 1280 px vil fejle ("højden er … px, før … px").
- Kortsiden viser alle kort som knapper (`#valg`) over kortet. Knappen "Multi 2♦" kommer med, så kortsiden og alle 49 kort vil afvige fra tagget, også uden sidefoden.

`tjek_bred_multi.mjs` skjuler allerede sidefoden (`SPEC-sidefod.md`) og rammes ikke. Intet er skjult i de to tests; mulige løsninger står i spørgsmål 1.

**Valg, specen ikke afgør:**
1. **Bonusspørgsmålene i `ret`:** punkt 3 kræver et helt engelsk bonusspørgsmål, og `bilingual` udelader tekster, der er ens på begge sprog (fx "2♠"). Svarene er derfor skrevet som tekst, der er forskellig på de to sprog, og spørgsmålet efter 2♥ er "Hvad betyder svarers 2♥ efter 2♦?". Specens seks spørgsmål står ordret.
2. **Linjen om alertering:** skabelonen har ingen note under afsnit 1, og feltet `alert` vises i hovedet (mærket "Alertér") og i Situation, ikke under Meldinger. Linjen står derfor sidst i 2♦-rækkens "viser", så den også ses i kompaktvisningen bag ⓘ i træneren. Feltet `alert` er ikke brugt (spørgsmål 2).
3. **Forklaringerne** nævner håndens tal (længder, honnører og hp) og kildens regel, men ikke grænserne fra generatoren. Over 2♠ er 3♥ forklaret som "støtte til hjerter. Når modparten melder spar, har åbner oftest hjerter." Det er Claude Codes begrundelse, ikke kildens.
4. **Hænderne:** samplerne trækker fordelinger, der passer til reglen, og bedømmelsen afgør svaret. Åbners hånd har højst fire kort i hver minor. "Resten" (2♥) trækkes blandt tilfældige hænder med 0–12 hp og hænder med 13–15 hp, der mangler tre kort i en major.
5. **Renonce og singleton i forklaringerne:** "ingen hjerter" og "1 hjerter" (engelsk "no hearts" og "1 heart").
6. **Modellerne under Trin** stod urettet i arbejdskopien ved sessionens start og er committet for sig i `1c8bdec`.

**Spørgsmål til Frank:**
1. **Pixeltestene i session 3:** hvordan skal sidefoden og knappen "Multi 2♦" behandles i sammenligningen med tagget?
   - (a) Som Makker 2-dokumentet (`NYERE`): siden før henter `assets/footer.js`, `data/kort/index.json` og `data/kort/multi-2ru.json` fra en godkendt commit på grenen, så kun utilsigtede ændringer tæller. Tagget har da også 50 kort, og `NYE_KORT` holder multi-2ru uden for pixelsammenligningen. Claude Codes forslag.
   - (b) Sidefoden skjules som i `tjek_bred_multi.mjs`, og kortlisten `#valg` skjules også.
   - (c) Ingen ændring: session 3 får røde pixeltjek og vurderer dem ud fra skærmbillederne.
2. **Alertering:** skal kortet også have feltet `alert` ("2♦ alerteres"), så mærket "Alertér" står i hovedet som på fx Flannery-kortet?
3. **Sidefoden på forsiden og i Fordelingstræneren:** skal de også have Modspil, så sidefødderne igen er ens (hver i sit repo)?
4. **Forsidens tal:** "45 konventioner" i topbåndet hentes ikke automatisk. Med Multi går posterne med status "klar" i `data/konventioner.json` fra 48 til 49. Skal tallet rettes, når Multi udgives?
5. **Teksterne:** forklaringerne og bonusspørgsmålene i `dealer/multi_2ru.py` venter på Franks godkendelse før fletningen (specen, Forklaringer og bonusspørgsmål).

**Tilbage til session 3:**
- svaret på spørgsmål 1, før pixeltestene køres;
- hele testsuiten én gang i forgrunden, med de nye tjek af `multi-2ru` i `tjek_viden_320.mjs` og `tjek_crowhurst_390.mjs`;
- skærmbillederne af `traener.html?k=multi-2ru` (specen, Accepttest) i `C:\Users\frank\Kontraktbridge\skaermbilleder\multi-2ru\`;
- stop før fletning og en rapport med tokenforbruget.

**Tokenforbrug i session 2** (97 svar, 14:37–14:59 UTC, målt før den sidste commit): nye input 194 · skrevet til cachen 309.681 · læst fra cachen 19.760.828 · output 116.651; i alt 20.187.354.

### Franks svar 2, 24. nov. 2026

Ordret fra Franks besked til session 2b:

> "Svar på session 2's spørgsmål:
> Pixeltestene: (a). Siden før henter footer.js, index.json og multi-2ru.json fra commit <hash>, som skrives under Afklaret. Gem skærmbilleder af én side i viden/ og af kortsiden med knappen 'Multi 2♦'.
> Kortet får også feltet alert, hvis andre kort bruger det. Linjen under Meldinger bliver stående.
> Sidefoden i Forside og Fordelingstræneren kommer på næste gren i de repoer, ikke her.
> Forsidens tal rettes på Forsides næste gren. Skriv i rapporten, hvad tallet '45 konventioner' tæller.
> Læg alle forklaringer og bonusspørgsmål i en tabel til gennemgang, dansk og engelsk side om side. Forklaringen af 3♥ over 2♠ skal sige, hvad meldingen betyder efter Jyderup-arket. Agentens begrundelse markeres som tilføjelse.
> Kør hele suiten og pixeltestene i forgrunden. Stop før fletning."

### Tekster til gennemgang

Alle forklaringer og bonusspørgsmål i `dealer/multi_2ru.py`, som de står i puljen `pools/multi-2ru.json` fra session 2, med dansk og engelsk side om side. Tabellen har én række pr. situation og melding (57) og én række med bonusspørgsmålet pr. situation (15), i alt 72 rækker.
- Tallene er håndens tal fra ét eksempel i puljen. Har en melding flere udgaver af teksten, står de under hinanden.
- Minimum og maksimum er specens grænser (5–7 og 8–10 hp).
- **(tilføjelse)** markerer tekst, der bygger på Claude Codes egen begrundelse eller på en betydning, som kilden ikke giver. Noterne under tabellen siger hvorfor. De nævner også, hvor en tekst bygger på en grænse fra specen eller på Franks svar i stedet for kildens ord.

| Situation | Melding | Dansk | Engelsk |
| --- | --- | --- | --- |
| `aabning`<br>? | Pas | 6 spar og kun 1 hp: pas – Multi 2♦ kræver mindst 5 hp. | 6 spades and only 1 HCP: pass – Multi 2♦ needs at least 5 HCP. |
| `aabning`<br>? | 1♥ | 6 hjerter og 14 hp: 1♥ – med 11–15 hp er hånden for stærk til Multi 2♦ (5–10 hp). (note 5) | 6 hearts and 14 HCP: 1♥ – with 11–15 HCP the hand is too strong for Multi 2♦ (5–10 HCP). |
| `aabning`<br>? | 1♠ | 6 spar og 11 hp: 1♠ – med 11–15 hp er hånden for stærk til Multi 2♦ (5–10 hp). (note 5) | 6 spades and 11 HCP: 1♠ – with 11–15 HCP the hand is too strong for Multi 2♦ (5–10 HCP). |
| `aabning`<br>? | 2♦ | 6 spar uden firfarve i hjerter, 7 hp og intet es: 2♦ – seksfarve i hjerter eller spar, 5–10 hp, ingen firfarve i den anden major og højst ét es. | 6 spades without four hearts, 7 HCP and no ace: 2♦ – a six-card suit in hearts or spades, 5–10 HCP, no four-card suit in the other major and at most one ace. |
| `aabning`<br>? | Bonusspørgsmål | Hvilke krav stiller Multi 2♦ til hånden?<br>Rigtigt: 5–10 hp, seksfarve i en major, ingen firfarve i den anden major og højst ét es<br>Forkert: 5–10 hp og en seksfarve i en hvilken som helst farve; 11–15 hp og en seksfarve i en major<br>Forklaring: Multi 2♦ viser en svag 2 i hjerter eller spar: 5–10 hp og en seksfarve uden firfarve i den anden major og med højst ét es. Formålet er at frigøre 2♥ og 2♠. | What does Multi 2♦ require of the hand?<br>Right: 5–10 HCP, a six-card major, no four-card suit in the other major and at most one ace<br>Wrong: 5–10 HCP and a six-card suit in any suit; 11–15 HCP and a six-card major<br>Explanation: Multi 2♦ shows a weak two in hearts or spades: 5–10 HCP and a six-card suit without a four-card suit in the other major and with at most one ace. The purpose is to free 2♥ and 2♠. |
| `svar`<br>2♦ – pas – ? | 2♥ | 4 hjerter, 1 spar og 15 hp: 2♥ – søger farven (pas eller ret). Åbner passer med hjerter og melder 2♠ med spar. | 4 hearts, 1 spade and 15 HCP: 2♥ – asks for the suit (pass or correct). Opener passes with hearts and bids 2♠ with spades. |
| `svar`<br>2♦ – pas – ? | 2♠ | 5 hjerter og 11 hp: 2♠ – invit med hjerter. Åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum. | 5 hearts and 11 HCP: 2♠ – invitational in hearts. Opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum. |
| `svar`<br>2♦ – pas – ? | 2NT | 18 hp: 2NT – spørger om styrken. Åbner svarer 3♣ med maksimum, 3♦ med minimum og hjerter og 3♥ med minimum og spar. | 18 HCP: 2NT – asks about strength. Opener bids 3♣ with a maximum, 3♦ with a minimum and hearts and 3♥ with a minimum and spades. |
| `svar`<br>2♦ – pas – ? | 3♣ | 6 klør med 2 af de tre øverste honnører og 15 hp: 3♣ – krav med egen farve. | 6 clubs with 2 of the top three honours and 15 HCP: 3♣ – forcing with responder's own suit. |
| `svar`<br>2♦ – pas – ? | 3♦ | 6 ruder med 2 af de tre øverste honnører og 14 hp: 3♦ – krav med egen farve. | 6 diamonds with 2 of the top three honours and 14 HCP: 3♦ – forcing with responder's own suit. |
| `svar`<br>2♦ – pas – ? | 3♥ | 4 hjerter, 3 spar og 6 hp: 3♥ – pas eller ret, en spærremelding i makkers farve. Åbner passer med hjerter og melder 3♠ med spar. | 4 hearts, 3 spades and 6 HCP: 3♥ – pass or correct, a preempt in partner's suit. Opener passes with hearts and bids 3♠ with spades. |
| `svar`<br>2♦ – pas – ? | 3♠ | 4 hjerter, 5 spar og 8 hp: 3♠ – pas eller ret, en spærremelding i makkers farve. Åbner passer med spar og melder 4♥ med hjerter. | 4 hearts, 5 spades and 8 HCP: 3♠ – pass or correct, a preempt in partner's suit. Opener passes with spades and bids 4♥ with hearts. |
| `svar`<br>2♦ – pas – ? | 4♦ | 4 hjerter, 3 spar og 14 hp: 4♦ – åbner melder sin farve på 4-trinnet. | 4 hearts, 3 spades and 14 HCP: 4♦ – opener bids the suit at the four level. |
| `svar`<br>2♦ – pas – ? | 4♥ | 7 hjerter med 3 af de tre øverste honnører og 10 hp: 4♥ – svarers egen farve, og åbner passer. | 7 hearts with 3 of the top three honours and 10 HCP: 4♥ – responder's own suit, and opener passes. |
| `svar`<br>2♦ – pas – ? | 4♠ | 8 spar med 2 af de tre øverste honnører og 13 hp: 4♠ – svarers egen farve, og åbner passer. | 8 spades with 2 of the top three honours and 13 HCP: 4♠ – responder's own suit, and opener passes. |
| `svar`<br>2♦ – pas – ? | Bonusspørgsmål | Hvad betyder 2♠ som svar på Multi?<br>Rigtigt: Invit med hjerter<br>Forkert: Pas eller ret i makkers farve; Naturligt med egen sparfarve<br>Forklaring: 2♠ er invit med hjerter: åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum. Det er 2♥, der søger farven (pas eller ret). | What does 2♠ mean in response to Multi?<br>Right: Invitational in hearts<br>Wrong: Pass or correct in partner's suit; Natural with responder's own spade suit<br>Explanation: 2♠ is invitational in hearts: opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum. It is 2♥ that asks for the suit (pass or correct). |
| `ret_2h`<br>2♦ – pas – 2♥ – pas – ? | Pas | 6 hjerter: pas. 2♥ søger farven: åbner passer med hjerter og melder 2♠ med spar. | 6 hearts: pass. 2♥ asks for the suit: opener passes with hearts and bids 2♠ with spades. |
| `ret_2h`<br>2♦ – pas – 2♥ – pas – ? | 2♠ | 6 spar: 2♠. 2♥ søger farven: åbner passer med hjerter og melder 2♠ med spar. | 6 spades: 2♠. 2♥ asks for the suit: opener passes with hearts and bids 2♠ with spades. |
| `ret_2h`<br>2♦ – pas – 2♥ – pas – ? | Bonusspørgsmål | Hvad betyder svarers 2♥ efter 2♦?<br>Rigtigt: Søger farven: åbner passer med hjerter og melder 2♠ med spar<br>Forkert: Naturligt med egen hjertefarve; Invit med hjerter<br>Forklaring: 2♥ søger farven (pas eller ret): åbner passer med hjerter og melder 2♠ med spar. Det er 2♠, der er invit med hjerter. | What does responder's 2♥ mean after 2♦?<br>Right: Asks for the suit: opener passes with hearts and bids 2♠ with spades<br>Wrong: Natural with responder's own heart suit; Invitational in hearts<br>Explanation: 2♥ asks for the suit (pass or correct): opener passes with hearts and bids 2♠ with spades. It is 2♠ that is invitational in hearts. |
| `ret_2s`<br>2♦ – pas – 2♠ – pas – ? | Pas | 6 spar: pas. 2♠ er invit med hjerter: åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum. | 6 spades: pass. 2♠ is invitational in hearts: opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum. |
| `ret_2s`<br>2♦ – pas – 2♠ – pas – ? | 3♥ | 6 hjerter og 5 hp (minimum): 3♥. 2♠ er invit med hjerter: åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum. | 6 hearts and 5 HCP (a minimum): 3♥. 2♠ is invitational in hearts: opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum. |
| `ret_2s`<br>2♦ – pas – 2♠ – pas – ? | 4♥ | 6 hjerter og 8 hp (maksimum): 4♥. 2♠ er invit med hjerter: åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum. | 6 hearts and 8 HCP (a maximum): 4♥. 2♠ is invitational in hearts: opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum. |
| `ret_2s`<br>2♦ – pas – 2♠ – pas – ? | Bonusspørgsmål | Hvad melder åbner med hjerter efter 2♦ – 2♠?<br>Rigtigt: 3♥ med minimum og 4♥ med maksimum<br>Forkert: Pas, fordi 2♠ er pas eller ret; Altid 4♥<br>Forklaring: 2♠ er invit med hjerter: åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum. | What does opener bid with hearts after 2♦ – 2♠?<br>Right: 3♥ with a minimum and 4♥ with a maximum<br>Wrong: Pass, because 2♠ is pass or correct; Always 4♥<br>Explanation: 2♠ is invitational in hearts: opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum. |
| `ret_3h`<br>2♦ – pas – 3♥ – pas – ? | Pas | 6 hjerter: pas. 3♥ er pas eller ret: åbner passer med hjerter og melder 3♠ med spar. | 6 hearts: pass. 3♥ is pass or correct: opener passes with hearts and bids 3♠ with spades. |
| `ret_3h`<br>2♦ – pas – 3♥ – pas – ? | 3♠ | 6 spar: 3♠. 3♥ er pas eller ret: åbner passer med hjerter og melder 3♠ med spar. | 6 spades: 3♠. 3♥ is pass or correct: opener passes with hearts and bids 3♠ with spades. |
| `ret_3h`<br>2♦ – pas – 3♥ – pas – ? | Bonusspørgsmål | Hvad betyder svarers 3♥ efter 2♦?<br>Rigtigt: Pas eller ret: spærremelding i makkers farve<br>Forkert: Krav med egen hjertefarve; Invit med hjerter<br>Forklaring: 3♥ og 3♠ er pas eller ret: svarer spærrer i makkers farve. Efter 3♥ passer åbner med hjerter og melder 3♠ med spar. | What does responder's 3♥ mean after 2♦?<br>Right: Pass or correct: a preempt in partner's suit<br>Wrong: Forcing with responder's own heart suit; Invitational in hearts<br>Explanation: 3♥ and 3♠ are pass or correct: responder preempts in partner's suit. After 3♥ opener passes with hearts and bids 3♠ with spades. |
| `ret_3s`<br>2♦ – pas – 3♠ – pas – ? | Pas | 6 spar: pas. 3♠ er pas eller ret: åbner passer med spar og melder 4♥ med hjerter. | 6 spades: pass. 3♠ is pass or correct: opener passes with spades and bids 4♥ with hearts. |
| `ret_3s`<br>2♦ – pas – 3♠ – pas – ? | 4♥ | 6 hjerter: 4♥. 3♠ er pas eller ret: åbner passer med spar og melder 4♥ med hjerter. | 6 hearts: 4♥. 3♠ is pass or correct: opener passes with spades and bids 4♥ with hearts. |
| `ret_3s`<br>2♦ – pas – 3♠ – pas – ? | Bonusspørgsmål | Hvad melder åbner med hjerter efter 2♦ – 3♠?<br>Rigtigt: 4♥, fordi 3♠ er pas eller ret<br>Forkert: Pas, fordi 3♠ er naturligt; 4♦, farven under sin egen<br>Forklaring: 3♠ er pas eller ret: åbner passer med spar og melder 4♥ med hjerter. | What does opener bid with hearts after 2♦ – 3♠?<br>Right: 4♥, because 3♠ is pass or correct<br>Wrong: Pass, because 3♠ is natural; 4♦, the suit below his own<br>Explanation: 3♠ is pass or correct: opener passes with spades and bids 4♥ with hearts. |
| `ret_4c`<br>2♦ – pas – 4♣ – pas – ? | 4♦ | 6 hjerter: 4♦. 4♣ er transfer: åbner melder farven under sin egen, 4♦ med hjerter og 4♥ med spar. | 6 hearts: 4♦. 4♣ is a transfer: opener bids the suit below his own, 4♦ with hearts and 4♥ with spades. |
| `ret_4c`<br>2♦ – pas – 4♣ – pas – ? | 4♥ | 6 spar: 4♥. 4♣ er transfer: åbner melder farven under sin egen, 4♦ med hjerter og 4♥ med spar. | 6 spades: 4♥. 4♣ is a transfer: opener bids the suit below his own, 4♦ with hearts and 4♥ with spades. |
| `ret_4c`<br>2♦ – pas – 4♣ – pas – ? | Bonusspørgsmål | Hvad melder åbner efter 4♣?<br>Rigtigt: Farven under sin egen: 4♦ med hjerter og 4♥ med spar<br>Forkert: Sin egen farve: 4♥ eller 4♠; 4♦ uanset farven<br>Forklaring: 4♣ er transfer: åbner melder farven under sin egen, 4♦ med hjerter og 4♥ med spar. Efter 4♦ melder åbner sin egen farve. | What does opener bid after 4♣?<br>Right: The suit below his own: 4♦ with hearts and 4♥ with spades<br>Wrong: His own suit: 4♥ or 4♠; 4♦ whatever the suit<br>Explanation: 4♣ is a transfer: opener bids the suit below his own, 4♦ with hearts and 4♥ with spades. After 4♦ opener bids his own suit. |
| `ret_4d`<br>2♦ – pas – 4♦ – pas – ? | 4♥ | 6 hjerter: 4♥. Efter 4♦ melder åbner sin farve: 4♥ med hjerter og 4♠ med spar. | 6 hearts: 4♥. After 4♦ opener bids his suit: 4♥ with hearts and 4♠ with spades. |
| `ret_4d`<br>2♦ – pas – 4♦ – pas – ? | 4♠ | 6 spar: 4♠. Efter 4♦ melder åbner sin farve: 4♥ med hjerter og 4♠ med spar. | 6 spades: 4♠. After 4♦ opener bids his suit: 4♥ with hearts and 4♠ with spades. |
| `ret_4d`<br>2♦ – pas – 4♦ – pas – ? | Bonusspørgsmål | Hvad melder åbner efter 4♦?<br>Rigtigt: Sin egen farve: 4♥ eller 4♠<br>Forkert: Farven under sin egen; Pas<br>Forklaring: Efter 4♦ melder åbner sin egen farve. Efter 4♣ (transfer) melder han farven under sin egen. | What does opener bid after 4♦?<br>Right: His own suit: 4♥ or 4♠<br>Wrong: The suit below his own; Pass<br>Explanation: After 4♦ opener bids his own suit. After 4♣ (a transfer) he bids the suit below his own. |
| `spm`<br>2♦ – pas – 2NT – pas – ? | 3♣ | 6 spar og 9 hp (maksimum): 3♣ – maksimum. Farven vises bagefter med en krydsmelding. | 6 spades and 9 HCP (a maximum): 3♣ – a maximum. The suit is shown afterwards with a crossover bid. |
| `spm`<br>2♦ – pas – 2NT – pas – ? | 3♦ | 6 hjerter og 5 hp (minimum): 3♦ – minimum og hjerter. | 6 hearts and 5 HCP (a minimum): 3♦ – a minimum and hearts. |
| `spm`<br>2♦ – pas – 2NT – pas – ? | 3♥ | 6 spar og 5 hp (minimum): 3♥ – minimum og spar. | 6 spades and 5 HCP (a minimum): 3♥ – a minimum and spades. |
| `spm`<br>2♦ – pas – 2NT – pas – ? | Bonusspørgsmål | Hvad viser åbners 3♣ efter 2♦ – 2NT?<br>Rigtigt: Maksimum<br>Forkert: Minimum og hjerter; Klør<br>Forklaring: Efter 2NT viser 3♣ maksimum, 3♦ minimum og hjerter og 3♥ minimum og spar. Efter 3♣ søger svarer farven med 3♦, og åbner viser den med en krydsmelding. | What does opener's 3♣ show after 2♦ – 2NT?<br>Right: A maximum<br>Wrong: A minimum and hearts; Clubs<br>Explanation: After 2NT, 3♣ shows a maximum, 3♦ a minimum and hearts and 3♥ a minimum and spades. After 3♣ responder asks for the suit with 3♦, and opener shows it with a crossover bid. |
| `spm2`<br>2♦ – pas – 2NT – pas – 3♣ – pas – 3♦ – pas – ? | 3♥ | 6 spar: 3♥. Efter 3♦ viser åbner farven med en krydsmelding: 3♥ = spar og 3♠ = hjerter. | 6 spades: 3♥. After 3♦ opener shows the suit with a crossover bid: 3♥ = spades and 3♠ = hearts. |
| `spm2`<br>2♦ – pas – 2NT – pas – 3♣ – pas – 3♦ – pas – ? | 3♠ | 6 hjerter: 3♠. Efter 3♦ viser åbner farven med en krydsmelding: 3♥ = spar og 3♠ = hjerter. | 6 hearts: 3♠. After 3♦ opener shows the suit with a crossover bid: 3♥ = spades and 3♠ = hearts. |
| `spm2`<br>2♦ – pas – 2NT – pas – 3♣ – pas – 3♦ – pas – ? | Bonusspørgsmål | Hvad betyder svarers 3♥ efter 2♦ – 2NT – 3♣?<br>Rigtigt: Krav med egen farve<br>Forkert: Søger farven; Pas eller ret<br>Forklaring: Efter 3♣ (maksimum) er det 3♦, der søger farven, og åbner viser den med en krydsmelding: 3♥ = spar og 3♠ = hjerter. Svarers 3♥ og 3♠ er krav med egen farve. | What does responder's 3♥ mean after 2♦ – 2NT – 3♣?<br>Right: Forcing with responder's own suit<br>Wrong: Asks for the suit; Pass or correct<br>Explanation: After 3♣ (a maximum) it is 3♦ that asks for the suit, and opener shows it with a crossover bid: 3♥ = spades and 3♠ = hearts. Responder's 3♥ and 3♠ are forcing with responder's own suit. |
| `dobling`<br>2♦ – (X) – ? | Pas | 7 ruder og 6 hp: pas – en svag hånd med ruder, for at spille 2♦ doblet. | 7 diamonds and 6 HCP: pass – a weak hand with diamonds, to play 2♦ doubled. |
| `dobling`<br>2♦ – (X) – ? | XX | ingen hjerter, 1 spar og 15 hp: XX – styrke med interesse for straf. | no hearts, 1 spade and 15 HCP: XX – strength with interest in a penalty. |
| `dobling`<br>2♦ – (X) – ? | 2♥ | 4 hjerter, 3 spar og 4 hp: 2♥ – en svag hånd med fit i begge majorer, pas eller ret. | 4 hearts, 3 spades and 4 HCP: 2♥ – a weak hand with a fit in both majors, pass or correct. |
| `dobling`<br>2♦ – (X) – ? | 2♠ | 3 hjerter og 12 hp: 2♠ – invit med hjerter. Åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum. Doblingen ignoreres, og der meldes som uden dobling. | 3 hearts and 12 HCP: 2♠ – invitational in hearts. Opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum. The double is ignored, and responder bids as without the double. |
| `dobling`<br>2♦ – (X) – ? | 2NT | 18 hp: 2NT – spørger om styrken. Åbner svarer 3♣ med maksimum, 3♦ med minimum og hjerter og 3♥ med minimum og spar. Doblingen ignoreres, og der meldes som uden dobling. | 18 HCP: 2NT – asks about strength. Opener bids 3♣ with a maximum, 3♦ with a minimum and hearts and 3♥ with a minimum and spades. The double is ignored, and responder bids as without the double. |
| `dobling`<br>2♦ – (X) – ? | 3♣ | 6 klør med 2 af de tre øverste honnører og 13 hp: 3♣ – krav med egen farve. Doblingen ignoreres, og der meldes som uden dobling. | 6 clubs with 2 of the top three honours and 13 HCP: 3♣ – forcing with responder's own suit. The double is ignored, and responder bids as without the double. |
| `dobling`<br>2♦ – (X) – ? | 3♦ | 7 ruder med 2 af de tre øverste honnører og 15 hp: 3♦ – krav med egen farve. Doblingen ignoreres, og der meldes som uden dobling. | 7 diamonds with 2 of the top three honours and 15 HCP: 3♦ – forcing with responder's own suit. The double is ignored, and responder bids as without the double. |
| `dobling`<br>2♦ – (X) – ? | 3♥ | 3 hjerter, 3 spar og 10 hp: 3♥ – pas eller ret, en spærremelding i makkers farve. Åbner passer med hjerter og melder 3♠ med spar. Doblingen ignoreres, og der meldes som uden dobling. | 3 hearts, 3 spades and 10 HCP: 3♥ – pass or correct, a preempt in partner's suit. Opener passes with hearts and bids 3♠ with spades. The double is ignored, and responder bids as without the double. |
| `dobling`<br>2♦ – (X) – ? | 3♠ | 5 hjerter, 4 spar og 7 hp: 3♠ – pas eller ret, en spærremelding i makkers farve. Åbner passer med spar og melder 4♥ med hjerter. Doblingen ignoreres, og der meldes som uden dobling. | 5 hearts, 4 spades and 7 HCP: 3♠ – pass or correct, a preempt in partner's suit. Opener passes with spades and bids 4♥ with hearts. The double is ignored, and responder bids as without the double. |
| `dobling`<br>2♦ – (X) – ? | 4♦ | 4 hjerter, 4 spar og 13 hp: 4♦ – åbner melder sin farve på 4-trinnet. Doblingen ignoreres, og der meldes som uden dobling. | 4 hearts, 4 spades and 13 HCP: 4♦ – opener bids the suit at the four level. The double is ignored, and responder bids as without the double. |
| `dobling`<br>2♦ – (X) – ? | 4♥ | 8 hjerter med 2 af de tre øverste honnører og 10 hp: 4♥ – svarers egen farve, og åbner passer. Doblingen ignoreres, og der meldes som uden dobling. | 8 hearts with 2 of the top three honours and 10 HCP: 4♥ – responder's own suit, and opener passes. The double is ignored, and responder bids as without the double. |
| `dobling`<br>2♦ – (X) – ? | 4♠ | 7 spar med 2 af de tre øverste honnører og 11 hp: 4♠ – svarers egen farve, og åbner passer. Doblingen ignoreres, og der meldes som uden dobling. | 7 spades with 2 of the top three honours and 11 HCP: 4♠ – responder's own suit, and opener passes. The double is ignored, and responder bids as without the double. |
| `dobling`<br>2♦ – (X) – ? | Bonusspørgsmål | Hvad viser redobling, når modparten dobler 2♦?<br>Rigtigt: Styrke med interesse for straf<br>Forkert: Ruder, for at spille; En svag hånd med fit i begge majorer<br>Forklaring: Når modparten dobler 2♦, er pas en svag hånd med ruder, XX styrke med interesse for straf og 2♥ en svag hånd med fit i begge majorer. Andre meldinger er som uden dobling. | What does a redouble show when the opponents double 2♦?<br>Right: Strength with interest in a penalty<br>Wrong: Diamonds, to play; A weak hand with a fit in both majors<br>Explanation: When the opponents double 2♦, pass is a weak hand with diamonds, XX strength with interest in a penalty and 2♥ a weak hand with a fit in both majors. Other bids are as without the double. |
| `ind_2s`<br>2♦ – (2♠) – ? | Pas | 5 hjerter og 3 hp: pas – hånden er for svag til at doble og til at støtte hjerter.<br>2 hjerter og 6 hp: pas – hånden er for svag til at doble og har ikke støtte til hjerter. **(tilføjelse, note 2)** | 5 hearts and 3 HCP: pass – the hand is too weak to double and to support hearts.<br>2 hearts and 6 HCP: pass – the hand is too weak to double and has no support for hearts. |
| `ind_2s`<br>2♦ – (2♠) – ? | X | 11 hp: X – styrke (negativ dobling). Med spar passer åbner, så doblingen står som straf. | 11 HCP: X – strength (negative double). With spades opener passes, so the double stands for penalty. |
| `ind_2s`<br>2♦ – (2♠) – ? | 3♥ | 5 hjerter og 9 hp: 3♥ – støtte til hjerter. Når modparten melder spar, har åbner oftest hjerter. **(tilføjelse, note 1)** | 5 hearts and 9 HCP: 3♥ – support for hearts. When the opponents bid spades, opener usually has hearts. |
| `ind_2s`<br>2♦ – (2♠) – ? | Bonusspørgsmål | Hvad betyder dobling efter 2♦ – (2♠)?<br>Rigtigt: Styrke (negativ dobling)<br>Forkert: Straf med spar; Pas eller ret med hjerter<br>Forklaring: Over 2♠ er dobling styrke (negativ dobling). Med spar passer åbner, så doblingen står som straf. | What does a double mean after 2♦ – (2♠)?<br>Right: Strength (negative double)<br>Wrong: Penalty with spades; Pass or correct with hearts<br>Explanation: Over 2♠ a double shows strength (negative double). With spades opener passes, so the double stands for penalty. |
| `ind_3c`<br>2♦ – (3♣) – ? | Pas | 3 hp: pas – intet at tilføje.<br>1 hjerter, 3 spar og 11 hp: pas – uden tre kort i begge majorer er der intet at tilføje. (note 3) | 3 HCP: pass – nothing to add.<br>1 heart, 3 spades and 11 HCP: pass – without three cards in both majors there is nothing to add. |
| `ind_3c`<br>2♦ – (3♣) – ? | X | 5 klør med 2 af de fire øverste honnører og 12 hp: X – straf. | 5 clubs with 2 of the top four honours and 12 HCP: X – penalty. |
| `ind_3c`<br>2♦ – (3♣) – ? | 3♦ | 7 ruder med 2 af de tre øverste honnører og 11 hp: 3♦ – naturligt og ikke krav. | 7 diamonds with 2 of the top three honours and 11 HCP: 3♦ – natural and non-forcing. |
| `ind_3c`<br>2♦ – (3♣) – ? | 3♥ | 4 hjerter, 3 spar og 8 hp: 3♥ – pas eller ret. Åbner passer med hjerter og melder 3♠ med spar. | 4 hearts, 3 spades and 8 HCP: 3♥ – pass or correct. Opener passes with hearts and bids 3♠ with spades. |
| `ind_3c`<br>2♦ – (3♣) – ? | Bonusspørgsmål | Hvad betyder dobling efter 2♦ – (3♣)?<br>Rigtigt: Straf<br>Forkert: Styrke (negativ dobling); Pas eller ret<br>Forklaring: Over 3♣, 3♦ og 4♥ er dobling straf, hjerter eller spar er pas eller ret, og en minor er naturlig og ikke krav. Over 2♠ er dobling styrke. | What does a double mean after 2♦ – (3♣)?<br>Right: Penalty<br>Wrong: Strength (negative double); Pass or correct<br>Explanation: Over 3♣, 3♦ and 4♥ a double is for penalty, hearts or spades are pass or correct, and a minor is natural and non-forcing. Over 2♠ a double shows strength. |
| `ind_3d`<br>2♦ – (3♦) – ? | Pas | 4 hjerter, 2 spar og 9 hp: pas – uden tre kort i begge majorer er der intet at tilføje. Klør kan kun meldes på 4-trinnet.<br>1 hjerter, 4 spar og 9 hp: pas – uden tre kort i begge majorer er der intet at tilføje.<br>6 hp: pas – intet at tilføje. (note 3) | 4 hearts, 2 spades and 9 HCP: pass – without three cards in both majors there is nothing to add. Clubs can only be bid at the four level.<br>1 heart, 4 spades and 9 HCP: pass – without three cards in both majors there is nothing to add.<br>6 HCP: pass – nothing to add. |
| `ind_3d`<br>2♦ – (3♦) – ? | X | 5 ruder med 3 af de fire øverste honnører og 14 hp: X – straf. | 5 diamonds with 3 of the top four honours and 14 HCP: X – penalty. |
| `ind_3d`<br>2♦ – (3♦) – ? | 3♥ | 3 hjerter, 4 spar og 11 hp: 3♥ – pas eller ret. Åbner passer med hjerter og melder 3♠ med spar. | 3 hearts, 4 spades and 11 HCP: 3♥ – pass or correct. Opener passes with hearts and bids 3♠ with spades. |
| `ind_3d`<br>2♦ – (3♦) – ? | Bonusspørgsmål | Hvad betyder 3♥ efter 2♦ – (3♦)?<br>Rigtigt: Pas eller ret<br>Forkert: Naturligt med egen hjertefarve; Krav<br>Forklaring: Over 3♣, 3♦ og 4♥ er dobling straf, hjerter eller spar er pas eller ret, og en minor er naturlig og ikke krav. Over 2♠ er dobling styrke. | What does 3♥ mean after 2♦ – (3♦)?<br>Right: Pass or correct<br>Wrong: Natural with responder's own heart suit; Forcing<br>Explanation: Over 3♣, 3♦ and 4♥ a double is for penalty, hearts or spades are pass or correct, and a minor is natural and non-forcing. Over 2♠ a double shows strength. |
| `ind_4h`<br>2♦ – (4♥) – ? | Pas | 5 hp: pas – intet at tilføje.<br>3 spar og 10 hp: pas – uden fire spar er der intet at tilføje. (note 4) | 5 HCP: pass – nothing to add.<br>3 spades and 10 HCP: pass – without four spades there is nothing to add. |
| `ind_4h`<br>2♦ – (4♥) – ? | X | 5 hjerter med 2 af de fire øverste honnører og 13 hp: X – straf. | 5 hearts with 2 of the top four honours and 13 HCP: X – penalty. |
| `ind_4h`<br>2♦ – (4♥) – ? | 4♠ | 4 spar og 7 hp: 4♠ – pas eller ret. Makker har sikkert spar, når modparten melder 4♥. | 4 spades and 7 HCP: 4♠ – pass or correct. Partner very likely has spades when the opponents bid 4♥. |
| `ind_4h`<br>2♦ – (4♥) – ? | Bonusspørgsmål | Hvad betyder 4♠ efter 2♦ – (4♥)?<br>Rigtigt: Pas eller ret<br>Forkert: Egen sparfarve og krav; Straf<br>Forklaring: Over 4♥ er 4♠ pas eller ret: makker har sikkert spar. Dobling er straf. | What does 4♠ mean after 2♦ – (4♥)?<br>Right: Pass or correct<br>Wrong: Responder's own spade suit, forcing; Penalty<br>Explanation: Over 4♥, 4♠ is pass or correct: partner very likely has spades. A double is for penalty. |

**Noter:**
1. **3♥ over 2♠:** Betydningen "støtte til hjerter" er Claude Codes tolkning af specens grænse `STOETTE_HJ` (3+ hjerter og 6–9 hp, rådgiverens forslag), og "Når modparten melder spar, har åbner oftest hjerter." er Claude Codes egen begrundelse. Jyderup-arket nævner kun dobling over 2♠ og siger intet om 3♥. Teksten rettes efter Franks svar på spørgsmål 1 under Session 2b.
2. **Pas over 2♠:** "til at støtte hjerter" og "har ikke støtte til hjerter" bygger på samme betydning af 3♥ som note 1 og rettes sammen med den. "For svag til at doble" bygger på arket (dobling viser styrke) og grænsen `NEGATIV_X` (10+ hp).
3. **Pas over 3♣ og 3♦:** "uden tre kort i begge majorer" er specens grænse `PAS_RET` (3+ i begge majorer og 7+ hp, bekræftet af Frank, Afklaret 6). W siger kun "intet at tilføje". "Klør kan kun meldes på 4-trinnet" er W's begrundelse til eksempel 8.
4. **Pas over 4♥:** "uden fire spar" bygger på Franks svar 21. nov. (4♠ er 4+ spar og 7+ hp).
5. **1♥ og 1♠ ved åbningen:** 1♥/1♠ med 11–15 hp er specens regel (Regler, `aabning`). Kilden giver kun 5–10 hp for 2♦, og "for stærk til Multi 2♦" bygger på den.

### Session 2b (24. nov. 2026)

**Status:** Franks svar 2 står ordret, kortet har fået feltet `alert`, og teksterne står i tabellen ovenfor. Sessionen stoppede ved 3♥ over 2♠, fordi Jyderup-arket ikke afgør meldingens betydning (spørgsmål 1). Forklaringen og puljen er derfor ikke rettet. Pixeltestene har heller ikke fået hashen (punkt 5 i opgaven), for den skal pege på den commit, hvor kortet er færdigt efter svaret. Hele suiten og pixeltestene er ikke kørt. Intet er flettet eller pushet.

**Commits på `multi-2ru`:**
- `351d47f`: Franks svar 2 ordret;
- `e06cd63`: feltet `alert` på kortet;
- `2481da0`: tabellen med teksterne;
- derefter dette afsnit og tokenforbruget.

**`alert`:** 25 af de 49 kort i tagget bruger feltet med én kort tekst, fx Flannery ("2♦ alerteres"). Multi-2ru-kortet har nu `"alert": "2♦ alerteres"` lige efter `noegle`, som på de andre kort. Kortsiden viser mærket "Alertér" i hovedet og sætter "2♦ alerteres." efter teksten under Situation. Linjen "2♦ er kunstig og alerteres." står stadig i 2♦-rækken under Meldinger. `build_konventionskort.py` ændrede ikke de byggede filer, fordi siden henter kortene fra `data/kort/`.

**3♥ over 2♠:** Jyderup-arket (`Kontraktbridge\Multi_2ru_Jyderup.pdf`, læst i denne session efter Franks svar 2) har kun én linje om indmeldingen over 2♠: "2ru – 2sp - ? D: styrke (negativ), beder makker strafpasse med sparfarve". Arket siger intet om 3♥ over 2♠:
- uden indmelding er 3♥ "korriger (spær i makkers farve)";
- efter dobling står "Ellers: doblingen ignoreres og der meldes efter systemet", men den linje gælder kun doblingen.

I dag forklarer appen 3♥ som "støtte til hjerter. Når modparten melder spar, har åbner oftest hjerter." Betydningen er Claude Codes tolkning af grænsen `STOETTE_HJ`, og den sidste sætning er Claude Codes begrundelse. Begge er markeret som tilføjelse i tabellen (note 1 og 2).

**Tabellen** står under "Tekster til gennemgang" ovenfor. Den har 72 rækker (57 forklaringer og 15 bonusspørgsmål), og 2 rækker er markeret som tilføjelse: 3♥ og pas over 2♠. Noterne 3–5 viser, hvor en tekst bygger på en grænse fra specen eller på Franks svar.

**"45 konventioner"** på forsiden er antallet af trænere med status "klar" på Træn (`index.html` i Konventionstræneren). Siden tæller det selv i linjen "45 trænere · 8 meldeforløb pr. runde": posterne i `data/konventioner.json`, der har et system, ikke er fravalgt og har status "klar".
- **I dag** (`main` og tagget `v-foer-multi-2ru`) er der 50 poster, og 48 har status "klar". Tre af dem står ikke på Træn: `ff-2kl` og `ff-revers` er fravalgt, og `kamp-landy` har intet system. Træn viser derfor 45.
- **Da forsiden fik tallet** 17. okt. 2026, passede det også (48 poster og 46 "klar", minus `kamp-landy`).
- **Med Multi 2♦** bliver tallet 46 (49 "klar" minus de samme tre).
- Session 2's "fra 48 til 49" var de klare poster i alt, ikke det, forsiden tæller.

**Testresultater:**
- `tjek_multi_2ru.py`: i orden (8 af 8 punkter);
- `tjek_konventionskort.py`: "50 konventionskort er i orden";
- `tjek_kort_eksempler.py multi-2ru`: "4 meldeeksempler er i orden (0 advarsler)";
- `tjek_fagord.py` og `tjek_bydeform.py`: i orden, og `tjek_sprog.py` er grøn som punkt 8 i accepttesten;
- `sprogtjek.py`: ingen ukendte ord.

**Spørgsmål til Frank:**
1. **3♥ over 2♠:** hvad betyder 3♥ efter 2♦ – (2♠)? Arket giver kun doblingen.
   - (a) Som uden indmelding: "korriger (spær i makkers farve)", altså pas eller ret. Det svarer til arkets regel efter dobling og til W over de andre indmeldinger. Med spar kan åbner dog kun rette til 3♠ i modpartens farve.
   - (b) Støtte til hjerter som nu (grænsen `STOETTE_HJ`: 3+ hjerter og 6–9 hp), men uden Claude Codes begrundelse. Forklaringen siger så, at arket kun giver doblingen over 2♠, og at 3♥ er specens antagelse.
   - (c) 3♥ trænes ikke over 2♠. Situationen har kun dobling og pas, som arket og specen giver, og 3♥ står kun som forkert valgmulighed.

   Under alle tre rettes forklaringen af pas over 2♠ (note 2), og puljen bygges igen.
2. **Teksterne:** tabellen venter på Franks godkendelse før fletningen.

**Tilbage til session 2c (Opus):**
- Franks svar på spørgsmål 1 ordret under Afklaret.
- Forklaringen af 3♥ og pas over 2♠ rettes i `dealer/multi_2ru.py`, puljen bygges med `python build_pools.py multi-2ru`, og tabellen rettes.
- **Punkt 5 (pixeltestene, Franks svar 2 (a)):**
  - Sidefoden har været færdig siden `425462f`, og kortet står i `e06cd63`. Ændrer svaret ikke kortet, er `e06cd63` hashen; ellers bruges den commit, hvor kortet bliver færdigt.
  - I `tools/tjek_viden_320.mjs` og `tools/tjek_crowhurst_390.mjs` kommer `assets/footer.js`, `data/kort/index.json` og `data/kort/multi-2ru.json` med i `NYERE` med den hash. Resten af siden før kommer stadig fra tagget.
  - Siden før får dermed 50 kort, så tjekket "tagget 49" i `tjek_crowhurst_390.mjs` skal være 50. Pixelsløjfen springer stadig `NYE_KORT` over.
  - Hashen og forklaringen skrives under Afklaret, og begge scripts tjekkes med `node --check`.
- `tjek_multi_2ru.py`, kortets tjek, fagord, bydeform og `sprogtjek.py` køres.

**Session 3 (Sonnet):**
- hele testsuiten og de fulde pixeltests i forgrunden;
- skærmbilleder af én side i `viden/` og af kortsiden med knappen "Multi 2♦", sammen med specens skærmbilleder af træneren, i `C:\Users\frank\Kontraktbridge\skaermbilleder\multi-2ru\`;
- stop før fletning og en rapport med tokenforbruget.
