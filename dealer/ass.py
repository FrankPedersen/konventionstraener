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
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx

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
            names_en = " and ".join(f"4 {SUIT_NAME_EN[s]}" for s in four)
            return "2♣", tx(f"{names} og {hp} hp – mindst invit: 2♣ (ASS) undersøger åbners majorfordeling.",
                            f"{names_en} and {hp} HCP – at least invitational: 2♣ (ASS) explores opener's major-suit holding.")
        return "Pas", tx(f"{hp} hp – ASS kræver mindst invit (9+). Pas.", f"{hp} HCP – ASS needs at least invitational values (9+). Pass.")
    if not balanced(L):
        return None
    if hp < INVITE[0]:
        return "Pas", tx(f"Jævn hånd med {hp} hp: sansstigen siger pas (0–8).", f"Balanced hand with {hp} HCP: the notrump ladder says pass (0–8).")
    if hp <= INVITE[1]:
        return "2NT", tx(f"Jævn hånd uden 4-farve i major og {hp} hp: 2NT er invit (9–10).",
                         f"Balanced hand without a four-card major and {hp} HCP: 2NT is invitational (9–10).")
    return "3NT", tx(f"Jævn hånd uden 4-farve i major og {hp} hp: 3NT (11–15).",
                     f"Balanced hand without a four-card major and {hp} HCP: 3NT (11–15).")

def classify_opener(hand, hp):
    L = lengths_of(hand)
    if not (15 <= hp <= 17) or not balanced(L):
        return None
    five = [s for s in ('H', 'S') if L[s] == 5]
    four = [s for s in ('H', 'S') if L[s] == 4]
    if five:
        s = five[0]
        return f"2{SUIT_SYM[s]}", tx(f"Præcis 5 {SUIT_NAME[s]}: 2{SUIT_SYM[s]}.", f"Exactly 5 {SUIT_NAME_EN[s]}: 2{SUIT_SYM[s]}.")
    if four:
        names = " og ".join(SUIT_NAME[s] for s in four)
        names_en = " and ".join(SUIT_NAME_EN[s] for s in four)
        return "2♦", tx(f"4-farve i {names}: 2♦ viser mindst én 4-farve i major – makker fortæller, hvilken han har.",
                        f"Four cards in {names_en}: 2♦ shows at least one four-card major – partner tells which one they hold.")
    if hp < MAX_OPENER:
        return "2NT", tx(f"Ingen 4-farve i major og {hp} hp – minimum: 2NT.", f"No four-card major and {hp} HCP – a minimum: 2NT.")
    return "3NT", tx(f"Ingen 4-farve i major og {hp} hp – maksimum: 3NT.", f"No four-card major and {hp} HCP – a maximum: 3NT.")

def classify_after_2ru(hand, hp):
    L = lengths_of(hand)
    if not responder_ok(L, hp) or hp < INVITE[0] or max(L['H'], L['S']) < 4:
        return None
    if L['S'] == 4:
        extra = " – at du også har 4 hjerter, må makker gætte, for 2♥ benægter dem ikke" if L['H'] == 4 else ""
        extra_en = " – partner must guess that you also have 4 hearts, as 2♥ does not deny them" if L['H'] == 4 else ""
        return "2♥", tx(f"Krydsvendt: 2♥ viser 4 spar{extra}.", f"Crosswise: 2♥ shows 4 spades{extra_en}.")
    return "2♠", tx("Krydsvendt: 2♠ viser 4 hjerter og benægter 4 spar.", "Crosswise: 2♠ shows 4 hearts and denies 4 spades.")

def after_five(M):
    sym, name, en = SUIT_SYM[M], SUIT_NAME[M], SUIT_NAME_EN[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if not responder_ok(L, hp) or hp < INVITE[0] or max(L['H'], L['S']) < 4:
            return None
        fit = L[M] >= 3
        if hp <= INVITE[1]:
            if fit:
                return f"3{sym}", tx(f"{L[M]} {name} giver fit med åbners 5-farve, og {hp} hp er invit: 3{sym}.",
                                     f"{L[M]} {en} give a fit with opener's five-card suit, and {hp} HCP is invitational: 3{sym}.")
            return "2NT", tx(f"Kun {L[M]} {name} – intet fit – og {hp} hp er invit: 2NT.",
                             f"Only {L[M]} {en} – no fit – and {hp} HCP is invitational: 2NT.")
        if fit:
            return f"4{sym}", tx(f"{L[M]} {name} giver fit, og {hp} hp er udgang: 4{sym}.", f"{L[M]} {en} give a fit, and {hp} HCP is game: 4{sym}.")
        return "3NT", tx(f"Kun {L[M]} {name} – intet fit – og {hp} hp er udgang: 3NT.", f"Only {L[M]} {en} – no fit – and {hp} HCP is game: 3NT.")
    return classify

def classify_after_2nt(hand, hp):
    L = lengths_of(hand)
    if not responder_ok(L, hp) or hp < INVITE[0] or max(L['H'], L['S']) < 4:
        return None
    if hp <= INVITE[1]:
        return "Pas", tx(f"Åbner har minimum og ingen 4-farve i major; med {hp} hp er der hverken fit eller styrke til mere: pas.",
                         f"Opener has a minimum and no four-card major; with {hp} HCP there is neither a fit nor the strength for more: pass.")
    return "3NT", tx(f"{hp} hp er udgang, selv over et minimum: 3NT.", f"{hp} HCP is game, even opposite a minimum: 3NT.")

C_NT = tx("15–17 hp jævn – kan rumme 5-farve i major", "15–17 HCP balanced – may contain a five-card major")
NT_BONUS = {"q": tx("Hvad viser makkers 1NT-åbning?", "What does partner's 1NT opening show?"),
            "correct": C_NT,
            "options": [C_NT, tx("12–14 hp jævn", "12–14 HCP balanced"), tx("15–17 hp jævn – aldrig 5-farve i major", "15–17 HCP balanced – never a five-card major")],
            "why": tx("1NT er 15–17 jævn, og alle jævne hænder åbnes 1NT – også med 5-farve i major. Derfor undersøger ASS hele majorfordelingen.",
                      "1NT is 15–17 balanced, and every balanced hand is opened 1NT – also with a five-card major. "
                      "That is why ASS explores the whole major-suit holding.")}
C_AAB = tx("Mindst invit – ikke nødvendigvis en 4-farve i major", "At least invitational – not necessarily a four-card major")
C_2RU = tx("Mindst én 4-farve i major", "At least one four-card major")
C_2M = tx("Præcis 5 kort i den viste major", "Exactly 5 cards in the major shown")
C_2NT = tx("Ingen 4-farve i major, minimum", "No four-card major, a minimum")
BONUS = {
    "svar": NT_BONUS,
    "aabner": {"q": tx("Hvad lover makkers 2♣ (ASS)?", "What does partner's 2♣ (ASS) promise?"),
               "correct": C_AAB,
               "options": [C_AAB, tx("Altid en 4-farve i major, ingen pointkrav", "Always a four-card major, no point requirement"),
                           tx("Lang klør, svag hånd", "Long clubs, a weak hand")],
               "why": tx("ASS er mindst invitation til udgang og lover ikke nødvendigvis en 4-farve i major.",
                         "ASS is at least a game invitation and does not necessarily promise a four-card major.")},
    "2ru": {"q": tx("Hvad viste åbners 2♦?", "What did opener's 2♦ show?"),
            "correct": C_2RU,
            "options": [C_2RU, tx("Ingen 4-farve i major", "No four-card major"), tx("5 ruder", "5 diamonds")],
            "why": tx("2♦ viser mindst én 4-farve i major. Svarer fortsætter krydsvendt: 2♥ = 4 spar, 2♠ = 4 hjerter.",
                      "2♦ shows at least one four-card major. Responder continues crosswise: 2♥ = 4 spades, 2♠ = 4 hearts.")},
    "2M": {"q": tx("Hvad viste åbners 2♥/2♠?", "What did opener's 2♥/2♠ show?"),
           "correct": C_2M,
           "options": [C_2M, tx("4 kort i den viste major", "4 cards in the major shown"), tx("Maksimum og 4 kort i major", "A maximum and four cards in the major")],
           "why": tx("2♥/2♠ som svar på ASS viser præcis 5 kort i den viste major.", "2♥/2♠ in response to ASS shows exactly 5 cards in the major shown.")},
    "2nt": {"q": tx("Hvad viste åbners 2NT?", "What did opener's 2NT show?"),
            "correct": C_2NT,
            "options": [C_2NT, tx("Ingen 4-farve i major, maksimum", "No four-card major, a maximum"), tx("Begge majorer", "Both majors")],
            "why": tx("2NT viser ingen 4-farve i major og minimum; 3NT viser det samme med maksimum.",
                      "2NT shows no four-card major and a minimum; 3NT shows the same with a maximum.")},
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
