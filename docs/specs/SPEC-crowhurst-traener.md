# SPEC-crowhurst-traener

23. oktober 2026 · Frank

En ny træner for **Crowhurst med Lebensohl**: forsvaret mod modpartens 2♦-åbning, når den er Multi (svag 2 i en ukendt major) eller Ekren (begge majorer). Kilden er Jyderup Bridgeklubs ark "Crowhurst med Lebensohl" (1 side). Træneren følger samme opbygning som de øvrige meldetrænere: et konventionskort i `data/kort/`, et modul i `dealer/`, en pulje i `pools/` og en post i `data/konventioner.json`. Træningssiden er den fælles `traener.html?k=crowhurst`.

## Afgrænsning

Før arbejdet starter:

1. Commit og tag den nuværende side, fx `v-foer-crowhurst`.
2. Arbejd på grenen `crowhurst`, og flet først ind efter godkendelse.
3. Læg kilden i repoet som `docs/kilder/crowhurst_med_lebensohl.pdf`.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `data/kort/crowhurst.json` (ny) | konventionskortet efter skabelonen `konvention/2`, type `melding`, med kilden som henvisning; tilføjes i `data/kort/index.json` | tal eller meldinger, som kilden ikke har, i kortet |
| `dealer/crowhurst.py` (ny) | generator og bedømmelse efter reglerne nedenfor, med `export_pool(path)` som `dealer/truscott.py` | — |
| `build_pools.py` | importere `crowhurst` og tilføje `"crowhurst": crowhurst` i `CONVENTIONS` | ændre andre konventioner |
| `pools/crowhurst.json` (ny) | genereres med `python build_pools.py crowhurst` | rettes i hånden |
| `data/konventioner.json` | én ny post (se nedenfor) | ændre de eksisterende poster |
| `dealer/multiforsvar.py`, `dealer/ff_lebensohl.py`, deres puljer og kort | intet | alt. Multiforsvar er et forsvar mod 1NT og Lebensohl mod svag 2♥/2♠; de er andre konventioner |
| `traener.html`, `dealer/core.py` | intet | alt |
| Sprog | al tekst med `tx('dansk', 'English')`; posten får et `en`-felt; husets fagord (`tools/tjek_fagord.py`) | dansk tekst på den engelske side |

Kræver noget alligevel en ændring ud over tabellen, skal Claude Code stoppe og spørge.

Besked til Claude Code:

> Læs CLAUDE.md, docs/konventionskort-skabelon.md, SPEC-truscott-traener.md og SPEC-crowhurst-traener.md. Byg konventionskortet først og stop, så jeg kan godkende det. Byg derefter træneren på grenen `crowhurst` og stop, når puljen er tjekket.

## Kilden kort fortalt

Modparten åbner 2♦ (Multi eller Ekren). Direkte efter åbningen:

| Melding | Viser |
| --- | --- |
| D | 12–16 jævn eller 17+ |
| 2♥/2♠ | naturligt, 5+ farve, 12–16 |
| 2NT | 17–19 jævn; herpå amerikansk Stayman |
| 3♣/3♦ | naturligt, 5+ farve, 12–16 |
| 3NT | for at spille, typisk minorlængde og styrke |
| 4♣/4♦ | 5+ hjerter og 5+ i minoren (med spar og minor venter man og melder 4 i minoren i næste runde) |
| 4♥/4♠ | for at spille |
| 4NT | begge minorer, styrke |
| Pas | med en tvivlsom minorindmelding eller en trefarvet hånd med korthed i en major; man kommer igen senere |

Videre meldinger:

| Meldeforløb | Melding | Viser |
| --- | --- | --- |
| (2♦) – pas – (2♥) – pas – (pas) – ? | D | oplysning, typisk 4 spar og korthed i hjerter |
| (2♦) – D – (2♥) – ? | D | straf |
| | 2♠ | for at spille |
| | 2NT | Lebensohl, beder om 3♣ (makker bryder med 17+) |
| | 3♣/3♦ | konstruktiv, invit |
| | 3♠ | krav, 5+ farve |
| (2♦) – D – (2♥) – 2NT – (pas) – 3♣ – (pas) – ? | pas/3♦ | svag med minorfarve |
| | 3 i major | invit med 5-farve major |
| (2♦) – 4♣ – (pas) – ? | 4♦ | krav med hjerter som trumf |
| | 4♥ | for at spille |
| | 4♠ | krav med klør som trumf |
| | 4NT | esspørgsmål med 6 esser |
| (2♦) – 4♦ – (pas) – ? | 4♥ | for at spille |

## Situationer

Modstanderens 2♦ vises som "2♦ (Multi eller Ekren)". Kun den hånd, der skal melde, genereres, som i Truscott-træneren.

| Nøgle | Rolle | Meldeforløb | Knapper (`calls`) |
| --- | --- | --- | --- |
| `direkte` | Indmelder | `[["Modstander", "2♦"]]` | Pas, X, 2♥, 2♠, 2NT, 3♣, 3♦, 3NT, 4♣, 4♦, 4♥, 4♠, 4NT |
| `genaabning` | Genåbner | `[["Modstander", "2♦"], ["Dig", "Pas"], ["Modstander", "2♥"], ["Makker", "Pas"], ["Modstander", "Pas"]]` | Pas, X, 2♠, 3♣, 3♦ |
| `svar_d` | Svarer | `[["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "2♥"]]` | Pas, X, 2♠, 2NT, 3♣, 3♦, 3♠, 4♠ |
| `svar_relae` | Svarer | `[["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "2♥"], ["Dig", "2NT"], ["Modstander", "Pas"], ["Makker", "3♣"], ["Modstander", "Pas"]]` | Pas, 3♦, 3♥, 3♠ |
| `dobler` | Dobler | `[["Modstander", "2♦"], ["Dig", "X"], ["Modstander", "2♥"], ["Makker", "2NT"], ["Modstander", "Pas"]]` | 3♣, 3♦, 3♥, 3♠, 3NT, 4♣ |
| `svar_4kl` | Svarer | `[["Modstander", "2♦"], ["Makker", "4♣"], ["Modstander", "Pas"]]` | 4♦, 4♥, 4♠ |
| `svar_d_sp` | Svarer | `[["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "2♠"]]` | Pas, X, 2NT, 3♣, 3♦, 3♥, 4♥ |
| `svar_relae_sp` | Svarer | `[["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "2♠"], ["Dig", "2NT"], ["Modstander", "Pas"], ["Makker", "3♣"], ["Modstander", "Pas"]]` | Pas, 3♦, 3♥, 3♠ |
| `svar_pas` | Svarer | `[["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "Pas"]]` | Pas, 2♥, 2♠, 2NT, 3♣, 3♥, 3♠ |

`direkte` og `genaabning` har `"allowX": true`, `svar_d` og `svar_d_sp` også (straf).

## Regler

Bedømmelsen går reglerne igennem i rækkefølge; den første, der passer, er svaret. Grænser, som kilden ikke angiver, står som konstanter øverst i `dealer/crowhurst.py` (se nedenfor). Hænder, der ikke passer nogen regel, kommer ikke med i puljen.

**`direkte`:**

| # | Hånd | Svar |
| --- | --- | --- |
| 1 | 17–19 hp, jævn | 2NT |
| 2 | 5+ hjerter og 5+ i en minor, `TOFARVE_HP` | 4 i minoren |
| 3 | 5-5 eller længere i minorerne, `MINOR_4NT_HP` | 4NT |
| 4 | 7+ i en major med `MAJOR_4M_KVALITET`, `MAJOR_4M_HP` | 4 i majoren |
| 5 | 5+ i en major, 12–16 hp | 2 i den længste major; ved lige længde spar |
| 6 | 6+ i en minor med `MINOR_3NT_KVALITET` og `MINOR_3NT_HP`, uden 5-farve major | 3NT |
| 7 | 17+ hp, som ikke er 17–19 jævn (og ingen regel ovenfor) | X |
| 8 | 5+ i en minor med `MINOR_KVALITET`, 12–16 hp | 3 i minoren |
| 9 | 12–16 hp, jævn | X |
| 10 | 12+ hp, trefarvet med korthed i en major, eller en minor uden `MINOR_KVALITET` | Pas |
| 11 | højst 11 hp | Pas |

Jævn = 4-3-3-3, 4-4-3-2 eller 5-3-3-2. En jævn hånd med en 5-farve major og 12–16 hp får 2 i majoren (regel 5 før regel 9). En 5-farve major med 12–16 hp melder 2♥/2♠, også med en god 6-farve minor; 3NT er til hænder med minorlængde uden 5-farve major. 3NT-reglen står før X med 17+, så en god 6-farve minor uden 5-farve major og med 16–19 hp får 3NT; ved 16 hp vinder 3NT over 3 i minoren (Franks rettelser, Afklaret 5 og 15).

**`genaabning`** (hånden skal give Pas efter reglerne for `direkte`):

| # | Hånd | Svar |
| --- | --- | --- |
| 1 | 4+ spar, højst 1 hjerter, 12+ hp | X |
| 2 | 5+ i en minor, 12–16 hp | 3 i minoren |
| 3 | ellers | Pas |

**`svar_d` og `svar_d_sp`** (makker har 12–16 jævn eller 17+). M er deres major (hjerter i `svar_d`, spar i `svar_d_sp`), og A er den anden major. Over 2♠ er det samme struktur som over 2♥ med farverne byttet om (Franks valg 28. oktober 2026):

| # | Hånd | Svar |
| --- | --- | --- |
| 1 | 4+ i M og `STRAF_HP` | X |
| 2 | 6+ i A og `KRAV_HP` | 4A (for at spille) |
| 3 | 5 i A og `KRAV_HP` | 3A (krav) |
| 4 | 5+ i en minor og `INVIT_HP` | 3 i minoren |
| 5 | 5+ i A og `INVIT_HP` | 2NT (for at invitere med 3A efter 3♣) |
| 6 | `INVIT_HP`, højst 4 i A og ingen 5+ minor | 2NT (for at invitere til 3NT med 3M efter 3♣) |
| 7 | over 2♥: 4+ spar og højst `SVAG_HP` | 2♠ |
| 8 | 5+ i en minor og højst `SVAG_HP` | 2NT (for at spille 3♣ eller 3♦) |
| 9 | ellers, højst `SVAG_HP` | Pas |

**`svar_relae` og `svar_relae_sp`** (efter 2NT – 3♣):

| # | Hånd | Svar |
| --- | --- | --- |
| 1 | 5+ i A og `INVIT_HP` | 3A (invit med 5+ kort) |
| 2 | `INVIT_HP`, højst 4 i A og ingen 5+ minor | 3M (holdspørgsmål til 3NT) |
| 3 | 5+ ruder og højst `SVAG_HP` | 3♦ |
| 4 | 5+ klør og højst `SVAG_HP` | Pas |

3 i deres major kan ikke være naturlig, fordi svareren dobler for straf med 4+ kort i den (Franks valg 27. oktober 2026).

**`svar_pas`** (efter (2♦) – X – (pas); Franks valg 28. oktober 2026 med Claude Codes grænser, Afklaret 19):

| # | Hånd | Svar |
| --- | --- | --- |
| 1 | `RUDER_STRAF`+ ruder og højst `STRAF_HP[1]` hp | Pas (straf med lange ruder) |
| 2 | 5+ spar, hjerter eller klør og `KRAV_HP` | 3 i farven (krav) |
| 3 | 4+ i en major og højst `SVAG_HP` | 2 i majoren (for at spille) |
| 4 | 5+ klør og højst `SVAG_HP` | 2NT (Lebensohl; for at spille 3♣) |

Har hånden to lige lange farver, der begge passer i regel 2 eller 3, kommer den ikke med i puljen. Hænder, som reglerne over pas ikke nævner (fx en invit med 8–11 hp uden lange ruder), kommer heller ikke med.

**`dobler`** (dobleren efter makkers Lebensohl-2NT; hånden har doblet efter reglerne for `direkte`):

| # | Hånd | Svar |
| --- | --- | --- |
| 1 | 12–16 hp (jævn) | 3♣ |
| 2 | 20–21 hp, jævn, med hjerterhold | 3NT |
| 3 | 17+ hp og 5+ spar | 3♠ (krav) |
| 4 | 17+ hp og 5+ ruder | 3♦ (krav) |
| 5 | 17+ hp og 5+ klør | 4♣ |
| 6 | 17+ hp uden egen farve (ingen 5+ spar, ruder eller klør) | 3♥ (beder om hjerterhold) |

Har hånden to 5-farver blandt spar, ruder og klør, meldes den længste; er de lige lange, kommer hånden ikke med i puljen. En hånd med 17+ og 5+ hjerter, der ikke er jævn, og en jævn hånd med 22+ kommer heller ikke med; reglerne siger ikke, hvad de melder. Hjerterhold er es, konge med mindst ét kort til, dame med mindst to eller knægt med mindst tre (`HJERTERHOLD`).

**`svar_4kl`** (makker har 5+ hjerter og 5+ klør):

| # | Hånd | Svar |
| --- | --- | --- |
| 1 | 3+ klør, flere klør end hjerter, `SLEM_HP` | 4♠ |
| 2 | 3+ hjerter, `SLEM_HP` | 4♦ |
| 3 | ellers med 2+ hjerter | 4♥ |

## Konstanter

Kilden giver ikke disse tal. De står øverst i `dealer/crowhurst.py` med en kommentar, ligesom i `dealer/multiforsvar.py`, og Frank kan rette dem:

```python
# --- Grænser, som kilden ikke giver tal for – ret dem her ------------------------
TOFARVE_HP = (10, 16)        # 4♣/4♦: 5+ hjerter og 5+ minor
MINOR_4NT_HP = (14, 20)      # 4NT: begge minorer, "styrke"
MAJOR_4M_HP = (12, 17)       # 4♥/4♠: for at spille
MAJOR_4M_KVALITET = 2        # 4M: mindst 2 af E, K, D i farven
MINOR_3NT_HP = (16, 19)      # 3NT: "typisk minorlængde/styrke"
MINOR_3NT_KVALITET = 2       # 3NT: mindst 2 af E, K, D i minoren
MINOR_KVALITET = 2           # 3♣/3♦: mindst 2 af E, K, D, ellers 6+ kort; ellers "tvivlsom" → pas
STRAF_HP = (8, 15)           # svar_d: X straf med 4+ i deres major
SVAG_HP = 7                  # svar_d, svar_relae og svar_pas: højst 7 hp er svag
INVIT_HP = (8, 11)           # svar_d: konstruktiv invit
KRAV_HP = (12, 17)           # svar_d: 3 i den anden major krav (4 med 6+); svar_pas: ny farve på 3-trinnet krav
RUDER_STRAF = 5              # svar_pas: pas er straf med 5+ ruder og højst STRAF_HP[1] hp
SLEM_HP = (14, 20)           # svar_4kl: krav (4♦/4♠) med sleminteresse
DOBLER_HP_MAX = 22           # dobler: stærkere hænder genereres ikke
# dobler: hjerterhold er es, konge med 1+ kort til, dame med 2+ eller knægt med 3+ (laveste længde for hver honnør)
HJERTERHOLD = {14: 1, 13: 2, 12: 3, 11: 4}
PER_CALL = 7
```

## Forklaringer og bonusspørgsmål

Forklaringen (`why`) siger, hvad hånden har, og hvad meldingen viser, fx "18 hp og jævn: 2NT – 17–19 jævn; herpå amerikansk Stayman." og "4 spar og en hjerter i genåbningen: X – oplysning, typisk 4 spar og korthed i hjerter."

Hver situation får ét bonusspørgsmål, skiftevis blandt disse:

| Spørgsmål | Rigtigt | Forkerte |
| --- | --- | --- |
| Hvad viser X direkte over 2♦? | 12–16 jævn eller 17+ | Straf af ruder · Oplysning med korthed i ruder |
| Hvad viser 2NT fra makker efter (2♦) – X – (2♥)? | Lebensohl: beder om 3♣ | Naturligt, 10–12 jævn · Krav til udgang |
| Hvad viser 4NT efter (2♦) – 4♣? | Esspørgsmål med 6 esser | Begge minorer · For at spille |
| Hvad gør dobleren efter makkers 2NT med 17+? | Bryder i stedet for at melde 3♣ | Melder 3♣ og passer bagefter · Melder altid 3NT |
| Hvad viser svarerens 3♥ efter 2NT – 3♣? | Invit til 3NT, beder om hjerterhold | Naturligt med 5 hjerter · Krav til udgang |
| Hvad viser svarerens X i (2♦) – X – (2♠)? | Straf med 4+ spar | Oplysning med hjerter · 12+ uden farve |
| Hvad viser svarerens 3♠ i (2♦) – X – (2♠) – 2NT – 3♣? | Invit til 3NT, beder om sparhold | Naturligt med 5 spar · Krav til udgang |
| Hvad viser svarerens pas i (2♦) – X – (pas)? | Straf med lange ruder | Svag hånd uden farve · Venter på makkers næste melding |

`dobler` spørger om dobleren efter 2NT, `svar_relae` om svarerens 3♥, `svar_d_sp` om X over 2♠, `svar_relae_sp` om 3♠ efter 2NT – 3♣ over 2♠ og `svar_pas` om pas. Forklaringen til 4NT-spørgsmålet nævner svarene (Afklaret 18).

## Post i data/konventioner.json

```json
{
  "id": "crowhurst",
  "titel": "Forsvar mod Multi 2♦ (Crowhurst)",
  "gruppe": "Konkurrence",
  "emne": "indmeldinger",
  "beskrivelse": "Modparten åbner 2♦ (Multi eller Ekren): X 12–16 jævn eller 17+, 2♥/2♠ og 3♣/3♦ naturligt 12–16, 2NT 17–19, 4♣/4♦ hjerter og minor, 4NT begge minorer – og Lebensohl efter makkers dobling.",
  "roller": ["Indmelder", "Genåbner", "Svarer", "Dobler"],
  "status": "klar",
  "system": "generel",
  "viden": "viden/konventionskort.html#crowhurst",
  "en": {
    "titel": "Defence against Multi 2♦ (Crowhurst)",
    "gruppe": "Competition",
    "beskrivelse": "The opponents open 2♦ (Multi or Ekren): X 12–16 balanced or 17+, 2♥/2♠ and 3♣/3♦ natural 12–16, 2NT 17–19, 4♣/4♦ hearts and a minor, 4NT both minors – and Lebensohl after partner's double."
  }
}
```

## Trin

1. Konventionskortet `data/kort/crowhurst.json` ud fra kilden. Kør `python3 tools/tjek_konventionskort.py`. Stop, så Frank kan godkende det.
2. `dealer/crowhurst.py` efter reglerne og konstanterne. Mål: 7 hænder pr. melding.
3. Modulet i `build_pools.py` og `python build_pools.py crowhurst`. Der må ikke komme nogen "Advarsel: kun …".
4. Tjek puljen med `python3 tools/tjek_crowhurst.py`: hver hånds `correct` er det svar, reglerne giver, og ingen hånd falder uden for reglerne.
5. Posten i `data/konventioner.json`. Kør `tools/tjek_fagord.py` og `tools/tjek_kort_eksempler.py crowhurst`.
6. Åbn `traener.html?k=crowhurst` via lokal webserver på dansk og engelsk, på computer og mobil, og spil en runde.

## Afklaret

1. **Kortet er uafhængigt af makker** og nævner hverken Jyderup Bridgeklub eller makkerskab i teksten; kilden står i kortets kildefelt.
2. **4NT efter (2♦) – 4♣** og **4♥ efter (2♦) – 4♦** står kun som bonusspørgsmål og på kortet, ikke som situationer, fordi kilden ikke giver grænser for, hvornår man spørger, og 4♦ kun har ét svar.

Franks svar (23. oktober 2026):

3. **System "generel"**: det er klubbens ark og ikke en makkeraftale. Træneren står på Træn med ⓘ og konventionskortet, men ikke under Mine makkeraftaler.
4. **Navnet** er "Forsvar mod Multi 2♦ (Crowhurst)", både på kortet og i `data/konventioner.json`, så det ikke forveksles med Crowhurst som checkback efter åbners 1NT-genmelding.
5. **Konstanterne** er godkendt. `MINOR_KVALITET`: en 5-farve kræver 2 af E, K og D, og en 6-farve er altid god nok. Rækkefølgen er rettet: 3NT-reglen står før X med 17+, og `MINOR_3NT_HP` er stadig (16, 19). 2 i major er siden rykket op foran 3NT (punkt 15).
6. **3♥ efter 2NT – 3♣** er ikke med i træneren; kun 3♠. Kortet beholder kildens "3 i major" og har det som åbent spørgsmål. (Erstattet af punkt 16.)
7. **Rollen Dobler** venter, til det er afklaret, hvordan dobleren bryder 3♣ med 17+. (Erstattet af punkt 16.)
8. **Bonusspørgsmål 4** spørger om dobleren, ikke doblerens makker: det er dobleren, der har 17+ og bryder i stedet for at melde 3♣.
9. **Kortet** er godkendt: noten om 6 esser siger "normalt", da forklaringen ikke står i kilden; efter doblingen står "2♠" og kildens "3 i major" (træneren bruger 2♠ og 3♠); direkte X og genåbnings-X er blå, straffedoblingen brun; ingen alertering, da kilden ikke nævner den. Eksemplerne hentes fra puljen.

Claude Codes valg i træneren (23. oktober 2026):

10. **"2♦ (Multi eller Ekren)"** står som situationens `note` under meldeforløbet, som i Multiforsvar-træneren; selve meldingen i `auction` er "2♦", så `traener.html` og kortets eksempler kan læse den.
11. **Hænder med to lige lange minorer**, der begge giver 3 i minoren (`direkte` regel 8, `svar_d` regel 3 og `genaabning` regel 2), kommer ikke med i puljen, fordi reglerne ikke siger, hvilken der meldes.
12. **Sammenhæng mellem runderne:** en hånd i `svar_relae` er en hånd, der meldte 2NT efter reglerne for `svar_d`, ligesom en hånd i `genaabning` passede efter reglerne for `direkte`.
13. **Bonusspørgsmålene** passer til situationen: `direkte` og `genaabning` spørger om X over 2♦, `svar_d` om 2NT, `svar_relae` om doblerens brud og `svar_4kl` om 4NT.
14. **Kortets fem eksempler** er hænder fra puljen (`tools/tjek_kort_eksempler.py crowhurst` finder dem alle), og kortet har fået `traener`-feltet. "Crowhurst" og mappenavnet "docs" (fra kildefeltet) står i `tools/ordliste.txt`, så `tools/sprogtjek.py` kender dem.

Franks svar efter udgivelsen (23. oktober 2026, grenen `crowhurst-raekkefoelge`):

15. **2 i major vinder over 3NT.** En hånd med en 5-farve major og 12–16 hp melder 2♥/2♠, også med en god 6-farve minor; 3NT er til hænder med minorlængde uden 5-farve major. Rækkefølgen i `direkte` er: 2NT, 4 i minoren, 4NT, 4 i major, 2 i major (12–16), 3NT (16–19, uden 5-farve major), X med 17+, 3 i minoren, X med 12–16 jævn, pas. En hånd med 17–19 hp, en 5-farve major og en god 6-farve minor får derfor X. Puljen er bygget igen, kortets eksempler er hentet fra den nye pulje, og den uafhængige test af reglerne ligger nu i repoet som `tools/tjek_crowhurst.py`.

Franks valg 27. oktober 2026 (grenen `crowhurst-dobler`, appen før er tagget `v-foer-crowhurst-dobler`):

16. **Dobleren efter (2♦) – X – (2♥) – 2NT – (pas):** 3♣ = 12–16 jævn, 3♦ = 5+ ruder og 17+ (krav), 3♥ = 17+ uden egen farve og beder om hjerterhold, 3♠ = 5+ spar og 17+ (krav), 3NT = 20–21 jævn med hjerterhold, 4♣ = 5+ klør og 17+. **Svarerens 3♥ efter 2NT – 3♣** er invit til 3NT og beder om hjerterhold; den kan ikke være naturlig, fordi svareren dobler 2♥ for straf med 4+ hjerter. Rollen Dobler (punkt 7) og 3♥ (punkt 6) er dermed med i træneren. Det står ikke i kilden og er markeret som Franks valg på kortet.
17. **Claude Codes valg til punkt 16:** hjerterhold er es, konge med mindst ét kort til, dame med mindst to eller knægt med mindst tre. To lige lange 5-farver blandt spar, ruder og klør, en hånd med 17+ og 5+ hjerter, der ikke er jævn, og en jævn hånd med 22+ kommer ikke med i puljen. Svarerens invit uden farve (8–11 hp, højst 4 spar, ingen 5+ minor og højst 3 hjerter, da 4+ hjerter dobler) går over 2NT og melder 3♥ efter 3♣; en invit med 6+ spar beskriver reglerne stadig ikke. Puljen er bygget igen, kortets eksempler er hentet fra den nye pulje, og kortet har fået et eksempel på svarerens 3♥ og et på doblerens 3♥. "hjerterhold" står i ordlisten.

Franks valg 28. oktober 2026 (grenen `crowhurst-dobler`, appen før er tagget `v-foer-crowhurst-svar`):

18. **Svarerens meldinger efter doblingen og svarene på 4NT:**
    - **Over (2♠)** gælder samme struktur som over (2♥) med farverne byttet om: X er straf med 4+ spar, 2NT er Lebensohl, 3♥ er krav med 5+ hjerter, og 3♣/3♦ er konstruktive og invit.
    - **Over pas** er 2♥/2♠ for at spille, 2NT Lebensohl, nye farver på 3-trinnet krav og pas straf med lange ruder.
    - **Efter 2NT – 3♣** er 3 i modpartens major et holdspørgsmål til 3NT, og 3 i den anden major er invit med 5+ kort.
    - **4NT med 6 esser** besvares som RKC 1430: 5♣ = 1/4, 5♦ = 0/3/6, 5♥ = 2/5 uden trumfdame og 5♠ = 2/5 med trumfdame.
    - **Invit med 6+ spar** går også over 2NT – 3♣ – 3♠: reglen er "5+ spar og `INVIT_HP`", og hænderne er med i træneren. Med 6+ spar og udgangsstyrke melder svareren 4♠ direkte.

    Kortets tre åbne spørgsmål er dermed besvaret og fjernet: svarers 2♠ og pas efter doblingen, "3 i major" og svarene på 4NT. Situationerne `svar_d_sp`, `svar_relae_sp` og `svar_pas` er nye, og `svar_d` har 4♠.
19. **Claude Codes valg til punkt 18:**
    - Over 2♠ melder svareren 4♥ med 6+ hjerter og udgangsstyrke (`KRAV_HP`), som 4♠ over 2♥. En svag hånd med hjerter har ingen 2♥ at melde og passer.
    - Over pas: pas er straf med 5+ ruder (`RUDER_STRAF`) og højst 15 hp (`STRAF_HP[1]`), uden nedre grænse. 2♥/2♠ er svage (højst `SVAG_HP`) med 4+ kort, nye farver på 3-trinnet har 5+ kort og `KRAV_HP`, og 2NT er en svag hånd med 5+ klør, der vil spille 3♣. To lige lange farver og hænder, reglerne ikke nævner (fx en invit med 8–11 hp), er ikke med i puljen.
    - 4NT-svarene står på kortet og i forklaringen til bonusspørgsmålet om 4NT, men ikke som en situation med hænder, fordi trumfen ikke er aftalt, når 4NT meldes direkte over 4♣. Den situation kan bygges, når det er afgjort, hvilken dame der er trumfdamen.
    - Puljen er bygget igen (492 hænder), kortets eksempler er hentet fra den nye pulje, og kortet har to nye eksempler: X over 2♠ og pas over pas.
