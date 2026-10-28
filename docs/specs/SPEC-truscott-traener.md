# SPEC-truscott-traener

17. oktober 2026 · Frank

En ny træner for **Truscott 2NT** som svarer efter modpartens oplysningsdobling af makkers åbning. Træneren bygger på konventionskortet `data/kort/truscott.json` (kilde: Kromann, Truscott 2 UT + redobling, 2012) og følger samme opbygning som de øvrige meldetrænere: et modul i `dealer/`, en pulje i `pools/` og en post i `data/konventioner.json`. Selve træningssiden er den fælles `traener.html?k=truscott`.

Forudsætning: `SPEC-konventionskort.md` er gennemført, så `data/kort/truscott.json` findes.

## Afgrænsning

Før arbejdet starter:

1. Commit og tag den nuværende side, fx `v-foer-truscott`.
2. Arbejd på grenen `truscott`, og flet først ind efter godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `dealer/truscott.py` (ny) | generator og bedømmelse efter reglerne nedenfor, med `export_pool(path)` | — |
| `build_pools.py` | importere `truscott` og tilføje `"truscott": truscott` i `CONVENTIONS` | ændre andre konventioner |
| `pools/truscott.json` (ny) | genereres med `python build_pools.py truscott` | rettes i hånden |
| `data/konventioner.json` | én ny post (se nedenfor) | ændre de eksisterende poster |
| `data/kort/truscott.json` | tilføje `"traener": {"url": "traener.html?k=truscott", "pool": "pools/truscott.json"}` | ændre kortets indhold |
| `dealer/kamp_stoette.py`, `pools/kamp-efter-od.json` | intet | alt – Kampen om kontrakten har sine egne regler (se Afklaret, punkt 1) |
| `traener.html`, `dealer/core.py` | intet (undtagen kildelinjen for system "generel", Afklaret punkt 4) | alt andet |
| Sprog | al tekst i træneren med `tx('dansk', 'English')`; posten i `data/konventioner.json` får et `en`-felt | dansk tekst på den engelske side |

Kræver noget alligevel en ændring ud over tabellen, skal Claude Code stoppe og spørge.

## Situationer

Rolle: **Svarer**. Makker åbner 1 i farve, og modparten dobler til oplysning. Kortet siger, at konventionen gælder for alle almindelige farveåbninger på 1-trinnet, så der er fire situationer:

| Nøgle | Meldeforløb |
| --- | --- |
| `od_kl` | `[["Makker", "1♣"], ["Modstander", "X"]]` |
| `od_ru` | `[["Makker", "1♦"], ["Modstander", "X"]]` |
| `od_hj` | `[["Makker", "1♥"], ["Modstander", "X"]]` |
| `od_sp` | `[["Makker", "1♠"], ["Modstander", "X"]]` |

Alle situationer har `"allowXX": true`. Meldeknapperne (`calls`) er: Pas, XX, 2NT, 2, 3 og 4 i åbningsfarven, hver ny farve på billigste trin og hver ny farve med ét springs trin. Sortér som i `kamp_stoette.py`.

## Regler

Bedømmelsen går igennem reglerne i denne rækkefølge, og den første, der passer, er det rigtige svar. "Støtte" er antal kort i åbningsfarven.

| # | Hånd | Rigtigt svar | Fra kortet |
| --- | --- | --- | --- |
| 1 | 10+ hp og 3+ støtte | 2NT | 10+ hp, støtte til åbningsfarven |
| 2 | 10+ hp og højst 2 støtte | XX | 10+ hp, ingen støtte |
| 3 | 0–9 hp og præcis 3 støtte | 2 i farven | 3-kortstøtte, 0–9 hp |
| 4 | 0–9 hp og præcis 4 støtte | 3 i farven | 4-kortstøtte, 0–9 hp |
| 5 | 0–9 hp og 5+ støtte | 4 i farven | 5+ kortstøtte, 0–9 hp |
| 6 | Højst 2 støtte, 6+ farve og højst `SPRING_HP_MAX` hp | spring i den lange farve | spærremelding, ingen støtte |
| 7 | Højst 2 støtte, 5+ farve og 5–8 hp | ny farve på billigste trin | 5–8 hp, 5+ farve, ingen støtte |
| 8 | Højst 2 støtte og 0–5 hp | Pas | højst 4–5 hp, ingen støtte |
| – | Alt andet, fx 6–9 hp uden støtte og uden 5-farve | `None` – hånden kommer ikke med i puljen | kortet beskriver den ikke |

Grænser, som kortet ikke angiver, står som konstanter øverst i `dealer/truscott.py`, ligesom i `dealer/multiforsvar.py`:

```python
# --- Grænser, som konventionskortet ikke giver tal for – ret dem her ------------
STOETTE_MIN = 3        # 2NT: "støtte" læses som 3+ kort, fordi kortet bruger 3-kortstøtte på 2-trinnet
SPRING_LAENGDE = 6     # spring i ny farve: 6+ farve
SPRING_HP_MAX = 6      # spring i ny farve: svag hånd; med 7–8 hp og 5+ farve meldes den billigt
HP_MAX = 15            # stærkere hænder genereres ikke
```

Er der flere mulige nye farver i regel 6 eller 7, vælges den længste og ved lige længde den højeste.

## Forklaringer og bonusspørgsmål

Forklaringen (`why`) siger, hvad hånden har, og hvad meldingen viser, fx:

- 2NT: `"{n} kort i {farve} og {hp} hp: 2NT – 10+ med støtte."`
- XX: `"{hp} hp uden støtte: redobling – 10+, lægger op til straf."`
- 3 i farven: `"4 kort i {farve} og {hp} hp: 3{sym} – spærrende efter doblingen."`
- Spring: `"{n} {farve} og {hp} hp: spring til {melding} – spærrende uden støtte."`

Hver situation får ét bonusspørgsmål, skiftevis blandt disse:

| Spørgsmål | Rigtigt | Forkerte |
| --- | --- | --- |
| Hvad viser 2NT efter modpartens oplysningsdobling? | 10+ hp med støtte | Naturligt, 11–12 hp jævn · 10+ hp uden støtte |
| Hvad viser redobling? | 10+ hp uden støtte | 10+ hp med støtte · Ønske om at spille redoblet uanset hånd |
| Hvad viser 3 i åbningsfarven efter doblingen? | 4-kortstøtte, 0–9 hp, spærrende | Invit med 10–12 hp · 3-kortstøtte, 6–9 hp |

Alle tekster skrives med `tx()` på dansk og engelsk.

## Post i data/konventioner.json

```json
{
  "id": "truscott",
  "titel": "Truscott 2NT",
  "gruppe": "Konkurrence",
  "emne": "stoette-konkurrence",
  "beskrivelse": "Makker åbner, modparten dobler: XX 10+ uden støtte, 2NT 10+ med støtte, direkte støtte er svag og viser antallet af trumf.",
  "roller": ["Svarer"],
  "status": "klar",
  "system": "generel",
  "viden": "viden/konventionskort.html#truscott",
  "en": {
    "titel": "Truscott 2NT",
    "gruppe": "Competition",
    "beskrivelse": "Partner opens, the opponents double: XX 10+ without support, 2NT 10+ with support, a direct raise is weak and shows the number of trumps."
  }
}
```

`viden` peger på konventionskortet i stedet for et systemdokument, fordi kortet er uafhængigt af makker.

## Trin

1. Skriv `dealer/truscott.py` efter reglerne og konstanterne ovenfor. Brug `tpl`, `either` og `build_pool` fra `dealer/core.py` ligesom `kamp_stoette.py`. Mål: 7 hænder pr. melding (`PER_CALL`).
2. Tilføj modulet i `build_pools.py` og kør `python build_pools.py truscott`. Der må ikke komme nogen "Advarsel: kun …".
3. Tjek puljen: for hver hånd skal `correct` være det samme svar, som reglerne giver, og ingen hånd må falde under "Alt andet".
4. Tilføj posten i `data/konventioner.json` og `traener`-feltet i `data/kort/truscott.json`. Kør `python3 tools/tjek_konventionskort.py`.
5. Åbn `traener.html?k=truscott` via lokal webserver på dansk og engelsk, på computer og mobil, og spil en runde.

## Afklaret

1. **Forskel fra `kamp-efter-od`.** Træneren "Efter modpartens oplysningsdobling" følger Kampen om kontrakten og bliver uændret. De to trænere svarer forskelligt på disse hænder:

   | Hånd | Truscott (Kromann) | Kampen om kontrakten |
   | --- | --- | --- |
   | 10+ hp med 3-kortstøtte | 2NT | XX |
   | 2NT | 3+ støtte | 4+ støtte |
   | Ny farve uden støtte | 5–8 hp, 5+ farve, ikke krav | 1♠ rundekrav, 6-farve i minor konstruktiv |
   | Støtte på 2-trinnet | 0–9 hp | 6–9 hp |

2. **Fortsættelser.** Åbners melding efter 2NT og XX (kortets afsnit 2) kommer i en senere udgave med rollen Åbner.
3. **System.** Konventionskortet er uafhængigt af makker, men posten i `data/konventioner.json` skal have et `system`. Claude Code spørger Frank, om det er `"kf"`, `"ff"` eller begge.

Claude Codes gennemgang og Franks svar (18. oktober 2026):

4. **System "generel"** (Franks valg: "Kun træner"). Truscott er en træner, ikke en makkeraftale: den står på Træn og har ⓘ med konventionskortet, men står ikke under Mine makkeraftaler og ikke på Viden. `traener.html` har fået én rettelse ud over tabellen: for system "generel" siger kildelinjen "Beskrivelsen står i konventionskortet" i stedet for "Aftalerne står i vores system" (Franks ja).
5. **Konflikter med de øvrige konventioner** i 1 i farve – (X) – ?. Truscott-træneren er en selvstændig træner; makkerskaberne spiller anderledes:
   - Bridgesystemet 8.4: Omvendt Bergen og Bekkasin gælder fortsat efter dobling, så 2NT er Bekkasin (13+ sp, 4+ trumf) og 3♣/3♦ over 1M er Omvendt Bergen. I Truscott er 2NT 10+ med 3+ støtte, og 3♣/3♦ er spærrende spring.
   - Det andet systemdokument: Bekkasin gælder også efter dobling (afsnit 2, rettet i afsnit 17, punkt 6). Direkte støtte er 6–9 sp (Truscott: 0–9 hp); ny farve på 1-trinnet er 6–9 hp med 4+ kort, på 2-trinnet højst 9 hp med god 6-farve; 1NT er 6–9 jævn (findes ikke i Truscott).
   - Omvendt minor (det andet system): efter 1♣/1♦ – (X) ændrer doblingen intet, så 2 i minor er 10+ med stærk støtte og 2NT er naturlig 11–12. I Truscott er 2 i minor svag (3-kortstøtte, 0–9 hp), og 2NT viser 10+ med støtte. Det er den skarpeste forskel.
   - Notatet Standard 2 over 1: 2NT er 10+ sp med 4+ støtte (Truscott: 3+).
   - Kampen om kontrakten: se punkt 1.
6. **Bekkasin overalt** (Franks valg). I det andet systemdokument stod 1M – (X) – 2NT både som Bekkasin (afsnit 2) og som "10+ sp med støtte (Truscott)" (afsnit 17). Afsnit 17, Doblinger-træneren (`dealer/ff_doblinger.py`, `pools/ff-doblinger.json`), dens kort og beskrivelse er rettet til Bekkasin: 13+ sp og 4+ trumf; redoblingen viser 10+ uden primær (4-korts) støtte. 10–12 sp med 4+ trumf efter dobling beskriver kilden ikke; de hænder er ikke med i træneren og står som åbent spørgsmål på kortet. (Erstattet af punkt 8.)
7. **Kortets eksempler.** De tre eksempler på `truscott`-kortet kommer fra leverancen og findes ikke i puljen (tjekket giver advarsler, ikke fejl). Træneren giver samme svar på alle tre.
8. **Truscott efter dobling hos Makker 2** (Franks valg 27. oktober 2026). Afløser punkt 6 og det andet systemdokuments del af punkt 5: hos Makker 2 er 1M – (X) – 2NT Truscott med 10+ sp og 4+ trumf, og 3 i farven er spærremelding med 4 trumf. Afsnit 2 og 17, Doblinger-træneren, dens kort og beskrivelse er rettet, og det åbne spørgsmål om 10–12 sp er fjernet (SPEC-konventionskort.md, punkt 39). Makker 2 kræver stadig 4+ trumf til 2NT (Truscott-træneren: 3+). Bridgesystemet 8.4 (Makker 1) er uændret, og Truscott-træneren er uændret.
