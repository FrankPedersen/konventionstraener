"""
Minimal constraint-based bridge hand dealer — no external dependencies.
Builds a hand to match a shape first (incl. "free suit" roles like marmic's
unspecified short suit), then fills honours to hit an hp AND sp target
range simultaneously. The honour-fill step is retried first; if it keeps
missing, the generator draws a new shape and tries again. sp uses the 5/3/1 shortness scale (renonce/singleton/dobbelt).

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

def fmt(hand):
    names = {14:'E',13:'K',12:'D',11:'B',10:'10'}
    out = []
    for s in SUITS:
        cards = hand[s]
        out.append(''.join(names.get(r, str(r)) for r in cards) or '—')
    return ' / '.join(f"{s}:{c}" for s, c in zip(['♠','♥','♦','♣'], out))

def export_pool(path, n_per_category=20):
    import json
    cats = {
        "multi_2klor_54": gen_5_4_majors,
        "multi_2klor_marmic": gen_marmic_majors,
        "dobling_2klor_relae": gen_double_relay_hand,
    }
    pool = {}
    for key, fn in cats.items():
        hands = []
        tries = 0
        while len(hands) < n_per_category and tries < n_per_category * 30:
            tries += 1
            r = fn()
            if r:
                hand, hp, sp = r
                hands.append({
                    "hand": {s: hand[s] for s in SUITS},
                    "hp": hp, "sp": sp
                })
        pool[key] = hands
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)
    return {k: len(v) for k, v in pool.items()}

def main():
    samples = [
        ("2♣: 5-4 i majorerne", gen_5_4_majors),
        ("2♣: marmic med begge majorer", gen_marmic_majors),
        ("Dobling: 2♣-relæ (svag, ingen 5-farve)", gen_double_relay_hand),
    ]
    for title, fn in samples:
        print(f"=== {title} ===")
        for _ in range(4):
            r = fn()
            if r:
                hand, hp, sp = r
                print(f"{fmt(hand)}   [{hp} hp / {sp} sp]")
        print()

    print("=== Eksport til JSON-pulje ===")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hand_pool_sample.json')
    counts = export_pool(path, n_per_category=20)
    print(counts)

if __name__ == '__main__':
    main()
