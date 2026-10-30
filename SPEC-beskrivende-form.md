# SPEC-beskrivende-form (konventionstræneren)

30. oktober 2026 · Franks regel og opgave, skrevet ud af Claude Code

Husets regel (`../CLAUDE.md`, Husets ord; Franks valg 30. oktober 2026): instruktioner og forklaringer skrives i beskrivende form, ikke i bydeform, på dansk og engelsk. Knapper og links og navne bliver i bydeform. "Du" som grundled er beskrivende form; mange passive -es-former i træk undgås. Fordelingstræneren er lavet først; denne spec gælder konventionstrænerens sider, kort, puljer og trænere, og forsiden har sin egen. Sidefodens sætning rettes i alle tre repoer på én gang.

## Afgrænsning

`main` er tagget `v-foer-beskrivende-form`, og arbejdet sker på grenen `beskrivende-form`. Der flettes først efter Franks godkendelse.

Kun ordlyd i dansk og engelsk tekst. Ingen ændringer i logik, data eller layout ud over det, en ny ordlyd kræver.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| Siderne (`index.html`, trænerne, `makkeraftaler.html`, `viden/index.html`), `tools/konventionskort.src.html` og `data/konventioner.json` | ordlyden i de instruktioner og forklaringer, Frank godkender i listen | knapper, links, navne, layout |
| Konventionskortene (`data/kort/`), puljerne (`pools/`), `dealer/` og systemdokumenterne i `viden/` | kun det, Frank vælger i listen (A2–A4) | resten; kortene følger kilderne |
| `assets/footer.js` | kun det, Frank vælger i A1 | links |
| `tools/` | testen `tjek_bydeform.py` | fagordstesten |

## Arbejdsgang

1. Listen i `docs/beskrivende-form.md` med bilag. Intet rettes før Franks godkendelse.
2. Teksterne rettes; konventionskortenes side bygges igen med `tools/build_konventionskort.py`, hvis kilden ændres.
3. `tools/tjek_bydeform.py` (som `tjek_fagord.py`) fejler, hvis en dansk instruktion begynder med et udsagnsord i bydeform.
4. `tjek_fagord.py`, `tjek_konventionskort.py`, `tjek_sprog.py` og `tjek_bydeform.py` køres, og Claude Code stopper før fletning.

## Accepttest

- [ ] Listen er godkendt af Frank.
- [ ] De godkendte tekster står i beskrivende form på dansk og engelsk; knapper, links og navne er uændrede.
- [ ] Sidefoden følger Franks valg i A1, samtidig med forsiden og Fordelingstræneren.
- [ ] `python3 tools/tjek_bydeform.py`, `tjek_fagord.py`, `tjek_konventionskort.py` og `tjek_sprog.py` består.

## Afklaret

1. **Reglen** er Franks valg 30. oktober 2026; den står i `../CLAUDE.md`.
2. **Konventionskortenes meldinger og forklaringer følger kilderne** (Franks ord 30. oktober 2026); de står under Til afgørelse.
