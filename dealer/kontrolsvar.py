"""
Forslag: 2♣ med kontrolsvar (notat efter Michael Staub, 2019).

Kontroller: es = 2, konge = 1. Puljen dækker:
  svar_1     – svarers første melding på 2♣: 2♦ 0–1 · 2♥ 2 · 2♠ 3 · 2NT 4 · 3♣ 5+ kontroller ·
               overføring med H-H-x-x-x-x (3♦ ♥ · 3♥ ♠ · 3♠ ♣ · 3NT ♦) · gående farve (4♣ ♦ · 4♦ ♥ · 4♥ ♠ · 4♠ ♣)
  aabner_*   – åbners sansmelding efter svaret: efter 2♦ 2NT 22–23 · 3NT 24–25 · 4NT 26–27 · 5NT 28–29;
               efter 2♥/2♠ 2NT 24+ · 3NT 22–23 (fast arrival)
  trumf_*    – svarer efter 2♣ – 2♦ – 3♥/3♠ (trumf fastlagt): ny farve = kontrol dér · 3NT = 0 kontroller,
               men 4+ hp i damer og knægte · udgang i trumf = 0 kontroller, negativ hånd
  konk_*     – svarer efter indmelding på 2-trinnet: pas 0–1 · dobling præcis 2 uden hæderlig langfarve ·
               ny farve hæderlig 5-farve og 1–2 kontroller · 2NT 3+ kontroller
Antagelser: H-H = præcis to af E, K, D i en 6-farve; gående = E K D B i 6+ kort eller E K D i 7+;
overføringshænder har ingen kontroller uden for farven; »hæderlig 5-farve« = 5+ kort med mindst to af
E, K, D, B. Splinter, relæ og spring i konkurrence er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, rnd, either, build_pool, tx

ORDER = ['C', 'D', 'H', 'S']
CTRL = {14: 2, 13: 1}
TRANSFER3 = {'H': "3♦", 'S': "3♥", 'C': "3♠", 'D': "3NT"}     # viser farven lige over
TRANSFER4 = {'D': "4♣", 'H': "4♦", 'S': "4♥", 'C': "4♠"}
STRAINS = ['♣', '♦', '♥', '♠', 'NT']

def rank(call):
    return int(call[0]) * 5 + STRAINS.index(call[1:])

def controls(hand, suits=SUITS):
    return sum(CTRL.get(r, 0) for s in suits for r in hand[s])

def top3(hand, s):
    return sum(1 for r in hand[s] if r >= 12)

def running(hand, s):
    n, cards = len(hand[s]), set(hand[s])
    return ({14, 13, 12, 11} <= cards and n >= 6) or ({14, 13, 12} <= cards and n >= 7)

def decent_five(hand, s):
    return len(hand[s]) >= 5 and sum(1 for r in hand[s] if r >= 11) >= 2

def ctrl_text(c):
    return f"{c} kontrol" if c == 1 else f"{c} kontroller"

def ctrl_text_en(c):
    return f"{c} control" if c == 1 else f"{c} controls"

# --- Svarers første melding -------------------------------------------------

def classify_first(hand, hp):
    L = lengths_of(hand)
    long = [s for s in SUITS if L[s] >= 6]
    if long:
        s = long[0]
        if len(long) > 1 or controls(hand, [x for x in SUITS if x != s]) > 0:
            return None
        if running(hand, s):
            call = TRANSFER4[s]
            return call, tx(f"Gående {SUIT_NAME[s]}farve: {call} er overføring og viser den.",
                            f"A solid {SUIT_NAME_EN[s][:-1]} suit: {call} is a transfer and shows it.")
        if top3(hand, s) == 2 and L[s] <= 7:
            call = TRANSFER3[s]
            return call, tx(f"To af de tre øverste i {SUIT_NAME[s]} ({L[s]} kort), men ikke gående: {call} er overføring til {SUIT_NAME[s]}.",
                            f"Two of the top three in {SUIT_NAME_EN[s]} ({L[s]} cards), but not solid: {call} is a transfer to {SUIT_NAME_EN[s]}.")
        return None
    c = controls(hand)
    call = "2♦" if c <= 1 else {2: "2♥", 3: "2♠", 4: "2NT"}.get(c, "3♣")
    what = {"2♦": "0–1 kontrol", "2♥": "præcis 2", "2♠": "præcis 3", "2NT": "præcis 4", "3♣": "5+ – krav til lilleslem"}[call]
    what_en = {"2♦": "0–1 controls", "2♥": "exactly 2", "2♠": "exactly 3", "2NT": "exactly 4", "3♣": "5+ – forcing to small slam"}[call]
    return call, tx(f"Du har {ctrl_text(c)} (es = 2, konge = 1): {call} viser {what}.",
                    f"You have {ctrl_text_en(c)} (ace = 2, king = 1): {call} shows {what_en}.")

# --- Åbners sansmelding --------------------------------------------------------

BALANCED = ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def opener_nt(after):
    def classify(hand, hp):
        L = lengths_of(hand)
        if sorted(L.values()) not in BALANCED or not (22 <= hp <= 29):
            return None
        if after == "2♦":
            call = "2NT" if hp <= 23 else "3NT" if hp <= 25 else "4NT" if hp <= 27 else "5NT"
            rng = {"2NT": "22–23", "3NT": "24–25", "4NT": "26–27", "5NT": "28–29"}[call]
            return call, tx(f"Sanshånd med {hp} hp efter makkers 2♦ (0–1 kontrol): {call} viser {rng} hp.",
                            f"A notrump hand with {hp} HCP after partner's 2♦ (0–1 controls): {call} shows {rng} HCP.")
        if hp <= 23:
            return "3NT", tx(f"{hp} hp efter et positivt svar: 3NT er fast arrival med 22–23 – intervallerne vender.",
                             f"{hp} HCP after a positive response: 3NT is fast arrival with 22–23 – the ranges are reversed.")
        return "2NT", tx(f"{hp} hp efter et positivt svar: 2NT viser 24+ og giver plads til slemundersøgelsen.",
                         f"{hp} HCP after a positive response: 2NT shows 24+ and leaves room to explore slam.")
    return classify

# --- Svarer efter fastlagt trumf ---------------------------------------------------

def responder_trump(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        c = controls(hand)
        if c > 1 or any(L[s] >= 6 for s in SUITS):
            return None
        if L[M] >= 3 and any(L[s] <= 1 for s in SUITS if s != M):
            return None      # splinterhånd – ikke med
        if c == 1:
            king = next(s for s in SUITS if 13 in hand[s])
            if king == M:
                return None
            call = next(f"{lv}{SUIT_SYM[king]}" for lv in (3, 4) if rank(f"{lv}{SUIT_SYM[king]}") > rank(f"3{sym}"))
            return call, tx(f"Trumf er fastlagt, og du har {SUIT_NAME[king]} konge: {call} viser kontrollen.",
                            f"Trumps are agreed, and you have the king of {SUIT_NAME_EN[king]}: {call} shows the control.")
        if hp >= 4:
            return "3NT", tx(f"0 kontroller, men {hp} hp i damer og knægte: 3NT.", f"0 controls, but {hp} HCP in queens and jacks: 3NT.")
        return f"4{sym}", tx(f"0 kontroller og en negativ hånd ({hp} hp): udgang i trumf, 4{sym}.",
                             f"0 controls and a negative hand ({hp} HCP): game in trumps, 4{sym}.")
    return classify

# --- Svarer efter indmelding -------------------------------------------------------

def responder_after_overcall(X):
    def classify(hand, hp):
        L = lengths_of(hand)
        if any(L[s] >= 6 for s in SUITS):
            return None      # spring / 4-trinnet er ikke med
        c = controls(hand)
        fives = [s for s in ORDER if s != X and decent_five(hand, s)]
        if c >= 3:
            return "2NT", tx(f"{ctrl_text(c)}: laveste sans viser mindst 3 kontroller.", f"{ctrl_text_en(c)}: the cheapest notrump shows at least 3 controls.")
        if fives and c >= 1:
            s = fives[0]
            call = f"2{SUIT_SYM[s]}" if ORDER.index(s) > ORDER.index(X) else f"3{SUIT_SYM[s]}"
            return call, tx(f"Hæderlig {L[s]}-farve i {SUIT_NAME[s]} og {ctrl_text(c)}: {call}.",
                            f"A decent {L[s]}-card suit in {SUIT_NAME_EN[s]} and {ctrl_text_en(c)}: {call}.")
        if c == 2:
            return "X", tx("Præcis 2 kontroller uden hæderlig langfarve: dobling – den erstatter 2♥ og er ikke straf.",
                           "Exactly 2 controls without a decent long suit: double – it replaces 2♥ and is not for penalty.")
        return "Pas", tx(f"{ctrl_text(c)}: pas afløser 2♦-svaret.", f"{ctrl_text_en(c)}: pass replaces the 2♦ response.")
    return classify

# --- Situationer -------------------------------------------------------------------

C_SVAR = tx("Es = 2, konge = 1", "Ace = 2, king = 1")
C_01 = tx("0–1 kontrol", "0–1 controls")
C_2 = tx("Præcis 2 kontroller", "Exactly 2 controls")
C_3 = tx("Præcis 3 kontroller", "Exactly 3 controls")
C_TRUMF = tx("0 kontroller, negativ hånd", "0 controls, a negative hand")
C_KONK = tx("Præcis 2 kontroller uden hæderlig langfarve", "Exactly 2 controls without a decent long suit")
BONUS = {
    "svar": {"q": tx("Hvordan tæller I kontroller?", "How do you count controls?"),
             "correct": C_SVAR,
             "options": [C_SVAR, tx("Es = 1, konge = 1", "Ace = 1, king = 1"), tx("Es = 4, konge = 3, dame = 2", "Ace = 4, king = 3, queen = 2")],
             "why": tx("Es = 2 kontroller, konge = 1. Damer og knægte tæller ikke – de stopper sjældent tabere i slem.",
                       "Ace = 2 controls, king = 1. Queens and jacks do not count – they rarely stop losers in slam.")},
    "2ru": {"q": tx("Hvad viste makkers 2♦?", "What did partner's 2♦ show?"),
            "correct": C_01,
            "options": [C_01, tx("Waiting – intet om styrken", "Waiting – nothing about strength"), C_2],
            "why": tx("2♦ viser 0–1 kontrol: intet es og højst én konge.", "2♦ shows 0–1 controls: no ace and at most one king.")},
    "2hj": {"q": tx("Hvad viste makkers 2♥?", "What did partner's 2♥ show?"),
            "correct": C_2,
            "options": [C_2, tx("5+ hjerter", "5+ hearts"), C_01],
            "why": tx("2♥ viser præcis 2 kontroller – ét es eller to konger.", "2♥ shows exactly 2 controls – one ace or two kings.")},
    "2sp": {"q": tx("Hvad viste makkers 2♠?", "What did partner's 2♠ show?"),
            "correct": C_3,
            "options": [C_3, tx("5+ spar", "5+ spades"), C_2],
            "why": tx("2♠ viser præcis 3 kontroller – es og konge, eller tre konger.", "2♠ shows exactly 3 controls – ace and king, or three kings.")},
    "trumf": {"q": tx("Hvad viser udgang i trumffarven her?", "What does game in the trump suit show here?"),
              "correct": C_TRUMF,
              "options": [C_TRUMF, tx("Maksimum og god støtte", "A maximum and good support"), tx("Kontrol i alle farver", "Controls in every suit")],
              "why": tx("Når åbner har fastlagt trumf, viser udgang i trumf 0 kontroller og en negativ hånd; 3NT viser 0 kontroller med 4+ hp i damer og knægte.",
                        "When opener has agreed trumps, game in trumps shows 0 controls and a negative hand; "
                        "3NT shows 0 controls with 4+ HCP in queens and jacks.")},
    "konk": {"q": tx("Hvad betyder din dobling efter deres indmelding?", "What does your double mean after their overcall?"),
             "correct": C_KONK,
             "options": [C_KONK, tx("Straf", "Penalty"), tx("Mindst 3 kontroller", "At least 3 controls")],
             "why": tx("Kontrolsvaret oversættes: pas afløser 2♦, dobling afløser 2♥ (ikke straf), og laveste sans dækker 3+ kontroller.",
                       "The control responses are translated: pass replaces 2♦, double replaces 2♥ (not for penalty), "
                       "and the cheapest notrump covers 3+ controls.")},
}

PAS = ["Modstander", "Pas"]
SITUATIONS = {
    "svar_1": {"rolle": "Svarer", "auction": [["Makker", "2♣"], PAS],
               "calls": ["2♦", "2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "3NT", "4♣", "4♦", "4♥", "4♠"], "bonus": BONUS["svar"]},
    "aabner_2ru": {"rolle": "Åbner", "auction": [["Dig", "2♣"], PAS, ["Makker", "2♦"], PAS],
                   "calls": ["2♥", "2♠", "2NT", "3NT", "4NT", "5NT"], "bonus": BONUS["2ru"]},
    "aabner_2hj": {"rolle": "Åbner", "auction": [["Dig", "2♣"], PAS, ["Makker", "2♥"], PAS],
                   "calls": ["2♠", "2NT", "3♣", "3♦", "3NT"], "bonus": BONUS["2hj"]},
    "aabner_2sp": {"rolle": "Åbner", "auction": [["Dig", "2♣"], PAS, ["Makker", "2♠"], PAS],
                   "calls": ["2NT", "3♣", "3♦", "3♥", "3NT"], "bonus": BONUS["2sp"]},
}
CLASSIFIERS = {"svar_1": classify_first, "aabner_2ru": opener_nt("2♦"), "aabner_2hj": opener_nt("2♥"),
               "aabner_2sp": opener_nt("2♠")}

def bal(hp, **b):
    return tpl(hp, **{'S': (2, 5), 'H': (2, 5), 'D': (2, 5), 'C': (2, 5), **b})

def hand_free(hp, **b):
    return tpl(hp, **{'S': (1, 5), 'H': (1, 5), 'D': (1, 5), 'C': (1, 5), **b})

def long_suit(s, n):
    return tpl((5, 10), **{x: (n, n) if x == s else (0, 4) for x in SUITS})

SAMPLERS = {
    "svar_1": {"2♦": hand_free((0, 6)), "2♥": hand_free((4, 9)), "2♠": hand_free((6, 11)),
               "2NT": hand_free((8, 13)), "3♣": hand_free((10, 16)),
               **{TRANSFER3[s]: long_suit(s, 6) for s in SUITS},
               **{TRANSFER4[s]: either(long_suit(s, 6), long_suit(s, 7)) for s in SUITS}},
    "aabner_2ru": {"2NT": bal((22, 23)), "3NT": bal((24, 25)), "4NT": bal((26, 27)), "5NT": bal((28, 29))},
    "aabner_2hj": {"2NT": bal((24, 28)), "3NT": bal((22, 23))},
    "aabner_2sp": {"2NT": bal((24, 28)), "3NT": bal((22, 23))},
}
PER_CALL = {"svar_1": 4, "aabner_2ru": 14, "aabner_2hj": 16, "aabner_2sp": 16}

for M, key in (('H', 'hj'), ('S', 'sp')):
    sym = SUIT_SYM[M]
    sk = f"trumf_{key}"
    calls = (["3♠", "3NT", "4♣", "4♦", "4♥", "4♠"] if M == 'H' else ["3NT", "4♣", "4♦", "4♥", "4♠", "5♣"])
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", "2♣"], PAS, ["Dig", "2♦"], PAS, ["Makker", f"3{sym}"], PAS],
                      "calls": calls, "bonus": BONUS["trumf"]}
    CLASSIFIERS[sk] = responder_trump(M)
    side = [s for s in ('C', 'D', 'H', 'S') if s != M]
    SAMPLERS[sk] = {f"4{sym}": bal((0, 3)), "3NT": bal((4, 7))}
    for s in side:
        call = next(f"{lv}{SUIT_SYM[s]}" for lv in (3, 4) if rank(f"{lv}{SUIT_SYM[s]}") > rank(f"3{sym}"))
        SAMPLERS[sk][call] = bal((1, 6))
    PER_CALL[sk] = 3

for X, key in (('D', 'ru'), ('H', 'hj'), ('S', 'sp')):
    sk = f"konk_{key}"
    above = [f"2{SUIT_SYM[s]}" for s in ORDER if ORDER.index(s) > ORDER.index(X)]
    below = [f"3{SUIT_SYM[s]}" for s in ORDER if ORDER.index(s) < ORDER.index(X)]
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", "2♣"], ["Modstander", f"2{SUIT_SYM[X]}"]], "allowX": True,
                      "calls": ["Pas", "X", "2NT"] + above + below, "bonus": BONUS["konk"]}
    CLASSIFIERS[sk] = responder_after_overcall(X)
    SAMPLERS[sk] = {"Pas": hand_free((0, 6)), "X": hand_free((4, 9)), "2NT": hand_free((6, 12))}
    for s in ORDER:
        if s != X:
            call = f"2{SUIT_SYM[s]}" if ORDER.index(s) > ORDER.index(X) else f"3{SUIT_SYM[s]}"
            SAMPLERS[sk][call] = tpl((3, 9), **{x: (5, 5) if x == s else (1, 4) for x in SUITS})
    PER_CALL[sk] = 3

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
