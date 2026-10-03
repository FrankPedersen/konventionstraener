"""
Amerikansk Stayman (ASS) – Makker 2 & mig, afsnit 8 og 9.

1NT = 15–17 jævn og kan rumme en 5-farve i major. 2♣ er mindst invit og lover ikke nødvendigvis
en 4-farve i major. Puljen dækker:
  svar_1nt   – svarer over 1NT: sansstigen for jævne hænder uden 4-farve i major (pas 0–8, 2NT 9–10,
               3NT 11–15) og 2♣ med en 4-farve i major og mindst invit (9+)
  aabner     – åbners svar på 2♣: 2♦ mindst én 4-farve i major · 2♥/2♠ præcis 5-farve · 2NT ingen
               4-farve, minimum · 3NT ingen 4-farve, maksimum
  svar_2ru   – efter 2♦, krydsvendt: 2♥ = 4 spar (kan have 4 hjerter) · 2♠ = 4 hjerter, ikke 4 spar
  svar_2M    – efter 2♥/2♠ (5-farve): 2NT invit uden fit · 3M invit med fit · 3NT / 4M slutmelding
  svar_2nt   – efter 2NT (minimum): pas med invit · 3NT med udgangsstyrke
Antagelser: åbners minimum er 15–16, maksimum 17; fit = 3+ kort i åbners 5-farve. Hænder med 5+ i major
(overføring), 6+ i minor og 16+ hp (slem) er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

BALANCED = ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])
MAX_OPENER = 17          # antagelse: 17 = maksimum, 15–16 = minimum
INVITE = (9, 10)         # sansstigen: 2NT 9–10 invit
GAME = (11, 15)          # sansstigen: 3NT 11–15

def balanced(L):
    return sorted(L.values()) in BALANCED

def responder_ok(L, hp):
    return L['S'] <= 4 and L['H'] <= 4 and L['D'] <= 5 and L['C'] <= 5 and hp <= GAME[1] and min(L.values()) >= 1

def classify_first(hand, hp):
    L = lengths_of(hand)
    if not responder_ok(L, hp):
        return None
    four = [s for s in ('H', 'S') if L[s] == 4]
    if four:
        if hp >= INVITE[0]:
            names = " og ".join(f"4 {SUIT_NAME[s]}" for s in four)
            return "2♣", f"{names} og {hp} hp – mindst invit: 2♣ (ASS) undersøger åbners majorfordeling."
        return "Pas", f"{hp} hp – ASS kræver mindst invit (9+). Pas."
    if not balanced(L):
        return None
    if hp < INVITE[0]:
        return "Pas", f"Jævn hånd med {hp} hp: sansstigen siger pas (0–8)."
    if hp <= INVITE[1]:
        return "2NT", f"Jævn hånd uden 4-farve i major og {hp} hp: 2NT er invit (9–10)."
    return "3NT", f"Jævn hånd uden 4-farve i major og {hp} hp: 3NT (11–15)."

def classify_opener(hand, hp):
    L = lengths_of(hand)
    if not (15 <= hp <= 17) or not balanced(L):
        return None
    five = [s for s in ('H', 'S') if L[s] == 5]
    four = [s for s in ('H', 'S') if L[s] == 4]
    if five:
        s = five[0]
        return f"2{SUIT_SYM[s]}", f"Præcis 5 {SUIT_NAME[s]}: 2{SUIT_SYM[s]}."
    if four:
        names = " og ".join(SUIT_NAME[s] for s in four)
        return "2♦", f"4-farve i {names}: 2♦ viser mindst én 4-farve i major – makker fortæller, hvilken han har."
    if hp < MAX_OPENER:
        return "2NT", f"Ingen 4-farve i major og {hp} hp – minimum: 2NT."
    return "3NT", f"Ingen 4-farve i major og {hp} hp – maksimum: 3NT."

def classify_after_2ru(hand, hp):
    L = lengths_of(hand)
    if not responder_ok(L, hp) or hp < INVITE[0] or max(L['H'], L['S']) < 4:
        return None
    if L['S'] == 4:
        extra = " – at du også har 4 hjerter, må makker gætte, for 2♥ benægter dem ikke" if L['H'] == 4 else ""
        return "2♥", f"Krydsvendt: 2♥ viser 4 spar{extra}."
    return "2♠", "Krydsvendt: 2♠ viser 4 hjerter og benægter 4 spar."

def after_five(M):
    sym, name = SUIT_SYM[M], SUIT_NAME[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if not responder_ok(L, hp) or hp < INVITE[0] or max(L['H'], L['S']) < 4:
            return None
        fit = L[M] >= 3
        if hp <= INVITE[1]:
            if fit:
                return f"3{sym}", f"{L[M]} {name} giver fit med åbners 5-farve, og {hp} hp er invit: 3{sym}."
            return "2NT", f"Kun {L[M]} {name} – intet fit – og {hp} hp er invit: 2NT."
        if fit:
            return f"4{sym}", f"{L[M]} {name} giver fit, og {hp} hp er udgang: 4{sym}."
        return "3NT", f"Kun {L[M]} {name} – intet fit – og {hp} hp er udgang: 3NT."
    return classify

def classify_after_2nt(hand, hp):
    L = lengths_of(hand)
    if not responder_ok(L, hp) or hp < INVITE[0] or max(L['H'], L['S']) < 4:
        return None
    if hp <= INVITE[1]:
        return "Pas", f"Åbner har minimum og ingen 4-farve i major; med {hp} hp er der hverken fit eller styrke til mere: pas."
    return "3NT", f"{hp} hp er udgang, selv over et minimum: 3NT."

NT_BONUS = {"q": "Hvad viser makkers 1NT-åbning?",
            "correct": "15–17 hp jævn – kan rumme 5-farve i major",
            "options": ["15–17 hp jævn – kan rumme 5-farve i major", "12–14 hp jævn", "15–17 hp jævn – aldrig 5-farve i major"],
            "why": "1NT er 15–17 jævn, og alle jævne hænder åbnes 1NT – også med 5-farve i major. Derfor undersøger ASS hele majorfordelingen."}
BONUS = {
    "svar": NT_BONUS,
    "aabner": {"q": "Hvad lover makkers 2♣ (ASS)?",
               "correct": "Mindst invit – ikke nødvendigvis en 4-farve i major",
               "options": ["Mindst invit – ikke nødvendigvis en 4-farve i major", "Altid en 4-farve i major, ingen pointkrav", "Lang klør, svag hånd"],
               "why": "ASS er mindst invitation til udgang og lover ikke nødvendigvis en 4-farve i major."},
    "2ru": {"q": "Hvad viste åbners 2♦?",
            "correct": "Mindst én 4-farve i major",
            "options": ["Mindst én 4-farve i major", "Ingen 4-farve i major", "5 ruder"],
            "why": "2♦ viser mindst én 4-farve i major. Svarer fortsætter krydsvendt: 2♥ = 4 spar, 2♠ = 4 hjerter."},
    "2M": {"q": "Hvad viste åbners 2♥/2♠?",
           "correct": "Præcis 5 kort i den viste major",
           "options": ["Præcis 5 kort i den viste major", "4 kort i den viste major", "Maksimum og 4 kort i major"],
           "why": "2♥/2♠ som svar på ASS viser præcis 5 kort i den viste major."},
    "2nt": {"q": "Hvad viste åbners 2NT?",
            "correct": "Ingen 4-farve i major, minimum",
            "options": ["Ingen 4-farve i major, minimum", "Ingen 4-farve i major, maksimum", "Begge majorer"],
            "why": "2NT viser ingen 4-farve i major og minimum; 3NT viser det samme med maksimum."},
}

PAS = ["Modstander", "Pas"]
OPEN = [["Makker", "1NT"], PAS]
SITUATIONS = {
    "svar_1nt": {"rolle": "Svarer", "auction": OPEN, "calls": ["Pas", "2♣", "2♦", "2♥", "2NT", "3NT"], "bonus": BONUS["svar"]},
    "aabner": {"rolle": "Åbner", "auction": [["Dig", "1NT"], PAS, ["Makker", "2♣"], PAS],
               "calls": ["2♦", "2♥", "2♠", "2NT", "3NT"], "bonus": BONUS["aabner"]},
    "svar_2ru": {"rolle": "Svarer", "auction": OPEN + [["Dig", "2♣"], PAS, ["Makker", "2♦"], PAS],
                 "calls": ["2♥", "2♠", "2NT", "3♥", "3♠", "3NT"], "bonus": BONUS["2ru"]},
    "svar_2hj": {"rolle": "Svarer", "auction": OPEN + [["Dig", "2♣"], PAS, ["Makker", "2♥"], PAS],
                 "calls": ["2NT", "3♥", "3NT", "4♥", "Pas"], "bonus": BONUS["2M"]},
    "svar_2sp": {"rolle": "Svarer", "auction": OPEN + [["Dig", "2♣"], PAS, ["Makker", "2♠"], PAS],
                 "calls": ["2NT", "3♠", "3NT", "4♠", "Pas"], "bonus": BONUS["2M"]},
    "svar_2nt": {"rolle": "Svarer", "auction": OPEN + [["Dig", "2♣"], PAS, ["Makker", "2NT"], PAS],
                 "calls": ["Pas", "3♥", "3♠", "3NT"], "bonus": BONUS["2nt"]},
}
CLASSIFIERS = {"svar_1nt": classify_first, "aabner": classify_opener, "svar_2ru": classify_after_2ru,
               "svar_2hj": after_five('H'), "svar_2sp": after_five('S'), "svar_2nt": classify_after_2nt}

def resp(hp, **b):
    return tpl(hp, **{'S': (1, 4), 'H': (1, 4), 'D': (1, 5), 'C': (1, 5), **b})

SAMPLERS = {
    "svar_1nt": {"Pas": resp((2, 8), S=(2, 4), H=(2, 4), D=(2, 5), C=(2, 5)),
                 "2♣": either(resp((9, 15), S=(4, 4)), resp((9, 15), H=(4, 4))),
                 "2NT": resp(INVITE, S=(2, 3), H=(2, 3), D=(2, 5), C=(2, 5)),
                 "3NT": resp(GAME, S=(2, 3), H=(2, 3), D=(2, 5), C=(2, 5))},
    "aabner": {"2♦": either(tpl((15, 17), S=(4, 4), H=(2, 4), D=(2, 4), C=(2, 4)), tpl((15, 17), H=(4, 4), S=(2, 3), D=(2, 4), C=(2, 4))),
               "2♥": tpl((15, 17), H=(5, 5), S=(2, 3), D=(2, 3), C=(2, 3)),
               "2♠": tpl((15, 17), S=(5, 5), H=(2, 3), D=(2, 3), C=(2, 3)),
               "2NT": tpl((15, 16), S=(2, 3), H=(2, 3), D=(2, 5), C=(2, 5)),
               "3NT": tpl((17, 17), S=(2, 3), H=(2, 3), D=(2, 5), C=(2, 5))},
    "svar_2ru": {"2♥": resp((9, 15), S=(4, 4)), "2♠": resp((9, 15), H=(4, 4), S=(1, 3))},
    "svar_2hj": {"2NT": resp(INVITE, S=(4, 4), H=(1, 2)), "3♥": resp(INVITE, H=(3, 4)),
                 "3NT": resp(GAME, S=(4, 4), H=(1, 2)), "4♥": resp(GAME, H=(3, 4))},
    "svar_2sp": {"2NT": resp(INVITE, H=(4, 4), S=(1, 2)), "3♠": resp(INVITE, S=(3, 4)),
                 "3NT": resp(GAME, H=(4, 4), S=(1, 2)), "4♠": resp(GAME, S=(3, 4))},
    "svar_2nt": {"Pas": either(resp(INVITE, S=(4, 4)), resp(INVITE, H=(4, 4))),
                 "3NT": either(resp(GAME, S=(4, 4)), resp(GAME, H=(4, 4)))},
}
PER_CALL = {"svar_1nt": 8, "aabner": 20, "svar_2ru": 10, "svar_2hj": 6, "svar_2sp": 6, "svar_2nt": 8}

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
