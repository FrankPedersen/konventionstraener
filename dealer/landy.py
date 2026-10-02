"""
Landy mod modstandernes 1NT – Kampen om kontrakten.

  ind   – (1NT) ?: 2♣ = begge majorer, mindst 5-4, 8–14 hp · X = straf, 15+ hp · 2♦/2♥/2♠ = naturlig
          seksfarve 8–14 · 2NT = begge minorer, mindst 5-5, 8–14 · pas under 8 hp eller uden melding
  svar  – (1NT) 2♣ (pas) ?: 0–8: 2♥/2♠ = længste major (pas/ret) · 2♦ = lige lange majorer, makker vælger ·
          pas = lange klør (6+) og højst to i hver major · 9–11: spring til 3♥/3♠ med 4+ støtte (invit),
          ellers længste major på 2-trinnet · 12+: 2NT spørger
  valg  – (1NT) 2♣ (pas) 2♦ (pas) ?: indmelder vælger sin længste major
Antagelser: 15+ dobles altid (også med majorerne); en naturlig farve er seks kort; klør kan ikke meldes
naturligt (2♣ er Landy) og er ikke med; svarerhænder med 9–11 og lige lange firfarver i begge majorer er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either
from .kamp import build_pool as kbuild, zoneless

PAS = ["Modstander", "Pas"]
BONUS = {
    "ind": {"q": "Hvad viser Landy 2♣ over deres 1NT?",
            "correct": "Begge majorer, mindst 5-4",
            "options": ["Begge majorer, mindst 5-4", "Naturlige klør", "Én major og en minor"],
            "why": "Landy: 2♣ viser begge majorer, mindst 5-4. X er straf (15+), og de øvrige farvemeldinger er naturlige."},
    "svar": {"q": "Hvad betyder 2♦ som svar på makkers Landy 2♣?",
             "correct": "Lige lange majorer – makker vælger",
             "options": ["Lige lange majorer – makker vælger", "Naturlige ruder", "Stærk hånd, krav"],
             "why": "Med lige lange majorer lader svarer indmelder vælge med 2♦. Med en længere major meldes den direkte, og 2NT spørger med 12+."},
}

def overcall(hand, hp):
    L = lengths_of(hand)
    if hp > 18:
        return None
    if hp >= 15:
        return "X", f"{hp} hp: dobling er straf (15+) – du har lige så meget som åbneren."
    if hp < 8:
        return "Pas", f"Kun {hp} hp: pas – Landy og de naturlige meldinger kræver 8+."
    maj = sorted([L['H'], L['S']])
    if maj[0] >= 4 and maj[1] >= 5:
        return "2♣", f"{L['H']} hjerter og {L['S']} spar: 2♣ – Landy, begge majorer (mindst 5-4)."
    if L['C'] >= 5 and L['D'] >= 5:
        return "2NT", f"{L['C']} klør og {L['D']} ruder: 2NT – begge minorer."
    six = [s for s in ('D', 'H', 'S') if L[s] >= 6]
    if len(six) == 1 and max(L[s] for s in SUITS if s != six[0]) <= 4:
        s = six[0]
        return f"2{SUIT_SYM[s]}", f"{L[s]} {SUIT_NAME[s]} og {hp} hp: 2{SUIT_SYM[s]} – naturligt."
    if L['C'] >= 6:
        return None
    if max(L.values()) <= 5:
        return "Pas", f"{hp} hp, men ingen Landy-fordeling og ingen seksfarve: pas."
    return None

def advance(hand, hp):
    L = lengths_of(hand)
    h, s = L['H'], L['S']
    if hp > 16:
        return None
    if hp >= 12:
        return "2NT", f"{hp} hp: 2NT spørger – udgang er mulig, makker beskriver sin hånd."
    if hp >= 9:
        if max(h, s) >= 4:
            if h == s:
                return None
            M = 'H' if h > s else 'S'
            return f"3{SUIT_SYM[M]}", f"{L[M]} {SUIT_NAME[M]} og {hp} hp: spring til 3{SUIT_SYM[M]} – invit med støtte."
    if L['C'] >= 6 and h <= 2 and s <= 2:
        return ("Pas", f"{L['C']} klør og korte majorer: pas – 2♣ er den bedste kontrakt.") if hp <= 8 else None
    if h == s:
        return "2♦", f"Lige mange hjerter og spar ({h}-{s}): 2♦ – makker vælger sin længste major."
    M = 'H' if h > s else 'S'
    return f"2{SUIT_SYM[M]}", f"Flest {SUIT_NAME[M]} ({L[M]}): 2{SUIT_SYM[M]} – vi spiller i den major, der passer bedst."

def choose(hand, hp):
    L = lengths_of(hand)
    if not (8 <= hp <= 14) or sorted([L['H'], L['S']]) != [4, 5]:
        return None
    M = 'H' if L['H'] > L['S'] else 'S'
    return f"2{SUIT_SYM[M]}", f"Makker har lige lange majorer: vælg din femfarve – 2{SUIT_SYM[M]}."

SITUATIONS = {
    "ind": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"]], "allowX": True,
            "calls": ["Pas", "X", "2♣", "2♦", "2♥", "2♠", "2NT"], "bonus": BONUS["ind"]},
    "svar": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♣"], PAS],
             "calls": ["Pas", "2♦", "2♥", "2♠", "2NT", "3♥", "3♠"], "bonus": BONUS["svar"]},
    "valg": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♣"], PAS, ["Makker", "2♦"], PAS],
             "calls": ["Pas", "2♥", "2♠", "2NT", "3♥"], "bonus": BONUS["svar"]},
}
CLASSIFIERS = {"ind": zoneless(overcall), "svar": zoneless(advance), "valg": zoneless(choose)}
t = lambda hp, **b: tpl(hp, **{**{s: (1, 4) for s in SUITS}, **b})
SAMPLERS = {
    "ind": {"2♣": either(t((8, 14), H=(5, 5), S=(4, 5)), t((8, 14), S=(5, 5), H=(4, 5))),
            "X": t((15, 18), **{s: (2, 5) for s in SUITS}), "Pas": t((3, 7), **{s: (2, 5) for s in SUITS}),
            "2NT": t((8, 14), C=(5, 6), D=(5, 6), H=(0, 2), S=(0, 2)),
            "2♦": t((8, 14), D=(6, 7)), "2♥": t((8, 14), H=(6, 7)), "2♠": t((8, 14), S=(6, 7))},
    "svar": {"2NT": t((12, 15), **{s: (2, 4) for s in SUITS}), "3♥": t((9, 11), H=(4, 5), S=(1, 3)),
             "3♠": t((9, 11), S=(4, 5), H=(1, 3)), "2♦": t((0, 8), H=(2, 3), S=(2, 3)),
             "2♥": t((0, 10), H=(3, 4), S=(1, 2)), "2♠": t((0, 10), S=(3, 4), H=(1, 2)),
             "Pas": t((0, 8), C=(6, 7), H=(0, 2), S=(0, 2))},
    "valg": {"2♥": t((8, 14), H=(5, 5), S=(4, 4)), "2♠": t((8, 14), S=(5, 5), H=(4, 4))},
}
PER_CALL = {"ind": 10, "svar": 10, "valg": 15}

def export_pool(path):
    return kbuild(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
