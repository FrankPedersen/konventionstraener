"""
Moderne støtter – Kampen om kontrakten §5. Direkte støtter viser 6–9 og adskiller sig kun på antal trumfer.

  def   §5.1 – makker har meldt ind: enkeltstøtte 3 trumf · springstøtte 4 trumf · 4 i major 5 trumf, 0–9 (aftale) ·
               overmelding i fjendens farve 10+ med 3+ støtte · 1NT 8–11 med hold · ny farve 5+ 8–14, ikke krav ·
               støtte går forud for 1NT (aftale)
  off   §5.2 – makker har åbnet 1♥/1♠, modparten meldt ind på 2-trinnet: 2M 3 trumf · 3M 4 trumf · 4M 5 trumf (alle 6–9) ·
               overmelding 10+ med støtte · ny farve på 2-trinnet 10+ · negativ dobling 4 i umeldt major, 8+ ·
               2NT naturlig invit 10–12 med hold. Turnering (Stenberg): 2NT = 4-korts støtte og udgangskrav (13+),
               overmeldingen bliver præcis invit 10–12
  minor §5.4 – 1♣ (1♥) / 1♦ (1♠): én trumf mere end i major · majoren vises først (negativ dobling / 1♠) ·
               1NT 6–10 med hold · 2NT 10–12 med hold · overmelding 10+ med minorstøtte
  od    §5.3 – 1♥/1♠ (X): 2M 3 trumf · 3M 4 trumf · 4M 5 trumf (6–9) · 2NT 4 trumf 10+ · XX 10+ med højst
               3 trumf (aftale for præcis 3) · 1♠ firfarve, rundekrav · 2♣/2♦ konstruktiv seksfarve 5–9 (aftale)
Antagelser: makkers indmelding er en femfarve, åbningen i major en femfarve; »hold« = es, K-x, D-x-x eller B-x-x-x;
hænder, hvor skemaet ikke giver én melding, er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, tx
from .kamp import build_pool as kbuild
from .lebensohl import stopper

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
K = lambda c: (0, 0) if c in ("Pas", "X", "XX") else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))
AFT = {"aftale": True}

def sp_of(hand, hp, M):
    L = lengths_of(hand)
    sc = {0: 5, 1: 3, 2: 1} if L[M] >= 4 else {0: 3, 1: 2, 2: 1}
    return hp + sum(sc.get(L[s], 0) for s in SUITS if s != M)

def cheapest(after, s):
    for lv in (1, 2, 3, 4):
        if (lv, ORDER.index(s)) > K(after):
            return f"{lv}{SUIT_SYM[s]}"

# ---------------- §5.1 defensiven ----------------
C_DEF = tx("Firkortstøtte og 6–9 – spærrende", "Four-card support and 6–9 – preemptive")
BONUS_DEF = {"q": tx("Hvad viser et spring i makkers indmeldte farve?", "What does a jump in partner's overcalled suit show?"),
             "correct": C_DEF,
             "options": [C_DEF, tx("Invit, 10–12", "Invitational, 10–12"), tx("Udgangskrav", "Game forcing")],
             "why": tx("Direkte støtter viser alle 6–9 og adskiller sig kun på antal trumfer. Stærkere hænder går via fjendens farve. Spring i ny farve er derimod udgangskrav.",
                       "Direct raises all show 6–9 and differ only in the number of trumps. Stronger hands go via the opponents' suit. "
                       "A jump in a new suit, on the other hand, is game forcing.")}

def defense(O, M):
    sym, osym = SUIT_SYM[M], SUIT_SYM[O]
    def classify(hand, hp, zone):
        L = lengths_of(hand)
        n = L[M]
        if hp > 14:
            return None
        if n >= 3 and hp >= 10:
            return f"2{osym}", tx(f"{n} {SUIT_NAME[M]} og {hp} hp: overmelding i fjendens farve – støtte og 10+.",
                                  f"{n} {SUIT_NAME_EN[M]} and {hp} HCP: a cue-bid in the opponents' suit – support and 10+.")
        if n >= 5:
            if hp <= 5:
                return f"4{sym}", tx(f"5 trumf og kun {hp} hp: 4{sym} – direkte udgang er destruktiv (0–9).",
                                     f"5 trumps and only {hp} HCP: 4{sym} – a direct game bid is preemptive (0–9)."), AFT
            return f"4{sym}", tx(f"5 trumf og {hp} hp: 4{sym} – direkte udgang er destruktiv, aldrig konstruktiv.",
                                 f"5 trumps and {hp} HCP: 4{sym} – a direct game bid is preemptive, never constructive.")
        if n == 4 and 6 <= hp <= 9:
            c = cheapest(f"1{sym}", M)
            j = f"{int(c[0]) + 1}{sym}"
            return j, tx(f"4 trumf og {hp} hp: springstøtte {j} – 6–9 med fire trumf.",
                         f"4 trumps and {hp} HCP: the jump raise {j} – 6–9 with four trumps.")
        if n == 3 and 6 <= hp <= 9:
            c = cheapest(f"1{sym}", M)
            if 8 <= hp and stopper(hand, O):
                return c, tx(f"3 trumf og {hp} hp: {c} – støtten går forud for 1NT (fit før sansforbedring).",
                             f"3 trumps and {hp} HCP: {c} – support comes before 1NT (fit before improving to notrump)."), AFT
            return c, tx(f"3 trumf og {hp} hp: {c} – enkeltstøtte, 6–9.", f"3 trumps and {hp} HCP: {c} – a simple raise, 6–9.")
        if n >= 3 and hp < 6:
            return ("Pas", tx(f"Kun {hp} hp: pas.", f"Only {hp} HCP: pass.")) if n <= 4 else None
        if n <= 2:
            if 8 <= hp <= 11 and stopper(hand, O) and max(L.values()) <= 4:
                return "1NT", tx(f"{hp} hp og hold i {SUIT_NAME[O]}: 1NT – forbedring af kontrakten (8–11).",
                                 f"{hp} HCP and a stopper in {SUIT_NAME_EN[O]}: 1NT – improving the contract (8–11).")
            own = [s for s in ORDER if s not in (O, M) and L[s] >= 5]
            if own and 8 <= hp <= 14:
                s = own[0]
                c = cheapest(f"1{sym}", s)
                return c, tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: {c} – ny farve, ikke krav.",
                             f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: {c} – a new suit, non-forcing.")
            if hp < 8 and max(L.values()) <= 4:
                return "Pas", tx(f"{hp} hp uden støtte og uden farve: pas.", f"{hp} HCP without support and without a suit: pass.")
        return None
    return classify

# ---------------- §5.2 offensiven ----------------
C_OFF = tx("Firkortstøtte, 6–9", "Four-card support, 6–9")
BONUS_OFF = {"q": tx("Hvad viser 3 i makkers major efter en indmelding?", "What does three of partner's major show after an overcall?"),
             "correct": C_OFF,
             "options": [C_OFF, tx("Invit, 10–12", "Invitational, 10–12"), tx("Femkortstøtte, spærrende", "Five-card support, preemptive")],
             "why": tx("Efter indmeldingen viser 2M tre trumf, 3M fire og 4M fem – alle 6–9. Med 10+ og støtte meldes fjendens farve.",
                       "After the overcall, 2M shows three trumps, 3M four and 4M five – all 6–9. With 10+ and support, bid the opponents' suit.")}

def offense(M, O, ov):
    sym, osym = SUIT_SYM[M], SUIT_SYM[O]
    om = 'S' if M == 'H' else 'H'
    def classify(hand, hp, zone):
        L = lengths_of(hand)
        n = L[M]
        if hp > 16:
            return None
        if n >= 4 and hp >= 13:
            return (f"3{osym}", tx(f"{n} trumf og {hp} hp: overmelding i fjendens farve – støtte og 10+.",
                                   f"{n} trumps and {hp} HCP: a cue-bid in the opponents' suit – support and 10+."),
                    {"turnering": {"correct": "2NT", "why": tx(f"{n} trumf og {hp} hp: 2NT – Stenberg, firkortstøtte og udgangskrav.",
                                                               f"{n} trumps and {hp} HCP: 2NT – Stenberg, four-card support and game forcing.")}})
        if n >= 3 and 10 <= hp <= 12:
            return f"3{osym}", tx(f"{n} trumf og {hp} hp: overmelding i fjendens farve – støtte og 10+ (i Turnering præcis invit 10–12).",
                                  f"{n} trumps and {hp} HCP: a cue-bid in the opponents' suit – support and 10+ (in Tournament exactly invitational, 10–12).")
        if n == 3 and hp >= 13:
            return (f"3{osym}", tx(f"3 trumf og {hp} hp: overmelding i fjendens farve – støtte og 10+.",
                                   f"3 trumps and {hp} HCP: a cue-bid in the opponents' suit – support and 10+."),
                    {"only": ["grund", "klub"]})   # med Stenberg er overmeldingen præcis 10–12
        if 6 <= hp <= 9 and n >= 3:
            c = {3: f"2{sym}", 4: f"3{sym}"}.get(n, f"4{sym}")
            return c, tx(f"{n} trumf og {hp} hp: {c} – støtten viser antallet af trumf (6–9).",
                         f"{n} trumps and {hp} HCP: {c} – the raise shows the number of trumps (6–9).")
        if n <= 2:
            if L[om] == 4 and hp >= 8:
                return "X", tx(f"4 {SUIT_NAME[om]} og {hp} hp: negativ dobling.", f"4 {SUIT_NAME_EN[om]} and {hp} HCP: negative double.")
            if L[om] >= 4:
                return None
            if 10 <= hp <= 12 and stopper(hand, O) and max(L.values()) <= 4:
                return ("2NT", tx(f"{hp} hp og hold i {SUIT_NAME[O]}: 2NT – naturlig invit.",
                                  f"{hp} HCP and a stopper in {SUIT_NAME_EN[O]}: 2NT – a natural invitation."), {"only": ["grund", "klub"]})
            own = [s for s in ORDER if s not in (O, M) and L[s] >= 5 and (2, ORDER.index(s)) > K(ov)]
            if own and hp >= 10:
                s = own[0]
                return f"2{SUIT_SYM[s]}", tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: ny farve på 2-trinnet – 10+.",
                                             f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: a new suit at the two level – 10+.")
            if hp < 6:
                return "Pas", tx(f"{hp} hp: pas.", f"{hp} HCP: pass.")
        return None
    return classify

# ---------------- §5.4 minor ----------------
C_MIN = tx("Makker har normalt fire kort i minor, men fem i major", "Partner normally has four cards in a minor, but five in a major")
BONUS_MIN = {"q": tx("Hvorfor kræver minorstøtte én trumf mere?", "Why does minor-suit support need one more trump?"),
             "correct": C_MIN,
             "options": [C_MIN, tx("Minor giver færre point", "A minor scores fewer points"),
                         tx("Fordi majoren skal vises bagefter", "Because the major must be shown afterwards")],
             "why": tx("Én trumf mere end i major på hvert trin. Og majoren vises altid før minorstøtten – med negativ dobling eller farven på 1-trinnet.",
                       "One more trump than in a major at every level. And the major is always shown before the minor support – "
                       "with a negative double or the suit at the one level.")}

def minor(m, O):
    msym, osym = SUIT_SYM[m], SUIT_SYM[O]
    um = 'S' if O == 'H' else 'H'
    def classify(hand, hp, zone):
        L = lengths_of(hand)
        if hp > 14 or L[O] >= 4:
            return None
        if hp >= 6 and L[um] >= 4:
            if um == 'S':
                if L['S'] >= 5:
                    return "1♠", tx(f"{L['S']} spar og {hp} hp: 1♠ – femfarven meldes naturligt.",
                                    f"{L['S']} spades and {hp} HCP: 1♠ – the five-card suit is bid naturally.")
                return "X", tx(f"Præcis fire spar og {hp} hp: negativ dobling.", f"Exactly four spades and {hp} HCP: negative double.")
            return ("X", tx(f"{L['H']} hjerter og {hp} hp: negativ dobling – efter 1♦ (1♠) lover den fire eller flere hjerter.",
                            f"{L['H']} hearts and {hp} HCP: negative double – after 1♦ (1♠) it promises four or more hearts."),
                    AFT) if L['H'] >= 4 else None
        if L[um] >= 4:
            return None
        n = L[m]
        if n >= 4:
            if hp >= 10:
                return f"2{osym}", tx(f"{n} {SUIT_NAME[m]} og {hp} hp: overmelding i fjendens farve – minorstøtte og 10+.",
                                      f"{n} {SUIT_NAME_EN[m]} and {hp} HCP: a cue-bid in the opponents' suit – minor-suit support and 10+.")
            if 6 <= hp <= 9:
                c = f"2{msym}" if n == 4 else f"3{msym}"
                return c, tx(f"{n} {SUIT_NAME[m]} og {hp} hp: {c} – {'firkortstøtte' if n == 4 else 'femkortstøtte'} (én trumf mere end i major).",
                             f"{n} {SUIT_NAME_EN[m]} and {hp} HCP: {c} – {'four-card support' if n == 4 else 'five-card support'} (one more trump than in a major).")
        if stopper(hand, O) and max(L.values()) <= 4 and n <= 3:
            if 6 <= hp <= 9:
                return "1NT", tx(f"{hp} hp og hold i {SUIT_NAME[O]}: 1NT.", f"{hp} HCP and a stopper in {SUIT_NAME_EN[O]}: 1NT.")
            if 10 <= hp <= 12:
                return "2NT", tx(f"{hp} hp og hold i {SUIT_NAME[O]}: 2NT – invit.", f"{hp} HCP and a stopper in {SUIT_NAME_EN[O]}: 2NT – invitational.")
        if hp < 6 and n <= 3:
            return "Pas", tx(f"{hp} hp: pas.", f"{hp} HCP: pass.")
        return None
    return classify

# ---------------- §5.3 efter oplysningsdobling ----------------
C_OD = tx("10+ hp uden firkortstøtte", "10+ HCP without four-card support")
BONUS_OD = {"q": tx("Hvad viser redobling efter modpartens oplysningsdobling?", "What does a redouble after the opponents' takeout double show?"),
            "correct": C_OD,
            "options": [C_OD, tx("Svag hånd, flugt", "A weak hand, rescue"), tx("Firkortstøtte og udgangskrav", "Four-card support and game forcing")],
            "why": tx("XX = 10+ med højst trekortstøtte. Med firkortstøtte og 10+ meldes 2NT. Direkte støtter viser 6–9 og antallet af trumf.",
                      "XX = 10+ with at most three-card support. With four-card support and 10+, bid 2NT. "
                      "Direct raises show 6–9 and the number of trumps.")}

def after_od(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp, zone):
        L = lengths_of(hand)
        n = L[M]
        if hp > 15:
            return None
        if n >= 4 and hp >= 10:
            return "2NT", tx(f"{n} trumf og {hp} hp: 2NT – firkortstøtte og mindst 10.", f"{n} trumps and {hp} HCP: 2NT – four-card support and at least 10.")
        if hp >= 10:
            if n == 3:
                return "XX", tx(f"3 trumf og {hp} hp: redobling – 10+ med højst trekortstøtte.",
                                f"3 trumps and {hp} HCP: redouble – 10+ with at most three-card support."), AFT
            return "XX", tx(f"{hp} hp uden støtte: redobling – 10+, ofte interesseret i at straffe.",
                            f"{hp} HCP without support: redouble – 10+, often interested in a penalty.")
        if 6 <= hp <= 9 and n >= 3:
            c = {3: f"2{sym}", 4: f"3{sym}"}.get(n, f"4{sym}")
            return c, tx(f"{n} trumf og {hp} hp: {c} – støtten viser antallet af trumf.", f"{n} trumps and {hp} HCP: {c} – the raise shows the number of trumps.")
        if n <= 2:
            if M == 'H' and L['S'] >= 4 and hp >= 6:
                return "1♠", tx(f"{L['S']} spar og {hp} hp: 1♠ – naturligt rundekrav.", f"{L['S']} spades and {hp} HCP: 1♠ – natural and forcing.")
            six = [s for s in ('C', 'D') if L[s] >= 6]
            if six and 5 <= hp <= 9 and L['S'] < 4:
                s = six[0]
                return f"2{SUIT_SYM[s]}", tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: 2{SUIT_SYM[s]} – konstruktiv, ikke krav.",
                                             f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: 2{SUIT_SYM[s]} – constructive, non-forcing."), AFT
            if hp <= 5 and max(L.values()) <= 5:
                return "Pas", tx(f"{hp} hp: pas.", f"{hp} HCP: pass.")
        return None
    return classify

def build(kind):
    SIT, CL, SAM, PER = {}, {}, {}, {}
    t = lambda hp, **b: tpl(hp, **{**{s: (1, 4) for s in SUITS}, **b})
    if kind == "def":
        for O, M, key in (('C', 'H', 'kl_hj'), ('D', 'S', 'ru_sp'), ('C', 'S', 'kl_sp')):
            sk = f"def_{key}"
            sym, osym = SUIT_SYM[M], SUIT_SYM[O]
            calls = {"Pas", "1NT", f"2{osym}", f"2{sym}", f"3{sym}", f"4{sym}"} | {cheapest(f"1{sym}", s) for s in ORDER if s not in (O, M)}
            SIT[sk] = {"rolle": "Fortsætter", "auction": [["Modstander", f"1{osym}"], ["Makker", f"1{sym}"], PAS],
                       "calls": sorted(calls, key=K), "bonus": BONUS_DEF}
            CL[sk] = defense(O, M)
            others = [s for s in ORDER if s not in (O, M)]
            SAM[sk] = {f"2{sym}": t((6, 9), **{M: (3, 3), O: (1, 3)}), f"3{sym}": t((6, 9), **{M: (4, 4)}),
                       f"4{sym}": either(t((2, 9), **{M: (5, 5), O: (0, 2)}), t((0, 5), **{M: (5, 6)})),
                       f"2{osym}": t((10, 14), **{M: (3, 4)}), "1NT": t((8, 11), **{M: (1, 2), O: (3, 4)}),
                       "Pas": t((0, 5), **{M: (2, 4)})}
            for s in others:
                SAM[sk][cheapest(f"1{sym}", s)] = t((8, 13), **{M: (0, 2), s: (5, 6), O: (1, 3)})
            PER[sk] = 6
    if kind == "off":
        for M, O, ov, key in (('H', 'C', "2♣", 'hj_kl'), ('S', 'D', "2♦", 'sp_ru')):
            sk = f"off_{key}"
            sym, osym = SUIT_SYM[M], SUIT_SYM[O]
            om = 'S' if M == 'H' else 'H'
            calls = ["Pas", "X", "2♦", "2♥", "2♠", "2NT", f"3{osym}", f"3{sym}", f"4{sym}"]
            SIT[sk] = {"rolle": "Svarer", "auction": [["Makker", f"1{sym}"], ["Modstander", ov]], "allowX": True,
                       "calls": sorted(dict.fromkeys(c for c in calls if c in ("Pas", "X") or K(c) > K(ov)), key=K), "bonus": BONUS_OFF}
            CL[sk] = offense(M, O, ov)
            SAM[sk] = {f"2{sym}": t((6, 9), **{M: (3, 3), om: (0, 3)}), f"3{sym}": t((6, 9), **{M: (4, 4), om: (0, 3)}),
                       f"4{sym}": t((6, 9), **{M: (5, 5), om: (0, 3)}), f"3{osym}": t((10, 16), **{M: (3, 4), om: (0, 3)}),
                       "X": t((8, 12), **{M: (0, 2), om: (4, 4)}), "2NT": t((10, 12), **{M: (1, 2), om: (2, 3), O: (2, 4)}),
                       "Pas": t((0, 5), **{M: (0, 2), om: (0, 3)})}
            for s in ORDER:
                if s not in (O, M, om) and (2, ORDER.index(s)) > K(ov):
                    SAM[sk][f"2{SUIT_SYM[s]}"] = t((10, 14), **{M: (0, 2), om: (0, 3), s: (5, 6)})
            PER[sk] = 7
    if kind == "minor":
        for m, O, key in (('C', 'H', 'kl_hj'), ('D', 'S', 'ru_sp')):
            sk = f"min_{key}"
            msym, osym = SUIT_SYM[m], SUIT_SYM[O]
            um = 'S' if O == 'H' else 'H'
            calls = ["Pas", "X", "1NT", f"2{msym}", f"3{msym}", "2NT", f"2{osym}"] + (["1♠"] if O == 'H' else ["2♥"])
            SIT[sk] = {"rolle": "Svarer", "auction": [["Makker", f"1{msym}"], ["Modstander", f"1{osym}"]], "allowX": True,
                       "calls": sorted(calls, key=K), "bonus": BONUS_MIN}
            CL[sk] = minor(m, O)
            SAM[sk] = {"X": t((6, 12), **{um: (4, 4), O: (0, 3)}), f"2{msym}": t((6, 9), **{m: (4, 4), um: (0, 3), O: (0, 3)}),
                       f"3{msym}": t((6, 9), **{m: (5, 5), um: (0, 3), O: (0, 2)}), f"2{osym}": t((10, 14), **{m: (4, 5), um: (0, 3), O: (0, 3)}),
                       "1NT": t((6, 9), **{m: (2, 3), um: (2, 3), O: (3, 3)}), "2NT": t((10, 12), **{m: (2, 3), um: (2, 3), O: (3, 3)}),
                       "Pas": t((0, 5), **{um: (0, 3), O: (0, 3)})}
            if O == 'H':
                SAM[sk]["1♠"] = t((6, 12), S=(5, 6), H=(0, 3))
            PER[sk] = 7
    if kind == "od":
        for M, key in (('H', 'hj'), ('S', 'sp')):
            sk = f"od_{key}"
            sym = SUIT_SYM[M]
            calls = ["Pas", "XX"] + (["1♠"] if M == 'H' else []) + ["2♣", "2♦", f"2{sym}", "2NT", f"3{sym}", f"4{sym}"]
            SIT[sk] = {"rolle": "Svarer", "auction": [["Makker", f"1{sym}"], ["Modstander", "X"]], "allowXX": True,
                       "calls": sorted(calls, key=K), "bonus": BONUS_OD}
            CL[sk] = after_od(M)
            SAM[sk] = {f"2{sym}": t((6, 9), **{M: (3, 3)}), f"3{sym}": t((6, 9), **{M: (4, 4)}), f"4{sym}": t((6, 9), **{M: (5, 5)}),
                       "2NT": t((10, 14), **{M: (4, 5)}), "XX": either(t((10, 14), **{M: (0, 2)}), t((10, 14), **{M: (3, 3)})),
                       "2♣": t((5, 9), **{M: (0, 2), 'C': (6, 7), 'S': (0, 3)}), "2♦": t((5, 9), **{M: (0, 2), 'D': (6, 7), 'S': (0, 3)}),
                       "Pas": t((0, 5), **{M: (0, 2), **{s: (2, 5) for s in SUITS if s != M}})}
            if M == 'H':
                SAM[sk]["1♠"] = t((6, 9), H=(0, 2), S=(4, 5))
            PER[sk] = 7
    return SIT, CL, SAM, PER

def exporter(kind):
    return lambda path: kbuild(path, *build(kind))
