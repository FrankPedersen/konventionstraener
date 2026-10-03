"""
Michaels cuebid og usædvanlig 2NT – Makker 2 & mig, afsnit 15b.

  ind_*  – indmelder over 1-farve, mindst 5-5, 8–15 hp eller 17+ (under 8: pas):
           Michaels: over 1♣/1♦ begge majorer · over 1♥ spar + minor · over 1♠ hjerter + minor
           Usædvanlig 2NT: over 1♥/1♠ minorerne · over 1♦ klør + hjerter · over 1♣ ruder + hjerter
  svar_* – svarer: præference billigst 0–9 hp · spring med 4+ støtte 6–9 hp (spærrende) ·
           egen god 6-farve uden tilpasning 10+ (ikke krav) · 11+: cuebid i deres farve (krav) –
           efter Michaels i major spørger 2NT om minoren (11+), og cuebiddet viser støtte til majoren
Antagelser: 16 hp (meldes naturligt) er ikke med; præference ved lige længde går til den laveste farve;
svarer med 10 hp uden egen 6-farve og svag hånd uden 3 kort i den kendte major (efter Michaels
i major) er ikke med; pas med længde i deres farve er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

ORDER = ['C', 'D', 'H', 'S']
KEY = {'C': 'kl', 'D': 'ru', 'H': 'hj', 'S': 'sp'}
UNUSUAL = {'C': ('D', 'H'), 'D': ('C', 'H'), 'H': ('C', 'D'), 'S': ('C', 'D')}
PAS = ["Modstander", "Pas"]
BONUS = {
    "ind": {"q": "Hvilken styrke viser Michaels og usædvanlig 2NT?",
            "correct": "8–15 hp eller 17+",
            "options": ["8–15 hp eller 17+", "10–16 hp", "Altid under 10 hp"],
            "why": "Styrken er delt: 8–15 eller 17+. Med mellemstyrken og 5-5 meldes den bedste farve naturligt."},
    "svar": {"q": "Hvad viser 2NT efter makkers Michaels i en major?",
             "correct": "Spørger om minoren – 11+ og krav",
             "options": ["Spørger om minoren – 11+ og krav", "Naturligt, hold i deres farve", "Svag præference"],
             "why": "Over 1♥/1♠ viser Michaels den anden major og en uvist minor. 2NT spørger om minoren (11+); cuebid viser god støtte til majoren."},
}

def pair_call(O, pair):
    pair = set(pair)
    if O in ('C', 'D'):
        if pair == {'H', 'S'}:
            return f"2{SUIT_SYM[O]}", "begge majorer"
    else:
        om = 'S' if O == 'H' else 'H'
        if om in pair and len(pair & {'C', 'D'}) == 1:
            return f"2{SUIT_SYM[O]}", f"{SUIT_NAME[om]} og en minor"
    if pair == set(UNUSUAL[O]):
        a, b = UNUSUAL[O]
        return "2NT", f"{SUIT_NAME[a]} og {SUIT_NAME[b]} (de to laveste umeldte)"
    return None

def overcall(O):
    def classify(hand, hp):
        L = lengths_of(hand)
        pair = [s for s in ORDER if s != O and L[s] >= 5]
        if len(pair) != 2 or hp == 16 or hp > 19:
            return None
        r = pair_call(O, pair)
        if not r:
            return None
        call, what = r
        if hp < 8:
            return "Pas", f"5-5, men kun {hp} hp – kravet er 8–15 eller 17+. Pas."
        return call, f"5-5 og {hp} hp ({'8–15' if hp <= 15 else '17+'}): {call} viser {what}."
    return classify

def cheapest(after, s):
    for lv in (2, 3, 4):
        if lv * 5 + ORDER.index(s) > after:
            return f"{lv}{SUIT_SYM[s]}"

def advance(O, shown, after_call):
    after = 2 * 5 + (4 if after_call == "2NT" else ORDER.index(O))
    major_michaels = after_call != "2NT" and O in ('H', 'S')
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 15:
            return None
        if major_michaels:
            M = shown[0]
            if hp >= 11:
                if L[M] >= 3:
                    return f"3{SUIT_SYM[O]}", f"{hp} hp og {L[M]} {SUIT_NAME[M]}: cuebid 3{SUIT_SYM[O]} – god støtte, krav."
                return "2NT", f"{hp} hp uden støtte til {SUIT_NAME[M]}: 2NT spørger om minoren (11+, krav)."
            own = [s for s in ORDER if s not in (O, M) and L[s] >= 6]
            if hp == 10 and own and L[M] <= 2:
                c = cheapest(after, own[0])
                return c, f"{hp} hp og god {L[own[0]]}-farve uden tilpasning: {c} – naturligt, ikke krav."
            if hp >= 10 or L[M] < 3:
                return None
            if L[M] >= 4 and hp >= 6:
                c = cheapest(after, M)
                c = f"{int(c[0]) + 1}{c[1:]}"
                return c, f"{L[M]} {SUIT_NAME[M]} og {hp} hp: spring til {c} – spærrende."
            c = cheapest(after, M)
            return c, f"{L[M]} {SUIT_NAME[M]} og {hp} hp: præference på laveste niveau – {c}."
        a, b = shown
        if hp >= 10:
            own = [s for s in ORDER if s not in shown and s != O and L[s] >= 6]
            if own and L[a] <= 2 and L[b] <= 2:
                c = cheapest(after, own[0])
                return c, f"{hp} hp og god {L[own[0]]}-farve uden tilpasning: {c} – naturligt, ikke krav."
            if hp >= 11:
                return f"3{SUIT_SYM[O]}", f"{hp} hp: cuebid 3{SUIT_SYM[O]} – krav, beder makker beskrive videre."
            return None
        top = max(L[a], L[b])
        s = min((x for x in shown if L[x] == top), key=ORDER.index)
        if top >= 4 and hp >= 6 and L[a] != L[b]:
            c = cheapest(after, s)
            c = f"{int(c[0]) + 1}{c[1:]}"
            return c, f"{L[s]} {SUIT_NAME[s]} og {hp} hp: spring til {c} – spærrende."
        if top >= 4 and hp >= 6:
            return None
        c = cheapest(after, s)
        return c, f"Svag hånd ({hp} hp) med flest {SUIT_NAME[s]}: præference på laveste niveau – {c}."
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
order = lambda c: (0, 0) if c in ("Pas", "X") else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))
for O in ORDER:
    osym, key = SUIT_SYM[O], KEY[O]
    sk = f"ind_{key}"
    SITUATIONS[sk] = {"rolle": "Indmelder", "auction": [["Modstander", f"1{osym}"]], "allowX": True,
                      "calls": sorted({"Pas", "2NT"} | {f"2{SUIT_SYM[s]}" for s in ORDER}, key=order),
                      "bonus": BONUS["ind"]}
    CLASSIFIERS[sk] = overcall(O)
    two = lambda hp, p: tpl(hp, **{s: (5, 6) if s in p else (0, 3) for s in SUITS})
    mich = [('H', 'S')] if O in ('C', 'D') else [('S' if O == 'H' else 'H', m) for m in ('C', 'D')]
    SAMPLERS[sk] = {f"2{osym}": either(*[(lambda p=p: two((8, 15), p)()) for p in mich], *[(lambda p=p: two((17, 19), p)()) for p in mich]),
                    "2NT": either(two((8, 15), UNUSUAL[O]), two((17, 19), UNUSUAL[O])),
                    "Pas": either(*[(lambda p=p: two((4, 7), p)()) for p in mich + [UNUSUAL[O]]])}
    PER_CALL[sk] = 15
    for after_call, shown_list in ((f"2{osym}", [('H', 'S')] if O in ('C', 'D') else [('S' if O == 'H' else 'H',)]),
                                   ("2NT", [UNUSUAL[O]])):
        shown = shown_list[0]
        sk = f"svar_{key}_{'cue' if after_call != '2NT' else 'nt'}"
        after = 2 * 5 + (4 if after_call == "2NT" else ORDER.index(O))
        calls = {f"3{osym}"} | {cheapest(after, s) for s in ORDER if s != O} | {f"{int(cheapest(after, s)[0]) + 1}{SUIT_SYM[s]}" for s in shown}
        if after_call != "2NT" and O in ('H', 'S'):
            calls.add("2NT")
        SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Modstander", f"1{osym}"], ["Makker", after_call], PAS],
                          "calls": sorted(calls, key=order), "bonus": BONUS["svar"]}
        CLASSIFIERS[sk] = advance(O, shown, after_call)
        free = lambda hp, **b: tpl(hp, **{**{s: (1, 4) for s in SUITS}, **b})
        S = {}
        for s in shown:
            S[cheapest(after, s)] = free((0, 9), **{s: (3, 3), **{x: (1, 2) for x in shown if x != s}})
            S[f"{int(cheapest(after, s)[0]) + 1}{SUIT_SYM[s]}"] = free((6, 9), **{s: (4, 5), **{x: (0, 3) for x in shown if x != s}})
        S[f"3{osym}"] = free((11, 15), **{x: (2, 4) for x in shown})
        if len(shown) == 1:
            S["2NT"] = free((11, 15), **{shown[0]: (0, 2)})
            S[cheapest(after, shown[0])] = free((0, 9), **{shown[0]: (3, 3)})
        for s in ORDER:
            if s != O and s not in shown:
                S[cheapest(after, s)] = free((10, 10) if len(shown) == 1 else (10, 13), **{s: (6, 6), **{x: (0, 2) for x in shown}})
        SAMPLERS[sk] = S
        PER_CALL[sk] = 4

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
