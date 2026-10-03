"""
Genåbning i 4. hånd – Makker 2 & mig, afsnit 15c.

  gen_*  – 1♥/1♠ – pas – pas – ?:
           cuebid 15+ (krav) · 1NT 11–14 jævn med hold i deres farve · 2NT 5-5 i minorerne, 8–14 ·
           ny farve 6–13 med god 5-farve (billigst) · dobling 8–14 med højst 2 i deres farve ·
           pas med længde i deres farve eller under 8 hp
  svar_* – 1♥/1♠ – pas – pas – X – pas – ?: makker har passet første gang. Devaluér med 3 hp og svar
           som på en oplysningsdobling: længste farve (major før minor), billigst med 0–6 efter
           devaluering (dvs. 0–9 hp), spring med 7–10 (10–11 hp)
Antagelser: »god 5-farve« = to af de tre øverste honnører; hænder med 6+ i en farve (spærrespring),
5-5 uden for minorerne og 15+ jævne hænder er ikke med; svarer har 0–11 hp (har passet), højst 3 i
deres farve og mindst én 4-farve; svarer med hold i deres farve og 9+ hp (sans) er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from .lebensohl import stopper

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
BONUS = {
    "gen": {"q": "Hvor mange point lånes af makker ved genåbning?",
            "correct": "Ca. 3 hp",
            "options": ["Ca. 3 hp", "Ingen – samme krav som direkte", "Ca. 6 hp"],
            "why": "Makker kan sidde med 8–11 hp uden en brugbar melding. Genåbneren låner ca. 3 hp – derfor dobling fra 8 hp og 1NT 11–14."},
    "svar": {"q": "Hvordan vurderer du hånden efter makkers genåbning?",
             "correct": "Træk 3 hp fra – makker har lånt dem",
             "options": ["Træk 3 hp fra – makker har lånt dem", "Læg 3 hp til", "Som efter en direkte dobling"],
             "why": "Genåbning sker på lånte point. Svar som om du har 3 hp færre – ellers straffer du makker for at genåbne."},
}

def good5(cards):
    return len(cards) == 5 and sum(1 for r in cards[:3] if r >= 12) >= 2

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def cheapest(O, s):
    return f"{1 if ORDER.index(s) > ORDER.index(O) else 2}{SUIT_SYM[s]}"

def reopen(O):
    osym = SUIT_SYM[O]
    def classify(hand, hp):
        L = lengths_of(hand)
        if max(L.values()) >= 6 or hp > 18:
            return None
        if L['C'] >= 5 and L['D'] >= 5:
            return ("2NT", f"5-5 i minorerne og {hp} hp: 2NT – usædvanlig, som i direkte position.") if 8 <= hp <= 14 else None
        if sum(1 for s in SUITS if L[s] >= 5) >= 2:
            return None
        if hp >= 15:
            return None if balanced(L) else (f"2{osym}", f"{hp} hp: cuebid 2{osym} – den stærke hånd, krav (15+).")
        if 11 <= hp <= 14 and balanced(L) and stopper(hand, O):
            return "1NT", f"{hp} hp jævn med hold i {SUIT_NAME[O]}: 1NT (11–14 i genåbning)."
        five = [s for s in SUITS if s != O and good5(hand[s])]
        if five and 6 <= hp <= 13:
            c = cheapest(O, five[0])
            return c, f"God 5-farve i {SUIT_NAME[five[0]]} og {hp} hp: {c} – genåbning i farve (6–13)."
        if hp >= 8 and L[O] <= 2:
            return "X", f"{hp} hp og højst 2 {SUIT_NAME[O]}: dobling – hovedmeldingen i genåbning (8+)."
        if hp < 8:
            return "Pas", f"{hp} hp uden god 5-farve: pas."
        if L[O] >= 3:
            return "Pas", f"{L[O]} {SUIT_NAME[O]}: længde i deres farve – pas."
        return None
    return classify

def advance(O):
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 11 or L[O] > 3:
            return None
        cands = [s for s in SUITS if s != O and L[s] >= 4]
        if not cands or (hp >= 9 and stopper(hand, O)):
            return None
        top = max(L[s] for s in cands)
        best = [s for s in cands if L[s] == top]
        majors = [s for s in best if s in ('H', 'S')]
        s = majors[0] if majors else best[0]
        if len(majors) > 1 or (not majors and len(best) > 1):
            return None
        c = cheapest(O, s)
        dev = hp - 3
        if dev <= 6:
            return c, f"{hp} hp – devalueret {max(dev, 0)}: {L[s]} {SUIT_NAME[s]} billigst, {c}."
        j = f"{int(c[0]) + 1}{c[1:]}"
        return j, f"{hp} hp – devalueret {dev} (7–10): spring til {j} i {SUIT_NAME[s]}."
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
order = lambda c: (0, 0) if c in ("Pas", "X") else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))
for O, key in (('H', 'hj'), ('S', 'sp')):
    osym = SUIT_SYM[O]
    others = [s for s in SUITS if s != O]
    sk = f"gen_{key}"
    calls = {"Pas", "X", "1NT", "2NT", f"2{osym}"} | {cheapest(O, s) for s in others}
    SITUATIONS[sk] = {"rolle": "Genåbner", "auction": [["Modstander", f"1{osym}"], PAS, PAS], "allowX": True,
                      "calls": sorted(calls, key=order), "bonus": BONUS["gen"]}
    CLASSIFIERS[sk] = reopen(O)
    t = lambda hp, O=O, **b: tpl(hp, **{**{s: (2, 4) for s in SUITS}, **b})
    SAMPLERS[sk] = {"X": t((8, 14), **{O: (0, 2)}), "1NT": t((11, 14), **{O: (2, 4)}), f"2{osym}": t((15, 18), **{O: (0, 2), **{s: (1, 5) for s in others}}),
                    "2NT": t((8, 14), C=(5, 5), D=(5, 5), **{O: (0, 3)}), "Pas": either(t((3, 7), **{O: (2, 4)}), t((8, 12), **{O: (3, 5)}))}
    for s in others:
        SAMPLERS[sk][cheapest(O, s)] = t((7, 13), **{s: (5, 5), O: (1, 3)})
    PER_CALL[sk] = 10
    sk = f"svar_{key}"
    calls = {cheapest(O, s) for s in others} | {f"{int(cheapest(O, s)[0]) + 1}{SUIT_SYM[s]}" for s in others} | {"Pas"}
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Modstander", f"1{osym}"], ["Dig", "Pas"], ["Modstander", "Pas"], ["Makker", "X"], PAS],
                      "calls": sorted(calls, key=order), "bonus": BONUS["svar"]}
    CLASSIFIERS[sk] = advance(O)
    SAMPLERS[sk] = {}
    for s in others:
        a = lambda hp, s=s, O=O: tpl(hp, **{**{x: (1, 3) for x in SUITS}, s: (4, 5), O: (2, 3)})
        SAMPLERS[sk][cheapest(O, s)] = a((0, 9))
        SAMPLERS[sk][f"{int(cheapest(O, s)[0]) + 1}{SUIT_SYM[s]}"] = a((10, 11))
    PER_CALL[sk] = 12

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
