# SPEC-konventionskort

17. oktober 2026 · Frank

Konventionerne og modspilsaftalerne får en fast beskrivelse: ét konventionskort pr. konvention efter skabelonen `konvention/2` i `docs/konventionskort-skabelon.md`. Skabelonen har to typer, `melding` og `modspil`, med de samme seks afsnit. Kortene er uafhængige af makker og ligger som data i `data/kort/`. Siden `viden/konventionskort.html` viser dem. Designgrundlaget er artifactet "Konventionskortet" (https://claude.ai/artifact/KjwqP8ZPqSzh3WzRZyq4fx).

Filerne i denne leverance er færdige og testet. Opgaven er at lægge dem ind, linke til siden og gøre arbejdsgangen fast.

## Afgrænsning

Før arbejdet starter:

1. Commit og tag den nuværende side, fx `v-foer-konventionskort`.
2. Arbejd på grenen `konventionskort`, og flet først ind efter godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `data/kort/` (ny) | kortene, `index.json` og `konvention.schema.json` fra leverancen | — |
| `docs/konventionskort-skabelon.md` (ny) | skabelonen fra leverancen | — |
| `tools/` | `tjek_konventionskort.py`, `build_konventionskort.py`, `konventionskort.src.html` og `konventionskort-shell.html` fra leverancen; `konventionskort-hint-shell.js` (ny, Afklaret 8) | ændre de eksisterende værktøjer |
| `viden/konventionskort.html` (ny) | genereres med `build_konventionskort.py` | rettes i hånden |
| `viden/index.html` | ét fælles felt "Konventionskort" over systemerne, der linker til siden | ændre listen over systemdokumenter |
| `CLAUDE.md` (ny) | arbejdsreglerne fra leverancen | — |
| `assets/konventionskort-hint.js` (ny) | genereres med `build_konventionskort.py` (Afklaret 8) | rettes i hånden |
| `traener.html`, `markering.html`, `multi-svar-traener.html` | ⓘ ved titlen (Afklaret 5) | ændre træningen |
| `data/konventioner.json`, puljerne | intet i denne omgang | alt |
| Sprog | sidens faste tekster forbliver på dansk; kortene er kun på dansk | engelske kort uden ny version af skabelonen |

Kræver noget alligevel en ændring ud over tabellen, skal Claude Code stoppe og spørge.

## Trin

1. Læg filerne fra leverancen ind i samme mapper som i leverancen.
2. Kør `pip install jsonschema` og derefter `python3 tools/tjek_konventionskort.py`. Den skal melde "5 konventionskort er i orden".
3. Kør `python3 tools/build_konventionskort.py` og kontrollér, at `viden/konventionskort.html` ikke ændrer sig i forhold til leverancen.
4. Tilføj feltet "Konventionskort" på `viden/index.html` med samme kortstil (`.tile`) som systemdokumenterne. Tekst: "Konventionerne beskrevet i én fast skabelon – uafhængigt af makker."
5. Åbn via lokal webserver: `viden/konventionskort.html`, `#truscott`, `#truscott-1klor`, `#multiforsvar`, `#lavinthal` og `#udspil`. Tjek fuld visning, kompakt og skabelon på computer og mobil.

## Afklaret

1. Kortet har samme `id` som træneren i `data/konventioner.json`, når der findes en (`multiforsvar`, `lavinthal`). Lavinthal-kortets eksempler er hentet fra `pools/lavinthal.json`. Et link fra træneren til kortet er næste skridt, ikke denne opgave.
2. Siden ligger i shadow DOM, så `site.css` og kortets egne klasser (`.wrap`, `.chip`, `.kort`) ikke påvirker hinanden. Topbjælke og sidefod er sitets egne.
3. Nye konventioner følger arbejdsgangen i `CLAUDE.md`: ny fil i `data/kort/`, tilføj i `index.json`, kør tjekket.
4. Udspilsaftalerne samles på ét kort, `udspil`. Markeringer (kald, antal, afkast) bliver næste modspilskort med `id` = `markeringer`, så det matcher træneren.

ⓘ i trænerne – Franks ønske og svar (17. oktober 2026):

5. **ⓘ i trænerne** (Franks valg: "ⓘ nu, kort løbende"): `traener.html`, `markering.html` og `multi-svar-traener.html` viser et ⓘ ved titlen, når `data/kort/index.json` har et kort med samme `id` som træneren. I dag gælder det Lavinthal (`markering.html?k=lavinthal`) og Multiforsvar (`traener.html?k=multiforsvar` og multitræneren). Trænere uden kort viser intet. Deres ⓘ kommer af sig selv, når kortet lægges ind. Dermed er "næste skridt" fra punkt 1 taget.
6. **Visningen** (Franks valg: "Fold ud under titlen"): et tryk folder kompaktvisningen ud under trænerens beskrivelse (i multitræneren under indledningen), og et nyt tryk lukker den. Kortet er lukket, når siden åbnes. "Hele konventionen →" fører til `viden/konventionskort.html#<id>`. Knappen har `aria-expanded` og `aria-label` "Om konventionen" / "About the convention (in Danish)". ⓘ og kortet vises ikke ved udskrift.
7. **Kun på trænerne** (Franks valg): Træn-siden får ingen ⓘ.
8. **Én kilde:** `assets/konventionskort-hint.js` genereres af `build_konventionskort.py`. Den bruger de samme visningsfunktioner i `konventionskort.src.html` som siden (fra `KATEGORI` til `vaelg`) og den nye skal `tools/konventionskort-hint-shell.js`. Kortet ligger i shadow DOM som på siden. Ret aldrig i hint-filen direkte.
9. **Engelsk:** kortene findes kun på dansk. På engelsk hedder knappen "About the convention (in Danish)", og øverst i kortet står "The convention card is in Danish.".
10. **Linjeskift:** `build_konventionskort.py` skriver med LF (`newline='\n'`), så siden bliver byte for byte som leverancen, også på Windows. Før gav Windows CRLF (Claude Codes fund ved trin 3).
11. **Centreret tekst i kompaktvisningen:** kildens regel `.ramme p` er ment for noten under kortet, men rammer også kortets egne afsnit. Derfor står undertitel, situation og kort fortalt centreret i en smal spalte. I ⓘ er det rettet i hintets egne regler. På Viden-siden er det uændret, fordi siden skal være som leverancen. Det kan rettes i kilden (`.ramme > p`) og i artifactet, hvis Frank vil (Claude Codes fund).
12. **Feltet på Viden** står øverst under overskriften "Alle konventioner" / "All conventions" med mærket "Opslag" / "Reference · in Danish". Siden SPEC-traen-side, Afklaret 26, står makkerskabernes systemer ikke længere på Viden, så "over systemerne" i trin 4 betyder øverst.
13. **Knappen står inde i overskriften**, så den følger titlen på alle skærmbredder. Overskriftens tekst (`textContent`) indeholder derfor også "i". Skriver variantvælgeren i `traener.html` titlen om, sætter komponenten knappen ind igen.
