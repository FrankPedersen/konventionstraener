"""
Omvendt minor – Flemming & Frank, afsnit 6.

1♣ lover 2+ kort, 1♦ 4+. Støtte = 5+ klør / 4+ ruder.
  svar_* – svarer: 4-farve i major meldes først (1♥/1♠; over 1♣ også 1♦ med 4+ ruder) ·
           2 i farven 10+ sp med støtte (stærk) · 3 i farven 6–9 sp med støtte (spærrende) ·
           1NT 6–10 · 2NT 11–12 jævn · 3NT 13–15 jævn med hold i begge majorer · pas 0–5
  aab_*  – åbner efter 1m – 2m: 12–14: 2NT jævn med hold i de tre umeldte farver, ellers 3m ·
           15+ (ujævn): 3NT med hold overalt, ellers ny farve = billigste hold (benægter hold under)
Antagelser: støttepoint 5/3/1 med 4+ trumf og 3/2/1 med 3; hold = es, K-x, D-x-x eller B-x-x-x;
over 1♦ er 5+ klør med 11+ (Two over One/2NT-valg) og 4 i farven (sleminvit) ikke med; svarer med
4-farve i major vælger den længste (ved 4-4 hjerter). Åbner med 15+ uden noget hold er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from .lebensohl import stopper

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
BONUS = {
    "svar": {"q": "Hvad viser 1♦ – 2♦ hos Flemming & Frank?",
             "correct": "10+ sp med stærk støtte – udgangskrav",
             "options": ["10+ sp med stærk støtte – udgangskrav", "6–9 sp, svag støtte", "Naturlig, 5+ ruder og svag"],
             "why": "Omvendt minor: 2 i åbningsfarven er stærk (10+ sp), 3 i farven er spærrende (6–9 sp)."},
    "aab": {"q": "Hvad viser åbners nye farve efter 1m – 2m?",
            "correct": "Hold i farven – og benægter hold i farverne under",
            "options": ["Hold i farven – og benægter hold i farverne under", "En 4-farve", "Korthed"],
            "why": "Efter den stærke støtte leder vi efter 3NT: ny farve viser hold, billigste først. 2NT = minimum med hold i alle tre umeldte farver."},
}

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def sp_minor(hand, hp, m):
    L = lengths_of(hand)
    scale = {0: 5, 1: 3, 2: 1} if L[m] >= 4 else {0: 3, 1: 2, 2: 1}
    return hp + sum(scale.get(L[s], 0) for s in SUITS if s != m)

def responder(m):
    msym = SUIT_SYM[m]
    need = 4 if m == 'D' else 5
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 15:
            return None
        if (L['H'] >= 4 or L['S'] >= 4) and hp >= 6:
            M = 'S' if L['S'] > L['H'] else 'H'
            return f"1{SUIT_SYM[M]}", f"{L[M]} {SUIT_NAME[M]}: 4-farven i major meldes først – 1{SUIT_SYM[M]}."
        if L['H'] >= 4 or L['S'] >= 4:
            return None
        if L[m] >= need:
            sp = sp_minor(hand, hp, m)
            if sp < 6:
                return ("Pas", f"Kun {sp} sp: pas.") if hp <= 5 else None
            if sp <= 9:
                return f"3{msym}", f"{L[m]} {SUIT_NAME[m]} og {sp} sp: 3{msym} – spærrende (6–9)."
            return f"2{msym}", f"{L[m]} {SUIT_NAME[m]} og {sp} sp: 2{msym} – stærk støtte (10+)."
        if hp < 6:
            return "Pas", f"{hp} hp: pas."
        if m == 'C' and L['D'] >= 4:
            return "1♦", f"{L['D']} ruder: 1♦ – naturligt, 6+."
        if m == 'D' and L['C'] >= 5 and hp >= 11:
            return None
        if hp <= 10:
            return "1NT", f"{hp} hp uden 4-farve i major og uden støtte: 1NT (6–10)."
        if not balanced(L):
            return None
        if hp <= 12:
            return "2NT", f"Jævn hånd og {hp} hp: 2NT – invit (11–12)."
        if stopper(hand, 'H') and stopper(hand, 'S'):
            return "3NT", f"Jævn hånd, {hp} hp og hold i begge majorer: 3NT (13–15)."
        return None
    return classify

def opener(m):
    msym = SUIT_SYM[m]
    others = [s for s in ORDER if s != m]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[m] < (4 if m == 'D' else 3) or not (12 <= hp <= 19) or max(L[s] for s in others) > L[m]:
            return None
        held = [s for s in others if stopper(hand, s)]
        if hp <= 14:
            if balanced(L) and len(held) == 3:
                return "2NT", f"Minimum ({hp} hp), jævn og hold i {', '.join(SUIT_NAME[s] for s in others)}: 2NT."
            return f"3{msym}", f"Minimum ({hp} hp) uden hold overalt: 3{msym}."
        if balanced(L) or not held:
            return None
        if len(held) == 3:
            return "3NT", f"Tillæg ({hp} hp) og sikkert hold i alle umeldte farver: 3NT."
        above = [s for s in others if ORDER.index(s) > ORDER.index(m)] + [s for s in others if ORDER.index(s) < ORDER.index(m)]
        s = next(x for x in above if x in held)
        lv = 2 if ORDER.index(s) > ORDER.index(m) else 3
        skipped = above[:above.index(s)]
        deny = f" og benægter hold i {', '.join(SUIT_NAME[x] for x in skipped)}" if skipped else ""
        return f"{lv}{SUIT_SYM[s]}", f"Tillæg ({hp} hp): {lv}{SUIT_SYM[s]} viser hold i {SUIT_NAME[s]}{deny}."
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
key = lambda c: (0, 0) if c == "Pas" else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))
for m, mk in (('D', 'ru'), ('C', 'kl')):
    msym = SUIT_SYM[m]
    sk = f"svar_{mk}"
    calls = ["Pas", "1♥", "1♠", "1NT", f"2{msym}", "2NT", f"3{msym}", "3NT"] + (["1♦"] if m == 'C' else [])
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", f"1{msym}"], PAS], "calls": sorted(calls, key=key), "bonus": BONUS["svar"]}
    CLASSIFIERS[sk] = responder(m)
    o = 'C' if m == 'D' else 'D'
    need = 4 if m == 'D' else 5
    ow = 4 if m == 'D' else 3
    t = lambda hp, **b: tpl(hp, **{'S': (2, 3), 'H': (2, 3), 'D': (1, 4), 'C': (1, 4), **b})
    SAMPLERS[sk] = {"Pas": t((0, 5)), "1♥": t((6, 14), H=(4, 5)), "1♠": t((6, 14), S=(4, 5)),
                    f"2{msym}": t((9, 15), **{m: (need, need + 1), o: (1, 3)}), f"3{msym}": t((4, 9), **{m: (need, need + 1), o: (1, 3)}),
                    "1NT": t((6, 10), **{m: (1, need - 1), o: (1, ow)}), "2NT": t((11, 12), **{m: (2, need - 1), o: (2, ow)}),
                    "3NT": t((13, 15), **{m: (2, need - 1), o: (2, ow)})}
    if m == 'C':
        SAMPLERS[sk]["1♦"] = t((6, 14), D=(4, 5), C=(1, 4))
    PER_CALL[sk] = 8
    sk = f"aab_{mk}"
    calls = sorted({f"2{SUIT_SYM[s]}" for s in ORDER if ORDER.index(s) > ORDER.index(m)} | {"2NT", "3♣", f"3{msym}", "3NT"}, key=key)
    SITUATIONS[sk] = {"rolle": "Åbner", "auction": [["Dig", f"1{msym}"], PAS, ["Makker", f"2{msym}"], PAS], "calls": calls, "bonus": BONUS["aab"]}
    CLASSIFIERS[sk] = opener(m)
    a = lambda hp, **b: tpl(hp, **{**{s: (2, 4) for s in SUITS}, m: (4, 6) if m == 'D' else (4, 6), **b})
    SAMPLERS[sk] = {"2NT": a((12, 14), **{m: (4, 5)}), f"3{msym}": a((12, 14), **{m: (5, 6)}), "3NT": a((15, 19), **{m: (5, 6)})}
    for s in ORDER:
        if s != m:
            lv = 2 if ORDER.index(s) > ORDER.index(m) else 3
            SAMPLERS[sk][f"{lv}{SUIT_SYM[s]}"] = a((15, 19), **{m: (5, 6)})
    PER_CALL[sk] = 9

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
