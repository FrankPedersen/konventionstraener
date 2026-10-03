"""
Lebensohl mod svag 2 – Makker 2 & mig, bilag C4, udvidet efter Jyderup Bridgeklubs Lebensohl-ark.

Modparten åbner svag 2♥/2♠, makker dobler, næste mand passer.
  svar_*   – svarer: farve højere end deres (billigst) = naturligt og svagt (0–7) · 2NT relæ = svag hånd (0–7)
             med en farve lavere end deres – eller, over 2♥, invit (8–11) med 5+ spar · farve lavere end deres
             direkte på 3-trinnet = invit (8–11) · 3♠ direkte over 2♥ = udgangskrav med 5+ spar ·
             3NT = naturligt med hold i deres farve og ingen 4-korts major at vise
  dobler_* – dobler efter svarers 2NT: 3♣ med en normal dobling; andet end 3♣ viser ekstra styrke (udgangskrav)
  relae_*  – svarer efter 2NT – 3♣: pas med klør, 3♦/3♥ = svag med farven, 3♠ (over 2♥) = invit med 5+ spar
Antagelser: farven er svarers længste (4+) og entydig; 3NT og 3♠ direkte kræver 12+ hp; invit og udgangskrav
med spar kræver 5+ spar; 8+ hænder med kun 4 spar og 12+ hænder med en lavere farve uden hold er ikke med
(hverken skemaet eller arket siger hvad). Doblers stærke meldinger trænes ikke – arket siger ikke hvilke;
dobler-hænderne holdes på 12–16 hp.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from .lebensohl import stopper

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
BONUS = {"q": "Hvad viser 2NT, når makker har doblet deres svage 2?",
         "correct": "Relæ – svag hånd med en farve lavere end deres",
         "options": ["Relæ – svag hånd med en farve lavere end deres", "Naturligt, 11–12 hp med hold", "Begge minorer"],
         "why": "2NT er relæ: dobler melder 3♣, og svarer passer eller retter til sin farve – stadig svagt. Samme farve direkte på 3-trinnet viser invit (8–11)."}
BONUS_HJ = {"q": "Hvad viser 3♠ direkte, når makker har doblet deres svage 2♥?",
            "correct": "Udgangskrav med 5+ spar",
            "options": ["Udgangskrav med 5+ spar", "Invit med 5+ spar (8–11 hp)", "Svag hånd med spar"],
            "why": "3♠ direkte er udgangskrav. Med invit går du via 2NT og melder 3♠ efter makkers 3♣; med en svag hånd melder du bare 2♠."}

def long_suit(L, X):
    """Svarers længste farve uden for deres (4+), eller None, hvis den ikke er entydig."""
    cand = [s for s in ORDER if s != X and L[s] >= 4]
    if not cand:
        return None
    top = max(L[s] for s in cand)
    longest = [s for s in cand if L[s] == top]
    return longest[0] if len(longest) == 1 else None

def advance(X):
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 16:
            return None
        s = long_suit(L, X)
        if hp >= 12:
            if X == 'H' and s == 'S' and L['S'] >= 5:
                return "3♠", f"{hp} hp og {L['S']} spar: 3♠ direkte er udgangskrav. Invit ville gå via 2NT-relæet."
            if stopper(hand, X) and not any(L[m] >= 4 for m in ('H', 'S') if m != X):
                return "3NT", f"{hp} hp og hold i {SUIT_NAME[X]}: 3NT – naturligt."
            return None
        if not s:
            return None
        ss = SUIT_SYM[s]
        if ORDER.index(s) > ORDER.index(X):
            if hp <= 7:
                return f"2{ss}", f"Svag hånd ({hp} hp) med {L[s]} {SUIT_NAME[s]} – højere end deres: 2{ss}, naturligt."
            if L[s] >= 5:
                return "2NT", (f"{hp} hp og {L[s]} {SUIT_NAME[s]} – invit med en farve højere end deres: 2NT relæ først. "
                               f"Makker melder 3♣, og du melder 3{ss} (invit). 3{ss} direkte ville være udgangskrav.")
            return None
        if hp <= 7:
            return "2NT", (f"Svag hånd ({hp} hp) med {L[s]} {SUIT_NAME[s]} – lavere end deres farve: 2NT relæ. "
                           + ("Makker melder 3♣, og du passer." if s == 'C' else f"Makker melder 3♣, og du retter til 3{ss}."))
        return f"3{ss}", f"{hp} hp og {L[s]} {SUIT_NAME[s]}: 3{ss} direkte – invit (8–11)."
    return classify

def doubler(X):
    after = "passer, retter til sin farve eller melder 3♠ som invit" if X == 'H' else "passer eller retter til sin farve"
    def classify(hand, hp):
        return "3♣", (f"Makkers 2NT er relæ: med en normal dobling ({hp} hp) melder du 3♣. Makker {after}. "
                      "Andet end 3♣ ville vise ekstra styrke og være udgangskrav.")
    return classify

def relay(X):
    first = advance(X)
    def classify(hand, hp):
        res = first(hand, hp)
        if not res or res[0] != "2NT":
            return None
        L = lengths_of(hand)
        s = long_suit(L, X)
        ss = SUIT_SYM[s]
        if hp >= 8:
            return f"3{ss}", f"{hp} hp og {L[s]} {SUIT_NAME[s]}: 3{ss} efter relæet er invit (8–11). 3{ss} direkte ville have været udgangskrav."
        if s == 'C':
            return "Pas", f"Svag hånd ({hp} hp) med {L[s]} klør: 2NT var relæ, og makker har meldt din farve – du passer."
        return f"3{ss}", f"Svag hånd ({hp} hp) med {L[s]} {SUIT_NAME[s]}: du retter til 3{ss} – stadig svagt."
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for X, key in (('H', 'hj'), ('S', 'sp')):
    xs = SUIT_SYM[X]
    bonus = BONUS_HJ if X == 'H' else BONUS
    one = lambda hp, s, X=X: tpl(hp, **{x: (5, 6) if x == s else ((1, 3) if x != X else (2, 3)) for x in SUITS})

    sk = f"svar_{key}"
    above = [f"2{SUIT_SYM[s]}" for s in ORDER if ORDER.index(s) > ORDER.index(X)]
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Modstander", f"2{xs}"], ["Makker", "X"], PAS],
                      "calls": above + ["2NT", "3♣", "3♦", "3♥", "3♠", "3NT"], "bonus": bonus}
    CLASSIFIERS[sk] = advance(X)
    SAMPLERS[sk] = {"2NT": either(one((0, 7), 'C'), one((0, 7), 'D'),
                                  *([one((0, 7), 'H')] if X == 'S' else [one((8, 11), 'S')])),
                    "3♣": one((8, 11), 'C'), "3♦": one((8, 11), 'D'),
                    "3NT": tpl((12, 16), **{x: (2, 4) if x != X else (3, 4) for x in SUITS})}
    if X == 'S':
        SAMPLERS[sk]["3♥"] = one((8, 11), 'H')
    else:
        SAMPLERS[sk]["2♠"] = one((0, 7), 'S')
        SAMPLERS[sk]["3♠"] = one((12, 16), 'S')
    PER_CALL[sk] = 16

    sk = f"dobler_{key}"
    SITUATIONS[sk] = {"rolle": "Dobler", "auction": [["Modstander", f"2{xs}"], ["Dig", "X"], PAS, ["Makker", "2NT"], PAS],
                      "calls": ["Pas", "3♣", "3♦", "3NT"] + (["3♥"] if X == 'S' else []), "bonus": bonus}
    CLASSIFIERS[sk] = doubler(X)
    SAMPLERS[sk] = {"3♣": tpl((12, 16), **{x: (3, 4) if x != X else (0, 2) for x in SUITS})}
    PER_CALL[sk] = 20

    sk = f"relae_{key}"
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Modstander", f"2{xs}"], ["Makker", "X"], PAS, ["Dig", "2NT"], PAS,
                                                      ["Makker", "3♣"], PAS],
                      "calls": ["Pas", "3♦", "3♥", "3♠", "3NT"], "bonus": bonus}
    CLASSIFIERS[sk] = relay(X)
    SAMPLERS[sk] = {"Pas": one((0, 7), 'C'), "3♦": one((0, 7), 'D')}
    if X == 'S':
        SAMPLERS[sk]["3♥"] = one((0, 7), 'H')
    else:
        SAMPLERS[sk]["3♠"] = one((8, 11), 'S')
    PER_CALL[sk] = 12

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
