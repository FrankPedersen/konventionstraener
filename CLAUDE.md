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

Et kort har samme `id` som konventionen i `data/konventioner.json`, når der findes en træner til den.
