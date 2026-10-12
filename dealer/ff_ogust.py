"""
Ogust 2NT og svar på svag 2 – Makker 2 & mig, afsnit 12 og 13.

  aab_*  – åbner med svag 2 (6-farve, 5–11 hp) efter makkers 2NT:
           3♣ dårlig (5–7) med én af E-K-D · 3♦ dårlig med to · 3♥ god (8–11) med én · 3♠ god med to ·
           3NT god med alle tre
  svar_* – svarer over makkers svage 2♥/2♠:
           15+ med 2+ støtte: 2NT (Ogust) · 15+ med egen 6-farve og højst 1 i makkers: ny farve (rundekrav) ·
           under 15: 3 i farven med 3-korts støtte, 4 i farven med 4+ (Loven: 9 hhv. 10 trumf) · ellers pas
Antagelser: »god« = 8–11 hp; åbner har mindst én af de tre øverste; svarer med 15+ og 3–4 korts
støtte går via 2NT; svarerhænder med 15+ uden støtte og uden 6-farve er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
C_AAB = tx("Dårlig hånd (5–7) med to af de tre øverste", "A poor hand (5–7) with two of the top three honours")
C_SVAR = tx("Ogust – 15+ og udgangsinteresse, rundekrav", "Ogust – 15+ and game interest, forcing")
BONUS = {
    "aab": {"q": tx("Hvad viser 3♦ som svar på Ogust?", "What does 3♦ show in response to Ogust?"),
            "correct": C_AAB,
            "options": [C_AAB, tx("God hånd med én af de tre øverste", "A good hand with one of the top three honours"),
                        tx("Ruderfarve", "A diamond suit")],
            "why": tx("Huskeregel »mindste minorer, 1-2-1-2-3«: 3♣ dårlig/1 · 3♦ dårlig/2 · 3♥ god/1 · 3♠ god/2 · 3NT E-K-D.",
                      "Memory aid »1-2-1-2-3«: 3♣ poor/1 · 3♦ poor/2 · 3♥ good/1 · 3♠ good/2 · 3NT A-K-Q.")},
    "svar": {"q": tx("Hvad viser 2NT over makkers svage 2?", "What does 2NT over partner's weak two show?"),
             "correct": C_SVAR,
             "options": [C_SVAR, tx("Naturligt, 11–12 hp", "Natural, 11–12 HCP"), tx("Spærrende med støtte", "Preemptive with support")],
             "why": tx("2NT er Ogust: 15+ med udgangsinteresse. Med svag hånd og støtte spærrer man efter Loven: 3 i farven med 9 trumf, 4 med 10.",
                       "2NT is Ogust: 15+ with game interest. With a weak hand and support you preempt by the Law: "
                       "three of the suit with 9 trumps, four with 10.")},
}

def ogust(M):
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] != 6 or not (5 <= hp <= 11):
            return None
        tops = sum(1 for r in hand[M] if r >= 12)
        if tops == 0:
            return None
        good = hp >= 8
        call = (["3♥", "3♠", "3NT"] if good else ["3♣", "3♦", None])[tops - 1]
        if call is None:
            return None
        word = "God" if good else "Dårlig"
        word_en = "Good" if good else "Poor"
        return call, tx(f"{word} hånd ({hp} hp) med {tops} af de tre øverste honnører: {call}.",
                        f"{word_en} hand ({hp} HCP) with {tops} of the top three honours: {call}.")
    return classify

def responder(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 18:
            return None
        if hp >= 15:
            if L[M] >= 2:
                return "2NT", tx(f"{hp} hp og {L[M]} {SUIT_NAME[M]}: 2NT – Ogust.", f"{hp} HCP and {L[M]} {SUIT_NAME_EN[M]}: 2NT – Ogust.")
            own = [s for s in SUITS if s != M and L[s] >= 6]
            if own:
                s = own[0]
                lv = 2 if ORDER.index(s) > ORDER.index(M) else 3
                return f"{lv}{SUIT_SYM[s]}", tx(f"{hp} hp og egen {L[s]}-farve: {lv}{SUIT_SYM[s]} – ny farve er rundekrav.",
                                                f"{hp} HCP and your own {L[s]}-card suit: {lv}{SUIT_SYM[s]} – a new suit is forcing.")
            return None
        if L[M] >= 4:
            return f"4{sym}", tx(f"{L[M]} {SUIT_NAME[M]} = {L[M] + 6} trumf: 4{sym} efter Loven – spærrende.",
                                 f"{L[M]} {SUIT_NAME_EN[M]} = {L[M] + 6} trumps: 4{sym} by the Law – preemptive.")
        if L[M] == 3:
            return f"3{sym}", tx(f"3 {SUIT_NAME[M]} = 9 trumf: 3{sym} efter Loven – spærrende.",
                                 f"3 {SUIT_NAME_EN[M]} = 9 trumps: 3{sym} by the Law – preemptive.")
        return "Pas", tx(f"{hp} hp og ingen støtte: pas.", f"{hp} HCP and no support: pass.")
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for M, mk in (('D', 'ru'), ('H', 'hj'), ('S', 'sp')):
    sym = SUIT_SYM[M]
    sk = f"aab_{mk}"
    SITUATIONS[sk] = {"rolle": "Åbner", "auction": [["Dig", f"2{sym}"], PAS, ["Makker", "2NT"], PAS],
                      "calls": ["3♣", "3♦", "3♥", "3♠", "3NT"], "bonus": BONUS["aab"]}
    CLASSIFIERS[sk] = ogust(M)
    w = lambda hp, M=M: tpl(hp, **{**{s: (1, 3) for s in SUITS}, M: (6, 6)})
    SAMPLERS[sk] = {"3♣": w((5, 7)), "3♦": w((5, 7)), "3♥": w((8, 11)), "3♠": w((8, 11)), "3NT": w((9, 11))}
    PER_CALL[sk] = 7
    if M == 'D':
        continue
    sk = f"svar_{mk}"
    calls = sorted({"Pas", "2NT", f"3{sym}", f"4{sym}", "3♣", "3♦"} | ({"2♠"} if M == 'H' else {"3♥"}),
                   key=lambda c: (0, 0) if c == "Pas" else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:])))
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", f"2{sym}"], PAS], "calls": calls, "bonus": BONUS["svar"]}
    CLASSIFIERS[sk] = responder(M)
    r = lambda hp, M=M, **b: tpl(hp, **{**{s: (2, 4) for s in SUITS}, M: (0, 2), **b})
    SAMPLERS[sk] = {"Pas": r((0, 14)), f"3{sym}": r((3, 13), **{M: (3, 3)}), f"4{sym}": r((3, 13), **{M: (4, 5)}),
                    "2NT": r((15, 18), **{M: (2, 4)})}
    for s in ORDER:
        if s != M:
            lv = 2 if ORDER.index(s) > ORDER.index(M) else 3
            SAMPLERS[sk][f"{lv}{SUIT_SYM[s]}"] = r((15, 17), **{M: (0, 1), s: (6, 7)})
    PER_CALL[sk] = 7

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
