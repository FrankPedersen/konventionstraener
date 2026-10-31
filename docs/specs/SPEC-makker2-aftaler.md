# SPEC-makker2-aftaler

31. oktober 2026 · Franks valg, skrevet ud af Claude Code

To Makker 2-aftaler er bekræftet (Franks valg 31. oktober 2026):

1. **Åbners nye højere farve på 2-trinnet** (fx 1♦ – 1♠ – 2♥) er naturlig, 5-4, 12–15 hp og ikke krav. **Spring i ny højere farve (fx 1♦ – 1♠ – 3♥) er 16+ hp og krav i én runde**; med 19+ viser åbner udgangskraft i næste melding. Revers spilles ikke. Ny *lavere* farve er uændret (Franks rettelse samme dag): 1♦ – 1♠ – 2♣ er naturlig, 12–18 og ikke krav, og 1♦ – 1♠ – 3♣ er 19+ og udgangskrav. Efter 1♥ – 1NT er 2♠ 12–15, og 3♠ viser 5-4 eller 5-5 med 16+, krav i én runde; 3♣ og 3♦ er fortsat 5-5 med 15–18. Træneren `ff-revers` tages af Træn; filerne og kortet bliver.
2. **Svar på makkers konkurrencedobling:** 0–7 hp laveste farve, 8–11 hp spring i farven (invit) og 12+ hp cuebid af modpartens farve (krav).

Det lukker de to Makker 2-punkter, der stod åbne: "foreløbig – bekræftes" (SPEC-konventionskort, punkt 37) og konkurrencedoblingens intervaller (punkt 31).

## Afgrænsning

`main` er tagget `v-foer-makker2-aftaler`, og arbejdet sker på grenen `makker2-aftaler`. Der flettes først efter Franks godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `viden/2-over-1-makker2.html` | de 9 linjer med "foreløbig – bekræftes" og deres grænser; spørgsmålet i C1 lukkes; Bilag G siger, at revers er overvejet og fravalgt; konkurrencedoblingens svar i afsnit 17 | andre aftaler |
| `data/konventioner.json` og `_design/tegneflade/Main.dc.html` | beskrivelsen af `ff-staerke-genmeldinger`; `ff-revers` markeres som fravalgt i Makker 2-systemet | andre trænere |
| `index.html` (Træn) | fravalgte trænere vises ikke | resten af Træn |
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

- [x] `dealer/ff_genmeld.py`: 12–15 hp med 5-4 giver den nye højere farve (2♥), 16–18 hp giver spring (3♥, krav i én runde), og 19+ giver spring efterfulgt af udgangskrav i næste melding. 1♦ – 1♠ – 2♣ med 5-4 giver 2♣ med 12–18, også med 16–18, og 3♣ (udgangskrav) med 19+.
- [x] Puljen `ff-staerke-genmeldinger` er bygget igen og følger grænserne; bonusspørgsmålet har de nye grænser.
- [x] "foreløbig – bekræftes" (og "provisional – to be confirmed") findes ingen steder: Makker 2-dokumentet, `data/konventioner.json`, kortene, dealeren, puljen og tegnefladen.
- [x] Makker 2-dokumentet: afsnit 1, 4 og 6 og B1/B3 har de nye grænser, C1 har ikke længere spørgsmålet om revers, og Bilag G siger, at revers er overvejet og fravalgt.
- [x] Afsnit 4 skelner mellem ny højere farve (2♥ 12–15, spring 3♥ 16+) og ny lavere farve (2♣ 12–18, spring 3♣ 19–21); kortet `ff-staerke-genmeldinger` og beskrivelsen gør det samme.
- [x] Efter 1♥ – 1NT: 2♠ 12–15, 3♠ 5-4 eller 5-5 med 16+ (krav i én runde) og 3♣/3♦ 5-5 med 15–18 står i afsnit 1 og på kortet `ff-staerke-genmeldinger`.
- [x] `ff-revers` er markeret som fravalgt i Makker 2-systemet i `data/konventioner.json` og står ikke på Træn; træneren, puljen og kortet findes stadig.
- [x] Konkurrencedoblingens svar (0–7 hp laveste farve, 8–11 hp spring i farven, 12+ hp cuebid) står i afsnit 17 og på kortet `ff-doblinger`, og det åbne spørgsmål er væk begge steder.
- [x] `tjek_makker2_aftaler.py`, `tjek_konventionskort.py`, `tjek_kort_eksempler.py`, `tjek_fagord.py`, `tjek_sprog.py`, `tjek_bydeform.py`, `tjek_crowhurst.py`, `tjek_skrifttyper.py`, `tjek_skrifttyper.mjs` og `sprogtjek.py` består.
- [x] SPEC-konventionskort (punkt 37 og 40) og `../SYSTEM.md` er opdateret.
- [x] Flettet ind på `main` efter Franks godkendelse og udgivet.

## Afklaret

1. **Valget** er Franks, 31. oktober 2026: begge aftaler er bekræftet med Makker 2.
2. **Kun den nye højere farve får de nye grænser** (Franks rettelse 31. oktober 2026; første udgave af grenen gav også 2♣ dem). En ny lavere farve koster ikke plads, fordi svarer kan give præference på 2-trinnet: 1♦ – 1♠ – 2♣ er 12–18 og ikke krav, og 1♦ – 1♠ – 3♣ er 19+ og udgangskrav, som før. Med 16–18 og 5-4 i de to lave farver meldes 2♣, så der er intet hul. Afsnit 4 har nu en række for hver af de fire meldinger, og springet i højere farve har eksemplet 1♦ – 1♠ – 3♥.
3. **Træneren øver kun åbners genmelding.** Med 16–18 og 19–21 er svaret det samme spring til 3♥; forklaringen siger, at springet er krav i én runde, og at åbner med 19+ viser udgangskraft i næste melding.
4. **Tagget** følger konventionstrænerens navne uden nummer (`v-foer-<gren>`); kun Fordelingstræneren nummererer.
5. **"Laveste farve"** (godkendt af Frank) er læst som farven billigst muligt, som dokumentets egen række "Meld længste/bedste farve, billigst muligt". Rækken "Støtte i doblers senest viste farve" bliver uden "lidt ekstra styrke": med fit foretrækkes doblers farve, og niveauet følger de samme intervaller. "Spring i egen farve" er afløst af "Spring i farven" (8–11, invit), og "Pas" er uændret.
6. **Følgerettelser** (godkendt af Frank): revers er også taget ud af rækkefølgen i C3, så "De åbne punkter ovenfor" er nr. 4; i B3 er "og intervallet er bredt" fjernet, fordi 12–15 ikke er bredere end Flannerys 11–15; Bilag G hedder "Revers (fravalgt)" i overskriften og indholdsfortegnelsen.
7. **Hullet efter 1M – 1NT er lukket** (Franks valg): det gjaldt kun 1♥ – 1NT – 2♠, hvor spar er højere end åbningsfarven. 3♠ viser 5-4 eller 5-5 med 16+, krav i én runde, som springet i hovedreglen; "3 i ny farve" med 5-5 og 15–18 gælder fortsat for 3♣ og 3♦. Afsnit 1 og kortet har det; kortet har det som fortsættelsen "Åbner efter 1♥ – 1NT".
8. **`ff-revers` er taget af Træn** (Franks valg): `data/konventioner.json` har `"fravalgt": "ff"` og "Fravalgt i Makker 2-systemet" i beskrivelsen, og Træn viser ikke fravalgte trænere. `traener.html?k=ff-revers`, puljen, dealeren og kortet om revers findes stadig; kortene er neutrale.
9. **Fletningen er godkendt**, når alle tests er grønne (Frank, 31. oktober 2026).
