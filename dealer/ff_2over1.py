"""
Two over One udgangskrav – Makker 2 & mig, afsnit 1 og 5.

  svar_* – svarer over makkers 1♥/1♠ uden 3 korts støtte:
           pas 0–5 · 1NT 6–12 (semikrav) · 1♠ over 1♥ med 4+ spar · 3NT over 1♠: 13–15 jævn med
           præcis 2 spar · ny farve på 2-trinnet: 13+ hp og udgangskrav, 5+ kort (klør 4+)
  aab_*  – åbner efter Two over One, uden 3 korts støtte til svarers farve:
           2M 6-farve 12–14 · 2NT jævn 12–14 · 3M god 6-farve 15+ · 3NT jævn 18–19 ·
           ny farve 15+ med 4 kort: 2♠ efter 1♥ – 2X, ellers en lavere farve på 3-trinnet
Antagelser: svarer vælger sin længste farve, ved 5-5 den højeste, og 4 klør kun uden en 5-farve;
jævne hænder med 13–15 over 1♥ og åbners 5-4 med minimum er ikke med (skemaet siger ikke hvad).
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
BONUS = {"q": "Hvad lover Two over One hos Makker 2 & mig?",
         "correct": "13+ hp og udgangskrav",
         "options": ["13+ hp og udgangskrav", "10+ hp, rundekrav", "11–12 hp, invit"],
         "why": "Ny farve på 2-trinnet fra en uforhåndspasset svarer er udgangskrav med 13+ hp (hos Makker 1 & mig er det 10+ og rundekrav)."}

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def responder(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] >= 3 or hp > 17:
            return None
        if hp < 6:
            return "Pas", f"{hp} hp: pas."
        if M == 'H' and L['S'] >= 4:
            return "1♠", f"{L['S']} spar: 1♠ – naturligt rundekrav, før Two over One."
        if hp <= 12:
            return "1NT", f"{hp} hp uden støtte: 1NT (6–12, semikrav)."
        if balanced(L) and L[M] == 2 and hp <= 15:
            if M == 'S':
                return "3NT", f"{hp} hp jævn med præcis 2 spar: 3NT (13–15) – slutmelding."
            return None
        cands = [s for s in ORDER if ORDER.index(s) < ORDER.index(M) and L[s] >= 5]
        if not cands:
            if L['C'] >= 4 and all(L[s] < 5 for s in SUITS):
                return "2♣", f"{hp} hp og {L['C']} klør: 2♣ – Two over One, udgangskrav (klør kan være 4)."
            return None
        top = max(L[s] for s in cands)
        s = max((x for x in cands if L[x] == top), key=ORDER.index)
        call = f"2{SUIT_SYM[s]}"
        return call, f"{hp} hp og {L[s]} {SUIT_NAME[s]}: {call} – Two over One, 13+ og udgangskrav."
    return classify

def opener(M, X):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or L[X] >= 3 or not (12 <= hp <= 19):
            return None
        if balanced(L):
            if hp <= 14:
                return "2NT", f"Jævn hånd, {hp} hp: 2NT (12–14)."
            if hp >= 18:
                return "3NT", f"Jævn hånd, {hp} hp: 3NT (18–19)."
            return None
        if L[M] >= 6:
            if hp <= 14:
                return f"2{sym}", f"{L[M]} {SUIT_NAME[M]} og {hp} hp: 2{sym} (12–14)."
            good = sum(1 for r in hand[M][:3] if r >= 12) >= 2
            return (f"3{sym}", f"God {L[M]}-farve og {hp} hp: 3{sym} (15+).") if good else None
        if hp < 15:
            return None
        if M == 'H' and L['S'] >= 4:
            return "2♠", f"4 spar ved siden af hjerterne og {hp} hp: 2♠ (15+)."
        lower = [s for s in ORDER if ORDER.index(s) < ORDER.index(X) and L[s] >= 4 and s != M]
        if len(lower) == 1:
            call = f"3{SUIT_SYM[lower[0]]}"
            return call, f"4 {SUIT_NAME[lower[0]]} og {hp} hp: ny farve på 3-trinnet, {call} (15+)."
        return None
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
key = lambda c: (0, 0) if c == "Pas" else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))
for M, mk in (('H', 'hj'), ('S', 'sp')):
    sym = SUIT_SYM[M]
    sk = f"svar_{mk}"
    lower = [s for s in ORDER if ORDER.index(s) < ORDER.index(M)]
    calls = ["Pas", "1NT", "2NT", "3NT"] + [f"2{SUIT_SYM[s]}" for s in lower] + (["1♠"] if M == 'H' else [])
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", f"1{sym}"], PAS], "calls": sorted(calls, key=key), "bonus": BONUS}
    CLASSIFIERS[sk] = responder(M)
    base = {M: (0, 2)}
    if M == 'H':
        base['S'] = (0, 3)
    t = lambda hp, **b: tpl(hp, **{**{s: (1, 5) for s in SUITS}, **base, **b})
    SAMPLERS[sk] = {"Pas": t((0, 5)), "1NT": t((6, 12))}
    for s in lower:
        SAMPLERS[sk][f"2{SUIT_SYM[s]}"] = t((13, 17), **{s: (5, 6)})
    if M == 'H':
        SAMPLERS[sk]["1♠"] = tpl((6, 15), H=(0, 2), S=(4, 5), D=(1, 5), C=(1, 5))
    else:
        SAMPLERS[sk]["3NT"] = tpl((13, 15), S=(2, 2), H=(3, 4), D=(3, 4), C=(3, 4))
    PER_CALL[sk] = 12
    for X in lower:
        xs = SUIT_SYM[X]
        sk = f"aab_{mk}_{X.lower()}"
        news = (["2♠"] if M == 'H' else []) + [f"3{SUIT_SYM[s]}" for s in ORDER if ORDER.index(s) < ORDER.index(X)]
        calls = sorted({f"2{sym}", "2NT", f"3{sym}", "3NT", *news}, key=key)
        SITUATIONS[sk] = {"rolle": "Åbner", "auction": [["Dig", f"1{sym}"], PAS, ["Makker", f"2{xs}"], PAS],
                          "calls": calls, "bonus": BONUS}
        CLASSIFIERS[sk] = opener(M, X)
        rest = [s for s in SUITS if s not in (M, X)]
        o = lambda hp, n, M=M, X=X, rest=rest, **b: tpl(hp, **{M: (n, n), X: (1, 2), **{s: (1, 4) for s in rest}, **b})
        SAMPLERS[sk] = {f"2{sym}": o((12, 14), 6), "2NT": o((12, 14), 5, **{X: (2, 2)}), f"3{sym}": o((15, 18), 6),
                        "3NT": o((18, 19), 5, **{X: (2, 2)})}
        for c in news:
            s = {'♠': 'S', '♣': 'C', '♦': 'D'}[c[1]]
            SAMPLERS[sk][c] = o((15, 18), 5, **{s: (4, 4)})
        PER_CALL[sk] = 6

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
