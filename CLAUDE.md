# Konventionstræner — arbejdsregler

## Konventionskort

Alle konventioner beskrives som konventionskort efter den faste skabelon i `docs/konventionskort-skabelon.md`. Læs den, før du opretter eller ændrer en konvention.

- Ét kort = én JSON-fil i `data/kort/`, med filnavn = `id`. Tilføj filnavnet i `data/kort/index.json`.
- Kortene er uafhængige af makker: ingen systemnavne, makkernavne eller status som aftalt/forslag.
- Hvert kort har `type`: `melding` eller `modspil`. Alle seks afsnit (meldinger, fortsættelser, indmelding, eksempler, faldgruber, åbne spørgsmål) bruges i den rækkefølge for begge typer. Ingen nye afsnit eller felter uden at skabelonen, skemaet og `viden/konventionskort.html` opdateres samtidig, og versionen i `skabelon` hæves.
- Meldeforløb og hænder bruger samme format som træner-puljerne i `pools/`. Modspilseksempler bruger markeringstrænerens format og hentes helst fra dens puljer.
- Tal, som kilden ikke angiver, skrives ikke ind.
- Kør `python3 tools/tjek_konventionskort.py` efter hver ændring. Den skal melde "i orden", før der committes.

Siden `viden/konventionskort.html` viser kortene; `viden/konventionskort.html#<id>` åbner et bestemt kort. Siden genereres: ret i `tools/konventionskort.src.html` og kør `python3 tools/build_konventionskort.py`. Ret aldrig i `viden/konventionskort.html` direkte.

Trænerne viser kortets kompaktvisning bag et ⓘ ved titlen, når der findes et kort med trænerens `id`. Komponenten `assets/konventionskort-hint.js` bygges af det samme script fra `tools/konventionskort.src.html` og `tools/konventionskort-hint-shell.js`. Ret aldrig i den direkte (SPEC-konventionskort.md, Afklaret 5–13).

Et kort har samme `id` som konventionen i `data/konventioner.json`, når der findes en træner til den. Hver træner får sit eget kort, også når samme konvention trænes i begge makkerskaber; kortet nævner ikke makkerskabet.

### Nye kort – arbejdsgang

- Ét emne ad gangen på en gren `kort-<emne>`. Frank godkender kortene, før de flettes ind (SPEC-konventionskort.md, Afklaret 14–16).
- Kilder: systemdokumentet i trænerens felt `viden` og trænerens pulje i `pools/`. Eksempler er hænder fra puljen med samme meldeforløb og svar.
- Tilføj filen i `data/kort/index.json`, kør `python3 tools/tjek_konventionskort.py` og `python3 tools/tjek_kort_eksempler.py <id>`, og byg siden. Træneren får sin ⓘ af sig selv.

## Sprog og fagord

- Husets fagord i dansk tekst (SPEC-sprog-og-ordbog.md): bordet, kipning, forbindelser og slutspil (indspil kun om den særlige form), og hp, doubleton og fittet (derfor et fit). Engelsk beholder HCP.
- Kør `python3 tools/tjek_fagord.py` efter tekstændringer; den skal melde "i orden". `python3 tools/tjek_sprog.py` er specens accepttest.
- Stavekontrol med hånden før udgivelse: `python3 tools/sprogtjek.py` (kræver `pip install spylls`; den danske ordbog hentes første gang). Rigtige ord, som hunspell ikke kender, står i `tools/ordliste.txt`; stavefejl rettes i teksten.

## Vedligeholdelse

- **Makker 2-dokumentet:** `viden/2-over-1-makker2.html` er kilden og rettes direkte i siden. Der importeres ikke længere fra Claude Design (Franks valg 25. oktober 2026); `tools/import_design.py` er kun til historik og stopper med en fejl, medmindre det køres med `--overskriv`.

## Systemdokumentation

**Systemdokumentation:** `docs/SYSTEM.md` i forsidens repo (lokalt `../githubUpload/docs/SYSTEM.md`) beskriver hele www.kontraktbridge.dk (de tre repoer, Azure, drift, data og arbejdsgang). Filen er privat: den står i githubUploads `.gitignore` og ligger kun lokalt. Ændrer en opgave noget af det – en ny side eller app, en Azure-ressource, en app-indstilling, udrulning, data der gemmes, eller en beslutning Frank træffer – så opdatér `docs/SYSTEM.md` i samme omgang, også beslutningsloggen og datoen øverst. Hemmeligheder skrives aldrig i filen.
