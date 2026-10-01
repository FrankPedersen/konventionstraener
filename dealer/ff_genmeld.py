"""
Åbners stærke genmeldinger og 3♣ checkback – Flemming & Frank, afsnit 4 og 8.

  aab_*   – åbner efter 1♦ – 1♠ (uden 4 spar):
            1NT jævn 12–14 · 2NT jævn 18–19 · 2♦ 6-farve 12–15 · 3♦ god 6-farve 16–18 ·
            2♣ 5-4 med klør 12–18 · 3♣ spring 19–21 (udgangskrav) · 2♥ 5-4 med hjerter 16–18 (rundekrav) ·
            3♥ spring 19–21
  svar_*  – svarer efter 1♦ – 1♠ – 2NT (18–19): 3♣ checkback med 5 spar eller 4 hjerter · 3NT ellers
            (efter 1♣ – 1♥ – 2NT: 5 hjerter eller 4 spar)
  check_* – åbner svarer på 3♣: 3 i svarers major = 3 korts støtte · 3 i den anden major = 4-farve ·
            3♦ ingen af delene · 3NT som 3♦ med maksimum (19)
Antagelser: »god 6-farve« = to af de tre øverste honnører; jævn = 4-3-3-3, 4-4-3-2 eller 5-3-3-2; 5-4 med
hjerter og 12–15 (kan ikke vise hjerterne) og svarer med 6+ spar eller 13+ er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

PAS = ["Modstander", "Pas"]
BONUS = {
    "aab": {"q": "Hvad er grænsen mellem ny farve og spring i ny farve?",
            "correct": "Ny farve 16–18, spring 19+ (udgangskrav)",
            "options": ["Ny farve 16–18, spring 19+ (udgangskrav)", "Ny farve 12–15, spring 16+", "Spring er altid spærrende"],
            "why": "Med 16–18 og 5-4 meldes den nye farve uden spring; med 19+ springes. Kun springet er udgangskrav."},
    "check": {"q": "Hvad spørger 3♣ efter åbners 2NT-genmelding om?",
              "correct": "Åbners majorfordeling – krav til udgang",
              "options": ["Åbners majorfordeling – krav til udgang", "Naturlig klør", "Esser"],
              "why": "3♣ checkback er kunstig: 3 i svarers major = 3 korts støtte, 3 i den anden major = 4-farve, 3♦ = ingen af delene."},
}

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def good(cards):
    return sum(1 for r in cards[:3] if r >= 12) >= 2

def rebid(hand, hp):
    L = lengths_of(hand)
    if L['S'] >= 4 or L['D'] < 4 or L['C'] > L['D'] or not (12 <= hp <= 21):
        return None
    if balanced(L):
        if hp <= 14:
            return "1NT", f"Jævn hånd, {hp} hp: 1NT (12–14)."
        if 18 <= hp <= 19:
            return "2NT", f"Jævn hånd, {hp} hp: 2NT (18–19)."
        return None
    if L['D'] >= 6 and L['H'] < 4 and L['C'] < 4:
        if hp <= 15:
            return "2♦", f"{L['D']} ruder og {hp} hp: 2♦ (12–15)."
        if hp <= 18 and good(hand['D']):
            return "3♦", f"God {L['D']}-farve ruder og {hp} hp: 3♦ – inviterende (16–18)."
        return None
    if L['D'] >= 5 and L['H'] == 4 and L['C'] < 4:
        if 16 <= hp <= 18:
            return "2♥", f"5-4 med hjerter og {hp} hp: 2♥ – rundekrav (16+)."
        if hp >= 19:
            return "3♥", f"5-4 med hjerter og {hp} hp: spring til 3♥ – udgangskrav (19–21)."
        return None
    if L['D'] >= 5 and L['C'] == 4 and L['H'] < 4:
        if hp <= 18:
            return "2♣", f"5-4 med klør og {hp} hp: 2♣ – ny lavere farve (12–18)."
        return "3♣", f"5-4 med klør og {hp} hp: spring til 3♣ – udgangskrav (19–21)."
    return None

def checkback(M):
    O = 'S' if M == 'H' else 'H'
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 4 or L[M] > 5 or hp < 6 or hp > 12:
            return None
        if L[M] >= 5 or L[O] >= 4:
            why = f"{L[M]} {SUIT_NAME[M]}" if L[M] >= 5 else f"4 {SUIT_NAME[O]}"
            return "3♣", f"{why} og {hp} hp: 3♣ checkback – spørg om åbners majorfordeling."
        return "3NT", f"Kun 4 {SUIT_NAME[M]} og ingen 4 {SUIT_NAME[O]}: intet at spørge om – 3NT."
    return classify

def answer(M):
    O, sym, osym = ('S' if M == 'H' else 'H'), SUIT_SYM[M], SUIT_SYM['S' if M == 'H' else 'H']
    def classify(hand, hp):
        L = lengths_of(hand)
        if not balanced(L) or not (18 <= hp <= 19) or L[M] >= 4:
            return None
        if L[M] == 3:
            return f"3{sym}", f"3 {SUIT_NAME[M]}: 3{sym} – 3 korts støtte, fittet er fundet."
        if L[O] >= 4:
            return f"3{osym}", f"4 {SUIT_NAME[O]}, men ikke 3 {SUIT_NAME[M]}: 3{osym}."
        if hp == 18:
            return "3♦", "Hverken 3 korts støtte eller 4-farve i den anden major: 3♦."
        return "3NT", "Hverken støtte eller 4-farve, men maksimum (19): 3NT."
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
SITUATIONS["aab_1ru"] = {"rolle": "Åbner", "auction": [["Dig", "1♦"], PAS, ["Makker", "1♠"], PAS],
                         "calls": ["1NT", "2♣", "2♦", "2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3NT"], "bonus": BONUS["aab"]}
CLASSIFIERS["aab_1ru"] = rebid
t = lambda hp, **b: tpl(hp, **{'S': (1, 3), 'H': (1, 3), 'D': (4, 5), 'C': (1, 3), **b})
SAMPLERS["aab_1ru"] = {"1NT": t((12, 14)), "2NT": t((18, 19)), "2♦": t((12, 15), D=(6, 7)), "3♦": t((16, 18), D=(6, 6)),
                       "2♣": t((12, 18), D=(5, 6), C=(4, 4)), "3♣": t((19, 21), D=(5, 6), C=(4, 4)),
                       "2♥": t((16, 18), D=(5, 6), H=(4, 4)), "3♥": t((19, 21), D=(5, 6), H=(4, 4))}
PER_CALL["aab_1ru"] = 9
for M, op, mk in (('S', 'D', 'sp'), ('H', 'C', 'hj')):
    sym, osym = SUIT_SYM[M], SUIT_SYM[op]
    sk = f"svar_{mk}"
    SITUATIONS[sk] = {"rolle": "Svarer",
                      "auction": [["Makker", f"1{osym}"], PAS, ["Dig", f"1{sym}"], PAS, ["Makker", "2NT"], PAS],
                      "calls": ["Pas", "3♣", "3♦", f"3{sym}", "3NT", f"4{sym}"], "bonus": BONUS["check"]}
    CLASSIFIERS[sk] = checkback(M)
    O = 'S' if M == 'H' else 'H'
    s = lambda hp, M=M, O=O, **b: tpl(hp, **{M: (4, 4), O: (0, 3), 'D': (1, 5), 'C': (1, 5), **b})
    SAMPLERS[sk] = {"3♣": either(s((6, 12), **{M: (5, 5)}), s((6, 12), **{O: (4, 4)})), "3NT": s((6, 12))}
    PER_CALL[sk] = 28
    sk = f"check_{mk}"
    SITUATIONS[sk] = {"rolle": "Åbner",
                      "auction": [["Dig", f"1{osym}"], PAS, ["Makker", f"1{sym}"], PAS, ["Dig", "2NT"], PAS, ["Makker", "3♣"], PAS],
                      "calls": ["3♦", "3♥", "3♠", "3NT", f"4{sym}"], "bonus": BONUS["check"]}
    CLASSIFIERS[sk] = answer(M)
    a = lambda hp, M=M, O=O, op=op, **b: tpl(hp, **{M: (2, 3), O: (2, 3), 'D': (2, 5), 'C': (2, 5), op: (4, 5), **b})
    SAMPLERS[sk] = {f"3{sym}": a((18, 19), **{M: (3, 3)}), f"3{SUIT_SYM[O]}": a((18, 19), **{M: (2, 2), O: (4, 4)}),
                    "3♦": a((18, 18), **{M: (2, 2), O: (2, 3)}), "3NT": a((19, 19), **{M: (2, 2), O: (2, 3)})}
    PER_CALL[sk] = 8

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
