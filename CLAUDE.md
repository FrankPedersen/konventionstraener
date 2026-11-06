# Konventionstræner — arbejdsregler

Det, der gælder alle repoer – arbejdsgangen, husets ord, hemmeligheder og systemdokumentationen `../SYSTEM.md` – står i `../CLAUDE.md`.

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

- Ét emne ad gangen på en gren `kort-<emne>`. Frank godkender kortene, før de flettes ind (`docs/specs/SPEC-konventionskort.md`, Afklaret 14–16).
- Kilder: systemdokumentet i trænerens felt `viden` og trænerens pulje i `pools/`. Eksempler er hænder fra puljen med samme meldeforløb og svar.
- Tilføj filen i `data/kort/index.json`, kør `python3 tools/tjek_konventionskort.py` og `python3 tools/tjek_kort_eksempler.py <id>`, og byg siden. Træneren får sin ⓘ af sig selv.

## Sprog og fagord

- Husets fagord står i `../CLAUDE.md` (specen er `docs/specs/SPEC-sprog-og-ordbog.md`). Kør `python3 tools/tjek_fagord.py` efter tekstændringer; den skal melde "i orden". `python3 tools/tjek_sprog.py` er specens accepttest.
- Beskrivende form (`../CLAUDE.md`; `docs/specs/SPEC-beskrivende-form.md`, listen med de gamle og nye tekster i `docs/beskrivende-form.md`): `python3 tools/tjek_bydeform.py` fejler, hvis en dansk instruktion eller forklaring begynder med et udsagnsord i bydeform. Knapper, links og navne står på testens `UNDTAGELSER`; en ny knap i bydeform kommer på listen. Konventionskortene, puljerne, `dealer/` og systemdokumenterne i `viden/` følger kilderne, og testen springer dem over.
- Stavekontrol med hånden før udgivelse: `python3 tools/sprogtjek.py` (kræver `pip install spylls`; den danske ordbog hentes første gang). Rigtige ord, som hunspell ikke kender, står i `tools/ordliste.txt`; stavefejl rettes i teksten.

## Vedligeholdelse

- **Makker 2-dokumentet:** `viden/2-over-1-makker2.html` er kilden og rettes direkte i siden. Der importeres ikke længere fra Claude Design (Franks valg 25. oktober 2026); `tools/import_design.py` er kun til historik og stopper med en fejl, medmindre det køres med `--overskriv`.
- **Specerne** ligger i `docs/specs/` med én linje pr. spec i `docs/specs/README.md`. En ny spec kan ligge i roden, mens den er i arbejde, og flyttes dertil, når den er færdig. `_config.yml` udelukker `docs/` og `SPEC-*.md` og udviklerfilerne `CLAUDE.md`, `build_pools.py`, `dealer/` og `tools/` fra GitHub Pages, så de ligger på GitHub, men ikke på www.kontraktbridge.dk (Franks valg 27. og 28. oktober 2026). Mapper, der begynder med `_`, udgives ikke. En ny mappe eller fil, som siderne skal hente, må ikke stå i `exclude`.
- **Makker 2, aftalerne fra Bilag C** (`docs/specs/SPEC-makker2-bilag-c.md`, Franks valg 3. november 2026): 2♣ har kontrolsvar, og 2♦ er Flannery. Reglen om 1♥ med 5-4 under 16 hp står i `flannery` i `dealer/core.py`. `python3 tools/tjek_makker2_bilag_c.py` er accepttesten. Puljen `bekkasin` deles med Makker 1 og er bevidst ikke ændret.
- **Sidefoden** står kun i `assets/footer.js` og er ens med forsidens (`docs/specs/SPEC-sidefod.md`, Franks valg, udgivet 5. november 2026): logo og "Om mig og kontakt", Trænere, Opslag og ©-linjen; "Aftaler og notater" er væk fra den, og siderne nås fra topbjælken og Viden. `node tools/tjek_sidefod.mjs` tjekker målene på siderne ved 1280, 390 og 320 px og på engelsk; `--billeder=mappe` gemmer sidefoden.
- **Siderne i `viden/` ved 320 px** (docs/specs/SPEC-viden-320.md; bygget på grenen `viden-320`, før: `v-foer-viden-320`; godkendt af Frank og udgivet 5. november 2026): ingen vandret scroll ved 320 px, og 390 og 1280 px er pixel for pixel som før. `node tools/tjek_viden_320.mjs` tjekker alle sider og kort på begge sprog, lukket og åbent; `ingen` springer pixelsammenligningen over, og `--billeder=mappe` gemmer udsnit før og efter. Rettelserne står i `@media`-regler under 360 og 390 px, og chips brækker under 399 px (se crowhurst-kortet nedenfor). Kortsidens regler står i `tools/konventionskort.src.html`, som bygges med `python3 tools/build_konventionskort.py`.
- **Crowhurst-kortet ved 390–398 px** (docs/specs/SPEC-crowhurst-390.md; bygget på grenen `crowhurst-390`, før: `v-foer-crowhurst-390`; godkendt af Frank og udgivet 6. november 2026): chips må brække under 399 px (`@media (max-width:398px)` i `tools/konventionskort.src.html`), så chippen "Crowhurst (checkback efter åbners 1NT-genmelding)" ikke giver vandret scroll. `node tools/tjek_crowhurst_390.mjs` er accepttesten: crowhurst ved 390, 393, 395 og 398 px i alle visninger og i hint-vinduet, de andre kort og siderne ved 390 px og alt ved 399 og 1280 px pixel for pixel som tagget; `ingen` springer pixelsammenligningen over, og `--billeder=mappe` gemmer kortet før og efter.
- **Multi-svar-træneren** står fra 1000 px i to spalter med hånden til venstre (`docs/specs/SPEC-bred-layout.md`, bud A som i Fordelingstræneren; Franks valg 31. oktober 2026). Reglerne står i sidens egen `<style>` i én `@media (min-width: 1000px)`; under 1000 px er siden pixel for pixel som før. `node tools/tjek_bred_multi.mjs` er accepttesten (tagget `v-foer-bred-layout` vises med `git show`).
