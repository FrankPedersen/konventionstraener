"""
Lebensohl – Karina & Frank, systemkortets afsnit 8.2.

Modstanderen åbner en svag 2 (2♦/2♥/2♠), makker oplysningsdobler, og næste mand passer. Svarer:
  farve på 2-trinnet – naturligt og svagt, 0–8 hp
  2NT – relæ: svag hånd med en farve lavere end deres; dobler melder 3♣, svarer passer eller retter
  farve på 3-trinnet direkte – invit, ca. 9–12 hp
  3NT – naturligt med hold i deres farve
  cuebid i deres farve – udgangskrav, beder om 4-farve i major
Antagelser: 3NT og cuebid kræver 13+ hp; cuebid bruges med en 4-farve i umeldt major, 3NT uden;
hold = es, K-x, D-x-x eller B-x-x-x; farven er svarers længste (4+), og hænder med to lige lange
kandidater er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

ORDER = ['C', 'D', 'H', 'S']

def stopper(hand, s):
    cards, n = hand[s], len(hand[s])
    return 14 in cards or (13 in cards and n >= 2) or (12 in cards and n >= 3) or (11 in cards and n >= 4)

def advance(X):
    xs = SUIT_SYM[X]
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 17:
            return None
        if hp >= 13:
            majors = [s for s in ('H', 'S') if s != X and L[s] >= 4]
            st = stopper(hand, X)
            if majors and not st:
                return f"3{xs}", f"{hp} hp og 4 {SUIT_NAME[majors[0]]}: cuebid 3{xs} er udgangskrav og beder om 4-farve i major."
            if st and not majors:
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
        if hp >= 9:
            return f"3{ss}", f"{hp} hp og {L[s]} {SUIT_NAME[s]}: 3{ss} direkte er invit (9–12)."
        if ORDER.index(s) > ORDER.index(X):
            return f"2{ss}", f"Svag hånd ({hp} hp) med {L[s]} {SUIT_NAME[s]} – højere end deres farve: 2{ss}, naturligt og svagt."
        return "2NT", (f"Svag hånd ({hp} hp) med {L[s]} {SUIT_NAME[s]} – lavere end deres farve: 2NT relæ. "
                       f"Makker melder 3♣, og du passer eller retter til 3{ss}.")
    return classify

BONUS = {"q": "Hvad betyder 2NT, når makker har doblet deres svage 2?",
         "correct": "Relæ – svag hånd med en farve lavere end deres",
         "options": ["Relæ – svag hånd med en farve lavere end deres", "Naturligt, 11–12 hp med hold", "Begge minorer"],
         "why": "2NT er relæ: dobler melder 3♣, og svarer passer eller retter til sin farve. Samme farve meldt direkte på 3-trinnet viser invit."}

PAS = ["Modstander", "Pas"]
SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for X, key in (('D', 'ru'), ('H', 'hj'), ('S', 'sp')):
    xs = SUIT_SYM[X]
    sk = f"svar_{key}"
    above = [f"2{SUIT_SYM[s]}" for s in ORDER if ORDER.index(s) > ORDER.index(X)]
    three = [f"3{SUIT_SYM[s]}" for s in ORDER if s != X]
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Modstander", f"2{xs}"], ["Makker", "X"], PAS],
                      "calls": above + ["2NT"] + three + [f"3{xs}", "3NT"], "bonus": BONUS}
    CLASSIFIERS[sk] = advance(X)
    one = lambda hp, s: tpl(hp, **{x: (5, 6) if x == s else (1, 3) for x in SUITS})
    SAMPLERS[sk] = {}
    for s in ORDER:
        if s == X:
            continue
        ss = SUIT_SYM[s]
        weak = f"2{ss}" if ORDER.index(s) > ORDER.index(X) else "2NT"
        SAMPLERS[sk].setdefault(weak, [])
        SAMPLERS[sk][weak].append(lambda s=s: one((0, 8), s)())
        SAMPLERS[sk][f"3{ss}"] = lambda s=s: one((9, 12), s)()
    SAMPLERS[sk] = {c: (either(*v) if isinstance(v, list) else v) for c, v in SAMPLERS[sk].items()}
    others = [s for s in ('H', 'S') if s != X]
    SAMPLERS[sk][f"3{xs}"] = either(*[(lambda m=m: tpl((13, 16), **{x: (4, 4) if x == m else (2, 4) for x in SUITS})()) for m in others])
    SAMPLERS[sk]["3NT"] = tpl((13, 16), **{x: (2, 4) if x != X else (3, 4) for x in SUITS})
    PER_CALL[sk] = 9

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
