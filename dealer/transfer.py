"""
Transfer – Makker 1 & mig, systemkortets afsnit 3.

Over makkers 1NT (15–17):
  2♦ transfer til hjerter (5+) · 2♥ transfer til spar (5+) · 2♠ minortransfer til klør (6+) · 3♣ minortransfer til ruder (6+)
Åbner fuldfører transferen: 2♦ → 2♥ · 2♥ → 2♠ · 2♠ → 3♣ · 3♣ → 3♦.
Superaccept (som hos Makker 2 & mig): med 4-korts støtte og maksimum (17 hp) springer åbner til 3M efter
2♦/2♥. Minortransfererne fuldføres altid.
Antagelser: transfer bruges uanset styrke; minortransfer kun uden 4-farve i major; hænder med 5-5 eller
5-4 i majorerne er ikke med (kortet siger ikke, om Stayman eller transfer går først).
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, build_pool

TRANSFER = {'H': "2♦", 'S': "2♥", 'C': "2♠", 'D': "3♣"}
COMPLETE = {"2♦": "2♥", "2♥": "2♠", "2♠": "3♣", "3♣": "3♦"}
TARGET = {"2♦": 'H', "2♥": 'S', "2♠": 'C', "3♣": 'D'}

def responder(hand, hp):
    L = lengths_of(hand)
    if hp > 15:
        return None
    majors = [s for s in ('H', 'S') if L[s] >= 5]
    if majors:
        if len(majors) > 1 or L['H'] >= 4 and L['S'] >= 4:
            return None
        s = majors[0]
        return TRANSFER[s], f"{L[s]} {SUIT_NAME[s]}: {TRANSFER[s]} er transfer – makker melder {COMPLETE[TRANSFER[s]]}."
    minors = [s for s in ('C', 'D') if L[s] >= 6]
    if len(minors) == 1 and L['H'] < 4 and L['S'] < 4:
        s = minors[0]
        return TRANSFER[s], f"{L[s]} {SUIT_NAME[s]} og ingen 4-farve i major: {TRANSFER[s]} er minortransfer til {SUIT_NAME[s]}."
    return None

def opener(call):
    def classify(hand, hp):
        L = lengths_of(hand)
        if sorted(L.values()) not in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5]) or not (15 <= hp <= 17):
            return None
        done, T = COMPLETE[call], TARGET[call]
        if T in ('H', 'S') and L[T] == 4 and hp == 17:
            jump = f"3{SUIT_SYM[T]}"
            return jump, f"4 {SUIT_NAME[T]} og maksimum (17 hp): superaccept – spring til {jump}."
        if T in ('H', 'S') and L[T] == 4:
            return done, f"4 {SUIT_NAME[T]}, men ikke maksimum ({hp} hp): ingen superaccept – du melder {done}."
        return done, f"Makkers {call} er transfer til {SUIT_NAME[TARGET[call]]}: du melder {done}."
    return classify

BONUS = {
    "svar": {"q": "Hvad viser 2♠ over makkers 1NT?",
             "correct": "Minortransfer til klør",
             "options": ["Minortransfer til klør", "Naturlig spar", "Stayman"],
             "why": "2♠ er minortransfer til klør og 3♣ minortransfer til ruder. 2♦/2♥ er transfer til hjerter/spar."},
    "aabner": {"q": "Hvad skal du gøre efter makkers transfer?",
               "correct": "Melde farven – med 4-korts støtte og 17 hp springe (superaccept)",
               "options": ["Melde farven – med 4-korts støtte og 17 hp springe (superaccept)", "Passe", "Melde din egen længste farve"],
               "why": "Transferen beder åbner melde den viste farve. Kun med 4-korts støtte og maksimum må åbner springe et trin – superaccept. Minortransfer fuldføres altid."},
}

PAS = ["Modstander", "Pas"]
SITUATIONS = {"svar_1nt": {"rolle": "Svarer", "auction": [["Makker", "1NT"], PAS],
                           "calls": ["2♣", "2♦", "2♥", "2♠", "3♣", "3♦"], "bonus": BONUS["svar"]}}
CLASSIFIERS = {"svar_1nt": responder}
SAMPLERS = {"svar_1nt": {
    "2♦": tpl((0, 15), H=(5, 6), S=(0, 3), D=(0, 4), C=(0, 4)),
    "2♥": tpl((0, 15), S=(5, 6), H=(0, 3), D=(0, 4), C=(0, 4)),
    "2♠": tpl((0, 10), C=(6, 7), H=(0, 3), S=(0, 3), D=(0, 3)),
    "3♣": tpl((0, 10), D=(6, 7), H=(0, 3), S=(0, 3), C=(0, 3))}}
PER_CALL = {"svar_1nt": 25}
for call, key in (("2♦", "2ru"), ("2♥", "2hj"), ("2♠", "2sp"), ("3♣", "3kl")):
    sk = f"aabner_{key}"
    SITUATIONS[sk] = {"rolle": "Åbner", "auction": [["Dig", "1NT"], PAS, ["Makker", call], PAS],
                      "calls": sorted({"2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "3NT"} - {call},
                                      key=lambda c: int(c[0]) * 5 + ['♣', '♦', '♥', '♠', 'NT'].index(c[1:])),
                      "bonus": BONUS["aabner"]}
    SITUATIONS[sk]["calls"] = [c for c in SITUATIONS[sk]["calls"] if int(c[0]) * 5 + ['♣', '♦', '♥', '♠', 'NT'].index(c[1:])
                               > int(call[0]) * 5 + ['♣', '♦', '♥', '♠', 'NT'].index(call[1:])]
    if len(SITUATIONS[sk]["calls"]) < 4:
        SITUATIONS[sk]["calls"] = ["Pas"] + SITUATIONS[sk]["calls"]
    CLASSIFIERS[sk] = opener(call)
    SAMPLERS[sk] = {COMPLETE[call]: tpl((15, 17), S=(2, 5), H=(2, 5), D=(2, 5), C=(2, 5))}
    PER_CALL[sk] = 25
    if TARGET[call] in ('H', 'S'):
        T = TARGET[call]
        SAMPLERS[sk][f"3{SUIT_SYM[T]}"] = tpl((17, 17), **{x: (4, 4) if x == T else (2, 4) for x in SUITS})
        PER_CALL[sk] = 13

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
