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

- [x] Listen er godkendt af Frank.
- [x] De godkendte tekster står i beskrivende form på dansk og engelsk; knapper, links og navne er uændrede.
- [x] Sidefoden følger Franks valg i A1, samtidig med forsiden og Fordelingstræneren.
- [x] `python3 tools/tjek_bydeform.py`, `tjek_fagord.py`, `tjek_konventionskort.py` og `tjek_sprog.py` består.
- [x] Et skærmbillede af konventionstrænerens forside ligger i `C:\Users\frank\Kontraktbridge\skaermbilleder\beskrivende-form\`.

Efter Franks svar på listens Tillæg (31. oktober 2026):

- [x] T1–T4 står i beskrivende form på dansk og engelsk: søgningens besked uden træf, overskriften over metodevalget, trænernes slutskærm og de tre trænerbeskrivelser.
- [x] Testens venteliste er væk, så `tjek_bydeform.py` fejler på alle nye bydeformer, og den og de øvrige tests består.
- [x] Flettet ind på `main` efter Franks godkendelse og udgivet efter forsiden.

## Afklaret

1. **Reglen** er Franks valg 30. oktober 2026; den står i `../CLAUDE.md`.
2. **Konventionskortenes meldinger og forklaringer følger kilderne** (Franks ord 30. oktober 2026); de står under Til afgørelse.
3. **Listen er godkendt** (Frank, 30. oktober 2026): K1–K6 og A5 som foreslået; A2–A4 bliver, og testen springer dem over; A6 "Konventioner, der sidder på rygraden". K2's "Prøv et andet ord." er ikke rettet, fordi det godkendte forslag gentager overskriften; det står i listens Tillæg.
4. **Venteliste:** tekster, testen fandt, og som ikke stod på listen, stod i listens Tillæg og på testens `VENTER`, til Frank havde svaret.
5. **Tillægget er godkendt** (Frank, 31. oktober 2026): T1 "Et andet ord giver måske et træf.", T2 "Hvilken metode spiller I?" og T3 som foreslået. T4: "Lån …" og "Sælg ikke ud …" skulle blive som navne, hvis de var titler fra kildebogen. Det er de ikke: kapitlerne hedder "15c · Genåbning i 4. hånd", "4. 20-20-situationer" og "7. GIF — genåbning i fjerde hånd", og "Sælg 'aldrig' ud under 2♠ …" er en regel i bogens liste. De tre beskrivelser skrives derfor om; kortenes undertitler følger kilderne (A2) og bliver. Den engelske overskrift "Conventions that become second nature" er godkendt. Ventelisten fjernes. Når alle tests i de tre repoer er grønne, er fletningen godkendt; konventionstræneren udgives efter forsiden.
