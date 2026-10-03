"""
Michaels cuebid og usædvanlig 2NT – Makker 1 & mig, systemkortets afsnit 6.4 og 6.5.

Indmelder (modstanderen åbner 1-farve):
  Michaels: over 1♣/1♦ begge majorer · over 1♥ spar + minor · over 1♠ hjerter + minor
  Usædvanlig 2NT: de to laveste umeldte farver – over 1♥/1♠ minorerne, over 1♦ klør + hjerter,
  over 1♣ ruder + hjerter. Begge mindst 5-5 og 8–15 hp eller 17+.
Svarer (afsnit 6.5, bruges også efter Michaels): præference på laveste niveau 0–9 hp · spring med god
støtte 6–9 hp · cuebid i deres farve 10+ krav · egen god 6-farve uden tilpasning 10+.
Efter Michaels over 1♣/1♦ er 2NT relæ med lige længde i majorerne.
Antagelser: under 8 hp passer man; 16 hp (meldes naturligt) er ikke med; »god støtte« = 4+ kort;
svar efter Michaels over 1♥/1♠ er ikke med (2NT-spørgsmålets styrke står ikke i kortet).
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

ORDER = ['C', 'D', 'H', 'S']
UNUSUAL = {'C': ('D', 'H'), 'D': ('C', 'H'), 'H': ('C', 'D'), 'S': ('C', 'D')}

def five_five(L, opening):
    pair = [s for s in ORDER if s != opening and L[s] >= 5]
    return tuple(pair) if len(pair) == 2 else None

def overcall(opening, convention):
    osym = SUIT_SYM[opening]
    def classify(hand, hp):
        L = lengths_of(hand)
        pair = five_five(L, opening)
        if not pair or hp == 16 or hp > 20:
            return None
        a, b = pair
        desc = f"{L[a]} {SUIT_NAME[a]} og {L[b]} {SUIT_NAME[b]}"
        if convention == 'michaels':
            if opening in ('C', 'D'):
                ok = pair == ('H', 'S')
                what = "begge majorer"
            else:
                other = 'S' if opening == 'H' else 'H'
                ok = other in pair and (set(pair) - {other}) <= {'C', 'D'}
                what = f"{SUIT_NAME[other]} og en minor"
            call = f"2{osym}"
        else:
            ok = pair == UNUSUAL[opening]
            what = f"{SUIT_NAME[UNUSUAL[opening][0]]} og {SUIT_NAME[UNUSUAL[opening][1]]}"
            call = "2NT"
        if not ok:
            return None
        if hp < 8:
            return "Pas", f"{desc}, men kun {hp} hp – kravet er 8–15 eller 17+. Pas."
        strength = "8–15" if hp <= 15 else "17+"
        return call, f"{desc} og {hp} hp ({strength}): {call} viser {what}, mindst 5-5."
    return classify

def cheapest(after_rank, s):
    for lv in (2, 3, 4):
        call = f"{lv}{SUIT_SYM[s]}"
        if lv * 5 + ORDER.index(s) > after_rank:
            return call
    return None

def advance(opening, shown, after):
    """Svarer efter makkers to-farvede indmelding; shown = makkers to farver."""
    osym = SUIT_SYM[opening]
    after_rank = 2 * 5 + (4 if after == "2NT" else ORDER.index(opening))
    def classify(hand, hp):
        L = lengths_of(hand)
        a, b = shown
        if hp > 15:
            return None
        if hp >= 10:
            own = [s for s in ORDER if s not in shown and s != opening and L[s] >= 6]
            if own and L[a] <= 2 and L[b] <= 2:
                call = cheapest(after_rank, own[0])
                return call, f"{hp} hp og god {L[own[0]]}-farve i {SUIT_NAME[own[0]]} uden tilpasning: {call} – naturligt, ikke krav."
            call = f"3{osym}"
            return call, f"{hp} hp: cuebid i deres farve ({call}) er krav og beder makker beskrive videre."
        longer = a if L[a] > L[b] else b if L[b] > L[a] else None
        if max(L[a], L[b]) >= 4 and hp >= 6:
            if longer is None:
                return None
            jump = cheapest(after_rank, longer)
            jump = f"{int(jump[0]) + 1}{jump[1:]}"
            return jump, f"{L[longer]} {SUIT_NAME[longer]} og {hp} hp: spring til {jump} er spærrende med god støtte."
        if longer is None:
            if after != "2NT" and set(shown) == {'H', 'S'}:
                return "2NT", f"Lige mange hjerter og spar ({L['H']}-{L['S']}): 2NT er relæ."
            call = cheapest(after_rank, a)
            return call, f"Lige lange farver ({L[a]}-{L[b]}) og svag hånd: præference på laveste niveau – {call}."
        call = cheapest(after_rank, longer)
        return call, f"Svag hånd ({hp} hp) med flest {SUIT_NAME[longer]}: præference på laveste niveau – {call}."
    return classify

BONUS = {
    "michaels": {"q": "Hvilken styrke viser Michaels og usædvanlig 2NT?",
                 "correct": "8–15 hp eller 17+",
                 "options": ["8–15 hp eller 17+", "10–16 hp", "Altid under 10 hp"],
                 "why": "Styrken er delt: 8–15 eller 17+. Med mellemstyrken (ca. 16) og 5-5 meldes den bedste farve naturligt."},
    "svar": {"q": "Hvad er grundreglen for svarer?",
             "correct": "Vælg farve med svag hånd, cuebid med god",
             "options": ["Vælg farve med svag hånd, cuebid med god", "Pas med svag hånd", "Meld altid sans med hold"],
             "why": "Indmelder har mindst ti kort i to farver: vælg farve på laveste niveau med en svag hånd, cuebid med 10+."},
}

PAS = ["Modstander", "Pas"]

def build(convention):
    SIT, CL, SAM, PER = {}, {}, {}, {}
    for O in ORDER:
        osym = SUIT_SYM[O]
        key = {'C': 'kl', 'D': 'ru', 'H': 'hj', 'S': 'sp'}[O]
        if convention == 'michaels':
            pairs = [('H', 'S')] if O in ('C', 'D') else [('C', 'S' if O == 'H' else 'H'), ('D', 'S' if O == 'H' else 'H')]
            call = f"2{osym}"
        else:
            pairs = [UNUSUAL[O]]
            call = "2NT"
        sk = f"ind_{key}"
        SIT[sk] = {"rolle": "Indmelder", "auction": [["Modstander", f"1{osym}"]], "allowX": True,
                   "calls": ["Pas", "X", f"2{osym}", "2NT"] + [f"2{SUIT_SYM[s]}" for s in ORDER if ORDER.index(s) > ORDER.index(O)],
                   "bonus": BONUS["michaels"]}
        CL[sk] = overcall(O, convention)
        two = lambda hp, p: tpl(hp, **{s: (5, 6) if s in p else (0, 3) for s in SUITS})
        SAM[sk] = {call: either(*[(lambda p=p: two((8, 15), p)()) for p in pairs], *[(lambda p=p: two((17, 19), p)()) for p in pairs]),
                   "Pas": either(*[(lambda p=p: two((4, 7), p)()) for p in pairs])}
        PER[sk] = 10 if convention == 'michaels' else 20
        if convention == 'michaels' and O not in ('C', 'D'):
            continue
        shown = ('H', 'S') if convention == 'michaels' else UNUSUAL[O]
        sk = f"svar_{key}"
        a, b = shown
        after = call
        ar = 2 * 5 + (4 if after == "2NT" else ORDER.index(O))
        calls = sorted({cheapest(ar, a), cheapest(ar, b), f"3{osym}",
                        f"{int(cheapest(ar, a)[0]) + 1}{SUIT_SYM[a]}", f"{int(cheapest(ar, b)[0]) + 1}{SUIT_SYM[b]}"}
                       | ({"2NT"} if after != "2NT" else set()),
                       key=lambda c: int(c[0]) * 5 + ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))
        SIT[sk] = {"rolle": "Svarer", "auction": [["Modstander", f"1{osym}"], ["Makker", after], PAS],
                   "calls": calls, "bonus": BONUS["svar"]}
        CL[sk] = advance(O, shown, after)
        free = lambda hp, **bnd: tpl(hp, **{**{s: (0, 5) for s in SUITS}, **bnd})
        SAM[sk] = {cheapest(ar, a): free((0, 9), **{a: (3, 3), b: (1, 2)}),
                   cheapest(ar, b): free((0, 9), **{b: (3, 3), a: (1, 2)}),
                   f"{int(cheapest(ar, a)[0]) + 1}{SUIT_SYM[a]}": free((6, 9), **{a: (4, 5), b: (0, 3)}),
                   f"{int(cheapest(ar, b)[0]) + 1}{SUIT_SYM[b]}": free((6, 9), **{b: (4, 5), a: (0, 3)}),
                   f"3{osym}": free((10, 15), **{a: (2, 4), b: (2, 4)})}
        if after != "2NT":
            SAM[sk]["2NT"] = free((0, 9), **{a: (2, 3), b: (2, 3)})
        PER[sk] = 8
    return SIT, CL, SAM, PER

def export_michaels(path):
    return build_pool(path, *build('michaels'))

def export_unusual(path):
    return build_pool(path, *build('unusual'))
