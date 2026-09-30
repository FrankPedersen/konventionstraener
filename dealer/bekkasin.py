"""
Bekkasin 2NT (systemkortets afsnit 4.1, 4.3 og 4.5).

Puljen dækker tre situationer, begge majorer:
  svar_1x  – svarer vælger støttemelding over makkers 1♥/1♠ (4+ korts støtte):
             3M 0–6 sp · 3♦ 7–10 sp · 3♣ 10–11 sp · 2NT (Bekkasin) 12+ sp · 4M 5-korts støtte 0–9 sp
  aabner_1x – åbner beskriver efter 1M – 2NT: 3♣ minimum (12–14) uden renonce · 3♦ 15+ uden kortfarve ·
             3♥ 15+ kort ruder · 3♠ 15+ kort klør · 3NT 15+ kort i den anden major · 4-trinnet renonce
  spm_1x   – åbner svarer på svarers 3♦-spørgsmål efter 1M – 2NT – 3♣:
             3♥ kort ruder · 3♠ kort klør · 3NT kort i den anden major · 4M ingen kortfarve
Kortfarve betyder singleton; renonce vises altid på 4-trinnet.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, export

OTHER = {'H': 'S', 'S': 'H'}
MIN_HP = (12, 14)       # åbners minimum efter Bekkasin
MAX_HP = (15, 21)
SUPPORT_SP = {"3M": (0, 6), "3♦": (7, 10), "3♣": (10, 11), "2NT": 12}   # præcis 10 sp: svarer vælger selv

def short_suits(L, M):
    """Suits other than the trump suit with at most one card."""
    return [s for s in SUITS if s != M and L[s] <= 1]

def void_call(s, M):
    """Renonce cuebiddes på 4-trinnet: 4♣/4♦ i minorerne, 4♥ for renonce i den anden major."""
    return "4♥" if s == OTHER[M] else f"4{SUIT_SYM[s]}"

def shortness_step(s, M):
    """Trinene for kortfarve: 3♥ kort ruder, 3♠ kort klør, 3NT kort i den anden major."""
    return {'D': "3♥", 'C': "3♠"}.get(s, "3NT")

def opener_rebid(M):
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or not (MIN_HP[0] <= hp <= MAX_HP[1]):
            return None
        short = short_suits(L, M)
        if len(short) > 1:
            return None      # to kortfarver beskriver skemaet ikke
        if short and L[short[0]] == 0:
            s = short[0]
            call = void_call(s, M)
            return call, (f"Renonce i {SUIT_NAME[s]}: renonce cuebiddes på 4-trinnet, så du melder {call} "
                          f"— uanset styrke.")
        if hp <= MIN_HP[1]:
            extra = f" Singletonen i {SUIT_NAME[short[0]]} kan makker spørge efter med 3♦." if short else ""
            return "3♣", f"{hp} hp er minimum (12–14) uden renonce: 3♣.{extra}"
        if not short:
            return "3♦", f"{hp} hp er tillæg (15+) uden kortfarve: 3♦."
        s = short[0]
        call = shortness_step(s, M)
        return call, f"{hp} hp er tillæg (15+) med singleton {SUIT_NAME[s]}: {call}."
    return classify

def opener_answer_to_ask(M):
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or not (MIN_HP[0] <= hp <= MIN_HP[1]):
            return None
        short = short_suits(L, M)
        if len(short) > 1 or (short and L[short[0]] == 0):
            return None      # med renonce havde åbner ikke meldt 3♣
        if not short:
            return f"4{SUIT_SYM[M]}", f"Ingen kortfarve — jævn minimumshånd: 4{SUIT_SYM[M]}. Svarer passer normalt."
        s = short[0]
        call = shortness_step(s, M)
        return call, f"Singleton {SUIT_NAME[s]}: {call} viser kortfarven. Du har stadig minimum."
    return classify

def responder_support(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 4 or L[OTHER[M]] >= 4:
            return None      # uden støtte – eller med 4 i den anden major – er det ikke en støttemelding
        short = sum({0: 5, 1: 3, 2: 1}.get(L[s], 0) for s in SUITS if s != M)
        sp = hp + short
        if L[M] >= 5 and sp <= 9:
            return f"4{sym}", f"{L[M]}-korts støtte og {sp} sp: 4{sym} er destruktivt (0–9 sp)."
        if sp < 4 or sp == 10:
            return None      # for svag til at melde – eller præcis 10 sp, hvor svarer selv vælger
        if sp <= 6:
            return f"3{sym}", f"4-korts støtte og {sp} sp: 3{sym} er destruktivt (0–6 sp)."
        if sp <= 9:
            return "3♦", f"4+ korts støtte og {sp} sp: 3♦ – Omvendt Bergen, 7–10 sp."
        if sp == 11:
            return "3♣", f"4+ korts støtte og {sp} sp: 3♣ – Omvendt Bergen, 10–11 sp."
        return "2NT", f"4+ korts støtte og {sp} sp: 2NT – Bekkasin, 12+ sp."
    return classify

BONUS = {
    "aabner": {"q": "Hvad viser makkers 2NT?",
               "correct": "12+ sp og støtte – Bekkasin",
               "options": ["12+ sp og støtte – Bekkasin", "11–12 hp jævn, invit", "7–10 sp med 4-korts støtte"],
               "why": "2NT er Bekkasin: 12+ sp (inkl. kortfarvepoint) og støtte til majoren. Åbner beskriver nu kortfarve og styrke."},
    "spm": {"q": "Hvad spørger makkers 3♦ om?",
            "correct": "Om dit minimum alligevel har en kortfarve",
            "options": ["Om dit minimum alligevel har en kortfarve", "Om du har tillæg", "Om du har hold i ruder"],
            "why": "Efter 3♣ (minimum) er 3♦ krav og spørger efter kortfarve. Svarene er de samme trin som ved tillæg."},
    "svar": {"q": "Hvad lover makkers åbning i major?",
             "correct": "12(11)–21 hp og 5+ kort",
             "options": ["12(11)–21 hp og 5+ kort", "12–21 hp og 4+ kort", "15–17 hp, jævn"],
             "why": "Åbning på 1♥/1♠ er 12(11)–21 hp med 5+ kort i farven; 20-reglen anvendes."},
}

PAS = ["Modstander", "Pas"]
SITUATIONS, CLASSIFIERS, SAMPLERS = {}, {}, {}
for M in ('H', 'S'):
    sym, om = SUIT_SYM[M], OTHER[M]
    opening = f"1{sym}"
    key = 'h' if M == 'H' else 's'
    rebid_calls = ["3♣", "3♦", "3♥", "3♠", "3NT", "4♣", "4♦", "4♥"]
    SITUATIONS[f"aabner_1{key}"] = {"rolle": "Åbner", "auction": [["Dig", opening], PAS, ["Makker", "2NT"], PAS],
                                    "calls": rebid_calls, "bonus": BONUS["aabner"]}
    SITUATIONS[f"spm_1{key}"] = {"rolle": "Åbner",
                                 "auction": [["Dig", opening], PAS, ["Makker", "2NT"], PAS, ["Dig", "3♣"], PAS, ["Makker", "3♦"], PAS],
                                 "calls": ["3♥", "3♠", "3NT", f"4{sym}"], "bonus": BONUS["spm"]}
    SITUATIONS[f"svar_1{key}"] = {"rolle": "Svarer", "auction": [["Makker", opening], PAS],
                                  "calls": ["2NT", "3♣", "3♦", f"3{sym}", f"4{sym}"], "bonus": BONUS["svar"]}
    CLASSIFIERS[f"aabner_1{key}"] = opener_rebid(M)
    CLASSIFIERS[f"spm_1{key}"] = opener_answer_to_ask(M)
    CLASSIFIERS[f"svar_1{key}"] = responder_support(M)

    side = {s: (2, 4) for s in SUITS if s != M}
    def opener(hp, **short):
        return tpl(hp, **{M: (5, 6), **side, **short})
    SAMPLERS[f"aabner_1{key}"] = {
        "3♣": opener(MIN_HP, D=(1, 4), C=(1, 4)), "3♦": opener(MAX_HP),
        "3♥": opener(MAX_HP, D=(1, 1)), "3♠": opener(MAX_HP, C=(1, 1)), "3NT": opener(MAX_HP, **{om: (1, 1)}),
        "4♣": opener((12, 21), C=(0, 0), D=(2, 5)), "4♦": opener((12, 21), D=(0, 0), C=(2, 5)),
        "4♥": opener((12, 21), **{om: (0, 0)}, D=(2, 5), C=(2, 5)),
    }
    SAMPLERS[f"spm_1{key}"] = {
        "3♥": opener(MIN_HP, D=(1, 1)), "3♠": opener(MIN_HP, C=(1, 1)),
        "3NT": opener(MIN_HP, **{om: (1, 1)}), f"4{sym}": opener(MIN_HP),
    }
    SAMPLERS[f"svar_1{key}"] = {
        "2NT": tpl((10, 17), **{M: (4, 5), om: (0, 3), 'D': (1, 4), 'C': (1, 4)}),
        "3♣": tpl((7, 11), **{M: (4, 4), om: (0, 3), 'D': (1, 4), 'C': (1, 4)}),
        "3♦": tpl((5, 9), **{M: (4, 4), om: (0, 3), 'D': (1, 4), 'C': (1, 4)}),
        f"3{sym}": tpl((2, 6), **{M: (4, 4), om: (0, 3), 'D': (1, 4), 'C': (1, 4)}),
        f"4{sym}": tpl((1, 8), **{M: (5, 6), om: (0, 3), 'D': (0, 4), 'C': (0, 4)}),
    }

# Hænder pr. melding (åbner 64 + 32, svarer 100) – så begge roller kommer lige tit
PER_CALL = {"aabner_1h": 4, "aabner_1s": 4, "spm_1h": 4, "spm_1s": 4, "svar_1h": 10, "svar_1s": 10}

def export_pool(path):
    hands, seen = [], set()
    for situation, n in PER_CALL.items():
        for call, sampler in SAMPLERS[situation].items():
            made = tries = 0
            while made < n and tries < 20000:
                tries += 1
                r = sampler()
                if not r:
                    continue
                hand, hp, sp = r
                key = tuple(tuple(hand[s]) for s in SUITS)
                res = CLASSIFIERS[situation](hand, hp)
                if key in seen or not res or res[0] != call:
                    continue
                seen.add(key)
                hands.append({"situation": situation, "hand": {s: hand[s] for s in SUITS},
                              "hp": hp, "sp": sp, "correct": res[0], "why": res[1]})
                made += 1
            if made < n:
                print(f"Advarsel: kun {made}/{n} hænder til {situation} {call}")
    return export(path, SITUATIONS, hands)
