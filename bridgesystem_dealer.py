"""
Minimal constraint-based bridge hand dealer — no external dependencies.
Builds a hand to match a shape first (incl. "free suit" roles like marmic's
unspecified short suit), then fills honours to hit an hp AND sp target
range simultaneously. The honour-fill step is retried first; if it keeps
missing, the generator draws a new shape and tries again. sp uses the 5/3/1
shortness scale (renonce/singleton/dobbelt).

export_pool() writes the trainer's hand pool: hands for the auctions
1NT – 2♣/2♦/2♥ – pas – 2NT – pas – ?, each with its correct rebid worked out
from the Jyderup Bridgeklub multiforsvar card.

Verified runnable in this sandbox — no pip install required.
"""
import os
import random

SUITS = ['S', 'H', 'D', 'C']  # spar, hjerter, ruder, klør
RANKS = list(range(2, 15))     # 2..14 (14 = es)
HP = {14: 4, 13: 3, 12: 2, 11: 1}
SHORTNESS_SP = {0: 5, 1: 3, 2: 1}  # renonce / singleton / dobbeltton

def hp_of(cards):
    return sum(HP.get(r, 0) for r in cards)

def sp_of(lengths, hp):
    short = sum(SHORTNESS_SP.get(l, 0) for l in lengths.values())
    return hp + short

def deal_suit_lengths(fixed):
    """fixed: dict suit -> (min,max). Returns a concrete length per suit
    summing to 13, respecting each suit's bounds."""
    remaining = 13
    lengths = {}
    suits = list(fixed.keys())
    random.shuffle(suits)
    for i, s in enumerate(suits):
        lo, hi = fixed[s]
        # leave enough room for the remaining suits' minimums
        rest_min = sum(fixed[x][0] for x in suits[i+1:])
        hi_eff = min(hi, remaining - rest_min)
        lo_eff = max(lo, 0)
        if lo_eff > hi_eff:
            return None
        lengths[s] = random.randint(lo_eff, hi_eff)
        remaining -= lengths[s]
    if remaining != 0:
        return None
    return lengths

def fill_hand(lengths, hp_range, sp_range, max_tries=400):
    """Given fixed suit lengths, deal random cards per suit until the
    resulting hp and sp both land in range."""
    for _ in range(max_tries):
        hand = {}
        for s in SUITS:
            hand[s] = sorted(random.sample(RANKS, lengths[s]), reverse=True)
        hp = hp_of([r for cs in hand.values() for r in cs])
        sp = sp_of(lengths, hp)
        if hp_range[0] <= hp <= hp_range[1] and sp_range[0] <= sp <= sp_range[1]:
            return hand, hp, sp
    return None

def gen_5_4_majors(hp_range=(10,16), sp_range=(0,37), shape_tries=20):
    """Multi 2♣: begge majorer, 5-4 (den ene vej eller den anden).
    Minorerne er højst 3 lange — 5-4-4-0 hører under marmic."""
    for _ in range(shape_tries):
        order = random.choice([('S','H'), ('H','S')])
        long_s, short_s = order
        fixed = {long_s: (5,5), short_s: (4,4), 'D': (0,3), 'C': (0,3)}
        # split the remaining 4 cards across the minors: 3-1, 2-2 or 1-3
        lengths = None
        for _ in range(50):
            lengths = deal_suit_lengths(fixed)
            if lengths: break
        if not lengths: continue
        r = fill_hand(lengths, hp_range, sp_range)
        if r: return r
    return None

def gen_marmic_majors(hp_range=(10,16), sp_range=(0,37), shape_tries=20):
    """Multi 2♣: marmic med begge majorer — 4-4-4-1 eller 5-4-4-0,
    hvor den korte/udeladte rolle går til én af minorerne."""
    for _ in range(shape_tries):
        pattern = random.choice(['4441','5440'])
        short_minor = random.choice(['D','C'])
        long_minor = 'C' if short_minor == 'D' else 'D'
        if pattern == '4441':
            lengths = {'S':4, 'H':4, long_minor:4, short_minor:1}
        else:
            five_suit = random.choice(['S','H',long_minor])
            lengths = {'S':4, 'H':4, long_minor:4, short_minor:0}
            lengths[five_suit] = 5
        r = fill_hand(lengths, hp_range, sp_range)
        if r: return r
    return None

def gen_double_relay_hand(hp_range=(0,9), sp_range=(0,12)):
    """Avancer efter makkers dobling, 2♣-relæ: ingen 5-farve, svag hånd."""
    for _ in range(200):
        lengths = deal_suit_lengths({'S':(0,4),'H':(0,4),'D':(0,4),'C':(0,4)})
        if lengths and max(lengths.values()) <= 4:
            r = fill_hand(lengths, hp_range, sp_range, max_tries=200)
            if r: return r
    return None

def gen_one_suited_major(hp_range=(10,16), sp_range=(0,37), shape_tries=20):
    """Multi 2♦: énfarvet major — 6-7 kort i majoren, ingen anden 4-farve."""
    for _ in range(shape_tries):
        major = random.choice(['S','H'])
        fixed = {x: (0,3) for x in SUITS}
        fixed[major] = (6,7)
        lengths = None
        for _ in range(50):
            lengths = deal_suit_lengths(fixed)
            if lengths: break
        if not lengths: continue
        r = fill_hand(lengths, hp_range, sp_range)
        if r: return r
    return None

def gen_hearts_minor(hp_range=(10,16), sp_range=(0,37), shape_tries=20):
    """Multi 2♥: 5 hjerter + 4-korts minor."""
    for _ in range(shape_tries):
        minor = random.choice(['D','C'])
        fixed = {'S': (0,3), 'H': (5,5), 'D': (0,3), 'C': (0,3)}
        fixed[minor] = (4,4)
        lengths = None
        for _ in range(50):
            lengths = deal_suit_lengths(fixed)
            if lengths: break
        if not lengths: continue
        r = fill_hand(lengths, hp_range, sp_range)
        if r: return r
    return None

def fmt(hand):
    names = {14:'E',13:'K',12:'D',11:'B',10:'10'}
    out = []
    for s in SUITS:
        cards = hand[s]
        out.append(''.join(names.get(r, str(r)) for r in cards) or '—')
    return ' / '.join(f"{s}:{c}" for s, c in zip(['♠','♥','♦','♣'], out))

# --- Facit: genmelding efter makkers 2NT-spørgsmål ------------------------

SUIT_SYM = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
SUIT_NAME = {'S': 'spar', 'H': 'hjerter', 'D': 'ruder', 'C': 'klør'}
MIN_RANGE, MAX_RANGE = (10, 13), (14, 16)

def strength(hp):
    if hp >= MAX_RANGE[0]:
        return f"{hp} hp er maximum (14–16)"
    return f"{hp} hp er minimum (10–13)"

def lengths_of(hand):
    return {s: len(hand[s]) for s in SUITS}

def answer_after_2kl(hand, hp):
    """2kl – 2nt: 3kl min 5-4/4-5, 3ru min 4-4, 3hj max 4-5, 3sp max 5-4,
    3nt max lige længde, 4mi renonce."""
    L = lengths_of(hand)
    voids = [m for m in ('D', 'C') if L[m] == 0]
    if voids:
        m = voids[0]
        return f"4{SUIT_SYM[m]}", (f"Du har renonce i {SUIT_NAME[m]}. Efter 2♣ – 2NT viser "
                                  f"4{SUIT_SYM[m]} renonce i farven.")
    maximum = hp >= MAX_RANGE[0]
    s, h = L['S'], L['H']
    if s == h:
        if maximum:
            return "3NT", f"{strength(hp)}, og majorerne er lige lange ({s}-{h}). 3NT viser maximum med lige længde."
        return "3♦", f"{strength(hp)}, og majorerne er lige lange ({s}-{h}). 3♦ viser minimum med 4-4."
    if not maximum:
        return "3♣", (f"{strength(hp)} med {s} spar og {h} hjerter. 3♣ viser minimum med 5-4 eller 4-5 "
                      f"— makker kan derefter søge 5-farven med 3♦.")
    if s > h:
        return "3♠", f"{strength(hp)} med 5 spar og 4 hjerter. 3♠ viser maximum med 5-4."
    return "3♥", f"{strength(hp)} med 4 spar og 5 hjerter. 3♥ viser maximum med 4-5."

def answer_after_2ru(hand, hp):
    """2ru – 2nt: 3kl min hjerter, 3ru min spar, 3hj max hjerter, 3sp max spar."""
    L = lengths_of(hand)
    major = 'S' if L['S'] >= 6 else 'H'
    maximum = hp >= MAX_RANGE[0]
    call = {('H', False): '3♣', ('S', False): '3♦', ('H', True): '3♥', ('S', True): '3♠'}[(major, maximum)]
    return call, (f"{strength(hp)}, og din farve er {SUIT_NAME[major]}. Efter 2♦ – 2NT: 3♣ = min med hjerter, "
                  f"3♦ = min med spar, 3♥ = max med hjerter, 3♠ = max med spar.")

def answer_after_2hj(hand, hp):
    """2hj – 2nt: 3kl min klør, 3ru min ruder, 3hj max klør, 3sp max ruder."""
    L = lengths_of(hand)
    minor = 'C' if L['C'] == 4 else 'D'
    maximum = hp >= MAX_RANGE[0]
    call = {('C', False): '3♣', ('D', False): '3♦', ('C', True): '3♥', ('D', True): '3♠'}[(minor, maximum)]
    return call, (f"{strength(hp)}, og din sidefarve er {SUIT_NAME[minor]}. Efter 2♥ – 2NT: 3♣ = min med klør, "
                  f"3♦ = min med ruder, 3♥ = max med klør, 3♠ = max med ruder.")

SITUATIONS = {
    "2kl": {
        "auction": ["1NT", "2♣", "2NT"],
        "calls": ["3♣", "3♦", "3♥", "3♠", "3NT", "4♣", "4♦"],
        "bonus": {"q": "Hvad viste din 2♣-indmelding?",
                  "correct": "Begge majorer, typisk 5-4 eller god marmic",
                  "options": ["Begge majorer, typisk 5-4 eller god marmic", "Énfarvet major", "Begge minorer, 5/4+"],
                  "why": "2♣ viser begge majorer, typisk 5-4 eller god marmic — 10–16 hp, fordeling kan kompensere."},
    },
    "2ru": {
        "auction": ["1NT", "2♦", "2NT"],
        "calls": ["3♣", "3♦", "3♥", "3♠"],
        "bonus": {"q": "Hvad viste din 2♦-indmelding?",
                  "correct": "Énfarvet major",
                  "options": ["Énfarvet major", "Naturlig ruderfarve", "Begge majorer, typisk 5-4"],
                  "why": "2♦ viser en énfarvet major — 10–16 hp, fordeling kan kompensere."},
    },
    "2hj": {
        "auction": ["1NT", "2♥", "2NT"],
        "calls": ["3♣", "3♦", "3♥", "3♠"],
        "bonus": {"q": "Hvad viste din 2♥-indmelding?",
                  "correct": "Hjerter + minor, 5-4",
                  "options": ["Hjerter + minor, 5-4", "Énfarvet hjerter", "Begge majorer, typisk 5-4"],
                  "why": "2♥ viser hjerter + en minor, 5-4 — 10–16 hp, fordeling kan kompensere."},
    },
}

# situation, generator, facit, antal hænder (halvdelen minimum, halvdelen maximum)
POOL_PLAN = [
    ("2kl", gen_5_4_majors, answer_after_2kl, 60),
    ("2kl", gen_marmic_majors, answer_after_2kl, 40),
    ("2ru", gen_one_suited_major, answer_after_2ru, 50),
    ("2hj", gen_hearts_minor, answer_after_2hj, 50),
]

def export_pool(path):
    import json
    hands, seen = [], set()
    for situation, gen, answer, count in POOL_PLAN:
        for hp_range, n in ((MIN_RANGE, count // 2), (MAX_RANGE, count - count // 2)):
            made, tries = 0, 0
            while made < n and tries < n * 30:
                tries += 1
                r = gen(hp_range=hp_range)
                if not r: continue
                hand, hp, sp = r
                key = tuple(tuple(hand[s]) for s in SUITS)
                if key in seen: continue
                seen.add(key)
                correct, why = answer(hand, hp)
                hands.append({"situation": situation,
                              "hand": {s: hand[s] for s in SUITS},
                              "hp": hp, "sp": sp, "correct": correct, "why": why})
                made += 1
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"situations": SITUATIONS, "hands": hands}, f, ensure_ascii=False, indent=1)
    counts = {}
    for h in hands:
        counts[h["situation"]] = counts.get(h["situation"], 0) + 1
    return counts

def main():
    samples = [
        ("1NT – 2♣ – 2NT: 5-4 i majorerne", gen_5_4_majors, answer_after_2kl),
        ("1NT – 2♣ – 2NT: marmic med begge majorer", gen_marmic_majors, answer_after_2kl),
        ("1NT – 2♦ – 2NT: énfarvet major", gen_one_suited_major, answer_after_2ru),
        ("1NT – 2♥ – 2NT: hjerter + minor", gen_hearts_minor, answer_after_2hj),
    ]
    for title, gen, answer in samples:
        print(f"=== {title} ===")
        for _ in range(4):
            r = gen()
            if r:
                hand, hp, sp = r
                print(f"{fmt(hand)}   [{hp} hp / {sp} sp]  → {answer(hand, hp)[0]}")
        print()

    print("=== Eksport til JSON-pulje ===")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hand_pool_sample.json')
    print(export_pool(path))

if __name__ == '__main__':
    main()
