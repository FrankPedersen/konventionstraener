"""
Longsuit trial bids – Makker 2 & mig, afsnit 1 og 3.

Efter 1M – 2M (6–9 sp, 3 korts støtte):
  aab_*  – åbner: pas 12–14 sp · trial bid 15–16 sp i en sidefarve med 3+ kort og 2–3 tabere (den
           svageste – flest tabere, ved lighed den billigste) · 3M 15–16 uden en sådan farve · 4M 17+
  svar_* – svarer efter trial bid: 4M med hjælp i farven (es, konge eller dame, singleton/renonce eller
           4+ kort), 3M uden hjælp
Antagelser: åbner tæller støttepoint (hp + korthed 5/3/1 + 1 pr. trumf ud over fem), som i
omvendt Bergen; tabere tælles på de tre øverste pladser (es, konge, dame er vindere); trial bid
meldes billigst (over 1♥ – 2♥ er 2♠ trial bid). Svarers »ny farve = hjælp dér« er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from .omvendt_bergen import opener_sp, sp_detail

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
BONUS = {"q": "Hvad beder et trial bid om?",
         "correct": "Hjælp i den meldte farve",
         "options": ["Hjælp i den meldte farve", "Støtte til en ny trumffarv", "Kontrol til slem"],
         "why": "Trial bid meldes i en svag farve (3+ kort, 2–3 tabere). Makker melder 4M med hjælp dér – honnør, korthed eller 4 kort – og 3M uden."}

def losers(cards):
    top = cards[:3]
    return min(len(cards), 3) - sum(1 for i, r in enumerate(top) if (r == 14) or (r == 13 and len(cards) >= 2) or (r == 12 and len(cards) >= 3))

def cheapest(M, s):
    lv = 2 if ORDER.index(s) > ORDER.index(M) else 3
    return f"{lv}{SUIT_SYM[s]}"

def opener(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or hp < 11:
            return None
        sp = opener_sp(hand, hp, M)
        pts = f"{sp} sp ({sp_detail(hand, hp, M)})" if sp != hp else f"{sp} sp"
        if sp > 20:
            return None
        if sp <= 14:
            return "Pas", f"{pts}: pas – udgang er udelukket over for 6–9."
        if sp >= 17:
            return f"4{sym}", f"{pts}: 4{sym} direkte (17+)."
        weak = [s for s in SUITS if s != M and L[s] >= 3 and 2 <= losers(hand[s]) <= 3]
        if not weak:
            return f"3{sym}", f"{pts}, men ingen sidefarve med 2–3 tabere: 3{sym} – invit."
        most = max(losers(hand[s]) for s in weak)
        s = min((x for x in weak if losers(hand[x]) == most), key=lambda x: (int(cheapest(M, x)[0]), ORDER.index(x)))
        call = cheapest(M, s)
        return call, f"{pts} og {most} tabere i {SUIT_NAME[s]} – den svageste farve: {call} er trial bid og beder om hjælp dér."
    return classify

def helps(cards):
    return len(cards) <= 1 or len(cards) >= 4 or any(r >= 12 for r in cards)

def responder(M, s):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] != 3 or not (6 <= hp + sum({0: 3, 1: 2, 2: 1}.get(L[x], 0) for x in SUITS if x != M) <= 9) or hp < 5:
            return None
        cards = hand[s]
        if helps(cards):
            why = ("korthed" if len(cards) <= 1 else "4 kort" if len(cards) >= 4 else "honnør")
            return f"4{sym}", f"Hjælp i {SUIT_NAME[s]} ({why}): 4{sym}."
        return f"3{sym}", f"Ingen hjælp i {SUIT_NAME[s]} (ingen honnør, 2–3 små): 3{sym}."
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for M, key in (('H', 'hj'), ('S', 'sp')):
    sym = SUIT_SYM[M]
    trials = [cheapest(M, s) for s in ORDER if s != M]
    sk = f"aab_{key}"
    SITUATIONS[sk] = {"rolle": "Åbner", "auction": [["Dig", f"1{sym}"], PAS, ["Makker", f"2{sym}"], PAS],
                      "calls": sorted(["Pas"] + trials + [f"3{sym}", f"4{sym}"],
                                      key=lambda c: (0, 0) if c == "Pas" else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))),
                      "bonus": BONUS}
    CLASSIFIERS[sk] = opener(M)
    op = lambda hp, M=M, **b: tpl(hp, **{M: (5, 6), **{x: (1, 4) for x in SUITS if x != M}, **b})
    SAMPLERS[sk] = {"Pas": op((11, 13)), f"3{sym}": op((13, 15)), f"4{sym}": op((15, 19))}
    for s in ORDER:
        if s != M:
            SAMPLERS[sk][cheapest(M, s)] = op((12, 15), **{s: (3, 4)})
    PER_CALL[sk] = 8
    for s in ORDER:
        if s == M:
            continue
        call = cheapest(M, s)
        sk = f"svar_{key}_{s.lower()}"
        SITUATIONS[sk] = {"rolle": "Svarer",
                          "auction": [["Makker", f"1{sym}"], PAS, ["Dig", f"2{sym}"], PAS, ["Makker", call], PAS],
                          "calls": ["Pas", f"3{sym}", "3NT", f"4{sym}"], "bonus": BONUS}
        CLASSIFIERS[sk] = responder(M, s)
        rs = lambda hp, M=M, **b: tpl(hp, **{M: (3, 3), **{x: (2, 4) for x in SUITS if x != M}, **b})
        SAMPLERS[sk] = {f"4{sym}": either(rs((5, 9)), rs((4, 8), **{s: (1, 1)})), f"3{sym}": rs((5, 9), **{s: (2, 3)})}
        PER_CALL[sk] = 8

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
