"""
Lebensohl mod svag 2 (simpel udgave) – Makker 2 & mig, bilag C4.

Modparten åbner svag 2♥/2♠, makker dobler, næste mand passer.
  svar_*   – svarer: farve højere end deres (billigst) = naturligt og svagt · 2NT relæ = svag hånd (0–7)
             med en farve lavere end deres · farve lavere end deres direkte på 3-trinnet = invit (8–11) ·
             3NT = naturligt med hold i deres farve og ingen 4-korts major at vise
  dobler_* – dobler efter svarers 2NT: 3♣ – tvunget
Antagelser: farven er svarers længste (4+) og entydig; 3NT kræver 12+ hp; svag hånd med en højere
farve er 0–7 hp; invit med en højere farve og 12+ hænder uden hold er ikke med (skemaet siger ikke hvad).
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from .lebensohl import stopper

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
BONUS = {"q": "Hvad viser 2NT, når makker har doblet deres svage 2?",
         "correct": "Relæ – svag hånd med en farve lavere end deres",
         "options": ["Relæ – svag hånd med en farve lavere end deres", "Naturligt, 11–12 hp med hold", "Begge minorer"],
         "why": "2NT er relæ: dobler melder 3♣, og svarer passer eller retter til sin farve – stadig svagt. Samme farve direkte på 3-trinnet viser invit (8–11)."}

def advance(X):
    xs = SUIT_SYM[X]
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 16:
            return None
        if hp >= 12:
            if stopper(hand, X) and not any(L[s] >= 4 for s in ('H', 'S') if s != X):
                return "3NT", f"{hp} hp og hold i {SUIT_NAME[X]}: 3NT – naturligt."
            return None
        cand = [s for s in ORDER if s != X and L[s] >= 4]
        if not cand:
            return None
        top = max(L[s] for s in cand)
        longest = [s for s in cand if L[s] == top]
        if len(longest) > 1:
            return None
        s = longest[0]
        ss = SUIT_SYM[s]
        if ORDER.index(s) > ORDER.index(X):
            if hp <= 7:
                return f"2{ss}", f"Svag hånd ({hp} hp) med {L[s]} {SUIT_NAME[s]} – højere end deres: 2{ss}, naturligt."
            return None
        if hp <= 7:
            return "2NT", (f"Svag hånd ({hp} hp) med {L[s]} {SUIT_NAME[s]} – lavere end deres farve: 2NT relæ. "
                           f"Makker melder 3♣, og du passer eller retter til 3{ss}.")
        return f"3{ss}", f"{hp} hp og {L[s]} {SUIT_NAME[s]}: 3{ss} direkte – invit (8–11)."
    return classify

def doubler(hand, hp):
    return "3♣", "Makkers 2NT er relæ: du skal melde 3♣. Makker passer eller retter til sin farve."

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for X, key in (('H', 'hj'), ('S', 'sp')):
    xs = SUIT_SYM[X]
    sk = f"svar_{key}"
    above = [f"2{SUIT_SYM[s]}" for s in ORDER if ORDER.index(s) > ORDER.index(X)]
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Modstander", f"2{xs}"], ["Makker", "X"], PAS],
                      "calls": above + ["2NT", "3♣", "3♦"] + (["3♥"] if X == 'S' else []) + [f"3{xs}", "3NT"], "bonus": BONUS}
    CLASSIFIERS[sk] = advance(X)
    one = lambda hp, s, X=X: tpl(hp, **{x: (5, 6) if x == s else ((1, 3) if x != X else (2, 3)) for x in SUITS})
    SAMPLERS[sk] = {"2NT": either(one((0, 7), 'C'), one((0, 7), 'D'), *([one((0, 7), 'H')] if X == 'S' else [])),
                    "3♣": one((8, 11), 'C'), "3♦": one((8, 11), 'D'),
                    "3NT": tpl((12, 16), **{x: (2, 4) if x != X else (3, 4) for x in SUITS})}
    if X == 'S':
        SAMPLERS[sk]["3♥"] = one((8, 11), 'H')
    else:
        SAMPLERS[sk]["2♠"] = one((0, 7), 'S')
    PER_CALL[sk] = 16
    sk = f"dobler_{key}"
    SITUATIONS[sk] = {"rolle": "Dobler", "auction": [["Modstander", f"2{xs}"], ["Dig", "X"], PAS, ["Makker", "2NT"], PAS],
                      "calls": ["Pas", "3♣", "3♦", "3NT"] + (["3♥"] if X == 'S' else []), "bonus": BONUS}
    CLASSIFIERS[sk] = doubler
    SAMPLERS[sk] = {"3♣": tpl((12, 17), **{x: (3, 4) if x != X else (0, 2) for x in SUITS})}
    PER_CALL[sk] = 20

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
