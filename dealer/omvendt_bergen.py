"""
Omvendt Bergen – Karina & Frank, systemkortets afsnit 4.1, 4.3 og 4.4.

Svarer over makkers 1♥/1♠:
  pas 0–5 hp (uden 4-korts støtte) · 2M 6–9 sp med 3-korts støtte · 3M 0–6 sp med 4-korts støtte (destruktivt) ·
  3♦ 7–10 sp med 4+ · 3♣ 10–11 sp med 4+ · 4M 0–9 sp med 5-korts støtte (destruktivt) · 2NT Bekkasin 13+
Svar på åbners spørgsmål:
  1M – 3♣ – 3♦: 3M minimum (10 sp) · 4M maksimum (11 sp)
  1♠ – 3♦ – 3♥: 3♠ minimum (7–8 sp) · 4♠ maksimum (9–10 sp)
Støttepoint: hp + korthed, 5/3/1 med 4+ trumf og 3/2/1 med 3 trumf (notatets skala).
Ikke med: præcis 10 sp med 4-korts støtte (svarer vælger selv), 12 sp (hverken 3♣ eller Bekkasin dækker),
3-korts støtte med 10+ sp (meldes 2 over 1 først) og åbners valg mellem afmelding og udgang.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool

OTHER = {'H': 'S', 'S': 'H'}

def support_points(hand, hp, M):
    L = lengths_of(hand)
    scale = {0: 5, 1: 3, 2: 1} if L[M] >= 4 else {0: 3, 1: 2, 2: 1}
    return hp + sum(scale.get(L[s], 0) for s in SUITS if s != M)

def responder(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[OTHER[M]] >= 4 or hp > 17:
            return None
        sp = support_points(hand, hp, M)
        if L[M] < 3:
            return None
        if L[M] == 3:
            if hp <= 5:
                return "Pas", f"{hp} hp – 0–5 hp er pas."
            if 6 <= sp <= 9:
                return f"2{sym}", f"3-korts støtte og {sp} sp: 2{sym} – konstruktivt (6–9 sp)."
            return None
        if L[M] >= 5 and sp <= 9:
            return f"4{sym}", f"{L[M]}-korts støtte og {sp} sp: 4{sym} – destruktivt (0–9 sp)."
        if sp <= 6:
            return f"3{sym}", f"4-korts støtte og {sp} sp: 3{sym} – destruktivt (0–6 sp)."
        if sp <= 9:
            return "3♦", f"4+ korts støtte og {sp} sp: 3♦ – Omvendt Bergen, 7–10 sp."
        if sp == 11:
            return "3♣", f"4+ korts støtte og {sp} sp: 3♣ – Omvendt Bergen, 10–11 sp."
        if sp >= 13:
            return "2NT", f"4+ korts støtte og {sp} sp: 2NT – Bekkasin (13+)."
        return None
    return classify

def answer_3kl(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 4 or L[OTHER[M]] >= 4:
            return None
        sp = support_points(hand, hp, M)
        if sp == 10:
            return f"3{sym}", f"{sp} sp er minimum for 3♣: 3{sym}."
        if sp == 11:
            return f"4{sym}", f"{sp} sp er maksimum for 3♣: 4{sym}."
        return None
    return classify

def answer_3ru(hand, hp):
    L = lengths_of(hand)
    if L['S'] < 4 or L['H'] >= 4:
        return None
    sp = support_points(hand, hp, 'S')
    if sp in (7, 8):
        return "3♠", f"{sp} sp er minimum for 3♦ (7–8): 3♠."
    if sp in (9, 10):
        return "4♠", f"{sp} sp er maksimum for 3♦ (9–10): 4♠."
    return None

BONUS = {
    "svar": {"q": "Hvad viser 3♦ over makkers 1♥/1♠?",
             "correct": "4+ korts støtte og 7–10 sp",
             "options": ["4+ korts støtte og 7–10 sp", "Naturlig ruderfarve", "4+ korts støtte og 10–11 sp"],
             "why": "Omvendt Bergen: 3♦ = 7–10 sp og 3♣ = 10–11 sp, begge med 4+ korts støtte. Med præcis 10 sp vælger svarer selv."},
    "spm": {"q": "Hvad spørger åbner om?",
            "correct": "Minimum eller maksimum",
            "options": ["Minimum eller maksimum", "Kortfarve", "Antal esser"],
            "why": "Åbners næste trin spørger, om svarer har minimum eller maksimum for sin støttemelding: 3M = minimum, 4M = maksimum."},
}

PAS = ["Modstander", "Pas"]
SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for M, key in (('H', 'hj'), ('S', 'sp')):
    sym, om = SUIT_SYM[M], OTHER[M]
    SITUATIONS[f"svar_{key}"] = {"rolle": "Svarer", "auction": [["Makker", f"1{sym}"], PAS],
                                 "calls": ["Pas", f"2{sym}", "2NT", "3♣", "3♦", f"3{sym}", f"4{sym}"], "bonus": BONUS["svar"]}
    CLASSIFIERS[f"svar_{key}"] = responder(M)
    sup = lambda hp, n, M=M, om=om: tpl(hp, **{M: (n, n), om: (0, 3), 'D': (1, 5), 'C': (1, 5)})
    SAMPLERS[f"svar_{key}"] = {
        "Pas": sup((0, 5), 3), f"2{sym}": sup((6, 9), 3), f"3{sym}": sup((2, 6), 4),
        "3♦": sup((5, 9), 4), "3♣": sup((8, 11), 4), "2NT": sup((11, 16), 4), f"4{sym}": sup((1, 8), 5)}
    PER_CALL[f"svar_{key}"] = 10
    SITUATIONS[f"spm3kl_{key}"] = {"rolle": "Svarer",
                                   "auction": [["Makker", f"1{sym}"], PAS, ["Dig", "3♣"], PAS, ["Makker", "3♦"], PAS],
                                   "calls": [f"3{sym}", f"4{sym}", "3NT", "Pas"], "bonus": BONUS["spm"]}
    CLASSIFIERS[f"spm3kl_{key}"] = answer_3kl(M)
    SAMPLERS[f"spm3kl_{key}"] = {f"3{sym}": sup((8, 10), 4), f"4{sym}": sup((8, 11), 4)}
    PER_CALL[f"spm3kl_{key}"] = 12
SITUATIONS["spm3ru_sp"] = {"rolle": "Svarer", "auction": [["Makker", "1♠"], PAS, ["Dig", "3♦"], PAS, ["Makker", "3♥"], PAS],
                           "calls": ["3♠", "4♠", "3NT", "Pas"], "bonus": BONUS["spm"]}
CLASSIFIERS["spm3ru_sp"] = answer_3ru
SAMPLERS["spm3ru_sp"] = {"3♠": tpl((5, 8), S=(4, 4), H=(0, 3), D=(1, 5), C=(1, 5)),
                         "4♠": tpl((6, 10), S=(4, 4), H=(0, 3), D=(1, 5), C=(1, 5))}
PER_CALL["spm3ru_sp"] = 14

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
