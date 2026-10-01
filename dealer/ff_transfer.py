"""
Overføringer – Flemming & Frank, afsnit 10.

Over makkers 1NT (15–17): 2♦ → hjerter (5+) · 2♥ → spar (5+) · 2♠ → klør (6+, svag) · 3♣ → ruder (6+, svag).
Åbner melder farven; med 4-korts støtte og maksimum (17) superaccepterer han med spring (kun i major).
Svarers 2. melding efter majoroverføringen:
  5-farve: pas 0–7 · 2NT invit 8–9 · 3NT udgang 10–15 (åbner vælger)
  6-farve: pas 0–7 · 3M invit 8–9 · 4M udgang 10–15
Svarerens og åbnerens første melding trænes som i Transfer (samme regler som Karina & Frank).
Antagelser: invit = 8–9 hp over 15–17; svarerhænder med en 4-farve ved siden af (ny farve =
udgangskrav) er ikke med i 2. melding.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from . import transfer

PAS = ["Modstander", "Pas"]
BONUS_2 = {"q": "Hvad viser 1NT – 2♦ – 2♥ – 2NT?",
           "correct": "5 hjerter og invit (8–9 hp)",
           "options": ["5 hjerter og invit (8–9 hp)", "6 hjerter og invit", "Udgangskrav uden hjerter"],
           "why": "Med 5-farve: 2NT invit, 3NT udgang (åbner vælger). Med 6-farve: 3M invit, 4M udgang. Svag hånd passer."}

def second(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] not in (5, 6) or any(L[s] >= 4 for s in SUITS if s != M) or hp > 15:
            return None
        if hp <= 7:
            return "Pas", f"{L[M]} {SUIT_NAME[M]} og {hp} hp: pas – overføringen har fundet kontrakten."
        if L[M] == 5:
            if hp <= 9:
                return "2NT", f"5 {SUIT_NAME[M]} og {hp} hp: 2NT – invit."
            return "3NT", f"5 {SUIT_NAME[M]} og {hp} hp: 3NT – åbner vælger mellem 3NT og 4{sym}."
        if hp <= 9:
            return f"3{sym}", f"6 {SUIT_NAME[M]} og {hp} hp: 3{sym} – invit med 6-farve."
        return f"4{sym}", f"6 {SUIT_NAME[M]} og {hp} hp: 4{sym}."
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = dict(transfer.SITUATIONS), dict(transfer.CLASSIFIERS), dict(transfer.SAMPLERS), dict(transfer.PER_CALL)
PER_CALL = {k: (12 if k == "svar_1nt" else 18) for k in PER_CALL}
for M, bid, key in (('H', "2♦", "hj"), ('S', "2♥", "sp")):
    sym = SUIT_SYM[M]
    sk = f"svar2_{key}"
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", "1NT"], PAS, ["Dig", bid], PAS, ["Makker", f"2{sym}"], PAS],
                      "calls": sorted({"Pas", "2NT", f"3{sym}", "3NT", f"4{sym}"} | ({"2♠"} if M == 'H' else set()),
                                      key=lambda c: (0, 0) if c == "Pas" else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))),
                      "bonus": BONUS_2}
    CLASSIFIERS[sk] = second(M)
    t = lambda hp, n, M=M: tpl(hp, **{**{s: (2, 3) for s in SUITS}, M: (n, n)})
    SAMPLERS[sk] = {"Pas": either(t((0, 7), 5), t((0, 7), 6)), "2NT": t((8, 9), 5), "3NT": t((10, 15), 5),
                    f"3{sym}": t((8, 9), 6), f"4{sym}": t((10, 15), 6)}
    PER_CALL[sk] = 6

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
