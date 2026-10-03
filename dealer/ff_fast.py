"""
Fast og slow arrival – Makker 2 & mig, afsnit 5b.

I et udgangskrævende forløb betyder hurtig udgang minimum og langsom ankomst tillæg.
  svar_* – svarer efter 1M – 2X (Two over One) – 2M med 3 korts støtte:
           4M direkte = minimum (13–14 hp) · 3M = ekstra værdier (15–16 hp)
  aab_*  – åbner efter 1♠ – 2X – 2♥ – 3♥ (svarer støtter langsomt):
           4♥ = minimum (12–14 hp) · cuebid = tillæg (15+) og kontrol i farven, billigste først
Antagelser: kontrol = es, konge, singleton eller renonce; åbner cuebidder i klør eller ruder (3♠ i
egen farve er ikke med); tillæg uden kontrol i klør og ruder er ikke med; svarer med 17+ (slem) er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

PAS = ["Modstander", "Pas"]
BONUS = {"q": "Hvad viser den hurtige udgang i et udgangskrævende forløb?",
         "correct": "Minimum – intet at tilføje",
         "options": ["Minimum – intet at tilføje", "Tillæg – stærkeste vej", "Slemambition"],
         "why": "Fast arrival: ingen af jer kan passe under udgang, så den hurtige udgang viser minimum. Den langsomme vej (3M, cuebid) viser tillæg."}

def control(cards):
    return len(cards) <= 1 or cards[0] >= 13

def responder(M, X):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] != 3 or not (13 <= hp <= 16) or L[X] < (4 if X == 'C' else 5):
            return None
        if hp <= 14:
            return f"4{sym}", f"Fit og {hp} hp – minimum for Two over One: 4{sym} direkte (fast arrival)."
        return f"3{sym}", f"Fit og {hp} hp – ekstra værdier: 3{sym} lader plads til cuebids (slow arrival)."
    return classify

def opener(X):
    def classify(hand, hp):
        L = lengths_of(hand)
        if L['S'] != 5 or L['H'] != 4 or not (12 <= hp <= 18):
            return None
        if hp <= 14:
            return "4♥", f"{hp} hp – minimum: 4♥ direkte (fast arrival)."
        for s, call in (('C', '4♣'), ('D', '4♦')):
            if control(hand[s]):
                w = "renonce" if not hand[s] else "singleton" if len(hand[s]) == 1 else "es" if hand[s][0] == 14 else "konge"
                return call, f"{hp} hp – tillæg: cuebid {call} viser kontrol ({w}) i {SUIT_NAME[s]} – billigste først."
        return None
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for M, X in (('S', 'D'), ('S', 'C'), ('H', 'C'), ('H', 'D')):
    sym, xs = SUIT_SYM[M], SUIT_SYM[X]
    sk = f"svar_{M.lower()}_{X.lower()}"
    SITUATIONS[sk] = {"rolle": "Svarer",
                      "auction": [["Makker", f"1{sym}"], PAS, ["Dig", f"2{xs}"], PAS, ["Makker", f"2{sym}"], PAS],
                      "calls": ["2NT", f"3{sym}", "3NT", f"4{sym}"], "bonus": BONUS}
    CLASSIFIERS[sk] = responder(M, X)
    other = [s for s in SUITS if s not in (M, X)]
    r = lambda hp, M=M, X=X, other=other: tpl(hp, **{M: (3, 3), X: (4, 6) if X == 'C' else (5, 6), other[0]: (1, 4), other[1]: (1, 4)})
    SAMPLERS[sk] = {f"4{sym}": r((13, 14)), f"3{sym}": r((15, 16))}
    PER_CALL[sk] = 12
for X in ('D', 'C'):
    xs = SUIT_SYM[X]
    sk = f"aab_{X.lower()}"
    SITUATIONS[sk] = {"rolle": "Åbner",
                      "auction": [["Dig", "1♠"], PAS, ["Makker", f"2{xs}"], PAS, ["Dig", "2♥"], PAS, ["Makker", "3♥"], PAS],
                      "calls": ["3♠", "3NT", "4♣", "4♦", "4♥"], "bonus": BONUS}
    CLASSIFIERS[sk] = opener(X)
    o = lambda hp, **b: tpl(hp, **{'S': (5, 5), 'H': (4, 4), 'D': (1, 3), 'C': (1, 3), **b})
    SAMPLERS[sk] = {"4♥": o((12, 14)), "4♣": o((15, 18)), "4♦": o((15, 18), C=(2, 3))}
    PER_CALL[sk] = 16

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
