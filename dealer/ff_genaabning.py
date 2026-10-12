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
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx
from .lebensohl import stopper

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
C_GEN = tx("Ca. 3 hp", "About 3 HCP")
C_SVAR = tx("Træk 3 hp fra – makker har lånt dem", "Subtract 3 HCP – partner has borrowed them")
BONUS = {
    "gen": {"q": tx("Hvor mange point lånes af makker ved genåbning?", "How many points are borrowed from partner when balancing?"),
            "correct": C_GEN,
            "options": [C_GEN, tx("Ingen – samme krav som direkte", "None – the same requirements as in direct seat"), tx("Ca. 6 hp", "About 6 HCP")],
            "why": tx("Makker kan sidde med 8–11 hp uden en brugbar melding. Genåbneren låner ca. 3 hp – derfor dobling fra 8 hp og 1NT 11–14.",
                      "Partner may hold 8–11 HCP without a useful bid. The balancer borrows about 3 HCP – hence a double from 8 HCP and 1NT 11–14.")},
    "svar": {"q": tx("Hvordan vurderer du hånden efter makkers genåbning?", "How do you value your hand after partner balances?"),
             "correct": C_SVAR,
             "options": [C_SVAR, tx("Læg 3 hp til", "Add 3 HCP"), tx("Som efter en direkte dobling", "As after a direct double")],
             "why": tx("Genåbning sker på lånte point. Svar som om du har 3 hp færre – ellers straffer du makker for at genåbne.",
                       "Balancing is done on borrowed points. Respond as if you had 3 HCP fewer – otherwise you punish partner for balancing.")},
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
            return ("2NT", tx(f"5-5 i minorerne og {hp} hp: 2NT – usædvanlig, som i direkte position.",
                              f"5-5 in the minors and {hp} HCP: 2NT – unusual, as in direct seat.")) if 8 <= hp <= 14 else None
        if sum(1 for s in SUITS if L[s] >= 5) >= 2:
            return None
        if hp >= 15:
            return None if balanced(L) else (f"2{osym}", tx(f"{hp} hp: cuebid 2{osym} – den stærke hånd, krav (15+).",
                                                            f"{hp} HCP: the cue-bid 2{osym} – the strong hand, forcing (15+)."))
        if 11 <= hp <= 14 and balanced(L) and stopper(hand, O):
            return "1NT", tx(f"{hp} hp jævn med hold i {SUIT_NAME[O]}: 1NT (11–14 i genåbning).",
                             f"{hp} HCP balanced with a stopper in {SUIT_NAME_EN[O]}: 1NT (11–14 when balancing).")
        five = [s for s in SUITS if s != O and good5(hand[s])]
        if five and 6 <= hp <= 13:
            c = cheapest(O, five[0])
            return c, tx(f"God 5-farve i {SUIT_NAME[five[0]]} og {hp} hp: {c} – genåbning i farve (6–13).",
                         f"A good five-card suit in {SUIT_NAME_EN[five[0]]} and {hp} HCP: {c} – balancing in a suit (6–13).")
        if hp >= 8 and L[O] <= 2:
            return "X", tx(f"{hp} hp og højst 2 {SUIT_NAME[O]}: dobling – hovedmeldingen i genåbning (8+).",
                           f"{hp} HCP and at most 2 {SUIT_NAME_EN[O]}: double – the main balancing action (8+).")
        if hp < 8:
            return "Pas", tx(f"{hp} hp uden god 5-farve: pas.", f"{hp} HCP without a good five-card suit: pass.")
        if L[O] >= 3:
            return "Pas", tx(f"{L[O]} {SUIT_NAME[O]}: længde i deres farve – pas.", f"{L[O]} {SUIT_NAME_EN[O]}: length in their suit – pass.")
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
            return c, tx(f"{hp} hp – devalueret {max(dev, 0)}: {L[s]} {SUIT_NAME[s]} billigst, {c}.",
                         f"{hp} HCP – devalued to {max(dev, 0)}: {L[s]} {SUIT_NAME_EN[s]} as cheaply as possible, {c}.")
        j = f"{int(c[0]) + 1}{c[1:]}"
        return j, tx(f"{hp} hp – devalueret {dev} (7–10): spring til {j} i {SUIT_NAME[s]}.",
                     f"{hp} HCP – devalued to {dev} (7–10): jump to {j} in {SUIT_NAME_EN[s]}.")
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
