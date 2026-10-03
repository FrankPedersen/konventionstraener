"""
Gerber og sansstigen – Makker 2 & mig, afsnit 8 og 11.

  svar_1nt  – svarer med en jævn hånd uden 4-farve i major over 1NT (15–17), sansstigen:
              pas 0–8 · 2NT 9–10 · 3NT 11–15 · 4NT 16–17 (invit til 6NT) · 6NT 18–19 · 5NT 20–21 · 7NT 22+
  aab_es    – åbner svarer på Gerber 4♣: 4♦ 0/4 esser · 4♥ 1 · 4♠ 2 · 4NT 3
  aab_konge – åbner svarer på 5♣ (kongespørgsmål): 5♦ 0/4 konger · 5♥ 1 · 5♠ 2 · 5NT 3
Antagelse: jævn = 4-3-3-3, 4-4-3-2 eller 5-3-3-2 med 5-farven i minor.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

PAS = ["Modstander", "Pas"]
BONUS = {
    "svar": {"q": "Hvad betyder 4NT direkte over makkers 1NT?",
             "correct": "Invit til 6NT (16–17 hp)",
             "options": ["Invit til 6NT (16–17 hp)", "Esspørgsmål", "Slutmelding"],
             "why": "4NT over 1NT er kvantitativ: 16–17 hp, invit til 6NT. Esserne spørges med Gerber 4♣."},
    "aab": {"q": "Hvad viser 4♦ som svar på Gerber?",
            "correct": "0 eller 4 esser",
            "options": ["0 eller 4 esser", "1 es", "Ruderfarve"],
            "why": "Gerber: 4♦ 0/4 · 4♥ 1 · 4♠ 2 · 4NT 3. Efter 5♣ (konger) samme trin ét niveau højere."},
}
STEPS = {0: 0, 1: 1, 2: 2, 3: 3, 4: 0}

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def ladder(hand, hp):
    L = lengths_of(hand)
    if not balanced(L) or L['H'] >= 4 or L['S'] >= 4:
        return None
    for top, call, txt in ((8, "Pas", "0–8"), (10, "2NT", "9–10, invit"), (15, "3NT", "11–15"), (17, "4NT", "16–17, invit til 6NT"),
                           (19, "6NT", "18–19"), (21, "5NT", "20–21, invit til 7NT"), (40, "7NT", "22+")):
        if hp <= top:
            return call, f"Jævn hånd uden 4-farve i major og {hp} hp: {call} ({txt})."

def answer(rank, level):
    word = "esser" if rank == 14 else "konger"
    calls = [f"{level}♦", f"{level}♥", f"{level}♠", f"{level}NT"]
    def classify(hand, hp):
        if not (15 <= hp <= 17) or not balanced(lengths_of(hand)):
            return None
        n = sum(1 for s in SUITS if rank in hand[s])
        call = calls[STEPS[n]]
        return call, f"{n} {word}: {call} ({['0 eller 4', '1', '2', '3'][STEPS[n]]})."
    return classify

SITUATIONS = {
    "svar_1nt": {"rolle": "Svarer", "auction": [["Makker", "1NT"], PAS],
                 "calls": ["Pas", "2NT", "3NT", "4♣", "4NT", "5NT", "6NT", "7NT"], "bonus": BONUS["svar"]},
    "aab_es": {"rolle": "Åbner", "auction": [["Dig", "1NT"], PAS, ["Makker", "4♣"], PAS],
               "calls": ["4♦", "4♥", "4♠", "4NT", "5♣"], "bonus": BONUS["aab"]},
}
CLASSIFIERS = {"svar_1nt": ladder, "aab_es": answer(14, 4)}
bal = lambda hp: tpl(hp, S=(2, 3), H=(2, 3), D=(2, 5), C=(2, 5))
SAMPLERS = {"svar_1nt": {"Pas": bal((0, 8)), "2NT": bal((9, 10)), "3NT": bal((11, 15)), "4NT": bal((16, 17)),
                         "6NT": bal((18, 19)), "5NT": bal((20, 21)), "7NT": bal((22, 24))},
            "aab_es": {c: tpl((15, 17), **{s: (2, 5) for s in SUITS}) for c in ("4♦", "4♥", "4♠", "4NT")}}
PER_CALL = {"svar_1nt": 14, "aab_es": 14}
REACH = {"4♥": ("5♦", "5♥", "5♠", "5NT"), "4♠": ("5♦", "5♥", "5♠", "5NT"), "4NT": ("5♦", "5♥")}
for ace_call in REACH:   # efter 4♦ (0 eller 4 esser) kan 15–17 hp kun svare 5♦ – ikke med
    sk = f"aab_konge_{ace_call[1:].replace('♥', 'hj').replace('♠', 'sp').replace('NT', 'nt')}"
    SITUATIONS[sk] = {"rolle": "Åbner", "auction": [["Dig", "1NT"], PAS, ["Makker", "4♣"], PAS, ["Dig", ace_call], PAS, ["Makker", "5♣"], PAS],
                      "calls": ["5♦", "5♥", "5♠", "5NT", "6NT"], "bonus": BONUS["aab"]}
    aces = {"4♥": (1,), "4♠": (2,), "4NT": (3,)}[ace_call]
    base = answer(13, 5)
    CLASSIFIERS[sk] = (lambda aces, base: lambda hand, hp: base(hand, hp) if sum(1 for s in SUITS if 14 in hand[s]) in aces else None)(aces, base)
    SAMPLERS[sk] = {c: tpl((15, 17), **{s: (2, 5) for s in SUITS}) for c in REACH[ace_call]}
    PER_CALL[sk] = 5

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
