# SPEC-makker2-bilag-c

3. november 2026 · Franks valg, skrevet ud af Claude Code

Makker 2 og Frank har taget stilling til alle punkter i Bilag C. Aftalerne skrives ind i `viden/2-over-1-makker2.html`. `main` er tagget `v-foer-makker2-bilag-c`, og arbejdet sker på grenen `makker2-bilag-c`. Der flettes først efter Franks godkendelse.

## Afgrænsning

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `viden/2-over-1-makker2.html` | aftalerne nedenfor | andre aftaler |
| `tools/tjek_makker2_bilag_c.py` (ny), `tools/tjek_makker2_aftaler.py` | accepttesten og den ændrede 2♠ efter 1♥ – 1NT | de andre tjek |
| Puljer, kort, øvelser, `data/konventioner.json`, `data/viden.json`, `dealer/`, notatet om kontrolsvar | listen nedenfor under Træneren (Frank godkendte listen 3. november 2026) | puljen `bekkasin`, der deles med Makker 1 |

## Aftalerne

### Fra C1

1. **Forsvar mod svag 2 og 3** (nyt afsnit 15d i Del IV): dobling er oplysning op til og med 4♥; 2NT-indmelding over svag 2 er 15–18 hp med hold; 3NT er til spil; efter makkers oplysningsdobling af svag 2 bruges Lebensohl (C4 flyttes ind i afsnittet); mod svag 3 er der intet relæ, ny farve er naturlig, og 3NT er til spil.
2. **Responsiv dobling** (afsnit 17): efter 1x – dobling – 2x/3x er svarers dobling oplysning op til og med 3♠ med 6+ hp. Over støtte i major viser den begge minorer eller en farve, svarer ikke kan melde. Over støtte i minor viser den begge majorer.
3. **Forsvar mod deres to-farvede** (Michaels og 2NT; afsnit 15b): dobling er 10+ hp og interesse i straf; cuebid i deres laveste farve er støtte til vores farve, invit eller mere; cuebid i deres højeste farve er den anden major og krav; vores farve direkte er konkurrence og svag.
4. **Maksimal-dobling** (afsnit 17): når modparten konkurrerer til 3 i farven lige under vores, er dobling maksimum og invit, og 3 i vores farve er konkurrence.
5. **Udspil mod slem** (afsnit 19): mod lilleslem spilles der passivt ud, og et es spilles kun ud med en plan. Lightner: dobling af slem beder om et usædvanligt udspil, ofte bordets først meldte farve.

### Fra C2

6. **Splinter i 2/1-forløbet** bliver som en bevidst undtagelse, og det står ved 2/1-tabellen.
7. **Genåbnings-1NT** (11–14), **count** (højt-lavt = lige antal) og **E-K-x mod sans** (undgå) bliver, som de står.
8. **2♣ med kontrolsvar** erstatter 2♦ waiting i afsnit 14. Svarene og fortsættelserne følger kortet `data/kort/forslag-2kl-kontrolsvar.json`. Det andet negative udgår, og afsnittene "Svarers 2. melding — det andet negative" og "Hvorfor waiting frem for kontrolsvar" fjernes. Overføringssvarene alerteres (Bilag A).

### 2♦ er Flannery

9. **Bilag B1 er en aftale:** 11–15 hp, præcis 5♥ og 4♠, med B1's svarskema og 2NT-spørgsmål. Med 5-5 i majorerne åbnes 1♥. Efter modpartens indmelding er dobling oplysning med kort ruder, svar i major er naturligt og svagt, og 2NT er stadig krav.
10. **Den svage 2♦ udgår** i afsnit 12 og Bilag A, hvor Flannery alerteres. Ogust er uændret, men 2NT over Flannery er B1's spørgsmål.
11. **B2 og B3 beholdes som baggrund.** Overskriften siger, at Flannery er valgt.

### Bilag C

12. Alle emner er aftalt, så bilaget er én linje.

## Træneren

Frank fik listen, før noget blev ændret, og godkendte den 3. november 2026.

| Hvad | Ændring |
| --- | --- |
| `ff-2kl` | Taget af Træn som `ff-revers`: `"fravalgt": "ff"` og `"system": "forslag"`. Pulje, dealer og kort bliver, og siden kan stadig åbnes. Kortets åbne spørgsmål er besvaret |
| `forslag-2kl-kontrolsvar` | Hører nu til Makker 2 og linker til afsnit 14. Id'et bliver, så gemte links virker. Kortets krav til åbningen er dokumentets, og det åbne spørgsmål og henvisningen til waiting er væk. Svarmuligheden "Waiting" i bonusspørgsmålet er omskrevet |
| Notatet `viden/forslag-2klor-kontrolsvar.html` | Står ikke længere som forslag; afsnit 7 siger, at kontrolsvar er aftalt, og at aftalens åbningskrav er dokumentets |
| `ff-flannery` | Hører nu til Makker 2's åbninger. 5-5 i majorerne åbner 1♥ i puljen, kortet har aftalen efter indmelding, og det åbne spørgsmål er besvaret |
| `ff-ogust` | Situationen med svag 2♦ er væk (55 hænder), og kortets to eksempler med 2♦ er skiftet til hænder i 2♥ og 2♠ fra puljen |
| 1♥ med 5-4 under 16 hp | Udelukket i `ff-kravpas`, `ff-doblinger`, `ff-trial-bids`, `ff-revideret-omvendt-bergen` og `ff-two-over-one`, for de hænder åbner 2♦ |
| `ff-kravpas`, næsekravpas | Pas med lange spar er nu 5-5, for 5-4 med 12–14 hp åbner 2♦ |
| `ff-doblinger`, støttedobling | 2♠ med 4 spar og 12–15 hp er nu 6-4 |
| `ff-two-over-one` | 2♠ efter 1♥ – 2♣/2♦ er 5-5 eller 16+ med 5-4, i dealer, pulje og kort |
| `ff-lebensohl` | Kilden hedder afsnit 15d i stedet for bilag C4; linket virker uændret |
| `data/viden.json` | Bilag B og notatet om kontrolsvar hører til Makker 2 og står ikke længere som forslag |

Puljerne er ikke bygget helt forfra: kun hænder, der er blevet forkerte, er skiftet ud, så kortenes eksempler stadig findes i puljerne. Dealerne følger de nye regler, så en senere bygning giver det samme.

## Accepttest

`python3 tools/tjek_makker2_bilag_c.py` (skrevet først):

- [x] Afsnit 15d findes og har aftalerne mod svag 2 og 3 og Lebensohl-skemaet; ankeret `#afsnit-c4` virker stadig, så træneren `ff-lebensohl` linker rigtigt.
- [x] Afsnit 17 har responsiv dobling og maksimal-dobling, afsnit 15b forsvaret mod deres to-farvede, og afsnit 19 udspil mod slem og Lightner.
- [x] Afsnit 14 har kontrolsvarene, overføringerne, de vendte sansintervaller, svarers videre meldinger og skemaet efter indmelding. "Waiting" og "det andet negative" står ingen steder i dokumentet, og åbningskravet er uændret.
- [x] Sanstrappen i afsnit 8 følger afsnit 14.
- [x] Afsnit 12 har Flannery og ikke den svage 2♦. Bilag A har Flannery, 2NT-spørgsmålet og kontrolsvarene.
- [x] Afsnit 1 har 2♠ efter 1♥ som 5-5 med 12–15 og 3♠ som 16+; afsnit 5 har 2♠ efter 1♥ uden 15+. B1 siger det samme.
- [x] Afsnit 4's grænser for ny højere farve (12–15 og spring 16+) er uændrede.
- [x] Bilag B's overskrift siger, at Flannery er valgt, og B1's overskrift, at den er aftalt. B2 og B3 står der stadig.
- [x] Bilag C er én linje, og indholdsfortegnelsen har hverken C1–C4 eller et link, der peger ud i ingenting.
- [x] Træneren følger listen ovenfor, og `python3 tools/tjek_kort_eksempler.py` finder kortenes eksempler i puljerne.

Desuden: `tools/tjek_makker2_aftaler.py` med den ændrede 2♠, `tools/tjek_fagord.py`, `tools/tjek_bydeform.py`, `tools/tjek_sprog.py`, `tools/tjek_konventionskort.py` og `tools/sprogtjek.py`.

## Afklaret

1. **1♥ – 1NT – 2♠ og 3♠** (Franks valg 3. november 2026): B1's "16–18" stod i modstrid med aftalen fra 31. oktober og gav ikke 5-5 med 12–15 et sted at gå hen. Frank valgte: 2♠ er 5-5 med 12–15 og ikke krav, og 3♠ er 5-4 eller 5-5 med 16+ og krav i én runde. Reglen om at springe med 16+ holder dermed i hele systemet. Afsnit 4 er uændret: 1♦ – 1♠ – 2♥ er stadig 5-4 med 12–15.
2. **Kravet til 2♣-åbningen** (Franks valg): dokumentets krav bliver (20+ hp, eller 9 sikre stik i major / 10 i minor, eller jævn fra 22), ikke kortets 8½ spillestik. Kun svarene og fortsættelserne følger kortet.
3. **ASS, overføring og Gerber** (Franks valg): de gælder efter åbners 2NT og 3NT, uanset svarers kontrolsvar. Det direkte 4♣-svar på 2♣ er en overføring, ikke Gerber. 4NT og 5NT er naturlige uden fastlagt trumf, og RKC 1430 gælder med fastlagt trumf.
4. **Følgerettelser:** afsnit 5's "2♠ efter 1♥ = 4+ spar, 5+ hjerter, 15+" følger Flannery, for 5-4 med 15 hp åbnes nu 2♦. Afsnit 4's "Splinter indgår ikke i systemet" nævner de to undtagelser (2/1-forløbet og spring efter 2♣). Afsnit 8's sanstrappe følger afsnit 14. Bilag F's række om Flannery 2♦ er udfyldt, og "17 · De fem doblingstyper" hedder nu "17 · Doblingstyper", fordi afsnittet har flere end fem.
5. **Åbners farvemelding efter 2♣** følger notatet `viden/forslag-2klor-kontrolsvar.html`, der er kilden til kortet: naturlig med 5+ kort, og spring til 3♥, 3♠, 4♣ eller 4♦ fastlægger trumf.
6. **Ankeret `#afsnit-c4`** følger Lebensohl-skemaet med ind i afsnit 15d, så linket fra `data/konventioner.json` virker uændret.
7. **`ff-2kl`** er taget af Træn som `ff-revers` (Franks valg 3. november 2026). Waiting er ikke længere et åbent valg, så forslag ville give et forkert billede.
8. **`bekkasin`** har 5 hænder med 1♥ og 5-4 under 16 hp, men puljen deles med Makker 1, hvor hænderne er rigtige. Den er ikke ændret; det står Frank frit for at vælge.
