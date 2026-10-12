"""
Flannery 2♦ – forslag til Makker 2 & mig, bilag B1 (diskussionsoplæg, ikke vedtaget). Alertér 2♦ og 2NT.

2♦ viser præcis 5 hjerter og 4 spar, 11–15 hp. Ikke krav, men makker passer kun med ruderlængde.
  aabning – åbner: 5♥ og 4♠ med 11–15 → 2♦ · med 16–21 → 1♥ (1♥ benægter herefter fire spar under 16 hp) ·
            5♥ uden fire spar → 1♥
  svar    – svarer efter 2♦: pas = lang ruder og svag · 2♥/2♠ = præference, svag (slutmelding) · 2NT = spørger (krav) ·
            3♥/3♠ = invit med god støtte · 4♥/4♠ = udgang · 3♣/3♦ = naturligt, egen god 6-farve, ikke krav
  spm     – åbner efter 2♦ – 2NT: 3♣/3♦ fire kort i minoren, minimum (11–13) · 3♥ minimum uden sidefarve (5-4-2-2) ·
            3♠ maksimum uden sidefarve (14–15) · 3NT 5-4-2-2, maksimum og hold i begge minorer ·
            4♣/4♦ fire kort i minoren, maksimum
Antagelser, som bilaget ikke giver tal for: fit = 3+ hjerter eller 4+ spar; svag = 0–9 hp, invit = 10–12, udgang =
13–15; 2NT = 13–17 hp uden fit; pas = 6+ ruder og 0–7 hp uden fit; 3♣/3♦ = 8–11 hp, god 6-farve (to af de tre
øverste) uden fit; hold = es, K-x, D-x-x eller B-x-x-x. Ikke med: 5-5 i majorerne (skal aftales), 5♥ med 15–17 jævn
(1NT kan rumme en 5-farve), svarer med fit i begge majorer eller 16+ og fit, og 5-4-3-1 efter 2NT – bilaget siger
ikke hvad.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx
from .lebensohl import stopper

PAS = ["Modstander", "Pas"]
FLANNERY = tx("Præcis 5 hjerter og 4 spar, 11–15 hp", "Exactly 5 hearts and 4 spades, 11–15 HCP")
PASSE = tx("Kun med lang ruder og svag hånd", "Only with long diamonds and a weak hand")
MINIMUM = tx("Minimum uden sidefarve – 5-4-2-2", "A minimum without a side suit – 5-4-2-2")
BONUS = {
    "aabning": {"q": tx("Hvad viser Flannery 2♦?", "What does Flannery 2♦ show?"),
                "correct": FLANNERY,
                "options": [FLANNERY, tx("En svag 2 i ruder", "A weak two in diamonds"),
                            tx("En svag 2 i en ukendt major (Multi)", "A weak two in an unknown major (Multi)")],
                "why": tx("Flannery 2♦ viser præcis 5-4 i majorerne med 11–15 hp. Med 16+ åbner man 1♥ og melder spar bagefter, "
                          "så 1♥ benægter fire spar under 16 hp.",
                          "Flannery 2♦ shows exactly 5-4 in the majors with 11–15 HCP. With 16+ you open 1♥ and bid spades later, "
                          "so 1♥ denies four spades below 16 HCP.")},
    "svar": {"q": tx("Hvornår må svarer passe Flannery 2♦?", "When may responder pass Flannery 2♦?"),
             "correct": PASSE,
             "options": [PASSE, tx("Med enhver svag hånd", "With any weak hand"), tx("Aldrig – 2♦ er krav", "Never – 2♦ is forcing")],
             "why": tx("2♦ er ikke krav, men makker passer kun med ruderlængde. Med en svag hånd giver man præference til 2♥ eller 2♠, "
                       "og 2NT spørger efter åbners fordeling.",
                       "2♦ is not forcing, but partner passes only with diamond length. With a weak hand you give preference to 2♥ "
                       "or 2♠, and 2NT asks for opener's shape.")},
    "spm": {"q": tx("Hvad viser 3♥ som svar på 2NT efter Flannery?", "What does 3♥ in response to 2NT after Flannery show?"),
            "correct": MINIMUM,
            "options": [MINIMUM, tx("Maksimum uden sidefarve", "A maximum without a side suit"),
                        tx("Fire kort i en minor, minimum", "Four cards in a minor, a minimum")],
            "why": tx("3♣/3♦ = fire kort i minoren og minimum · 3♥ = 5-4-2-2 med minimum · 3♠ = 5-4-2-2 med maksimum · "
                      "3NT = maksimum med hold i begge minorer · 4♣/4♦ = fire kort i minoren og maksimum.",
                      "3♣/3♦ = four cards in the minor and a minimum · 3♥ = 5-4-2-2 with a minimum · 3♠ = 5-4-2-2 with a maximum · "
                      "3NT = a maximum with stoppers in both minors · 4♣/4♦ = four cards in the minor and a maximum.")},
}

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def good6(cards):
    return len(cards) >= 6 and sum(1 for r in cards[:3] if r >= 12) >= 2

def opening(hand, hp):
    L = lengths_of(hand)
    if L['H'] != 5 or L['S'] >= 5 or L['C'] > 4 or L['D'] > 4:
        return None
    if L['S'] == 4:
        if 11 <= hp <= 15:
            return "2♦", tx(f"5 hjerter, 4 spar og {hp} hp: Flannery 2♦ – præcis 5-4 i majorerne med 11–15.",
                            f"5 hearts, 4 spades and {hp} HCP: Flannery 2♦ – exactly 5-4 in the majors with 11–15.")
        if 16 <= hp <= 21:
            return "1♥", tx(f"5 hjerter, 4 spar og {hp} hp: for stærk til Flannery – åbn 1♥ og meld spar bagefter. "
                            "1♥ benægter fire spar under 16 hp.",
                            f"5 hearts, 4 spades and {hp} HCP: too strong for Flannery – open 1♥ and bid spades later. "
                            "1♥ denies four spades below 16 HCP.")
        return None
    if not (12 <= hp <= 21) or (15 <= hp <= 17 and balanced(L)):
        return None
    return "1♥", tx(f"5 hjerter, kun {L['S']} spar og {hp} hp: 1♥ – Flannery kræver præcis fire spar.",
                    f"5 hearts, only {L['S']} spades and {hp} HCP: 1♥ – Flannery needs exactly four spades.")

def answer(hand, hp):
    L = lengths_of(hand)
    if hp > 17:
        return None
    fit = [M for M, n in (('H', 3), ('S', 4)) if L[M] >= n]
    if len(fit) > 1:
        return None
    if fit:
        M = fit[0]
        sym, da, en = SUIT_SYM[M], SUIT_NAME[M], SUIT_NAME_EN[M]
        trumf = L[M] + (5 if M == 'H' else 4)
        if hp <= 9:
            return f"2{sym}", tx(f"{L[M]} {da} ({trumf} trumf sammen) og {hp} hp: 2{sym} – præference og slutmelding.",
                                 f"{L[M]} {en} ({trumf} trumps together) and {hp} HCP: 2{sym} – preference and to play.")
        if hp <= 12:
            return f"3{sym}", tx(f"{L[M]} {da} ({trumf} trumf sammen) og {hp} hp: 3{sym} – invit med god støtte.",
                                 f"{L[M]} {en} ({trumf} trumps together) and {hp} HCP: 3{sym} – invitational with good support.")
        if hp <= 15:
            return f"4{sym}", tx(f"{L[M]} {da} ({trumf} trumf sammen) og {hp} hp: 4{sym} – udgang, din egen beslutning.",
                                 f"{L[M]} {en} ({trumf} trumps together) and {hp} HCP: 4{sym} – game, your own decision.")
        return None
    if hp >= 13:
        return "2NT", tx(f"{hp} hp uden fit i majorerne: 2NT spørger om åbners nøjagtige fordeling og styrke (krav).",
                         f"{hp} HCP without a fit in the majors: 2NT asks for opener's exact shape and strength (forcing).")
    good = [m for m in ('C', 'D') if good6(hand[m])]
    if 8 <= hp <= 11 and len(good) == 1:
        m = good[0]
        return f"3{SUIT_SYM[m]}", tx(f"God {L[m]}-farve i {SUIT_NAME[m]} uden fit og {hp} hp: 3{SUIT_SYM[m]} – naturligt, ikke krav.",
                                     f"A good {L[m]}-card {SUIT_NAME_EN[m][:-1]} suit without a fit and {hp} HCP: 3{SUIT_SYM[m]} – natural, non-forcing.")
    if L['D'] >= 6 and hp <= 7:
        return "Pas", tx(f"{L['D']} ruder, ingen fit i majorerne og kun {hp} hp: pas – 2♦ er den bedste kontrakt.",
                         f"{L['D']} diamonds, no fit in the majors and only {hp} HCP: pass – 2♦ is the best contract.")
    return None

def relay(hand, hp):
    L = lengths_of(hand)
    if L['H'] != 5 or L['S'] != 4 or not (11 <= hp <= 15):
        return None
    mx = hp >= 14
    four = [m for m in ('C', 'D') if L[m] == 4]
    if four:
        m = four[0]
        call = f"{4 if mx else 3}{SUIT_SYM[m]}"
        return call, tx(f"Fire {SUIT_NAME[m]} og {hp} hp ({'maksimum' if mx else 'minimum'}): {call}.",
                        f"Four {SUIT_NAME_EN[m]} and {hp} HCP ({'a maximum' if mx else 'a minimum'}): {call}.")
    if L['C'] != 2 or L['D'] != 2:
        return None
    if not mx:
        return "3♥", tx(f"5-4-2-2 og {hp} hp – minimum uden sidefarve: 3♥.", f"5-4-2-2 and {hp} HCP – a minimum without a side suit: 3♥.")
    if stopper(hand, 'C') and stopper(hand, 'D'):
        return "3NT", tx(f"5-4-2-2, {hp} hp og hold i begge minorer: 3NT.", f"5-4-2-2, {hp} HCP and stoppers in both minors: 3NT.")
    return "3♠", tx(f"5-4-2-2 og {hp} hp – maksimum uden sidefarve, men ikke hold i begge minorer: 3♠.",
                    f"5-4-2-2 and {hp} HCP – a maximum without a side suit, but not stoppers in both minors: 3♠.")

SITUATIONS = {
    "aabning": {"rolle": "Åbner", "auction": [], "calls": ["Pas", "1♥", "1♠", "1NT", "2♦", "2♥"], "bonus": BONUS["aabning"]},
    "svar": {"rolle": "Svarer", "auction": [["Makker", "2♦"], PAS],
             "calls": ["Pas", "2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "4♥", "4♠"], "bonus": BONUS["svar"]},
    "spm": {"rolle": "Åbner", "auction": [["Dig", "2♦"], PAS, ["Makker", "2NT"], PAS],
            "calls": ["3♣", "3♦", "3♥", "3♠", "3NT", "4♣", "4♦"], "bonus": BONUS["spm"]},
}
CLASSIFIERS = {"aabning": opening, "svar": answer, "spm": relay}
fl = lambda hp, **b: tpl(hp, **{'H': (5, 5), 'S': (4, 4), 'D': (0, 4), 'C': (0, 4), **b})
r = lambda hp, **b: tpl(hp, **{'H': (0, 2), 'S': (0, 3), 'D': (1, 5), 'C': (1, 5), **b})
SAMPLERS = {
    "aabning": {"2♦": fl((11, 15)), "1♥": either(fl((16, 21)), tpl((12, 21), H=(5, 5), S=(1, 3), D=(1, 4), C=(1, 4)))},
    "svar": {"2♥": r((0, 9), H=(3, 4)), "2♠": r((0, 9), S=(4, 5)), "3♥": r((10, 12), H=(3, 4)), "3♠": r((10, 12), S=(4, 5)),
             "4♥": r((13, 15), H=(3, 4)), "4♠": r((13, 15), S=(4, 5)), "2NT": r((13, 17)),
             "3♣": r((8, 11), C=(6, 7), D=(1, 3)), "3♦": r((8, 11), D=(6, 7), C=(1, 3)), "Pas": r((0, 7), D=(6, 7), C=(1, 3))},
    "spm": {"3♣": fl((11, 13), C=(4, 4), D=(0, 0)), "3♦": fl((11, 13), D=(4, 4), C=(0, 0)),
            "4♣": fl((14, 15), C=(4, 4), D=(0, 0)), "4♦": fl((14, 15), D=(4, 4), C=(0, 0)),
            "3♥": fl((11, 13), C=(2, 2), D=(2, 2)), "3♠": fl((14, 15), C=(2, 2), D=(2, 2)), "3NT": fl((14, 15), C=(2, 2), D=(2, 2))},
}
PER_CALL = {"aabning": 20, "svar": 6, "spm": 8}

# Håndlavede eksempler (hånd, situation, facit) – kortgiveren skal give samme melding
EKSEMPLER = [
    ({'S': [13, 12, 8, 4], 'H': [14, 11, 9, 5, 2], 'D': [13, 3], 'C': [7, 2]}, "aabning", "2♦"),
    ({'S': [14, 12, 8, 4], 'H': [14, 13, 11, 5, 2], 'D': [13, 3], 'C': [7, 2]}, "aabning", "1♥"),
    ({'S': [13, 3], 'H': [12, 8, 4], 'D': [11, 9, 7, 6, 2], 'C': [8, 4, 3]}, "svar", "2♥"),
    ({'S': [11, 9], 'H': [13, 2], 'D': [14, 13, 11, 8, 7, 6], 'C': [12, 4, 3]}, "svar", "2NT"),
    ({'S': [13, 12, 8, 4], 'H': [14, 11, 9, 5, 2], 'D': [13, 3], 'C': [12, 2]}, "spm", "3♠"),
    ({'S': [13, 12, 8, 4], 'H': [14, 11, 9, 5, 2], 'D': [], 'C': [13, 8, 7, 2]}, "spm", "3♣"),
]

def export_pool(path):
    from .core import hp_of
    for hand, sit, facit in EKSEMPLER:
        hp = hp_of([r for s in SUITS for r in hand[s]])
        got = CLASSIFIERS[sit](hand, hp)
        assert got and got[0] == facit, (sit, facit, got)
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
