"""
Revideret omvendt Bergen – Flemming & Frank, afsnit 1.

Svarer over makkers 1♥/1♠:
  Pas 0–5 · 2M 6–9 sp med 3 korts støtte · 3♣ 10–12 sp med præcis 3 · 3♦ 10–12 sp med 4+ ·
  3M 6–9 sp med 4 – spærrende · 4M 4–9 sp med 5+ – spærrende · 2NT Bekkasin 13+ sp med 4+ ·
  1NT 6–12 hp uden 3 korts støtte (over 1♥ også uden 4 spar) · 1♠ over 1♥ med 4+ spar
Åbner efter 3♣/3♦ (10–12): er kaptajn – 3M med minimum, 4M med tillæg. Åbner tæller støttepoint
(som i Karina & Franks Omvendt Bergen) og regner med midten af makkers 10–12: 4M, når sp + 11 når 26.
Antagelser: 2M lover 3 kort og 3M 4 kort (skemaet giver 3–4 hhv. 4+); med 5 trumfer og 4–9 sp meldes 4M;
støttepoint 5/3/1 med 4+ trumf og 3/2/1 med 3 trumf. 3 korts støtte med 13+ (Two over One først),
4+ trumf med 0–3 sp og cuebid/slem efter 3♣/3♦ er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from .omvendt_bergen import support_points, opener_sp, sp_detail

GAME = 26
PAS = ["Modstander", "Pas"]
BONUS = {
    "svar": {"q": "Hvad er forskellen på 3♣ og 3♦ hos Flemming & Frank?",
             "correct": "3♣ = præcis 3 kort, 3♦ = 4+ kort – begge 10–12 sp",
             "options": ["3♣ = præcis 3 kort, 3♦ = 4+ kort – begge 10–12 sp", "3♣ = 10–11 sp, 3♦ = 7–10 sp", "3♣ er naturlig klør"],
             "why": "I revideret omvendt Bergen viser 3♣ og 3♦ samme styrke (10–12 sp). Forskellen er trumflængden: 3♣ præcis 3, 3♦ 4+."},
    "aab": {"q": "Hvem er kaptajn efter 1M – 3♣/3♦?",
            "correct": "Åbner – han vælger 3M, udgang eller cuebid",
            "options": ["Åbner – han vælger 3M, udgang eller cuebid", "Svarer", "Ingen – 3♣/3♦ er udgangskrav"],
            "why": "Svarer har beskrevet sin hånd præcist (10–12 sp). Åbner er kaptajn: 3M med minimum, 4M med tillæg, cuebid ved slem."},
}

def responder(M):
    sym, om = SUIT_SYM[M], ('S' if M == 'H' else 'H')
    def classify(hand, hp):
        L = lengths_of(hand)
        n = L[M]
        sp = support_points(hand, hp, M)
        if n >= 5 and 4 <= sp <= 9:
            return f"4{sym}", f"{n} trumf og {sp} sp: 4{sym} – spærrende (4–9 sp, 5+ støtte)."
        if n >= 3 and sp < 6:
            if hp > 5 or n >= 5:
                return None
            return "Pas", f"{hp} hp og kun {sp} sp: pas (0–5)."
        if n >= 5:
            if sp <= 9:
                return f"4{sym}", f"{n} trumf og {sp} sp: 4{sym} – spærrende (4–9 sp, 5+ støtte)."
            if sp <= 12:
                return "3♦", f"{n} trumf og {sp} sp: 3♦ – 10–12 sp med 4+ støtte."
            return "2NT", f"{n} trumf og {sp} sp: 2NT Bekkasin (13+)."
        if n == 4:
            if sp <= 9:
                return f"3{sym}", f"4 trumf og {sp} sp: 3{sym} – spærrende (6–9 sp, 4+ støtte)."
            if sp <= 12:
                return "3♦", f"4 trumf og {sp} sp: 3♦ – 10–12 sp med 4+ støtte."
            return "2NT", f"4 trumf og {sp} sp: 2NT Bekkasin (13+)."
        if n == 3:
            if sp <= 9:
                return f"2{sym}", f"3 trumf og {sp} sp: 2{sym} (6–9 sp)."
            if sp <= 12:
                return "3♣", f"Præcis 3 trumf og {sp} sp: 3♣ (10–12 sp)."
            return None
        if hp < 6:
            return "Pas", f"{hp} hp uden støtte: pas."
        if M == 'H' and L['S'] >= 4:
            return "1♠", f"Ingen støtte, men {L['S']} spar: 1♠ – naturligt rundekrav."
        if hp <= 12:
            return "1NT", f"{hp} hp uden 3 korts støtte: 1NT (6–12, semikrav)."
        return None
    return classify

def opener(M, bid):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or not (12 <= hp <= 18):
            return None
        sp = opener_sp(hand, hp, M)
        if sp > 20:
            return None
        pts = f"{sp} sp ({sp_detail(hand, hp, M)})" if sp != hp else f"{sp} sp"
        if sp + 11 >= GAME:
            return f"4{sym}", f"{pts} + 11 (midt i makkers 10–12) når {GAME}: du er kaptajn – 4{sym}."
        return f"3{sym}", f"{pts} + 11 (midt i makkers 10–12) er under {GAME}: 3{sym} med minimum."
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for M, key in (('H', 'hj'), ('S', 'sp')):
    sym, om = SUIT_SYM[M], ('S' if M == 'H' else 'H')
    calls = ["Pas", "1NT", f"2{sym}", "2NT", "3♣", "3♦", f"3{sym}", f"4{sym}"] + (["1♠"] if M == 'H' else [])
    order = lambda c: (0, 0) if c == "Pas" else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))
    SITUATIONS[f"svar_{key}"] = {"rolle": "Svarer", "auction": [["Makker", f"1{sym}"], PAS],
                                 "calls": sorted(calls, key=order), "bonus": BONUS["svar"]}
    CLASSIFIERS[f"svar_{key}"] = responder(M)
    sup = lambda hp, n, M=M, om=om: tpl(hp, **{M: (n, n), om: (0, 3), 'D': (1, 5), 'C': (1, 5)})
    SAMPLERS[f"svar_{key}"] = {
        "Pas": sup((0, 4), 3), f"2{sym}": sup((5, 9), 3), "3♣": sup((8, 12), 3),
        "3♦": either(sup((7, 12), 4), sup((6, 11), 5)), f"3{sym}": sup((3, 9), 4),
        f"4{sym}": sup((2, 8), 5), "2NT": either(sup((11, 16), 4), sup((10, 15), 5)),
        "1NT": tpl((6, 12), **{M: (0, 2), om: (0, 3), 'D': (2, 6), 'C': (2, 6)})}
    if M == 'H':
        SAMPLERS[f"svar_{key}"]["1♠"] = tpl((6, 14), H=(0, 2), S=(4, 5), D=(1, 5), C=(1, 5))
    PER_CALL[f"svar_{key}"] = 8
    for bid, bkey in (("3♣", "3kl"), ("3♦", "3ru")):
        sk = f"aab_{bkey}_{key}"
        SITUATIONS[sk] = {"rolle": "Åbner", "auction": [["Dig", f"1{sym}"], PAS, ["Makker", bid], PAS],
                          "calls": [c for c in ["3♦", "3♥", "3♠", "3NT", "4♣", f"4{sym}"] if (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:])) > order(bid)],
                          "bonus": BONUS["aab"]}
        CLASSIFIERS[sk] = opener(M, bid)
        op = lambda hp, M=M: tpl(hp, **{M: (5, 6), **{s: (1, 4) for s in SUITS if s != M}})
        SAMPLERS[sk] = {f"3{sym}": op((12, 13)), f"4{sym}": either(op((14, 18)), tpl((12, 14), **{M: (5, 6), **{s: (0, 5) for s in SUITS if s != M}}))}
        PER_CALL[sk] = 15

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
