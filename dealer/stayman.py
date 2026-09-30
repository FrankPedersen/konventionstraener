"""
Stayman – Karina & Frank, systemkortets afsnit 2.2 og 3.

1NT = 15–17 og må rumme en 5-farve i major. 2♣ er Stayman; med 5-farve i major melder åbner den,
som var det en 4-farve. 2NT er naturlig invit, 8–9 hp jævn uden 4-farve i major. Puljen dækker:
  svar_1nt – svarer over 1NT: 2♣ med en 4-farve i major og 8+ hp · 2NT 8–9 jævn uden 4-farve i major ·
             3NT 10–15 jævn uden 4-farve i major · pas 0–7
  aabner   – åbners svar på 2♣: 2♦ ingen 4-farve i major · 2♥ 4+ hjerter · 2♠ 4+ spar, ikke 4 hjerter
Antagelser (kortet siger det ikke): Stayman kræver 8+ hp; 3NT er 10–15; med 4-4 i majorerne svarer
åbner 2♥. Svarers melding efter åbners svar er ikke med – kortet beskriver den ikke.
Hænder med 5+ i major (transfer), 6+ i minor og 16+ hp er ikke med.
"""
from .core import SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

BALANCED = ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def balanced(L):
    return sorted(L.values()) in BALANCED

def classify_first(hand, hp):
    L = lengths_of(hand)
    if L['S'] > 4 or L['H'] > 4 or L['D'] > 5 or L['C'] > 5 or hp > 15 or min(L.values()) == 0:
        return None
    four = [s for s in ('H', 'S') if L[s] == 4]
    if four:
        if hp >= 8:
            names = " og ".join(f"4 {SUIT_NAME[s]}" for s in four)
            return "2♣", f"{names} og {hp} hp: 2♣ Stayman spørger efter åbners 4-farve i major."
        return "Pas", f"{hp} hp er for lidt til Stayman (8+). Pas."
    if not balanced(L):
        return None
    if hp <= 7:
        return "Pas", f"Jævn hånd med {hp} hp: pas."
    if hp <= 9:
        return "2NT", f"Jævn hånd uden 4-farve i major og {hp} hp: 2NT er naturlig invit (8–9)."
    return "3NT", f"Jævn hånd uden 4-farve i major og {hp} hp: 3NT."

def classify_opener(hand, hp):
    L = lengths_of(hand)
    if not (15 <= hp <= 17) or not balanced(L):
        return None
    five = " – 5-farven meldes, som var det en 4-farve" if 5 in (L['H'], L['S']) else ""
    if L['H'] >= 4:
        both = " – med begge majorer svarer du 2♥ først" if L['S'] >= 4 else ""
        return "2♥", f"{L['H']} hjerter: 2♥{five}{both}."
    if L['S'] >= 4:
        return "2♠", f"{L['S']} spar og ikke 4 hjerter: 2♠{five}."
    return "2♦", "Ingen 4-farve i major: 2♦."

BONUS = {
    "svar": {"q": "Hvad viser makkers 1NT-åbning?",
             "correct": "15–17 hp – må rumme 5-farve i major",
             "options": ["15–17 hp – må rumme 5-farve i major", "12–14 hp jævn", "20–21 hp jævn"],
             "why": "1NT er 15–17 hp og må rumme en 5-farve i major. 2NT er 20–21."},
    "aabner": {"q": "Hvad spørger makkers 2♣ om?",
               "correct": "Om du har en 4-farve i major",
               "options": ["Om du har en 4-farve i major", "Om du har en 5-farve i minor", "Om du har minimum eller maksimum"],
               "why": "2♣ er Stayman og spørger efter en 4-farve i major. En 5-farve i major meldes, som var det en 4-farve."},
}

PAS = ["Modstander", "Pas"]
SITUATIONS = {
    "svar_1nt": {"rolle": "Svarer", "auction": [["Makker", "1NT"], PAS],
                 "calls": ["Pas", "2♣", "2♦", "2♥", "2NT", "3NT"], "bonus": BONUS["svar"]},
    "aabner": {"rolle": "Åbner", "auction": [["Dig", "1NT"], PAS, ["Makker", "2♣"], PAS],
               "calls": ["2♦", "2♥", "2♠", "2NT", "3NT"], "bonus": BONUS["aabner"]},
}
CLASSIFIERS = {"svar_1nt": classify_first, "aabner": classify_opener}

def resp(hp, **b):
    return tpl(hp, **{'S': (1, 4), 'H': (1, 4), 'D': (1, 5), 'C': (1, 5), **b})

SAMPLERS = {
    "svar_1nt": {"Pas": resp((2, 7), S=(2, 4), H=(2, 4), D=(2, 5), C=(2, 5)),
                 "2♣": either(resp((8, 15), S=(4, 4)), resp((8, 15), H=(4, 4))),
                 "2NT": resp((8, 9), S=(2, 3), H=(2, 3), D=(2, 5), C=(2, 5)),
                 "3NT": resp((10, 15), S=(2, 3), H=(2, 3), D=(2, 5), C=(2, 5))},
    "aabner": {"2♦": tpl((15, 17), S=(2, 3), H=(2, 3), D=(2, 5), C=(2, 5)),
               "2♥": either(tpl((15, 17), H=(4, 5), S=(2, 3), D=(2, 4), C=(2, 4)), tpl((15, 17), H=(4, 4), S=(4, 4), D=(2, 3), C=(2, 3))),
               "2♠": tpl((15, 17), S=(4, 5), H=(2, 3), D=(2, 4), C=(2, 4))},
}
PER_CALL = {"svar_1nt": 25, "aabner": 33}

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
