"""
Fælles byggesten til konventionstrænerens hånd-dealere — ingen eksterne afhængigheder.

En hånd bygges i to trin: først fordelingen (farvelængder inden for grænser),
derefter honnørerne, som trækkes om, indtil hp og sp rammer de ønskede
intervaller. sp bruger kortfarveskalaen 5/3/1 (renonce/singleton/dobbeltton).

Hver konvention har sit eget modul (fx multiforsvar.py) med regler for facit,
situationer og en export_pool(); build_pools.py kører dem alle.
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

def fmt(hand):
    names = {14:'E',13:'K',12:'D',11:'B',10:'10'}
    out = []
    for s in SUITS:
        cards = hand[s]
        out.append(''.join(names.get(r, str(r)) for r in cards) or '—')
    return ' / '.join(f"{s}:{c}" for s, c in zip(['♠','♥','♦','♣'], out))

SUIT_SYM = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
SUIT_NAME = {'S': 'spar', 'H': 'hjerter', 'D': 'ruder', 'C': 'klør'}

def lengths_of(hand):
    return {s: len(hand[s]) for s in SUITS}

def longer(L, a, b):
    """The longer of two suits; ties go to the higher-ranking one."""
    return a if L[a] >= L[b] else b

# --- Samplers -----------------------------------------------------------------

def deal_random(hp_range):
    """A plain random 13-card hand within hp_range."""
    for _ in range(2000):
        cards = random.sample([(s, r) for s in SUITS for r in RANKS], 13)
        hand = {s: sorted((r for x, r in cards if x == s), reverse=True) for s in SUITS}
        hp = hp_of([r for _, r in cards])
        if hp_range[0] <= hp <= hp_range[1]:
            return hand, hp, sp_of(lengths_of(hand), hp)
    return None

def template(fixed, hp_range):
    """Deal suit lengths within fixed bounds, then fill honours to hp_range."""
    for _ in range(50):
        lengths = deal_suit_lengths(fixed)
        if lengths:
            return fill_hand(lengths, hp_range, (0, 40))
    return None

def rnd(hp_range):
    return lambda: deal_random(hp_range)

def tpl(hp_range, **bounds):
    fixed = {s: bounds.get(s, (0, 3)) for s in SUITS}
    return lambda: template(fixed, hp_range)

def either(*samplers):
    return lambda: random.choice(samplers)()

def two_suiter(hp_range):
    def sample():
        a, b = random.sample(SUITS, 2)
        return template({s: (4, 5) if s in (a, b) else (0, 3) for s in SUITS}, hp_range)
    return sample

def export(path, situations, hands):
    """Write a pool file: {"situations": {...}, "hands": [...]}. Returns counts per situation."""
    import json
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"situations": situations, "hands": hands}, f, ensure_ascii=False, indent=1)
    counts = {}
    for h in hands:
        counts[h["situation"]] = counts.get(h["situation"], 0) + 1
    return counts
