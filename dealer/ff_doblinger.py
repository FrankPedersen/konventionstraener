"""
Negativ dobling, støttedobling og redobling – Flemming & Frank, afsnit 17.

  neg_*   – svarer efter makkers åbning og en indmelding: negativ dobling med 4-farve i den uviste
            major (6+ hp efter indmelding på 1-trinnet, 8+ på 2-trinnet) · 1♠ med 5+ spar · pas ellers
  aab_neg – åbner efter 1♦ – (1♥) – X – (pas) (X viser 4 spar): 1♠ 12–15 · 2♠ 16–18 · 4♠ 19+ med 4 spar ·
            pas med 4+ hjerter og 12–14 · 1NT 12–14 jævn med hjertehold · 2NT 18–19 · 2♦ 6-farve 12–15 ·
            2♥ cuebid 18+ uden naturlig melding
  stoette – åbner efter 1♥ – (pas) – 1♠ – (2♣): X = præcis 3 spar · 2♠ 4 spar 12–15 · 3♠ 4 spar 16–18 ·
            uden 3 spar: 2♥ med 6 hjerter, ellers pas (minimum)
  redobl  – svarer efter 1♥/1♠ – (X): XX 10+ uden støtte · 2M 6–9 sp med 3 · 3M 6–9 sp med 4+ ·
            2NT 10+ sp med støtte · 1♠ 6–9 med 4+ spar (over 1♥) · 2 i ny farve højst 9 hp med god 6-farve ·
            1NT 6–9 jævn · pas under 6
Antagelser: støttepoint 5/3/1 med 4+ trumf og 3/2/1 med 3; hold = es, K-x, D-x-x eller B-x-x-x;
»god 6-farve« = to af de tre øverste. Hænder, hvor skemaet ikke giver én melding, er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from .lebensohl import stopper
from .omvendt_bergen import support_points

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
BONUS = {
    "neg": {"q": "Hvad viser en negativ dobling?",
            "correct": "4-farve i den uviste major",
            "options": ["4-farve i den uviste major", "Straf i deres farve", "Mindst 13 hp"],
            "why": "Negativ dobling: 4-farve i uvist major, 6+ hp efter indmelding på 1-trinnet og 8+ på 2-trinnet. Med 5+ spar meldes 1♠."},
    "aab": {"q": "Må åbner passe makkers negative dobling?",
            "correct": "Ja – med 4+ kort og styrke bag indmelderen",
            "options": ["Ja – med 4+ kort og styrke bag indmelderen", "Nej – den er krav til en farve", "Kun med 18+"],
            "why": "Åbner behandler den negative dobling som en farvemelding, men pas er en reel mulighed med længde bag indmelderen."},
    "stoette": {"q": "Hvad viser åbners dobling i 1♥ – (pas) – 1♠ – (2♣)?",
                "correct": "Præcis 3 spar – enhver styrke",
                "options": ["Præcis 3 spar – enhver styrke", "Straf i klør", "4 spar og tillæg"],
                "why": "Støttedobling: præcis 3 kort i svarers major. Støtte i farven viser 4 kort. Gælder til og med 2♠."},
    "redobl": {"q": "Hvad viser redobling efter dobling af makkers åbning?",
               "correct": "10+ hp uden primær støtte",
               "options": ["10+ hp uden primær støtte", "Straf af deres dobling", "SOS – flugt"],
               "why": "Redoblingen viser 10+ hp og benægter støtte. Med 10+ sp og støtte meldes 2NT (Bekkasin/Jordan)."},
}
order = lambda c: (0, 0) if c in ("Pas", "X", "XX") else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def good6(cards):
    return len(cards) >= 6 and sum(1 for r in cards[:3] if r >= 12) >= 2

def negative(open_, over, need, other_major):
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[open_] >= (3 if open_ in ('H', 'S') else 4) or hp > 11:
            return None
        if over == '1H' and L['S'] >= 5:
            return ("1♠", f"{L['S']} spar og {hp} hp: 1♠ – naturligt.") if hp >= 6 else None
        if L[other_major] == 4:
            if hp >= need:
                return "X", f"4 {SUIT_NAME[other_major]} og {hp} hp: negativ dobling ({need}+)."
            return "Pas", f"4 {SUIT_NAME[other_major]}, men kun {hp} hp: pas."
        if L[other_major] < 4 and hp < 6:
            return "Pas", f"{hp} hp uden 4 {SUIT_NAME[other_major]}: pas."
        return None
    return classify

def after_negative(hand, hp):
    L = lengths_of(hand)
    if L['D'] < 4 or L['C'] > L['D'] or not (12 <= hp <= 21) or 15 <= hp <= 17 and balanced(L):
        return None
    if L['S'] == 4:
        if hp <= 15:
            return "1♠", f"4 spar og {hp} hp: 1♠ – billigst (12–15)."
        if hp <= 18:
            return "2♠", f"4 spar og {hp} hp: spring til 2♠ (16–18)."
        return "4♠", f"4 spar og {hp} hp: udgang direkte, 4♠ (19+)."
    if L['S'] > 4:
        return None
    if L['H'] >= 4 and hp <= 14:
        return "Pas", f"{L['H']} hjerter bag indmelderen og {hp} hp: pas – vi spiller dem hjem."
    if balanced(L) and stopper(hand, 'H'):
        if hp <= 14:
            return "1NT", f"{hp} hp jævn med hold i hjerter: 1NT."
        if 18 <= hp <= 19:
            return "2NT", f"{hp} hp jævn med hold i hjerter: 2NT med spring."
    if L['D'] >= 6 and hp <= 15 and L['H'] < 4:
        return "2♦", f"{L['D']} ruder og {hp} hp: genmeld farven, 2♦."
    if hp >= 18 and not balanced(L) and L['D'] < 6:
        return "2♥", f"{hp} hp uden naturlig melding: cuebid 2♥ – krav."
    return None

def support_double(hand, hp):
    L = lengths_of(hand)
    if L['H'] < 5 or not (12 <= hp <= 18):
        return None
    if L['S'] == 3:
        return "X", f"Præcis 3 spar: støttedobling – enhver styrke ({hp} hp)."
    if L['S'] >= 4:
        if hp <= 15:
            return "2♠", f"4 spar og {hp} hp: 2♠ (præcis 4 kort, 12–15)."
        return "3♠", f"4 spar og {hp} hp: 3♠ (16–18)."
    if hp > 14:
        return None
    if L['H'] >= 6:
        return "2♥", f"Ikke 3 spar, men {L['H']} hjerter: 2♥."
    if L['D'] >= 4 or L['C'] >= 4:
        return None
    return "Pas", "Ikke 3 spar og minimum: pas – benægter 3 korts støtte."

def redouble(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp > 15:
            return None
        if L[M] >= 3:
            sp = support_points(hand, hp, M)
            if sp < 6:
                return ("Pas", f"{sp} sp: pas.") if hp < 6 else None
            if sp >= 10:
                return "2NT", f"{L[M]} {SUIT_NAME[M]} og {sp} sp: 2NT – støtte med 10+ sp (erstatter cuebiddet)."
            if L[M] == 3:
                return f"2{sym}", f"3 {SUIT_NAME[M]} og {sp} sp: 2{sym} – konstruktiv støtte."
            return f"3{sym}", f"{L[M]} {SUIT_NAME[M]} og {sp} sp: 3{sym} – spærrende."
        if hp < 6:
            return "Pas", f"{hp} hp uden støtte: pas – åbner får en ny chance."
        if hp >= 10:
            return "XX", f"{hp} hp uden støtte: redobling (10+)."
        if M == 'H' and L['S'] >= 4:
            return "1♠", f"{L['S']} spar og {hp} hp: 1♠ (6–9, ikke krav efter dobling)."
        six = [s for s in SUITS if s != M and good6(hand[s])]
        if six:
            s = six[0]
            return f"2{SUIT_SYM[s]}", f"God {L[s]}-farve i {SUIT_NAME[s]} og {hp} hp: 2{SUIT_SYM[s]} – spærrende."
        if balanced(L):
            return "1NT", f"{hp} hp jævn uden støtte og uden brugbar farve: 1NT."
        return None
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
t = lambda hp, **b: tpl(hp, **{**{s: (2, 4) for s in SUITS}, **b})
for sk, open_, over, oc, need, om in (("neg_1ru_1hj", 'D', '1H', "1♥", 6, 'S'), ("neg_1kl_1sp", 'C', '1S', "1♠", 6, 'H'),
                                       ("neg_1hj_2kl", 'H', '2C', "2♣", 8, 'S')):
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", f"1{SUIT_SYM[open_]}"], ["Modstander", oc]], "allowX": True,
                      "calls": {"1H": ["Pas", "X", "1♠", "1NT", "2♣", "2♦", "2♥", "2♠", "2NT"], "1S": ["Pas", "X", "1NT", "2♣", "2♦", "2♥", "2♠", "2NT"],
                                "2C": ["Pas", "X", "2♦", "2♥", "2♠", "2NT"]}[over],
                      "bonus": BONUS["neg"]}
    CLASSIFIERS[sk] = negative(open_, over, need, om)
    lim = {open_: (0, 2 if open_ in ('H', 'S') else 3)}
    SAMPLERS[sk] = {"X": t((need, 11), **{om: (4, 4), **lim}), "Pas": either(t((2, need - 1), **{om: (4, 4), **lim}), t((0, 5), **{om: (2, 3), **lim}))}
    if over == '1H':
        SAMPLERS[sk]["1♠"] = t((6, 11), S=(5, 6), **lim)
    PER_CALL[sk] = 10
SITUATIONS["aab_neg"] = {"rolle": "Åbner", "auction": [["Dig", "1♦"], ["Modstander", "1♥"], ["Makker", "X"], PAS], "allowX": False,
                         "calls": ["Pas", "1♠", "1NT", "2♦", "2♥", "2♠", "2NT", "3♠", "4♠"], "bonus": BONUS["aab"]}
CLASSIFIERS["aab_neg"] = after_negative
a = lambda hp, **b: tpl(hp, **{'S': (1, 3), 'H': (1, 3), 'D': (4, 5), 'C': (1, 3), **b})
SAMPLERS["aab_neg"] = {"1♠": a((12, 15), S=(4, 4)), "2♠": a((16, 18), S=(4, 4)), "4♠": a((19, 21), S=(4, 4)),
                       "Pas": a((12, 14), H=(4, 4), S=(1, 3)), "1NT": a((12, 14), H=(2, 3)), "2NT": a((18, 19), H=(2, 3)),
                       "2♦": a((12, 15), D=(6, 7), H=(1, 2)), "2♥": a((18, 21), D=(5, 5), H=(0, 1), C=(3, 4))}
PER_CALL["aab_neg"] = 9
SITUATIONS["stoette"] = {"rolle": "Åbner", "auction": [["Dig", "1♥"], PAS, ["Makker", "1♠"], ["Modstander", "2♣"]], "allowX": True,
                         "calls": ["Pas", "X", "2♦", "2♥", "2♠", "2NT", "3♠"], "bonus": BONUS["stoette"]}
CLASSIFIERS["stoette"] = support_double
s_ = lambda hp, **b: tpl(hp, **{'H': (5, 5), 'S': (2, 3), 'D': (1, 3), 'C': (1, 3), **b})
SAMPLERS["stoette"] = {"X": s_((12, 18), S=(3, 3)), "2♠": s_((12, 15), S=(4, 4)), "3♠": s_((16, 18), S=(4, 4)),
                       "2♥": s_((12, 14), H=(6, 6), S=(0, 2)), "Pas": s_((12, 14), S=(1, 2), D=(2, 3), C=(2, 3))}
PER_CALL["stoette"] = 14
for M, key in (('H', 'hj'), ('S', 'sp')):
    sym = SUIT_SYM[M]
    sk = f"redobl_{key}"
    calls = {"Pas", "XX", "1NT", f"2{sym}", "2NT", f"3{sym}", "2♣", "2♦"} | ({"1♠", "2♠"} if M == 'H' else {"2♥"})
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", f"1{sym}"], ["Modstander", "X"]], "allowXX": True, "calls": sorted(calls, key=order),
                      "bonus": BONUS["redobl"]}
    CLASSIFIERS[sk] = redouble(M)
    r = lambda hp, **b: tpl(hp, **{**{s: (2, 4) for s in SUITS}, **b})
    SAMPLERS[sk] = {"Pas": r((0, 5), **{M: (0, 2)}), "XX": r((10, 14), **{M: (0, 2)}), f"2{sym}": r((5, 9), **{M: (3, 3)}),
                    f"3{sym}": r((4, 9), **{M: (4, 4)}), "2NT": r((9, 14), **{M: (3, 4)}), "1NT": r((6, 9), **{M: (2, 2), **({'S': (2, 3)} if M == 'H' else {})})}
    if M == 'H':
        SAMPLERS[sk]["1♠"] = r((6, 9), H=(0, 2), S=(4, 5))
    SAMPLERS[sk]["2♣" if M == 'S' else "2♦"] = r((5, 9), **{M: (0, 2), ('C' if M == 'S' else 'D'): (6, 6), **({'S': (0, 3)} if M == 'H' else {})})
    PER_CALL[sk] = 7

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
