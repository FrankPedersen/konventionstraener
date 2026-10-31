# SPEC-makker2-aftaler

31. oktober 2026 · Franks valg, skrevet ud af Claude Code

To Makker 2-aftaler er bekræftet (Franks valg 31. oktober 2026):

1. **Åbners nye højere farve på 2-trinnet** (fx 1♦ – 1♠ – 2♥) er naturlig, 5-4, 12–15 hp og ikke krav. **Spring i ny farve er 16+ hp og krav i én runde**; med 19+ viser åbner udgangskraft i næste melding. Revers spilles ikke.
2. **Svar på makkers konkurrencedobling:** 0–7 hp laveste farve, 8–11 hp spring i farven (invit) og 12+ hp cuebid af modpartens farve (krav).

Det lukker de to Makker 2-punkter, der stod åbne: "foreløbig – bekræftes" (SPEC-konventionskort, punkt 37) og konkurrencedoblingens intervaller (punkt 31).

## Afgrænsning

`main` er tagget `v-foer-makker2-aftaler`, og arbejdet sker på grenen `makker2-aftaler`. Der flettes først efter Franks godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `viden/2-over-1-makker2.html` | de 9 linjer med "foreløbig – bekræftes" og deres grænser; spørgsmålet i C1 lukkes; Bilag G siger, at revers er overvejet og fravalgt; konkurrencedoblingens svar i afsnit 17 | andre aftaler |
| `data/konventioner.json` og `_design/tegneflade/Main.dc.html` | beskrivelsen af `ff-staerke-genmeldinger` | andre trænere |
| `dealer/ff_genmeld.py` og `pools/ff-staerke-genmeldinger.json` | de nye grænser; puljen bygges igen med `build_pools.py` | de andre situationer i træneren (2NT, checkback) ud over nye hænder |
| `data/kort/ff-staerke-genmeldinger.json`, `data/kort/ff-doblinger.json` og `viden/konventionskort.html` (bygges) | grænserne, svarene på konkurrencedoblingen, de åbne spørgsmål og eksempler fra den nye pulje | de andre kort |
| `docs/specs/SPEC-konventionskort.md` | punkt 37 og et nyt punkt 40 | resten |
| `../SYSTEM.md` | de to Makker 2-punkter under Kendte forbehold fjernes; beslutningsloggen | hemmeligheder |
| `tools/` | accepttesten `tjek_makker2_aftaler.py` | de andre tests |

## Arbejdsgang

1. Accepttesten `tools/tjek_makker2_aftaler.py` skrives først og fejler.
2. Dealeren rettes, og puljen bygges igen: `python build_pools.py ff-staerke-genmeldinger`.
3. Makker 2-dokumentet, beskrivelsen, tegnefladen og de to kort rettes; kortet `ff-staerke-genmeldinger` får eksempler fra den nye pulje med samme situationer og svar som før. Kortsiden bygges med `python3 tools/build_konventionskort.py`.
4. Alle tests køres, også `tjek_bydeform.py`, og Claude Code stopper før fletning.

## Accepttest

- [ ] `dealer/ff_genmeld.py`: 12–15 hp med 5-4 giver den nye farve (2♥ og 2♣), 16–18 hp giver spring (3♥ og 3♣, krav i én runde), og 19+ giver spring efterfulgt af udgangskrav i næste melding.
- [ ] Puljen `ff-staerke-genmeldinger` er bygget igen og følger grænserne; bonusspørgsmålet har de nye grænser.
- [ ] "foreløbig – bekræftes" (og "provisional – to be confirmed") findes ingen steder: Makker 2-dokumentet, `data/konventioner.json`, kortene, dealeren, puljen og tegnefladen.
- [ ] Makker 2-dokumentet: afsnit 1, 4 og 6 og B1/B3 har de nye grænser, C1 har ikke længere spørgsmålet om revers, og Bilag G siger, at revers er overvejet og fravalgt.
- [ ] Konkurrencedoblingens svar (0–7 hp laveste farve, 8–11 hp spring i farven, 12+ hp cuebid) står i afsnit 17 og på kortet `ff-doblinger`, og det åbne spørgsmål er væk begge steder.
- [ ] `tjek_makker2_aftaler.py`, `tjek_konventionskort.py`, `tjek_kort_eksempler.py`, `tjek_fagord.py`, `tjek_sprog.py`, `tjek_bydeform.py`, `tjek_crowhurst.py`, `tjek_skrifttyper.py`, `tjek_skrifttyper.mjs` og `sprogtjek.py` består.
- [ ] SPEC-konventionskort (punkt 37 og 40) og `../SYSTEM.md` er opdateret.

## Afklaret

1. **Valget** er Franks, 31. oktober 2026: begge aftaler er bekræftet med Makker 2.
2. **Springgrænsen gælder begge nye farver.** Afsnit 4 har én regel for spring i ny farve (eksemplet er 1♦ – 1♠ – 3♣), så den nye lavere farve (2♣) får samme grænser som den nye højere: 12–15 hp uden spring, 16+ med spring. Dokumentet nævnte ikke et interval for 2♣; dealeren brugte 12–18 som for den højere farve.
3. **Træneren øver kun åbners genmelding.** Med 16–18 og 19–21 er svaret det samme spring; forklaringen siger, at springet er krav i én runde, og at åbner med 19+ viser udgangskraft i næste melding.
4. **Tagget** følger konventionstrænerens navne uden nummer (`v-foer-<gren>`); kun Fordelingstræneren nummererer.
