"""
Omvendt Bergen – Karina & Frank, systemkortets afsnit 4.1, 4.3 og 4.4.

Svarer over makkers 1♥/1♠:
  pas 0–5 hp (uden 4-korts støtte) · 2M 6–9 sp med 3-korts støtte · 3M 0–6 sp med 4-korts støtte (destruktivt) ·
  3♦ 7–10 sp med 4+ · 3♣ 10–11 sp med 4+ · 4M 0–9 sp med 5-korts støtte (destruktivt) · 2NT Bekkasin 13+
Svar på åbners spørgsmål:
  1M – 3♣ – 3♦: 3M minimum (10 sp) · 4M maksimum (11 sp)
  1♠ – 3♦ – 3♥: 3♠ minimum (7–8 sp) · 4♠ maksimum (9–10 sp)
Åbners valg (udgang ved 26 samlet – 25–26 er et skøn efter mellemkort og sekvenser; træneren bruger 26):
  åbner tæller støttepoint allerede i anden melding, fordi 3♣/3♦ viser støtte til majoren:
    1♠ – 3♦ (7–10): 3♠ afmelding ≤15 sp · 3♥ spørger 16–18 sp · 4♠ udgang 19+ sp
    1♥ – 3♦ (7–10): 3♥ afmelding ≤16 sp · 4♥ udgang 17+ sp (ingen plads til at spørge; midten 9)
    1M – 3♣ (10–11): 3M afmelding ≤14 sp · 3♦ spørger 15 sp · 4M udgang 16+ sp
  efter 1♠ – 3♦ – 3♥ – 3♠ (minimum 7–8): udgang, hvis åbners sp + 8 når 26, ellers pas.
  (Efter 1M – 3♣ – 3♦ – 3M giver 15 sp + 10 altid 25 – åbner passer altid, så den er ikke med.)
Støttepoint: hp + korthed, 5/3/1 med 4+ trumf og 3/2/1 med 3 trumf (notatets skala); åbner lægger
1 til for hver trumf ud over fem.
Ikke med: præcis 10 sp med 4-korts støtte (svarer vælger selv), 12 sp (hverken 3♣ eller Bekkasin dækker),
3-korts støtte med 10+ sp (meldes 2 over 1 først). Cuebid efter 3♣ kræver 22+ (33 samlet), hvilket
åbner på 1-trinnet ikke har.
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

# --- Åbners valg -------------------------------------------------------------

GAME = 26
SUPPORT = {"3♦": (7, 10), "3♣": (10, 11)}
MIN_ANSWER = {"3♦": (7, 8), "3♣": (10, 10)}

def opener_sp(hand, hp, M):
    L = lengths_of(hand)
    return hp + sum({0: 5, 1: 3, 2: 1}.get(L[s], 0) for s in SUITS if s != M) + max(0, L[M] - 5)

def sp_detail(hand, hp, M):
    L = lengths_of(hand)
    parts = [f"{hp} hp"]
    for s in SUITS:
        if s != M and L[s] <= 2:
            parts.append(f"{['renonce', 'single', 'double'][L[s]]} {SUIT_SYM[s]} = {[5, 3, 1][L[s]]}")
    if L[M] > 5:
        parts.append(f"{L[M] - 5} ekstra trumf")
    return " + ".join(parts)

def opener_first(M, bid):
    sym = SUIT_SYM[M]
    lo, hi = SUPPORT[bid]
    ask = {"3♦": "3♥", "3♣": "3♦"}[bid] if not (M == 'H' and bid == "3♦") else None
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or not (12 <= hp <= 21):
            return None
        sp = opener_sp(hand, hp, M)
        pts = f"{sp} sp ({sp_detail(hand, hp, M)})" if sp != hp else f"{sp} sp"
        if sp + hi < GAME:
            return f"3{sym}", f"{pts} + højst {hi} hos makker er under {GAME}: afmeld i 3{sym}."
        if sp + lo >= GAME:
            return f"4{sym}", f"{pts} + mindst {lo} hos makker giver {GAME}+: udgang, 4{sym}."
        if ask:
            return ask, f"{pts}: udgang afhænger af, om makker har minimum eller maksimum – {ask} spørger."
        mid = (lo + hi + 1) // 2
        if sp + mid >= GAME:
            return f"4{sym}", f"{pts}, og der er ikke plads til at spørge: {sp} + {mid} (midt i makkers {lo}–{hi}) – meld 4{sym}."
        return f"3{sym}", f"{pts}, og der er ikke plads til at spørge: {sp} + {mid} (midt i makkers {lo}–{hi}) – afmeld i 3{sym}."
    return classify

def opener_after_min(M, bid):
    sym = SUIT_SYM[M]
    lo, hi = MIN_ANSWER[bid]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or not opener_first(M, bid)(hand, hp) or opener_first(M, bid)(hand, hp)[0] in (f"3{sym}", f"4{sym}"):
            return None      # åbner har kun spurgt med de point, der giver spørgsmålet
        sp = opener_sp(hand, hp, M)
        if sp + hi >= GAME:
            return f"4{sym}", f"Makker har minimum ({lo}–{hi}): {sp} sp + {hi} = {sp + hi} – udgang, 4{sym}."
        return "Pas", f"Makker har minimum ({lo}–{hi}): {sp} sp + højst {hi} = {sp + hi} – under {GAME}, pas."
    return classify

BONUS["aab"] = {"q": "Må åbner tælle støttepoint efter makkers 3♣/3♦?",
                "correct": "Ja – meldingerne viser støtte til majoren",
                "options": ["Ja – meldingerne viser støtte til majoren", "Nej – de er kunstige, så kun honnørpoint", "Kun hvis makker har vist maksimum"],
                "why": "3♣ og 3♦ er kunstige, men de viser 4+ korts støtte. Åbner tæller derfor støttepoint i sin anden melding. Udgang ved 26 (25 med gode mellemkort)."}

for M, key in (('H', 'hj'), ('S', 'sp')):
    sym, om = SUIT_SYM[M], OTHER[M]
    ophand = lambda hp, M=M: tpl(hp, **{M: (5, 6), **{s: (1, 4) for s in SUITS if s != M}})
    # minimumshænder, der når udgang på fordelingen: renonce (5 sp) eller single (3 sp) i en sidefarve
    shorthand = lambda hp, n, M=M: either(*[tpl(hp, **{M: (5, 6), **{x: (n, n) if x == s else (2, 6) for x in SUITS if x != M}})
                                            for s in SUITS if s != M])
    distr = lambda M=M: either(ophand((14, 21), M), shorthand((12, 15), 0, M), shorthand((13, 16), 1, M))
    for bid, bkey in (("3♦", "3ru"), ("3♣", "3kl")):
        ask = "3♥" if bid == "3♦" else "3♦"
        has_ask = not (M == 'H' and bid == "3♦")
        sk = f"aab_{bkey}_{key}"
        calls = [f"3{sym}", f"4{sym}", "3NT"] + ([ask] if has_ask else ["Pas"])
        SITUATIONS[sk] = {"rolle": "Åbner", "auction": [["Dig", f"1{sym}"], PAS, ["Makker", bid], PAS],
                          "calls": sorted(set(calls), key=lambda c: (c == "Pas", c)), "bonus": BONUS["aab"]}
        CLASSIFIERS[sk] = opener_first(M, bid)
        SAMPLERS[sk] = {f"3{sym}": ophand((12, 15)), f"4{sym}": distr()}
        if has_ask:
            SAMPLERS[sk][ask] = ophand((13, 17))
        PER_CALL[sk] = 14
        if has_ask and bid == "3♦":   # efter 3♣ – 3♦ – 3M giver 15 sp + 10 altid 25: åbner passer altid
            sk2 = f"aab_min_{bkey}_{key}"
            SITUATIONS[sk2] = {"rolle": "Åbner",
                               "auction": [["Dig", f"1{sym}"], PAS, ["Makker", bid], PAS, ["Dig", ask], PAS, ["Makker", f"3{sym}"], PAS],
                               "calls": ["Pas", "3NT", f"4{sym}", f"5{sym}"], "bonus": BONUS["aab"]}
            CLASSIFIERS[sk2] = opener_after_min(M, bid)
            SAMPLERS[sk2] = {"Pas": ophand((13, 16)), f"4{sym}": ophand((13, 17))}
            PER_CALL[sk2] = 16

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
