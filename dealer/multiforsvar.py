"""
Multiforsvar mod 1NT (Jyderup Bridgeklub / systemkortets afsnit 8.1).

Puljen dækker hænder, hvor du enten er indmelder (1NT – ?, eller genmeldingen
efter makkers 2NT-spørgsmål) eller svarer (1NT – X/2♣/2♦/2♥ – pas – ?).
Facit regnes ud af klassifikatorerne herunder. Grænser, som systemkortet ikke
angiver, står som konstanter i afsnittet 'indmelding'.
"""
import random

from .core import (SUITS, SUIT_SYM, SUIT_NAME, deal_suit_lengths, fill_hand, fmt,
                   lengths_of, longer, deal_random, template, rnd, tpl, either,
                   two_suiter, export)

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

# --- Facit: genmelding efter makkers 2NT-spørgsmål ------------------------

MIN_RANGE, MAX_RANGE = (10, 13), (14, 16)

def strength(hp):
    if hp >= MAX_RANGE[0]:
        return f"{hp} hp er maximum (14–16)"
    return f"{hp} hp er minimum (10–13)"

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

# --- Facit: indmelding over 1NT og svar på makkers indmelding ---------------
# Grænser som dokumentet ikke giver tal for — ret dem her.

DOUBLE_MIN = 15        # D: "mindst samme styrke som sansåbner"; 15–16 dobler kun uden fordelingsmelding
PREEMPT_HP = (6, 9)    # 3M spær: 7+ major, under indmeldingsstyrke
GAME_MAJOR_HP = 13     # 4M: 7+ major og 13–16 hp; 7+ major med 10–12 melder 2♦
ADV_STRONG = 11        # svarer: 11+ hp = udgangsinteresse (2NT spørger, 3mi krav osv.)
ADV_3NT = {"2kl": 13, "2ru": 14}   # svarer: 3NT for at spille uden majorfit
ADV_INVITE = 8         # svarer efter 2♦: 2♠ = invit med hjerter, 8–10 hp
ADV_PREEMPT_MAX = 7    # svarer efter 2♦: 3♥ = spær i makkers farve, 0–7 hp
NILSLAND_MAX = 7       # svarer efter D (fjenden spiller Nilsland): svage hænder 0–7 hp

def classify_overcall(hand, hp):
    """1NT – ? : multiforsvarets indmeldinger (10–16, fordeling kan kompensere)."""
    L = lengths_of(hand)
    S, H, D, C = L['S'], L['H'], L['D'], L['C']
    major, minor = longer(L, 'S', 'H'), longer(L, 'D', 'C')
    if hp > 16:
        return "X", f"{hp} hp er over indmeldingsstyrke (10–16). D viser mindst samme styrke som sansåbneren."
    if PREEMPT_HP[0] <= hp <= PREEMPT_HP[1] and L[major] >= 7:
        return f"3{SUIT_SYM[major]}", f"{L[major]} {SUIT_NAME[major]} og kun {hp} hp: 3{SUIT_SYM[major]} er spær."
    if hp < 10:
        return "Pas", f"{hp} hp er under indmeldingsstyrke (10–16), og hånden har ikke en spærrefarve."
    if L[major] >= 7 and hp >= GAME_MAJOR_HP:
        return f"4{SUIT_SYM[major]}", f"{L[major]} {SUIT_NAME[major]} og {hp} hp: 4{SUIT_SYM[major]} for at spille."
    if L[minor] >= 7 and {14, 13, 12} <= set(hand[minor]):
        return "3NT", f"Gående {SUIT_NAME[minor]}farve (E K D + {L[minor] - 3}): 3NT for at spille."
    if S >= 4 and H >= 4 and (max(S, H) >= 5 or min(D, C) <= 1):
        kind = "5-4 i majorerne" if max(S, H) >= 5 else "marmic med begge majorer"
        return "2♣", f"{hp} hp og {kind}: 2♣ viser begge majorer, typisk 5-4 eller god marmic."
    if L[major] >= 6:
        return "2♦", f"{L[major]} {SUIT_NAME[major]} og {hp} hp: 2♦ viser en énfarvet major."
    for M in ('S', 'H'):
        if L[M] == 5 and L[minor] >= 4:
            return f"2{SUIT_SYM[M]}", (f"5 {SUIT_NAME[M]} og {L[minor]} {SUIT_NAME[minor]}: 2{SUIT_SYM[M]} viser "
                                       f"{SUIT_NAME[M]} + minor 5-4.")
    if D >= 4 and C >= 4 and max(D, C) >= 5:
        return "2NT", f"{D} ruder og {C} klør: 2NT viser begge minorer, 5/4+."
    if L[minor] >= 6:
        return f"3{SUIT_SYM[minor]}", f"{L[minor]} {SUIT_NAME[minor]} og {hp} hp: 3{SUIT_SYM[minor]} er naturligt."
    if hp >= DOUBLE_MIN:
        return "X", f"{hp} hp uden en fordeling, der passer til en indmelding: D viser mindst samme styrke som sansåbneren."
    return "Pas", f"{hp} hp, men ingen fordeling, der passer til en indmelding — og for svag til D."

def classify_after_2kl(hand, hp):
    """1NT – 2♣ – pas – ? : makker har begge majorer."""
    L = lengths_of(hand)
    S, H = L['S'], L['H']
    major, minor = longer(L, 'S', 'H'), longer(L, 'D', 'C')
    if hp >= ADV_STRONG:
        if max(S, H) <= 3 and L[minor] >= 5:
            return f"3{SUIT_SYM[minor]}", f"{hp} hp og {L[minor]} {SUIT_NAME[minor]} uden majorfit: 3{SUIT_SYM[minor]} er naturligt, 5+ farve og krav."
        if max(S, H) <= 3 and hp >= ADV_3NT["2kl"]:
            return "3NT", f"{hp} hp uden majorfit: 3NT for at spille."
        return "2NT", f"{hp} hp giver udgangsinteresse: 2NT spørger om makkers styrke og fordeling."
    if L[major] >= 5:
        return f"3{SUIT_SYM[major]}", f"Svag hånd med {L[major]} {SUIT_NAME[major]} — mindst 9 kort sammen: 3{SUIT_SYM[major]} er spær."
    if S == H:
        return "2♦", f"Svag hånd med lige mange spar og hjerter ({S}-{H}): 2♦ beder makker vælge farve."
    return f"2{SUIT_SYM[major]}", f"Svag hånd med flest {SUIT_NAME[major]} ({S} spar, {H} hjerter): 2{SUIT_SYM[major]} for at spille."

def classify_after_2ru(hand, hp):
    """1NT – 2♦ – pas – ? : makker har en énfarvet major."""
    L = lengths_of(hand)
    S, H = L['S'], L['H']
    major, minor = longer(L, 'S', 'H'), longer(L, 'D', 'C')
    if hp >= ADV_STRONG:
        if L[major] >= 6:
            return f"4{SUIT_SYM[major]}", f"{hp} hp og {L[major]} {SUIT_NAME[major]}: 4{SUIT_SYM[major]} for at spille i egen farve."
        if L[minor] >= 5:
            return f"3{SUIT_SYM[minor]}", f"{hp} hp og {L[minor]} {SUIT_NAME[minor]}: 3{SUIT_SYM[minor]} er naturligt, 5+ farve og krav."
        if hp >= ADV_3NT["2ru"]:
            return "3NT", f"{hp} hp og ingen lang farve: 3NT for at spille."
        return "2NT", f"{hp} hp giver udgangsinteresse: 2NT spørger."
    if hp <= ADV_PREEMPT_MAX and S >= 3 and H >= 3 and max(S, H) >= 4:
        return "3♥", f"Svag hånd med fit i begge majorer ({S} spar, {H} hjerter): 3♥ er spær i makkers farve."
    if hp >= ADV_INVITE and H >= 3 and S >= 2:
        return "2♠", f"{hp} hp med {H} hjerter: 2♠ er invit med hjerter — makker passer, hvis farven er spar."
    return "2♥", f"Svag hånd ({hp} hp): 2♥ søger makkers farve for at spille."

def classify_after_2hj(hand, hp):
    """1NT – 2♥ – pas – ? : makker har hjerter + minor 5-4."""
    L = lengths_of(hand)
    S, H, D, C = L['S'], L['H'], L['D'], L['C']
    if hp >= ADV_STRONG:
        if S >= 5 and H <= 2:
            return "2♠", f"{hp} hp og {S} spar uden hjertefit: 2♠ er naturligt og krav."
        if D >= 5 and H <= 2:
            return "3♦", f"{hp} hp og {D} ruder uden hjertefit: 3♦ er egen minorfarve og krav."
        return "2NT", f"{hp} hp giver udgangsinteresse: 2NT spørger."
    if H >= 4:
        return "3♥", f"Svag hånd med {H} hjerter: 3♥ er spær."
    if H <= 1 and D >= 3 and C >= 3:
        return "3♣", f"Svag hånd med kun {H} hjerter, men plads i begge minorer: 3♣ søger makkers minorfarve."
    return "Pas", f"Svag hånd ({hp} hp) med {H} hjerter: pas og spil 2♥."

def classify_after_double(hand, hp):
    """1NT – D – pas – ? (fjenden spiller Nilsland): svage hænder."""
    L = lengths_of(hand)
    if hp > NILSLAND_MAX:
        return None
    long_suits = [s for s in SUITS if L[s] >= 4]
    if len(long_suits) == 1 and L[long_suits[0]] >= 5:
        s = long_suits[0]
        return f"2{SUIT_SYM[s]}", f"Svag énfarvet hånd med {L[s]} {SUIT_NAME[s]}: 1NT – D – pas – 2{SUIT_SYM[s]}."
    if len(long_suits) == 2:
        a, b = long_suits
        return "Pas", (f"Svag tofarvet hånd ({SUIT_NAME[a]} og {SUIT_NAME[b]}): pas nu, og efter RD – pas – pas "
                       f"meldes 2 i den laveste farve.")
    return None

# --- Situationer ------------------------------------------------------------

BONUS = {
    "2kl": {"q": "Hvad viser 2♣-indmeldingen?",
            "correct": "Begge majorer, typisk 5-4 eller god marmic",
            "options": ["Begge majorer, typisk 5-4 eller god marmic", "Énfarvet major", "Begge minorer, 5/4+"],
            "why": "2♣ viser begge majorer, typisk 5-4 eller god marmic — 10–16 hp, fordeling kan kompensere."},
    "2ru": {"q": "Hvad viser 2♦-indmeldingen?",
            "correct": "Énfarvet major",
            "options": ["Énfarvet major", "Naturlig ruderfarve", "Begge majorer, typisk 5-4"],
            "why": "2♦ viser en énfarvet major — 10–16 hp, fordeling kan kompensere."},
    "2hj": {"q": "Hvad viser 2♥-indmeldingen?",
            "correct": "Hjerter + minor, 5-4",
            "options": ["Hjerter + minor, 5-4", "Énfarvet hjerter", "Begge majorer, typisk 5-4"],
            "why": "2♥ viser hjerter + en minor, 5-4 — 10–16 hp, fordeling kan kompensere."},
    "indmelding": {"q": "Hvilken styrke viser multiforsvarets indmeldinger (andre end D)?",
            "correct": "10–16 hp, fordeling kan kompensere",
            "options": ["10–16 hp, fordeling kan kompensere", "8–12 hp", "Mindst samme styrke som sansåbner"],
            "why": "Alle meldinger i multiforsvaret viser 10–16 hp (fordeling kan kompensere) — undtagen D, som viser mindst samme styrke som sansåbneren."},
    "dobling": {"q": "Hvad sker der, når makker dobler 1NT?",
            "correct": "Der er etableret semikrav, og senere doblinger er straf",
            "options": ["Der er etableret semikrav, og senere doblinger er straf", "Du skal altid melde en farve", "Doblingen er til udspil"],
            "why": "Når makker dobler, er der etableret semikrav. I det videre meldeforløb benyttes strafdoblinger."},
}

PAS = ["Modstander", "Pas"]
SITUATIONS = {
    "indmelding": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"]], "allowX": True,
                   "calls": ["X", "Pas", "2♣", "2♦", "2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "3NT", "4♥", "4♠"],
                   "bonus": BONUS["indmelding"]},
    "gen_2kl": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♣"], PAS, ["Makker", "2NT"], PAS],
                "calls": ["3♣", "3♦", "3♥", "3♠", "3NT", "4♣", "4♦"], "bonus": BONUS["2kl"]},
    "gen_2ru": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♦"], PAS, ["Makker", "2NT"], PAS],
                "calls": ["3♣", "3♦", "3♥", "3♠"], "bonus": BONUS["2ru"]},
    "gen_2hj": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♥"], PAS, ["Makker", "2NT"], PAS],
                "calls": ["3♣", "3♦", "3♥", "3♠"], "bonus": BONUS["2hj"]},
    "svar_2kl": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♣"], PAS],
                 "calls": ["2♦", "2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "3NT"], "bonus": BONUS["2kl"]},
    "svar_2ru": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♦"], PAS],
                 "calls": ["2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3NT", "4♥", "4♠"], "bonus": BONUS["2ru"]},
    "svar_2hj": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♥"], PAS],
                 "calls": ["Pas", "2♠", "2NT", "3♣", "3♦", "3♥"], "bonus": BONUS["2hj"]},
    "svar_dobling": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "X"], PAS],
                     "calls": ["Pas", "2♣", "2♦", "2♥", "2♠"], "bonus": BONUS["dobling"]},
}

CLASSIFIERS = {
    "indmelding": classify_overcall,
    "gen_2kl": answer_after_2kl, "gen_2ru": answer_after_2ru, "gen_2hj": answer_after_2hj,
    "svar_2kl": classify_after_2kl, "svar_2ru": classify_after_2ru,
    "svar_2hj": classify_after_2hj, "svar_dobling": classify_after_double,
}

SAMPLERS = {
    "indmelding": {
        "X": rnd((15, 19)), "Pas": rnd((4, 14)),
        "2♣": either(gen_5_4_majors, gen_marmic_majors), "2♦": gen_one_suited_major,
        "2♥": either(tpl((10, 16), H=(5, 5), D=(4, 5)), tpl((10, 16), H=(5, 5), C=(4, 5))),
        "2♠": either(tpl((10, 16), S=(5, 5), D=(4, 5)), tpl((10, 16), S=(5, 5), C=(4, 5))),
        "2NT": tpl((10, 16), D=(4, 6), C=(4, 6)),
        "3♣": tpl((10, 16), C=(6, 7)), "3♦": tpl((10, 16), D=(6, 7)),
        "3♥": tpl(PREEMPT_HP, H=(7, 8)), "3♠": tpl(PREEMPT_HP, S=(7, 8)),
        "3NT": either(tpl((10, 16), C=(7, 8)), tpl((10, 16), D=(7, 8))),
        "4♥": tpl((GAME_MAJOR_HP, 16), H=(7, 8)), "4♠": tpl((GAME_MAJOR_HP, 16), S=(7, 8)),
    },
    "svar_2kl": {
        "2♦": rnd((0, 10)), "2♥": rnd((0, 10)), "2♠": rnd((0, 10)), "2NT": rnd((11, 16)),
        "3♣": tpl((11, 16), C=(5, 6), D=(0, 4)), "3♦": tpl((11, 16), D=(5, 6), C=(0, 4)),
        "3♥": tpl((0, 10), H=(5, 6), D=(0, 4), C=(0, 4)), "3♠": tpl((0, 10), S=(5, 6), D=(0, 4), C=(0, 4)),
        "3NT": tpl((13, 17), S=(2, 3), H=(2, 3), D=(2, 4), C=(2, 4)),
    },
    "svar_2ru": {
        "2♥": rnd((0, 10)), "2♠": rnd((ADV_INVITE, 10)), "2NT": rnd((11, 13)),
        "3♣": tpl((11, 16), C=(5, 6), S=(0, 4), H=(0, 4), D=(0, 4)),
        "3♦": tpl((11, 16), D=(5, 6), S=(0, 4), H=(0, 4), C=(0, 4)),
        "3♥": tpl((0, ADV_PREEMPT_MAX), S=(3, 4), H=(3, 4), D=(0, 5), C=(0, 5)),
        "3NT": tpl((14, 17), S=(2, 4), H=(2, 4), D=(2, 4), C=(2, 4)),
        "4♥": tpl((11, 16), H=(6, 7)), "4♠": tpl((11, 16), S=(6, 7)),
    },
    "svar_2hj": {
        "2♠": tpl((11, 16), S=(5, 6), H=(0, 2), D=(0, 4), C=(0, 4)), "2NT": rnd((11, 15)),
        "3♣": tpl((0, 10), H=(0, 1), D=(3, 6), C=(3, 6), S=(0, 5)),
        "3♦": tpl((11, 16), D=(5, 6), H=(0, 2), S=(0, 4), C=(0, 4)),
        "3♥": tpl((0, 10), H=(4, 5), S=(0, 5), D=(0, 5), C=(0, 5)), "Pas": rnd((0, 10)),
    },
    "svar_dobling": {
        "2♣": tpl((0, NILSLAND_MAX), C=(5, 6)), "2♦": tpl((0, NILSLAND_MAX), D=(5, 6)),
        "2♥": tpl((0, NILSLAND_MAX), H=(5, 6)), "2♠": tpl((0, NILSLAND_MAX), S=(5, 6)),
        "Pas": two_suiter((0, NILSLAND_MAX)),
    },
}

# Genmelding efter 2NT: situation, generator, antal (halvdelen minimum, halvdelen maximum)
REBID_PLAN = [
    ("gen_2kl", gen_5_4_majors, 8), ("gen_2kl", gen_marmic_majors, 6),
    ("gen_2ru", gen_one_suited_major, 8), ("gen_2hj", gen_hearts_minor, 8),
]
# Hænder pr. meldning i de øvrige situationer (indmelder 70 + 30 genmeldinger, svarer 100)
PER_CALL = {"indmelding": 5, "svar_2kl": 4, "svar_2ru": 4, "svar_2hj": 3, "svar_dobling": 2}

def export_pool(path):
    hands, seen = [], set()

    def add(situation, r, target=None):
        if not r:
            return False
        hand, hp, sp = r
        key = tuple(tuple(hand[s]) for s in SUITS)
        if key in seen:
            return False
        res = CLASSIFIERS[situation](hand, hp)
        if not res or (target and res[0] != target):
            return False
        seen.add(key)
        hands.append({"situation": situation, "hand": {s: hand[s] for s in SUITS},
                      "hp": hp, "sp": sp, "correct": res[0], "why": res[1]})
        return True

    for situation, n in PER_CALL.items():
        for call, sampler in SAMPLERS[situation].items():
            made = tries = 0
            while made < n and tries < 20000:
                tries += 1
                made += add(situation, sampler(), call)
            if made < n:
                print(f"Advarsel: kun {made}/{n} hænder til {situation} {call}")

    for situation, gen, count in REBID_PLAN:
        for hp_range, n in ((MIN_RANGE, count // 2), (MAX_RANGE, count - count // 2)):
            made = tries = 0
            while made < n and tries < n * 30:
                tries += 1
                made += add(situation, gen(hp_range=hp_range))

    return export(path, SITUATIONS, hands)
