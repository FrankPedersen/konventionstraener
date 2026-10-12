"""
Stærkåbning 2♣ og 2♦ waiting – Makker 2 & mig, afsnit 14.

  svar_2kl  – svarer over 2♣: 2♦ waiting (alt andet) · 2♥/2♠/3♣/3♦ positivt: 8+ hp med god 5-farve ·
              2NT positivt: 8+ hp jævn uden 5-farve · 3NT gående 7-farve i minor (E-K-D) uden værdier udenfor
  aab_2ru   – åbner efter 2♣ – 2♦: 2NT jævn 22–24 · 3NT jævn 25–27 · ellers længste farve (5+) naturligt
  svar_2_*  – svarer efter 2♣ – 2♦ – 2M: 3M med 3-korts støtte (også 0–4) · 2NT andet negative (0–4 uden
              støtte) · ny god 5-farve (5+ hp) billigst · 3NT jævn 5+ uden støtte
Antagelser: »god 5-farve« = to af de tre øverste honnører; jævn = 4-3-3-3, 4-4-3-2 eller 5-3-3-2;
åbner med to lige lange farver melder den højeste; jævne 20–21 (åbnes 2NT) er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
C_SVAR = tx("Waiting – intet om styrken", "Waiting – says nothing about strength")
C_AAB = tx("Jævn 22–24 hp", "Balanced 22–24 HCP")
C_NEG = tx("2NT – 0–4 hp uden støtte og uden egen farve", "2NT – 0–4 HCP without support and without a suit of your own")
BONUS = {
    "svar": {"q": tx("Hvad viser 2♦ over makkers 2♣?", "What does 2♦ over partner's 2♣ show?"),
             "correct": C_SVAR,
             "options": [C_SVAR, tx("0–4 hp, negativ", "0–4 HCP, negative"), tx("Ruderfarve", "A diamond suit")],
             "why": tx("2♦ er waiting: alt, der ikke er et positivt svar. Den helt tomme hånd vises senere med det andet negative.",
                       "2♦ is waiting: everything that is not a positive response. The truly empty hand is shown later with the second negative.")},
    "aab": {"q": tx("Hvad viser 2♣ – 2♦ – 2NT?", "What does 2♣ – 2♦ – 2NT show?"),
            "correct": C_AAB,
            "options": [C_AAB, tx("Jævn 20–21 hp", "Balanced 20–21 HCP"), tx("Begge minorer", "Both minors")],
            "why": tx("Efter 2♣ – 2♦ viser 2NT 22–24 og 3NT 25–27 jævn. ASS, overføring og Gerber gælder ét trin højere.",
                      "After 2♣ – 2♦, 2NT shows 22–24 and 3NT 25–27 balanced. ASS, transfers and Gerber apply one step higher.")},
    "neg": {"q": tx("Hvad er det andet negative efter 2♣ – 2♦ – 2♥?", "What is the second negative after 2♣ – 2♦ – 2♥?"),
            "correct": C_NEG,
            "options": [C_NEG, "3♣", tx("Pas", "Pass")],
            "why": tx("Svarers billigste sansmelding er det andet negative. Med 3-korts støtte støtter man – også med 0–4.",
                      "Responder's cheapest notrump bid is the second negative. With three-card support you raise – even with 0–4.")},
}

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def good(cards):
    return len(cards) >= 5 and sum(1 for r in cards[:3] if r >= 12) >= 2

def solid_minor(hand, L):
    for s in ('C', 'D'):
        c = hand[s]
        if len(c) >= 7 and c[:3] == [14, 13, 12]:
            outside = sum({14: 4, 13: 3, 12: 2, 11: 1}.get(r, 0) for x in SUITS if x != s for r in hand[x])
            return s if outside <= 1 else None
    return None

def first(hand, hp):
    L = lengths_of(hand)
    if hp > 15:
        return None
    m = solid_minor(hand, L)
    if m:
        return "3NT", tx(f"Gående {L[m]}-farve i {SUIT_NAME[m]} med E-K-D: 3NT.", f"A solid {L[m]}-card {SUIT_NAME_EN[m][:-1]} suit with A-K-Q: 3NT.")
    if hp >= 8:
        goods = [s for s in SUITS if good(hand[s])]
        if goods:
            s = max(goods, key=lambda x: (L[x], ORDER.index(x)))
            call = f"{2 if s in ('H', 'S') else 3}{SUIT_SYM[s]}"
            return call, tx(f"{hp} hp og god {L[s]}-farve i {SUIT_NAME[s]}: {call} – positivt svar.",
                            f"{hp} HCP and a good {L[s]}-card suit in {SUIT_NAME_EN[s]}: {call} – a positive response.")
        if balanced(L) and max(L.values()) <= 4:
            return "2NT", tx(f"{hp} hp jævn uden 5-farve: 2NT – positivt svar.", f"{hp} HCP balanced without a five-card suit: 2NT – a positive response.")
        return "2♦", tx(f"{hp} hp, men ingen god 5-farve og ikke jævn 4-farvet: 2♦ waiting.",
                        f"{hp} HCP, but no good five-card suit and not balanced: 2♦ waiting.")
    return "2♦", tx(f"{hp} hp: 2♦ waiting.", f"{hp} HCP: 2♦ waiting.")

def rebid(hand, hp):
    L = lengths_of(hand)
    if hp < 20 or hp > 27:
        return None
    if balanced(L):
        if 22 <= hp <= 24:
            return "2NT", tx(f"Jævn hånd, {hp} hp: 2NT (22–24).", f"Balanced hand, {hp} HCP: 2NT (22–24).")
        if hp >= 25:
            return "3NT", tx(f"Jævn hånd, {hp} hp: 3NT (25–27).", f"Balanced hand, {hp} HCP: 3NT (25–27).")
        return None
    top = max(L.values())
    s = max((x for x in SUITS if L[x] == top), key=ORDER.index)
    call = f"{2 if s in ('H', 'S') else 3}{SUIT_SYM[s]}"
    return call, tx(f"Ujævn hånd med {L[s]} {SUIT_NAME[s]}: {call} – naturligt.", f"Unbalanced hand with {L[s]} {SUIT_NAME_EN[s]}: {call} – natural.")

def second(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 7 or first(hand, hp) is None or first(hand, hp)[0] != "2♦":
            return None
        if L[M] >= 3:
            return f"3{sym}", tx(f"{L[M]} {SUIT_NAME[M]}: 3{sym} – støtte, også med {hp} hp. Åbner er kaptajn.",
                                 f"{L[M]} {SUIT_NAME_EN[M]}: 3{sym} – support, even with {hp} HCP. Opener is captain.")
        if hp <= 4:
            return "2NT", tx(f"{hp} hp uden støtte: 2NT – det andet negative.", f"{hp} HCP without support: 2NT – the second negative.")
        goods = [s for s in SUITS if s != M and good(hand[s])]
        if goods:
            s = max(goods, key=lambda x: (L[x], ORDER.index(x)))
            lv = 2 if ORDER.index(s) > ORDER.index(M) else 3
            return f"{lv}{SUIT_SYM[s]}", tx(f"God {L[s]}-farve i {SUIT_NAME[s]} og {hp} hp: {lv}{SUIT_SYM[s]} – naturligt.",
                                            f"A good {L[s]}-card suit in {SUIT_NAME_EN[s]} and {hp} HCP: {lv}{SUIT_SYM[s]} – natural.")
        if balanced(L):
            return "3NT", tx(f"{hp} hp jævn uden støtte: 3NT – sans med hold.", f"{hp} HCP balanced without support: 3NT – notrump with stoppers.")
        return None
    return classify

SITUATIONS = {
    "svar_2kl": {"rolle": "Svarer", "auction": [["Makker", "2♣"], PAS],
                 "calls": ["2♦", "2♥", "2♠", "2NT", "3♣", "3♦", "3NT"], "bonus": BONUS["svar"]},
    "aab_2ru": {"rolle": "Åbner", "auction": [["Dig", "2♣"], PAS, ["Makker", "2♦"], PAS],
                "calls": ["2♥", "2♠", "2NT", "3♣", "3♦", "3NT"], "bonus": BONUS["aab"]},
}
CLASSIFIERS = {"svar_2kl": first, "aab_2ru": rebid}
r = lambda hp, **b: tpl(hp, **{**{s: (2, 4) for s in SUITS}, **b})
SAMPLERS = {"svar_2kl": {"2♦": either(r((0, 7)), r((8, 11), S=(1, 5), H=(1, 5), D=(1, 5), C=(1, 5))),
                         "2♥": r((8, 12), H=(5, 6)), "2♠": r((8, 12), S=(5, 6)), "3♣": r((8, 12), C=(5, 6)),
                         "3♦": r((8, 12), D=(5, 6)), "2NT": r((8, 12), S=(3, 4), H=(3, 4), D=(2, 4), C=(2, 4)),
                         "3NT": r((9, 10), C=(7, 7), S=(1, 3), H=(1, 3), D=(1, 3))},
            "aab_2ru": {"2NT": r((22, 24)), "3NT": r((25, 27)),
                        **{f"{2 if s in ('H', 'S') else 3}{SUIT_SYM[s]}": r((20, 24), **{s: (5, 7)}) for s in SUITS}}}
PER_CALL = {"svar_2kl": 8, "aab_2ru": 18}
for M, mk in (('H', 'hj'), ('S', 'sp')):
    sym = SUIT_SYM[M]
    sk = f"svar_2_{mk}"
    calls = sorted({"2NT", f"3{sym}", "3♣", "3♦", "3NT"} | ({"2♠"} if M == 'H' else {"3♥"}),
                   key=lambda c: (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:])))
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", "2♣"], PAS, ["Dig", "2♦"], PAS, ["Makker", f"2{sym}"], PAS],
                      "calls": calls, "bonus": BONUS["neg"]}
    CLASSIFIERS[sk] = second(M)
    SAMPLERS[sk] = {f"3{sym}": r((0, 7), **{M: (3, 4)}), "2NT": r((0, 4), **{M: (0, 2)}), "3NT": r((5, 7), **{M: (2, 2)})}
    for s in ORDER:
        if s != M:
            lv = 2 if ORDER.index(s) > ORDER.index(M) else 3
            SAMPLERS[sk][f"{lv}{SUIT_SYM[s]}"] = r((5, 7), **{M: (0, 2), s: (5, 6)})
    PER_CALL[sk] = 5

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
