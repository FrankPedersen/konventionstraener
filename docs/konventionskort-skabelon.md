# Konventionskortet — skabelon konvention/2

Alle konventioner beskrives i én fast skabelon. Ét kort pr. konvention, gemt som én JSON-fil i `data/kort/`. Kortet er uafhængigt af makker: hvem man spiller konventionen med, og om den er aftalt, hører til i makkersystemet, ikke her.

Siden `viden/konventionskort.html` viser kortene. Filen `data/kort/konvention.schema.json` kontrollerer, at en fil følger skabelonen.

## To typer

Feltet `type` er enten `melding` eller `modspil`. Begge typer har de samme seks afsnit i samme rækkefølge. Typen styrer afsnitstitlerne, farvenøglen, tabellens kolonner og eksemplernes form.

| | `melding` | `modspil` |
|---|---|---|
| Situation | budsekvens (`auction`) + tekst | tekst + `gaelderFor` (udspil, afkast, retur osv.), ingen budsekvens |
| Afsnit 1 | Meldingerne: melding → viser | Kortene: kort → viser, eller kort → mod farve / mod sans |
| Afsnit 2 | Fortsættelser | Makkers læsning |
| Afsnit 3 | Ved modpartens indmelding | Forrang og undtagelser |
| Afsnit 4 | Hånd + "Meld X" | Bordet, din hånd og stikket + "Læg/Kast/Spil ud X" |
| Farvenøgle | meldingsnøglen | modspilsnøglen |

Udspilsaftaler samles på ét kort, `udspil`. Hver markeringsaftale med eget navn, fx Lavinthal, får sit eget kort.

## Ny konvention — sådan

1. Kopiér en eksisterende fil af samme type, fx `truscott.json` (melding) eller `lavinthal.json` (modspil), og giv den et nyt `id` og filnavn (samme navn, små bogstaver, bindestreg i stedet for mellemrum).
2. Udfyld felterne efter tabellen nedenfor.
3. Tilføj filnavnet i `data/kort/index.json`.
4. Kontrollér filen mod skemaet (se nederst) og åbn `viden/konventionskort.html#<id>`.

## Kortets opbygning

Rækkefølgen er fast. De seks nummererede afsnit vises altid, også når de er tomme.

| Del | Felt | Indhold |
|---|---|---|
| Hoved | `navn`, `undertitel`, `kategori`, `alert` | Navn, én linje om brugen, kategori og evt. alertering |
| Ikke at forveksle med | `forveksles` | Konventioner med samme eller lignende navn |
| Situation | `situation.auction`, `situation.tekst`, `situation.gaelderFor` | Meldeforløbet frem til konventionen, én sætning, og hvilke åbninger eller trin den dækker |
| Formål | `formaal` | Hvorfor konventionen findes. Én sætning |
| Kort fortalt | `kortfortalt` | Princippet. Højst to sætninger. Vises også i kompaktvisningen |
| 1 Meldingerne / Kortene | `meldinger` | Melding: `bud`, `styrke`, `viser`, evt. `krav`. Modspil: `kort` og `viser`, eller `kort`, `farve` og `sans`. En række med kun `gruppe` giver en mellemoverskrift |
| 2 Fortsættelser / Makkers læsning | `fortsaettelser` | Grene med titel, meldinger og evt. note; melding har også auction. Bruges også når strukturen skifter, fx efter et negativt svar |
| 3 Indmelding / Forrang og undtagelser | `indmelding` | Rækker med situation og regel. Beskrives efter bedste praksis |
| 4 Eksempler | `eksempler` | Se formater nedenfor |
| 5 Faldgruber | `faldgruber` | Korte sætninger om typiske fejl |
| 6 Åbne spørgsmål | `aabne` | Punkter, hvor konventionen spilles forskelligt |
| Fod | `relaterede`, `kilde`, `traener` | Spiller sammen med, kilde og tilhørende træner |

## Formater

- **Meldeforløb** (`auction`): liste af `[rolle, melding]`, hvor rolle er `Modstander`, `Dig` eller `Makker`. Den melding, der skal findes, skrives `?`. Samme format som træner-puljerne.
- **Hånd** (`haand`, `bordet`): `{"S": [...], "H": [...], "D": [...], "C": [...]}` med kortværdier 14 = E, 13 = K, 12 = D, 11 = B, 10–2. Samme format som træner-puljerne.
- **Kortkode** (modspil): farvebogstav + værdi, fx `S10`, `H14`.
- **Modspilseksempel**: `kontrakt`, `trumf` (`S`/`H`/`D`/`C` eller `null`), `du` (Nord/Øst/Syd/Vest), `bordet` (udelades ved udspil), `haand`, `stik` (liste af `[plads, kortkode]`), `tekst`, `svar` (kortkode) og `forklaring`. Samme felter som markeringstrænerens puljer (`rigtige[0]` → `svar`, `hvorfor` → `forklaring`).
- **Styrke**: hp eller sp med tankestreg, fx `10–16 hp`.
- **Farvenøgle for meldinger** (`noegle`):

| Værdi | Betyder |
|---|---|
| `gron` | Naturlig / støtte |
| `bla` | Kaptajn / rundekrav |
| `gul` | Specialaftale, alertér |
| `brun` | Sans / jævn |
| `rosa` | Spærrende / advarsel |
| `gra` | Definition / pas |

- **Farvenøgle for modspil** (`noegle`) – bruger de samme seks farver:

| Værdi | Betyder | Farve |
|---|---|---|
| `kald` | Kald / opmuntrende | grøn |
| `afvis` | Afvisning / advarsel | rosa |
| `antal` | Antal | blå |
| `farvevalg` | Farvevalg | gul |
| `udspil` | Udspilskort | brun |
| `gra` | Definition / regel | grå |

## Regler for ensretning

1. Tabellerne bærer beskrivelsen. Tekst bruges kun til det, en tabel ikke kan vise, og gentager aldrig tabellen.
2. Ingen fritekst-afsnit. Det, der ikke passer i de seks afsnit, skal ind som fortsættelse, faldgrube eller åbent spørgsmål.
3. Meldeforløb skrives altid som `auction` med roller, aldrig som løs tekst.
4. Kort skrives med E K D B 10. Spar og klør sort, hjerter og ruder rød.
5. Tal, som kilden ikke angiver, skrives ikke ind. Feltet står tomt.
6. Kortet er uafhængigt af makker. Ingen systemnavne, makkernavne eller status som aftalt/forslag.
7. Modspilseksempler hentes helst fra markeringstrænerens puljer, så kort og træner viser de samme hænder.

## Kontrol mod skemaet

```bash
python3 tools/tjek_konventionskort.py
```

Scriptet tjekker hver fil mod skemaet, at `id` svarer til filnavnet, at filen står i `data/kort/index.json`, at farvenøglen passer til typen, at hver eksempelhånd har 13 kort (modspil: højst 13), og at et modspilssvar er på hånden. Det kræver `pip install jsonschema`.
