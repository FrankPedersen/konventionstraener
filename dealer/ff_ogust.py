"""
Ogust 2NT og svar på svag 2 – Flemming & Frank, afsnit 12 og 13.

  aab_*  – åbner med svag 2 (6-farve, 5–11 hp) efter makkers 2NT:
           3♣ dårlig (5–7) med én af E-K-D · 3♦ dårlig med to · 3♥ god (8–11) med én · 3♠ god med to ·
           3NT god med alle tre
  svar_* – svarer over makkers svage 2♥/2♠:
           15+ med 2+ støtte: 2NT (Ogust) · 15+ med egen 6-farve og højst 1 i makkers: ny farve (rundekrav) ·
           under 15: 3 i farven med 3-korts støtte, 4 i farven med 4+ (Loven: 9 hhv. 10 trumf) · ellers pas
Antagelser: »god« = 8–11 hp; åbner har mindst én af de tre øverste; svarer med 15+ og 3–4 korts
støtte går via 2NT; svarerhænder med 15+ uden støtte og uden 6-farve er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
BONUS = {
    "aab": {"q": "Hvad viser 3♦ som svar på Ogust?",
            "correct": "Dårlig hånd (5–7) med to af de tre øverste",
            "options": ["Dårlig hånd (5–7) med to af de tre øverste", "God hånd med én af de tre øverste", "Ruderfarve"],
            "why": "Huskeregel »mindste minorer, 1-2-1-2-3«: 3♣ dårlig/1 · 3♦ dårlig/2 · 3♥ god/1 · 3♠ god/2 · 3NT E-K-D."},
    "svar": {"q": "Hvad viser 2NT over makkers svage 2?",
             "correct": "Ogust – 15+ og udgangsinteresse, rundekrav",
             "options": ["Ogust – 15+ og udgangsinteresse, rundekrav", "Naturligt, 11–12 hp", "Spærrende med støtte"],
             "why": "2NT er Ogust: 15+ med udgangsinteresse. Med svag hånd og støtte spærrer man efter Loven: 3 i farven med 9 trumf, 4 med 10."},
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
        return call, f"{word} hånd ({hp} hp) med {tops} af de tre øverste honnører: {call}."
    return classify

def responder(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 18:
            return None
        if hp >= 15:
            if L[M] >= 2:
                return "2NT", f"{hp} hp og {L[M]} {SUIT_NAME[M]}: 2NT – Ogust."
            own = [s for s in SUITS if s != M and L[s] >= 6]
            if own:
                s = own[0]
                lv = 2 if ORDER.index(s) > ORDER.index(M) else 3
                return f"{lv}{SUIT_SYM[s]}", f"{hp} hp og egen {L[s]}-farve: {lv}{SUIT_SYM[s]} – ny farve er rundekrav."
            return None
        if L[M] >= 4:
            return f"4{sym}", f"{L[M]} {SUIT_NAME[M]} = {L[M] + 6} trumf: 4{sym} efter Loven – spærrende."
        if L[M] == 3:
            return f"3{sym}", f"3 {SUIT_NAME[M]} = 9 trumf: 3{sym} efter Loven – spærrende."
        return "Pas", f"{hp} hp og ingen støtte: pas."
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
