# Beskrivende form i konventionstræneren – listen til godkendelse

SPEC-beskrivende-form.md (konventionstræneren), 30. oktober 2026. Intet er rettet endnu. Reglen står i `../CLAUDE.md` under Husets ord: instruktioner og forklaringer i beskrivende form; knapper, links og navne bliver i bydeform; "du" som grundled er beskrivende form.

Listen bygger på al dansk tekst, som `tools/tjek_fagord.py` læser: siderne, `assets/*.js`, `data/**.json`, puljerne, teksterne i `dealer/` og `docs/kampen-om-kontrakten.md`. 502 sætninger og led begynder med et ord, der kan være bydeform; teksterne i sidernes attributter (meta-beskrivelser, `title`, `placeholder`, `aria-label`) er gennemgået for sig. Langt de fleste står i kortene, puljernes forklaringer og systemdokumenterne i `viden/`; de står under Til afgørelse med et bilag nederst. I gruppe 3 står kun den del, der ændres; "…" er resten af teksten.

## 1. Knapper og links (bliver)

- **Siderne:** Vis alle trænere · Se resultat → (trænerne) · Gå til (navigationen på forsiden) · Hent som Word · Hent som Markdown · Træn emnerne → (`viden/kampen-om-kontrakten.html`)
- **Søgefelterne:** Søg (etiketten på forsiden) · Søg i indholdet… (`placeholder` og `aria-label` i `viden/`)
- **Knappernes `title`:** Vis reglen (`markering.html`) · Vis fire mulige meldinger (`traener.html`, `multi-svar-traener.html`)
- **Markeringstrænerens svar** (`valg` i puljerne, fra `dealer/markering.py`): fx Spil ruder tilbage · Skift til ruder

## 2. Navne (bliver)

- **Emner og trænere:** Svar på 1NT · Svar på doblingen — Multitræner · Giv markering · Læs markering
- **Beskrivelser, der begynder med et navneord:** "Svar på 4NT (1430) og på spørgsmålet efter trumfdamen: …" og "Svar på 4NT (5 nøglekort som 5♥/5♠), …" (svar = navneord)

## 3. Instruktioner og forklaringer (skrives om)

**K1** · `index.html`, under overskriften
- DA nu: Vælg en konvention og få 8 tilfældige meldeforløb. Nogle gange …
- DA forslag: Hver konvention giver 8 tilfældige meldeforløb. Nogle gange …
- EN nu: Choose a convention and get 8 random auctions. Sometimes …
- EN forslag: Each convention gives 8 random auctions. Sometimes …

**K2** · `index.html`, søgningen: overskriften for skærmlæsere og beskeden uden træf
- DA nu: Find en træner · Prøv et andet ord.
- DA forslag: Søgning efter en træner · Ingen træner passer på ordet.
- EN nu: Find a trainer · Try another word.
- EN forslag: Trainer search · No trainer matches the word.

**K3** · Fejlbeskederne, når siden åbnes som fil (`index.html`, `traener.html`, `markering.html`, `makkeraftaler.html`, `viden/index.html` og `tools/konventionskort.src.html`)
- DA nu: … Åbn siden via GitHub Pages eller en lokal webserver. · … Åbn siden via GitHub Pages eller en lokal webserver — ikke direkte som fil. · … Tjek at data/kort/index.json findes, og åbn siden via GitHub Pages eller en lokal webserver.
- DA forslag: … Siden skal åbnes via GitHub Pages eller en lokal webserver. · … Siden skal åbnes via GitHub Pages eller en lokal webserver – ikke direkte som fil. · … data/kort/index.json skal findes, og siden skal åbnes via GitHub Pages eller en lokal webserver.
- EN nu: … Open the page via GitHub Pages or a local web server. (og tilsvarende)
- EN forslag: … The page must be opened via GitHub Pages or a local web server. (og tilsvarende)

**K4** · `multi-svar-traener.html`, under overskriften
- DA nu: … Vælg dit svar i meldekassen — tryk på pæren for et hint, hvis du er i tvivl.
- DA forslag: … Du vælger dit svar i meldekassen; pæren giver et hint, hvis du er i tvivl.
- EN nu: … Choose your response in the bidding box — tap the bulb for a hint if you are unsure.
- EN forslag: … You choose your response in the bidding box; the bulb gives a hint if you are unsure.

**K5** · `data/konventioner.json`, trænernes beskrivelser
- multiforsvar · DA nu: Modstanderen åbner 1NT. Meld ind med D (straf), 2♣–2NT eller 3♣/3♦ – eller svar på makkers indmelding. → DA forslag: Modstanderen åbner 1NT. Du melder ind med D (straf), 2♣–2NT eller 3♣/3♦ – eller svarer på makkers indmelding. · EN nu: … Overcall with X (penalty), … – or respond to partner's overcall. → EN forslag: … You overcall with X (penalty), 2♣–2NT or 3♣/3♦ – or respond to partner's overcall.
- forslag-2kl-kontrolsvar · DA nu: Tæl kontroller (es = 2, konge = 1) og svar på makkers 2♣ – eller vis en god farve med overføring. … → DA forslag: Du tæller kontroller (es = 2, konge = 1) og svarer på makkers 2♣ – eller viser en god farve med overføring. … · EN nu: Count controls (ace = 2, king = 1) and respond to partner's 2♣ – or show a good suit with a transfer. … → EN forslag: You count controls (ace = 2, king = 1) and respond to partner's 2♣ – or show a good suit with a transfer. …
- kamp-forsvar-1ut · DA nu: Vælg jeres forsvar mod modstandernes 1NT – Landy, DONT eller Multi – før hænderne vises. … → DA forslag: I vælger jeres forsvar mod modstandernes 1NT – Landy, DONT eller Multi – før hænderne vises. … · EN nu: Choose your defence against the opponents' 1NT – … – before the hands are shown. … → EN forslag: You choose your defence against the opponents' 1NT – Landy, DONT or Multi – before the hands are shown. …
- markeringer · DA nu: … Giv eller læs markeringen. → DA forslag: … Du giver eller læser markeringen. · EN nu: … Give or read the signal. → EN forslag: … You give or read the signal.
- ff-flannery · DA nu: … Træn åbningen, svarene på 2♦ og åbners svar på 2NT-spørgsmålet. → DA forslag: … Træneren øver åbningen, svarene på 2♦ og åbners svar på 2NT-spørgsmålet. · EN nu: … Practise the opening, the responses to 2♦ and opener's answers to the 2NT ask. → EN forslag: … The trainer covers the opening, the responses to 2♦ and opener's answers to the 2NT ask.
- ff-revers · DA nu: … Træn åbners valg mellem revers og gentaget farve, og svarers anden melding efter 1♣/1♦ – 1♠ – 2♥. → DA forslag: … Træneren øver åbners valg mellem revers og gentaget farve og svarers anden melding efter 1♣/1♦ – 1♠ – 2♥. · EN nu: … Practise opener's choice between a reverse and a rebid suit, and responder's second bid … → EN forslag: … The trainer covers opener's choice between a reverse and a rebid suit and responder's second bid after 1♣/1♦ – 1♠ – 2♥.

**K6** · `index.html`, meta-beskrivelsen (søgemaskiner og delte links; kun dansk)
- nu: Træn bridgekonventioner med tilfældige meldeforløb – som indmelder, åbner og svarer – og slå op i vores aftaler og notater.
- forslag: Træning i bridgekonventioner med tilfældige meldeforløb – som indmelder, åbner og svarer – og opslag i vores aftaler og notater.

## 4. Til afgørelse

**A1 · Sidefoden.** `assets/footer.js` har ikke sætningen "Har du fundet en fejl, eller har du en idé til en ny træner? …"; den har "Gratis bridgetræning i browseren. Lavet af Frank Pedersen." og knappen "Om mig og kontakt →". Sætningen står kun i Fordelingstrænerens `Footer.tsx` og som variant på Om mig (se forsidens liste, A1). Valget står i forsidens liste, A1: med (a) ændres `footer.js` ikke; med (b) får den sætningen som en linje over knappen "Om mig og kontakt →" ligesom forsidens sidefødder.

**A2 · Konventionskortene** (`data/kort/*.json` og kortenes visning, 95 sætninger) følger kilderne: meldinger og forklaringer som "Spring i ny farve er udgangskrav.", "Svar på 1♥/1♠ uden indmelding i farve" (navneord), "Spil ikke væk fra E x x x mod sans.", "skift farve" og eksemplernes "Spil ud", "Kast" og "Læg" (`tools/konventionskort.src.html`). Mange er navneord ("spring", "svar", "hold"). **Forslag:** de bliver, som kilderne skriver dem; testen springer kortene over. Bilaget viser dem alle.

**A3 · Puljernes forklaringer** (`why` i `pools/*.json`, 155 sætninger, 1.211 forekomster) skrives af skabelonerne i `dealer/*.py` (37), fx "Hold i klør og tillæg (17 hp): spring til 3NT.", "11 hp – devalueret 8 (7–10): spring til 3♦ i ruder." og "Svar som om du har 3 hp færre – ellers straffer du makker for at genåbne." Det er meldeforklaringer efter kilderne, og "hold"/"spring" er ofte navneord. At ændre dem kræver nye skabeloner i `dealer/` og at alle puljer bygges igen med `build_pools.py`. **Forslag:** de bliver; testen springer puljerne og `dealer/` over. Multitrænerens forklaringer i `multi-svar-traener.html` ("Med 0–7 hp scrambles der: meld din laveste 4-farve. … Kildens eget eksempel.") hører til samme gruppe.

**A4 · Systemdokumenterne** i `viden/` (`bridgesystem.html`, `2-over-1.html`, `2-over-1-makker2.html`, `forslag-2klor-kontrolsvar.html`, `kampen-om-kontrakten.html` og kilden `docs/kampen-om-kontrakten.md`; 178 sætninger) er dine og makkernes aftaler, fx "Meld …", "Se svaret", "Del I · Trumfkontrakter" (navneord) og "Bemærk: …". **Forslag:** de bliver, som de er skrevet; testen springer dem over. Bilaget viser dem alle.

**A5 · `kamp-landy` i `data/konventioner.json`:** "… og makkers svar: vælg major, 2♦ lige lange, 2NT spørger, 3M invit." er meldenotation (betydningen af makkers svar). **Forslag:** "… og makkers svar: valg af major, 2♦ lige lange, 2NT spørger, 3M invit." / "… and partner's response: choice of major, 2♦ with equal length, 2NT asks, 3M invitational."

**A6 · Forsidens overskrift** (H1): "Træn konventionerne, til de sidder" / "Practise the conventions until they stick". Det er trænerens slogan, hverken knap, link eller navn på en øvelse. **Forslag:** "Konventioner, der sidder" / "Conventions that stick"; ellers bliver den som et navn. Forsidens "Træn bridge lidt hver dag" står i dens liste (A5) med samme valg.

## 5. Falske træf (bliver)

- "Spring i ny farve er …" og "spring i ny farve er 19–21 …": "spring" er navneord.
- "Hold i farven …": "hold" er navneord (stopper).

## Testen (efter godkendelsen)

`tools/tjek_bydeform.py` læser samme tekst som `tools/tjek_fagord.py` og fejler, hvis en dansk sætning eller et led efter kolon eller semikolon begynder med et udsagnsord i bydeform. Knapper, links, navne og de falske træf står på en liste over undtagelser, og kortene, puljerne, `dealer/` og systemdokumenterne springes over, hvis A2–A4 bliver som foreslået.



## Godkendelse (Frank, 30. oktober 2026)

Listen er godkendt med disse valg, og teksterne er rettet på grenen `beskrivende-form`:

- **K1–K6:** som foreslået, med én undtagelse i K2 (se Tillæg, T1).
- **A1 Sidefoden:** `footer.js` er uændret (forsidens A1, valg a).
- **A2–A4:** kortene, puljerne, skabelonerne og `viden/` bliver, og testen springer dem over.
- **A5 kamp-landy:** "valg af major" / "choice of major".
- **A6 Overskriften:** "Konventioner, der sidder på rygraden" / "Conventions that become second nature" (den engelske er Claude Codes oversættelse af Franks danske).

Gruppe 1 har fået de links og knapper, testen fandt: Træn (topbaren) · Træn 8 → (trænerkortene) · Vælg konvention · Skift forsvar · Forfra · Udskriv eller hent (værktøjslinjen i dokumenterne) · Udskriv eller gem som PDF.

## Tillæg: fundet, da testen blev skrevet

Testen læser med flere udsagnsord end skanningen (gennemgå, lån, sælg). De her tekster stod på testens venteliste, til Frank svarede.

**Godkendt** (Frank, 31. oktober 2026) og rettet som foreslået. T4 skulle blive som navne, hvis det var titler fra kildebogen; det er de ikke (kapitlerne hedder "15c · Genåbning i 4. hånd", "4. 20-20-situationer" og "7. GIF — genåbning i fjerde hånd", og "Sælg 'aldrig' ud under 2♠ …" er en regel i bogens liste), så de er skrevet om; på engelsk er ff-genaabning "The balancer borrows …" som i puljen. Kortenes undertitler følger kilderne (A2) og er uændrede. Ventelisten er fjernet, så testen fejler på alle nye bydeformer.

**T1 · K2, beskeden uden træf** (`index.html`): under overskriften "Ingen trænere passer" ville det godkendte "Ingen træner passer på ordet." gentage overskriften. "Prøv et andet ord." står derfor uændret.
- forslag: Et andet ord giver måske et træf. (EN: Another word may give a match.)

**T2 · Overskriften over metodevalget** (`traener.html`, når konventionen ikke har sit eget spørgsmål)
- nu: Vælg metode (EN: Choose a method)
- forslag: Hvilken metode spiller I? (EN: Which method do you play?), som konventionernes eget "Hvilket forsvar mod 1NT spiller I?"

**T3 · Trænernes slutskærm** (`traener.html`, `markering.html`, `multi-svar-traener.html`)
- nu: Gennemgå forklaringerne igen, og prøv en gang til. (EN: Go through the explanations again and have another go.)
- forslag: Du kan gennemgå forklaringerne igen og prøve en gang til. (EN: You can go through the explanations again and have another go.)

**T4 · Tre trænerbeskrivelser** (`data/konventioner.json`)
- ff-genaabning, nu: Lån ca. 3 hp af makker: … (EN: Borrow about 3 HCP from partner: …) → forslag: Genåbneren låner ca. 3 hp af makker: … (EN: The reopener borrows about 3 HCP from partner: …)
- kamp-gif, nu: Lån 3–4 hp på ujævne hænder: … (EN: Borrow 3–4 HCP with unbalanced hands: …) → forslag: Du låner 3–4 hp på ujævne hænder: … (EN: You borrow 3–4 HCP with unbalanced hands: …)
- kamp-2020, nu: Sælg ikke ud under 2♠, når de har fundet tilpasning – og meld efter trumfreglen og zonen, når I selv kæmper videre. (EN: Do not sell out below 2♠ … – and bid by the trump rule …) → forslag: I sælger ikke ud under 2♠, når de har fundet tilpasning – og melder efter trumfreglen og zonen, når I selv kæmper videre. (EN: You do not sell out below 2♠ when they have found a fit – and bid by the trump rule and the vulnerability when you compete further.)

## Bilag: alle sætninger under Til afgørelse

Fra skanningen 30. oktober 2026: filen, antal forekomster (×n) og sætningen eller leddet, som det begynder. Markeringstrænerens svar ("Spil … tilbage", "Skift til …") står med i puljerne, men er knapper (gruppe 1).

### A2 · Konventionskortene (95 sætninger, 100 forekomster)

- `assets/konventionskort-hint.js`: Spil ud
- `data/kort/bekkasin.json`: Svar på 1♥/1♠ uden indmelding i farve · spørg om korthed
- `data/kort/crowhurst.json`: Svar på 4NT med 6 esser
- `data/kort/cuebids.json`: Spring forbi en farve · Brug 1430 til at afklare esserne, før I går forbi udgang.
- `data/kort/ff-1430.json`: Meld slem på stikvurdering. · Spring spørgsmålet over.
- `data/kort/ff-2kl.json`: Svar på 2♣ og forløbet efter 2♦ · Hold i de umeldte farver, jævn
- `data/kort/ff-ass.json`: Spring i ny farve
- `data/kort/ff-doblinger.json`: spring til 2♠ (16–18).
- `data/kort/ff-fast-arrival.json`: luk kontrakten
- `data/kort/ff-genaabning.json`: Spring i farve (×2) · Hold i deres farve – en rigtig sanshånd · spring til 2♠ i spar.
- `data/kort/ff-kravpas.json`: Meld efter trumflængden – og genåbn med dobling, når makker kan strafpasse · meld op til lige så mange stik, som parret har trumfer – 8 trumfer til 2-trinnet, 9 til 3, 10 til 4.
- `data/kort/ff-lebensohl.json`: Svar på makkers oplysningsdobling af svag 2♥/2♠ · Ret til egen farve
- `data/kort/ff-michaels.json`: Spring i den viste farve
- `data/kort/ff-ogust.json`: Svar på svag 2 og på et svagt spring · Gentag farven
- `data/kort/ff-omvendt-minor.json`: Svar på 1♣/1♦ uden indmelding i farve · Hold i farven, benægter hold i farverne under
- `data/kort/ff-revers.json`: Gentag egen farve · Hold i ruder, ingen fit og 13 hp
- `data/kort/ff-revideret-omvendt-bergen.json`: Svar på 1♥/1♠ uden indblanding
- `data/kort/ff-staerke-genmeldinger.json`: Spring i ny farve · spring til 3♣ – udgangskrav (19–21).
- `data/kort/ff-trial-bids.json`: Meld trial bid i den svageste farve – aldrig i en stærk farve.
- `data/kort/ff-two-over-one.json`: Svar på 1♥/1♠ fra en uforhåndspasset svarer, når modparten tier · Spring i ny farve
- `data/kort/fjerde-farve.json`: Hold i den fjerde farve. · Hold i klør og 11 hp · gentag farven – 2♦. · meld den fjerde farve naturligt – 3♣ (sidste udvej).
- `data/kort/forslag-2kl-kontrolsvar.json`: Svar på 2♣ efter antal kontroller · Svar på 2♣, også efter indmelding · Spring i ny farve · Spring i farve
- `data/kort/kamp-1ut-forsvar.json`: Svar efter indmelding eller strafdobling over makkers 1NT
- `data/kort/kamp-1ut-indmeldt.json`: Svar efter modpartens 1NT-indmelding over makkers åbning
- `data/kort/kamp-efter-od.json`: Svar efter oplysningsdobling af makkers åbning
- `data/kort/kamp-forsvar-1ut.json`: Svar på Landy 2♣ · spring til 3♥ – invit med støtte. · vælg din femfarve – 2♠.
- `data/kort/kamp-gif.json`: Spring på 2-trinnet · Hold, op til 12–13 hp · Hold · spring er spærrende som i anden hånd. · spring til 2♥ – efter to passer er spring konstruktive (11–14).
- `data/kort/kamp-stoette-def.json`: spring i ny farve er udgangskrav. (×2) · Spring i ny farve (×2) · Svar på makkers simple indmelding (indmelder 8–17 hp) · Spring er konstruktive, ikke krav. · Spring i makkers farve er svagt (6–9)
- `data/kort/kamp-stoette-minor.json`: Svar efter indmelding over makkers 1♣/1♦ · Hold i deres farve, benægter firfarve i spar · Hold i deres farve – invit
- `data/kort/kamp-stoette-off.json`: Svar efter indmelding over makkers åbning
- `data/kort/lavinthal.json`: Skift til den højeste af de to sidefarver · Skift til den laveste af de to sidefarver · Spil den højeste af de to farver · Spil den laveste af de to farver · spil et højt kort, ♦10. · læg et lavt kort, ♥5.
- `data/kort/lebensohl.json`: Svar på makkers oplysningsdobling af en svag 2-åbning · Svar på dobling af svag 2 – ikke over vores egen 1NT · Ret til egen farve
- `data/kort/markeringer.json`: skift farve (×2) · fortsæt farven. · spil farven · fortsæt farven · læg det højeste, ♥9 (højt = ulige). · læg det laveste, ♦5 (lavt = lige).
- `data/kort/michaels.json`: Spring i farven
- `data/kort/multiforsvar.json`: Spring · Spring i farve
- `data/kort/omvendt-bergen.json`: Svar på 1♥/1♠ uden indmelding i farve · meld 4♥.
- `data/kort/truscott.json`: Svar efter oplysningsdobling af makkers åbning · Spring i ny farve
- `data/kort/udspil.json`: Spil ikke væk fra E x x x mod sans. (×2) · Undgå, spil fra en anden farve · fortsæt farven · Søg stik hurtigt · Byg en lang farve op · spil kongen.
- `data/kort/usaedvanlig-2nt.json`: vælg farve med svag hånd, cuebid med god. · Spring i en vist farve · spring til 4♥ er spærrende med god støtte.
- `data/kort/xy-sans.json`: Stop
- `viden/konventionskort.html`: Spil ud · Tjek at data/kort/index.json findes, og åbn siden via GitHub Pages eller en lokal webserver.

### A3 · Puljerne (155 sætninger, 1211 forekomster)

- `pools/ff-1430.json`: Svar (×4)
- `pools/ff-doblinger.json`: spring til 2♠ (16–18). (×12) · genmeld farven, 2♦. (×12)
- `pools/ff-genaabning.json`: spring til 3♦ i ruder. (×32) · spring til 3♣ i klør. (×32) · spring til 2♠ i spar. (×16) · spring til 3♥ i hjerter. (×16) · Træk 3 hp fra – makker har lånt dem (×4) · Læg 3 hp til (×2) · Svar som om du har 3 hp færre – ellers straffer du makker for at genåbne. (×2)
- `pools/ff-kravpas.json`: meld til det antal stik, der svarer til antallet af trumf – 8 trumf 2-trinnet, 9 trumf 3-trinnet, 10 trumf 4-trinnet. (×4)
- `pools/ff-michaels.json`: spring til 3♠ – spærrende. (×16) · spring til 4♦ – spærrende. (×15) · spring til 4♥ – spærrende. (×15) · spring til 4♣ – spærrende. (×15) · spring til 3♥ – spærrende. (×11)
- `pools/ff-omvendt-minor.json`: Hold i farven – og benægter hold i farverne under (×4)
- `pools/ff-revers.json`: Hold i ruder, ingen fit og 13 hp (×6) · Hold i ruder, ingen fit og 10 hp (×4) · Hold i klør, ingen fit og 13 hp (×4) · Hold i ruder, ingen fit og 14 hp (×3) · Hold i klør, ingen fit og 12 hp (×3) · Hold i klør, ingen fit og 9 hp (×3) · Hold i klør, ingen fit og 15 hp (×3) · Hold i ruder, ingen fit og 12 hp (×2) · Hold i ruder, ingen fit og 9 hp (×2) · Hold i klør, ingen fit og 10 hp (×2) · Hold i klør, ingen fit og 14 hp (×2) · Hold i ruder, ingen fit og 11 hp · Hold i klør, ingen fit og 11 hp
- `pools/ff-staerke-genmeldinger.json`: spring til 3♣ – udgangskrav (19–21). (×13) · spring til 3♥ – udgangskrav (19–21). (×13) · Spring er altid spærrende
- `pools/fjerde-farve.json`: spring til 3NT. (×35) · Hold i klør og 11 hp (×18) · gentag farven – 2♦. (×18) · meld den fjerde farve naturligt – 3♣ (sidste udvej). (×18) · gentag farven – 3♣. (×17) · Hold i ruder og 12 hp (×13) · Hold i ruder og 11 hp (×12) · Hold i klør og 13 hp (×10) · Hold i klør og tillæg (15 hp) (×9) · Hold i ruder og 13 hp (×9) · Hold i klør og minimum (12 hp) (×8) · Hold i ruder og minimum (14 hp) (×8) · Hold i ruder og tillæg (16 hp) (×8) · Hold i klør og 12 hp (×7) · Hold i klør og minimum (13 hp) (×7) · Hold i klør og tillæg (16 hp) (×7) · Hold i klør og 14 hp (×6) · Hold i ruder og 14 hp (×6) · Hold i ruder og tillæg (17 hp) (×6) · Hold i klør og 16 hp (×5) · Hold i ruder og 16 hp (×5) · Hold i ruder og 15 hp (×5) · Hold i ruder og minimum (12 hp) (×5) · Hold i ruder og minimum (13 hp) (×5) · Hold i klør og 15 hp (×4) · Hold i klør og minimum (14 hp) (×3) · Hold i ruder og tillæg (15 hp) (×3) · Hold i farven (×2) · Hold i klør og tillæg (17 hp) (×2)
- `pools/kamp-gif.json`: spring til 2♠ – efter to passer er spring konstruktive (11–14). (×18) · spring til 2♥ – efter to passer er spring konstruktive (11–14). (×9)
- `pools/kamp-landy.json`: vælg din femfarve – 2♥. (×23) · vælg din femfarve – 2♠. (×23) · spring til 3♥ – invit med støtte. (×16) · spring til 3♠ – invit med støtte. (×16)
- `pools/kamp-stoette-def.json`: Spring i ny farve er derimod udgangskrav. (×3)
- `pools/lavinthal.json`: Spil ruder tilbage (×32) · Skift til ruder (×30) · Spil klør tilbage (×29) · Skift til klør (×24) · Skift til hjerter (×20) · Spil hjerter tilbage (×13) · Spil spar tilbage (×13) · Skift til spar (×13) · spil et højt kort, ♦10. (×5) · læg et lavt kort, ♣2. (×5) · spil et højt kort, ♣9. (×3) · spil et lavt kort, ♦2. (×3) · spil et højt kort, ♠10. (×3) · læg et lavt kort, ♥5. (×3) · læg et højt kort, ♠10. (×3) · spil et lavt kort, ♥3. (×2) · spil et højt kort, ♣10. (×2) · spil et lavt kort, ♣3. (×2) · læg et lavt kort, ♦4. (×2) · læg et højt kort, ♣10. (×2) · læg et lavt kort, ♣3. (×2) · spil et lavt kort, ♥4. · spil et lavt kort, ♠3. · spil et lavt kort, ♣2. · spil et højt kort, ♦9. · spil et lavt kort, ♦4. · spil et højt kort, ♠8. · spil et lavt kort, ♠2. · spil et lavt kort, ♥6. · spil et lavt kort, ♣8. · læg et lavt kort, ♣4. · læg et lavt kort, ♥4. · læg et lavt kort, ♦2. · læg et højt kort, ♥9. · læg et højt kort, ♣9. · læg et lavt kort, ♠7. · læg et lavt kort, ♣5. · læg et højt kort, ♦8. · læg et højt kort, ♣8. · læg et lavt kort, ♠2. · læg et lavt kort, ♥3. · læg et højt kort, ♦10.
- `pools/markeringer.json`: læg det laveste, ♥3 (lavt = lige). (×5) · læg det højeste, ♥10 (højt = ulige). (×4) · læg det laveste, ♥2 (lavt = lige). (×3) · læg det laveste, ♣2 (lavt = lige). (×3) · læg det højeste, ♥9 (højt = ulige). (×3) · læg det laveste, ♦4 (lavt = lige). (×3) · læg det højeste, ♣10 (højt = ulige). (×3) · læg det laveste, ♥6 (lavt = lige). (×2) · læg det laveste, ♦5 (lavt = lige). (×2) · læg det laveste, ♦3 (lavt = lige). (×2) · læg det højeste, ♣9 (højt = ulige). (×2) · læg det laveste, ♠2 (lavt = lige). (×2) · læg det højeste, ♣7 (højt = ulige). · læg det højeste, ♦9 (højt = ulige). · læg det laveste, ♣3 (lavt = lige). · læg det laveste, ♦9 (lavt = lige). · læg det højeste, ♥7 (højt = ulige). · læg det laveste, ♠3 (lavt = lige). · læg det højeste, ♦7 (højt = ulige). · læg det højeste, ♠8 (højt = ulige). · læg det højeste, ♠9 (højt = ulige). · læg det laveste, ♦2 (lavt = lige).
- `pools/michaels.json`: spring til 3♥ er spærrende med god støtte. (×25) · spring til 3♠ er spærrende med god støtte. (×25) · Vælg farve med svag hånd, cuebid med god (×4) · Meld altid sans med hold (×2) · vælg farve på laveste niveau med en svag hånd, cuebid med 10+. (×2)
- `pools/multiforsvar.json`: spring til 3♠ er udgangsforslag i farven eller sans (mindst 5-farve, ca. 9–11 hp). (×4) · spring til 3♥ er udgangsforslag i farven eller sans (mindst 5-farve, ca. 9–11 hp). (×4) · spring til 3♦ er udgangsforslag i farven eller sans (mindst 5-farve, ca. 9–11 hp). (×4) · spring til 3♣ er udgangsforslag i farven eller sans (mindst 5-farve, ca. 9–11 hp). (×4)
- `pools/omvendt-bergen.json`: meld 4♥. (×9)
- `pools/truscott.json`: spring til 2♠ – spærrende uden støtte. (×27) · spring til 3♣ – spærrende uden støtte. (×27) · spring til 2♥ – spærrende uden støtte. (×18) · spring til 3♦ – spærrende uden støtte. (×18) · spring til 2♦ – spærrende uden støtte. (×9) · spring til 3♥ – spærrende uden støtte. (×9)
- `pools/usaedvanlig-2nt.json`: spring til 4♦ er spærrende med god støtte. (×31) · spring til 4♣ er spærrende med god støtte. (×31) · spring til 4♥ er spærrende med god støtte. (×22) · Vælg farve med svag hånd, cuebid med god (×8) · Meld altid sans med hold (×4) · vælg farve på laveste niveau med en svag hånd, cuebid med 10+. (×4)

### A3 · Skabelonerne i dealer/ (37 sætninger, 42 forekomster)

- `dealer/ff_doblinger.py`: genmeld farven, 2♦. · spring til 2♠ (16–18).
- `dealer/ff_genaabning.py`: Træk 3 hp fra – makker har lånt dem · Svar som om du har 3 hp færre – ellers straffer du makker for at genåbne. · Læg 3 hp til · spring til   i  .
- `dealer/ff_genmeld.py`: Spring er altid spærrende · spring til 3♣ – udgangskrav (19–21). · spring til 3♥ – udgangskrav (19–21).
- `dealer/ff_kravpas.py`: meld til det antal stik, der svarer til antallet af trumf – 8 trumf 2-trinnet, 9 trumf 3-trinnet, 10 trumf 4-trinnet.
- `dealer/ff_michaels.py`: spring til   – spærrende. (×2)
- `dealer/ff_minor.py`: Hold i farven – og benægter hold i farverne under
- `dealer/ff_revers.py`: Hold i  , ingen fit og   hp (×2)
- `dealer/ff_rkc.py`: Svar
- `dealer/fjerde_farve.py`: Hold i   og   hp (×2) · Hold i farven · Hold i   og tillæg (  hp) · spring til 3NT. · gentag farven –  . · meld den fjerde farve naturligt – 3  (sidste udvej). · Hold i   og minimum (  hp)
- `dealer/kamp_konk.py`: spring til   – efter to passer er spring konstruktive (11–14).
- `dealer/kamp_stoette.py`: Spring i ny farve er derimod udgangskrav.
- `dealer/landy.py`: vælg din femfarve – 2 . · spring til 3  – invit med støtte.
- `dealer/markering.py`: Spil   tilbage (×2) · Skift til (×2) · spil et   kort,  . · læg et   kort,  . · læg det laveste,   (lavt = lige). · læg det højeste,   (højt = ulige).
- `dealer/multiforsvar.py`: spring til 3  er udgangsforslag i farven eller sans (mindst 5-farve, ca. 9–11 hp).
- `dealer/tofarvet.py`: Vælg farve med svag hånd, cuebid med god · vælg farve på laveste niveau med en svag hånd, cuebid med 10+. · Meld altid sans med hold · spring til   er spærrende med god støtte.
- `dealer/truscott.py`: spring til   – spærrende uden støtte.

### A4 · Systemdokumenterne (178 sætninger, 203 forekomster)

- `docs/kampen-om-kontrakten.md`: Vær opmærksom på zonestillingen (se §2). · Meld på fordeling, ikke honnørpoint. · Spring i ny farve · Spring i ny farve er udgangskrav.** Samme meldetype, modsat betydning. · Bemærk · Spring er derfor konstruktive: · Svar på Landy 2♣
- `viden/2-over-1-makker2.html`: Svar (×4) · Del I · Trumfkontrakter (×2) · Del II · Sanskontrakter (×2) · Del III · Spærremeldinger (×2) · Del IV · Indmeldinger og doblinger (×2) · Del V · Modspil (×2) · Spring i ny farve (3 (×2) · Se (×2) · Svar på trial bid: · Se afsnit 3 · Se Bekkasin-skemaet i afsnit 2 · Se genmeldingsskemaet nedenfor · Se afsnit 5 · Spring i ny farve (fx 1 · Hold i den fjerde farve. · Gentag egen farve · Meld den fjerde farve naturligt · Følg åbners initiativ · stop Svag hånd, egen lang farve · Meld slem på stikvurdering i stedet. · Luk kontrakten — makker skal normalt · Spring forbi en farve · Vær opmærksom på den ene · Se det fulde ASS-skema nedenfor · Vælg først typen, derefter niveauet. · Genmeld farven. · Vis den anden farve billigst muligt, 12–15. · Meld sans efter stigen ovenfor · Meld makkers farve · Spring i ny farve · Bemærk forskellen på de to situationer · Se Ogust-skemaet nedenfor. · gentag egen farve · Meld farven · spring. · Hold i de umeldte farver, jævn fordeling, 5+ hp · Følg indmelders beslutning · Husk at makker har sat dig til 2–3 sikre · Svar på DONT · Undgå mellemstyrken — meld i stedet · Svar på begge konventioner · Meld på det laveste · Spring i den viste farve · vælg farve med · Husk Loven — indmelder har mindst · Spring i farve · Meld derfor, som om du har tre point · Spring kun med reelle værdier · Meld længste farve — major før minor. · Følg doblers plan · hold i den doblede farve, ca. 6–10 hp · Vælg minor eller meld naturligt videre · spring · 19+ hp · Genmeld egen farve · Meld længste/bedste farve, billigst muligt · Spring i egen farve · Meld op til det antal stik, der svarer til antallet af trumfer, · Meld til · Meld ikke frivilligt videre. · Meld til 3, også uden ekstra point. · Meld til 4 — som spil eller som ofring. · Meld · Følg Loven. · Følg Loven, men uden overdrivelser. · Vær forsigtig. · Meld ét trin under Loven · Dobl ikke en · Bemærk sammenhængen med afsnit 18 · se afsnit 15c · Undgå · Undgå — spil 4. · træk udspilskortets værdi fra 11 — · find selv på noget · brug altid attitude først, hvis den er · Træk udspilskortets · regn den altid, når der spilles lille ud mod sans. · Bemærk · Vælg Multi, hvis I hellere vil vinde på forstyrrelse end på · Vælg Flannery, hvis · Vælg ingen · Vælg ét · Skriv eksplicit ind, at 1 · Se B2 for den fulde beskrivelse — den er · vurdér grundigt, om gevinsten (mere præcise · Se Bilag B. · tag ét emne ad gangen, spil det i nogle · gør. · Meld den — halvdelen af felten gør · Meld den i begge zoner — grænsen er ca. 45 % uden for zone og 37 % i zonen · Undgå — koster overstik · Brug det — beskytter kontrakten · Følg afsnit 5 (15+ for ny farve på 3-trinnet)
- `viden/2-over-1.html`: Se svaret (×6) · Spil i fred (×2) · Spil efter indblanding (×2) · hold i deres farve (×2) · meld kun videre med reelt tillæg – hans spring kan være spærrende. · Spring i makkers major · Tæl dem aldrig, før fittet er bekræftet – og aldrig i sans. · Svar · meld 2 over 1 først, og støt bagefter (spil 4). · meld 2 over 1 først, og meld udgang bagefter (spil 3). · Spring i ny farve · Se, hvordan Syds svar skifter med pointene – og med antallet af trumf. · Svar 1NT, og vis ruderne næste gang billigst muligt: · spring i åbningsfarven · hold i de umeldte farver · spring i åbners major · Spil 1 · Læg mærke til, at Syd aldrig var i tvivl om sin første melding · Spil 2 · Spil 3 · Spil 4 · Vis støtten, før du viser noget andet. · hold i deres farve. · spring i makkers farve · spring i hans major · Spil 5 · Spil 6 · Spil 7 · Tæl pointene selv, før du åbner svaret. · Tag stilling til dem, før I sætter jer ved bordet.
- `viden/bridgesystem.html`: Svar (×3) · Svar på 1NT (×2) · Se 4.3 (×2) · Åbn 1♠. · svar på 3NT · Spring til 3NT · Meld med støtte (3 trumfer) – der skal sjældent passes. · Se skemaet i 4.5 · Se 4.2 · meld 2-over-1 først og vis · Hold i den fjerde farve. · Gentag egen farve · Meld den fjerde farve naturligt · Meld på det laveste · Spring i en af de viste farver · vælg farve med svag hånd, cuebid med · Svar på oplysningsdobling · Spring · Se 8.1 · Svar på 2♣, 2 · Svar på 2 · Svar på doblingen – særligt mod svag sans (12–14) · meld din laveste 4-farve. · Svar på dobling af svag 2 · Undgå – spil 4. · træk 4.-højeste-kortets
- `viden/forslag-2klor-kontrolsvar.html`: Svar (×3) · Spil, meldeforløb og konklusioner · Tæl i den lange farve kortene minus taberne og i sidefarverne topstikkene. · Bemærk · Spring i ny farve · Spring i farve · Spil 1 · Spil 2 · Spil 3 · Spil 4 · Spil 5
- `viden/kampen-om-kontrakten.html`: Svar på Landy 2♣ (×2) · Træn emnerne → · Vær opmærksom på zonestillingen (se §2). · Meld på fordeling, ikke honnørpoint. · Spring i ny farve · se afgrænsning nedenfor · Spring i makkers farve er svagt (6-9). · Spring i ny farve er udgangskrav. · Bemærk · Spring betyder · Spring er derfor konstruktive: · hold, op til 12-13
