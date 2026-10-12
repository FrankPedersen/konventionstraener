"""
1430 og trumfdame – Makker 1 & mig, systemkortets afsnit 5.

Nøglekort = 4 esser + trumfkonge. Svar på 4NT: 5♣ 1 eller 4 · 5♦ 0 eller 3 · 5♥ 2 uden trumfdame ·
5♠ 2 med trumfdame. Efter 5♣/5♦ spørger nærmeste trin efter trumfdamen:
  billigste genmelding (trumf) = har ikke damen · billigste konge = dame + konge(r) · 5NT = dame, ingen konger ·
  lilleslem = dame, intet yderligere at vise (kongerne ligger over 6 i trumf) – som hos Makker 2 & mig
Trumf er fastlagt med Bekkasin, og 4NT stilles enten af svarer (efter åbners 3♦) eller af åbner
(direkte over 2NT) – så du træner som både åbner og svarer.
Ikke med: 5 nøglekort, damespørgsmål efter 5♦ med hjerter som trumf (spørgsmålet bliver 5♠ og
genmeldingen 6♥ falder sammen med lilleslem).
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx

ORDER = ['C', 'D', 'H', 'S']
STR = ['♣', '♦', '♥', '♠', 'NT']

def rank(call):
    return int(call[0]) * 5 + STR.index(call[1:])

def keycards(hand, M):
    return sum(1 for s in SUITS if 14 in hand[s]) + (1 if 13 in hand[M] else 0)

def answer_4nt(M):
    def classify(hand, hp):
        kc = keycards(hand, M)
        if kc == 5:
            return None
        q = 12 in hand[M]
        if kc in (1, 4):
            return "5♣", tx(f"{kc} nøglekort (esser + trumfkonge): 5♣ viser 1 eller 4.",
                            f"{kc} keycard{'s' if kc > 1 else ''} (aces + trump king): 5♣ shows 1 or 4.")
        if kc in (0, 3):
            return "5♦", tx(f"{kc} nøglekort: 5♦ viser 0 eller 3.", f"{kc} keycards: 5♦ shows 0 or 3.")
        if q:
            return "5♠", tx("2 nøglekort og trumfdamen: 5♠.", "2 keycards and the trump queen: 5♠.")
        return "5♥", tx("2 nøglekort uden trumfdamen: 5♥.", "2 keycards without the trump queen: 5♥.")
    return classify

def answer_queen(M, shown, ask):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        kc = keycards(hand, M)
        if (shown == "5♣" and kc not in (1, 4)) or (shown == "5♦" and kc not in (0, 3)):
            return None
        if 12 not in hand[M]:
            call = next(f"{lv}{sym}" for lv in (5, 6) if rank(f"{lv}{sym}") > rank(ask))
            return call, tx(f"Du har ikke trumfdamen: billigste genmelding, {call}.",
                            f"You do not have the trump queen: the cheapest rebid, {call}.")
        kings = [s for s in SUITS if s != M and 13 in hand[s]]
        if not kings:
            return "5NT", tx("Trumfdamen, men ingen konger uden for trumf: 5NT.", "The trump queen, but no kings outside trumps: 5NT.")
        bids = []
        for s in kings:
            call = next(f"{lv}{SUIT_SYM[s]}" for lv in (5, 6) if rank(f"{lv}{SUIT_SYM[s]}") > rank(ask))
            if rank(call) < rank(f"6{sym}"):
                bids.append((rank(call), call, s))
        if not bids:
            return f"6{sym}", tx(f"Trumfdamen, men kongen kan ikke vises under 6{sym}: lilleslem – intet yderligere at vise.",
                                 f"The trump queen, but the king cannot be shown below 6{sym}: small slam – nothing more to show.")
        _, call, s = min(bids)
        return call, tx(f"Trumfdamen og {SUIT_NAME[s]} konge: billigste konge, {call}.",
                        f"The trump queen and the king of {SUIT_NAME_EN[s]}: the cheapest king, {call}.")
    return classify

C_4NT = tx("1 eller 4 nøglekort", "1 or 4 keycards")
C_DAME = tx("Trumfdamen, men ingen konger", "The trump queen, but no kings")
BONUS = {
    "4nt": {"q": tx("Hvad viser 5♣ som svar på 1430?", "What does 5♣ show in response to 1430?"),
            "correct": C_4NT,
            "options": [C_4NT, tx("0 eller 3 nøglekort", "0 or 3 keycards"), tx("2 nøglekort med trumfdame", "2 keycards with the trump queen")],
            "why": tx("1430: 5♣ = 1 eller 4, 5♦ = 0 eller 3, 5♥ = 2 uden trumfdame, 5♠ = 2 med trumfdame.",
                      "1430: 5♣ = 1 or 4, 5♦ = 0 or 3, 5♥ = 2 without the trump queen, 5♠ = 2 with the trump queen.")},
    "dame": {"q": tx("Hvad viser 5NT som svar på damespørgsmålet?", "What does 5NT show in response to the queen ask?"),
             "correct": C_DAME,
             "options": [C_DAME, tx("Ingen trumfdame", "No trump queen"), tx("Kongespørgsmål", "A king ask")],
             "why": tx("Billigste genmelding = ingen dame · billigste konge = dame + konge(r) · 5NT = dame uden konger · lilleslem = dame, intet yderligere at vise.",
                       "Cheapest rebid = no queen · cheapest king = queen + king(s) · 5NT = queen without kings · "
                       "small slam = queen, nothing more to show.")},
}

PAS = ["Modstander", "Pas"]
SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}

def calls_from(after, top):
    out = []
    for lv in (5, 6):
        for st in STR:
            c = f"{lv}{st}"
            if rank(after) < rank(c) <= rank(top):
                out.append(c)
    return out

for M, key in (('H', 'h'), ('S', 's')):
    sym, om = SUIT_SYM[M], ('S' if M == 'H' else 'H')
    opener_seq = [["Dig", f"1{sym}"], PAS, ["Makker", "2NT"], PAS, ["Dig", "3♦"], PAS, ["Makker", "4NT"], PAS]
    resp_seq = [["Makker", f"1{sym}"], PAS, ["Dig", "2NT"], PAS, ["Makker", "4NT"], PAS]
    opener_hand = lambda hp, M=M: tpl(hp, **{M: (5, 6), **{s: (2, 4) for s in SUITS if s != M}})
    resp_hand = lambda hp, M=M, om=om: tpl(hp, **{M: (4, 5), om: (2, 3), **{s: (2, 4) for s in ('C', 'D')}})
    for who, seq, gen, hp in (("aab", opener_seq, opener_hand, (16, 21)), ("svar", resp_seq, resp_hand, (12, 17))):
        rolle = "Åbner" if who == "aab" else "Svarer"
        sk = f"{who}_4nt_1{key}"
        SITUATIONS[sk] = {"rolle": rolle, "auction": seq, "calls": ["5♣", "5♦", "5♥", "5♠", "5NT"], "bonus": BONUS["4nt"]}
        CLASSIFIERS[sk] = answer_4nt(M)
        SAMPLERS[sk] = {c: (lambda gen=gen, hp=hp: gen(hp)()) for c in ("5♣", "5♦", "5♥", "5♠")}
        PER_CALL[sk] = 6
        asks = [("5♣", "5♦")] + ([("5♦", "5♥")] if M == 'S' else [])
        for shown, ask in asks:
            sk = f"{who}_dame_{'kl' if shown == '5♣' else 'ru'}_1{key}"
            me = "Dig"
            SITUATIONS[sk] = {"rolle": rolle, "auction": seq + [[me, shown], PAS, ["Makker", ask], PAS],
                              "calls": calls_from(ask, f"6{sym}"), "bonus": BONUS["dame"]}
            CLASSIFIERS[sk] = answer_queen(M, shown, ask)
            pool = {}
            reachable = {"5NT"}          # dame uden konger
            for s in ORDER:              # hver farves billigste melding over spørgsmålet
                c = next(f"{lv}{SUIT_SYM[s]}" for lv in (5, 6) if rank(f"{lv}{SUIT_SYM[s]}") > rank(ask))
                if rank(c) <= rank(f"6{sym}"):
                    reachable.add(c)
            for c in reachable:
                pool[c] = (lambda gen=gen, hp=hp: gen(hp)())
            SAMPLERS[sk] = pool
            PER_CALL[sk] = 3

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
