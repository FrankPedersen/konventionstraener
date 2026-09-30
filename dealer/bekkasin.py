"""
Bekkasin 2NT – fælles for begge systemer, efter Flemming & Franks afsnit 2 og 7.

1♥/1♠ – 2NT lover 13+ sp og 4+ korts støtte. Puljen dækker, begge majorer:
  aabner_1x  – åbners svar: 3♣ minimum (12–15) · 3♦ tillæg (16+) uden korthed ·
               3♥ tillæg og kort klør · 3♠ tillæg og kort ruder · 3NT tillæg og kort i den anden major
  spm_1x     – efter 3♣ – 3♦: 3♥ kort klør · 3♠ kort ruder · 3NT kort i den anden major · 4M ingen korthed
  svar_min_1x    – svarer efter 3♣: 3♦ spørger om korthed med 15+ sp (slemambition), ellers 4M
  svar_<trin>_1x – svarer efter åbners tillæg: cuebid i billigste kontrolfarve med slemambition, ellers 4M
Korthed = singleton eller renonce. Cuebids (afsnit 7, gælder for begge systemer): kontrol = es, konge,
singleton eller renonce; billigste kontrolfarve først; en oversprunget farve benægter kontrol.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, build_pool

OTHER = {'H': 'S', 'S': 'H'}
MIN_HP = (12, 15)
MAX_HP = (16, 21)
ASK_SP = 15        # 1M – 2NT – 3♣ – 3♦ kræver 15+ sp (afsnit 2)
SLAM_SP = 17       # slemambition over tillæg: 16 + 17 = 33 (antagelse – dokumentet giver ikke tallet)
STEP = {'C': "3♥", 'D': "3♠"}   # kort klør → 3♥, kort ruder → 3♠, anden major → 3NT
ORDER = ['C', 'D', 'H', 'S']
STRAINS = ['♣', '♦', '♥', '♠', 'NT']

def rank(call):
    return int(call[0]) * 5 + STRAINS.index(call[1:])

def short_suits(L, M):
    return [s for s in SUITS if s != M and L[s] <= 1]

def step_for(s):
    return STEP.get(s, "3NT")

def support_sp(hand, hp, M):
    L = lengths_of(hand)
    return hp + sum({0: 5, 1: 3, 2: 1}.get(L[s], 0) for s in SUITS if s != M)

def has_control(hand, s):
    return len(hand[s]) <= 1 or hand[s][0] >= 13

def control_word(hand, s):
    n = len(hand[s])
    if n == 0: return "renonce"
    if n == 1: return "singleton"
    return {14: "es", 13: "konge"}[hand[s][0]]

# --- Åbner ------------------------------------------------------------------

def opener_rebid(M):
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or not (MIN_HP[0] <= hp <= MAX_HP[1]):
            return None
        short = short_suits(L, M)
        if len(short) > 1:
            return None      # to korte farver beskriver skemaet ikke
        if hp <= MIN_HP[1]:
            extra = f" Makker kan spørge efter din korthed i {SUIT_NAME[short[0]]} med 3♦." if short else ""
            return "3♣", f"{hp} hp er minimum (højst 15): 3♣ – med eller uden korthed.{extra}"
        if not short:
            return "3♦", f"{hp} hp er tillæg (16+) uden korthed: 3♦."
        s = short[0]
        return step_for(s), f"{hp} hp er tillæg (16+) med korthed i {SUIT_NAME[s]}: {step_for(s)}."
    return classify

def opener_answer_to_ask(M):
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or not (MIN_HP[0] <= hp <= MIN_HP[1]):
            return None
        short = short_suits(L, M)
        if len(short) > 1:
            return None
        if not short:
            return f"4{SUIT_SYM[M]}", f"Ingen korthed – helt jævn minimumshånd: 4{SUIT_SYM[M]}. Svarer passer normalt."
        s = short[0]
        return step_for(s), f"Korthed i {SUIT_NAME[s]}: {step_for(s)}. Du har stadig minimum."
    return classify

# --- Svarer -------------------------------------------------------------------

def responder_ok(hand, hp, M):
    L = lengths_of(hand)
    return L[M] >= 4 and L[OTHER[M]] <= 3 and support_sp(hand, hp, M) >= 13

def responder_after_min(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        if not responder_ok(hand, hp, M):
            return None
        sp = support_sp(hand, hp, M)
        if sp >= ASK_SP:
            return "3♦", f"{sp} sp giver slemambition over et minimum: 3♦ spørger, om åbner alligevel har en korthed."
        return f"4{sym}", f"{sp} sp og åbner har minimum: 4{sym} som afmelding."
    return classify

def cue_bids(M, after):
    """Hver sidefarves billigste melding over `after` og under 4M, i meldeorden."""
    out = []
    for s in ORDER:
        if s == M:
            continue
        for level in (3, 4):
            call = f"{level}{SUIT_SYM[s]}"
            if rank(after) < rank(call):
                if rank(call) < rank(f"4{SUIT_SYM[M]}"):
                    out.append((call, s))
                break
    return sorted(out, key=lambda cs: rank(cs[0]))

def cheapest_cuebid(hand, M, after):
    """Billigste kontrolfarve; None hvis ingen sidefarve med kontrol kan meldes under 4M."""
    for call, s in cue_bids(M, after):
        if has_control(hand, s):
            return call, s
    return None

def responder_after_extra(M, after):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        if not responder_ok(hand, hp, M):
            return None
        sp = support_sp(hand, hp, M)
        if sp < SLAM_SP:
            return f"4{sym}", f"{sp} sp – ikke nok til slem over åbners tillæg: 4{sym} som afmelding."
        cue = cheapest_cuebid(hand, M, after)
        if not cue:
            return None      # ingen kontrol under udgang – skemaet dækker ikke situationen
        call, s = cue
        skipped = [SUIT_NAME[x] for c, x in cue_bids(M, after) if rank(c) < rank(call)]
        skip = f" Farver, du springer over ({', '.join(skipped)}), benægter kontrol." if skipped else ""
        return call, (f"{sp} sp giver slemambition: cuebid i billigste kontrolfarve – {call} viser "
                      f"{control_word(hand, s)} i {SUIT_NAME[s]}.{skip}")
    return classify

BONUS = {
    "aabner": {"q": "Hvad viser makkers 2NT?",
               "correct": "13+ sp og 4+ korts støtte – Bekkasin",
               "options": ["13+ sp og 4+ korts støtte – Bekkasin", "11–12 hp jævn, invit", "10–12 sp med præcis 3 korts støtte"],
               "why": "2NT er Bekkasin: 13+ støttepoint og mindst 4 korts støtte. Åbner beskriver i ét træk: minimum, tillæg uden korthed eller tillæg med korthed."},
    "spm": {"q": "Hvad spørger makkers 3♦ om?",
            "correct": "Om dit minimum alligevel har en korthed",
            "options": ["Om dit minimum alligevel har en korthed", "Om du har tillæg", "Om du har hold i ruder"],
            "why": "Efter 3♣ (minimum) er 3♦ krav og spørger efter korthed. Trinene er de samme som ved tillæg, og 4 i trumffarven viser en helt jævn hånd."},
    "svar": {"q": "Hvad er en kontrol, når I cuebidder?",
             "correct": "Es, konge, singleton eller renonce",
             "options": ["Es, konge, singleton eller renonce", "Kun esser og renoncer", "Es eller konge – aldrig korthed"],
             "why": "Vi viser enhver kontrol – es, konge, singleton eller renonce – uden at skelne mellem 1. og 2. rundes kontrol. Billigste kontrolfarve først; en oversprunget farve benægter kontrol."},
}

PAS = ["Modstander", "Pas"]
SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}

def calls_between(after, M):
    """Alle meldinger fra lige over `after` til og med 4M."""
    out = []
    for level in (3, 4):
        for st in STRAINS:
            call = f"{level}{st}"
            if rank(after) < rank(call) <= rank(f"4{SUIT_SYM[M]}"):
                out.append(call)
    return out

for M in ('H', 'S'):
    sym, om = SUIT_SYM[M], OTHER[M]
    key = 'h' if M == 'H' else 's'
    opening = f"1{sym}"
    base = [["Dig", opening], PAS, ["Makker", "2NT"], PAS]
    SITUATIONS[f"aabner_1{key}"] = {"rolle": "Åbner", "auction": base,
                                    "calls": ["3♣", "3♦", "3♥", "3♠", "3NT", f"4{sym}"], "bonus": BONUS["aabner"]}
    SITUATIONS[f"spm_1{key}"] = {"rolle": "Åbner", "auction": base + [["Dig", "3♣"], PAS, ["Makker", "3♦"], PAS],
                                 "calls": ["3♥", "3♠", "3NT", f"4{sym}"], "bonus": BONUS["spm"]}
    CLASSIFIERS[f"aabner_1{key}"] = opener_rebid(M)
    CLASSIFIERS[f"spm_1{key}"] = opener_answer_to_ask(M)

    side = {s: (2, 4) for s in SUITS if s != M}
    def opener(hp, **short):
        return tpl(hp, **{M: (5, 6), **side, **short})
    SAMPLERS[f"aabner_1{key}"] = {
        "3♣": opener(MIN_HP, D=(1, 4), C=(1, 4)), "3♦": opener(MAX_HP),
        "3♥": opener(MAX_HP, C=(0, 1), D=(2, 5)), "3♠": opener(MAX_HP, D=(0, 1), C=(2, 5)),
        "3NT": opener(MAX_HP, **{om: (0, 1)}, D=(2, 5), C=(2, 5)),
    }
    SAMPLERS[f"spm_1{key}"] = {
        "3♥": opener(MIN_HP, C=(0, 1), D=(2, 5)), "3♠": opener(MIN_HP, D=(0, 1), C=(2, 5)),
        "3NT": opener(MIN_HP, **{om: (0, 1)}, D=(2, 5), C=(2, 5)), f"4{sym}": opener(MIN_HP),
    }
    PER_CALL[f"aabner_1{key}"] = 6
    PER_CALL[f"spm_1{key}"] = 5

    resp = lambda hp: tpl(hp, **{M: (4, 5), om: (0, 3), 'D': (0, 5), 'C': (0, 5)})
    SITUATIONS[f"svar_min_1{key}"] = {"rolle": "Svarer",
                                      "auction": [["Makker", opening], PAS, ["Dig", "2NT"], PAS, ["Makker", "3♣"], PAS],
                                      "calls": ["3♦", "3♥", "3♠", "3NT", f"4{sym}"], "bonus": BONUS["svar"]}
    CLASSIFIERS[f"svar_min_1{key}"] = responder_after_min(M)
    SAMPLERS[f"svar_min_1{key}"] = {"3♦": resp((12, 18)), f"4{sym}": resp((10, 13))}
    PER_CALL[f"svar_min_1{key}"] = 7

    for after, tag in (("3♦", "3d"), ("3♥", "3h"), ("3♠", "3s"), ("3NT", "3nt")):
        sk = f"svar_{tag}_1{key}"
        SITUATIONS[sk] = {"rolle": "Svarer",
                          "auction": [["Makker", opening], PAS, ["Dig", "2NT"], PAS, ["Makker", after], PAS],
                          "calls": (lambda c: c if len(c) >= 4 else ["Pas"] + c)(calls_between(after, M)),
                          "bonus": BONUS["svar"]}
        CLASSIFIERS[sk] = responder_after_extra(M, after)
        SAMPLERS[sk] = {c: resp((14, 20)) for c, _ in cue_bids(M, after)}
        SAMPLERS[sk][f"4{sym}"] = resp((10, 14))
        PER_CALL[sk] = 3

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
