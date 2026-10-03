"""
RKC 1430, trumfdame og konger – Makker 2 & mig, afsnit 7.

Som 1430 hos Makker 1 & mig (svar på 4NT og på damespørgsmålet), men:
  5♥/5♠ viser 2 eller 5 nøglekort (uden/med trumfdamen)
  5NT efter RKC-svaret er kongespørgsmål: 6 i billigste farve med konge · 6 i trumf = ingen konger
Antagelser: kongespørgsmålet stilles af svarer efter Bekkasin (1M – 2NT – 3♦ – 4NT – svar – 5NT);
hænder med en konge, der kun kan vises over 6 i trumf (♠K med hjerter som trumf), er ikke med.
"""
import random
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from . import rkc1430
from .rkc1430 import keycards, rank, ORDER

PAS = ["Modstander", "Pas"]
BONUS_KONGE = {"q": "Hvad garanterer 5NT efter RKC-svaret?",
               "correct": "Alle fem nøglekort – invitation til storeslem",
               "options": ["Alle fem nøglekort – invitation til storeslem", "Trumfdamen", "Invit til 6NT"],
               "why": "5NT spørger om konger og garanterer, at parret har alle fem nøglekort. Svar: 6 i billigste farve med konge, 6 i trumf uden konger."}

def answer_4nt(M):
    base = rkc1430.answer_4nt(M)
    def classify(hand, hp):
        if keycards(hand, M) == 5:
            if 12 in hand[M]:
                return "5♠", "5 nøglekort og trumfdamen: 5♠ (2 eller 5 med dame)."
            return "5♥", "5 nøglekort uden trumfdamen: 5♥ (2 eller 5 uden dame)."
        return base(hand, hp)
    return classify

def answer_kings(M, shown):
    sym = SUIT_SYM[M]
    four = answer_4nt(M)
    def classify(hand, hp):
        r = four(hand, hp)
        if not r or r[0] != shown:
            return None
        kings = [s for s in SUITS if s != M and 13 in hand[s]]
        below = [s for s in kings if rank(f"6{SUIT_SYM[s]}") < rank(f"6{sym}")]
        if kings and not below:
            return None
        if not below:
            return f"6{sym}", f"Ingen konger uden for trumf: 6{sym}."
        s = min(below, key=ORDER.index)
        return f"6{SUIT_SYM[s]}", f"Konge i {SUIT_NAME[s]}: 6{SUIT_SYM[s]} – billigste konge først."
    return classify

def five_kc(M, gen):
    def sample():
        for _ in range(200):
            r = gen()
            if not r:
                continue
            hand, hp, sp = r
            if all(len(hand[s]) for s in SUITS) and len(hand[M]) >= 2:
                hand = {s: list(c) for s, c in hand.items()}
                for s in SUITS:
                    if 14 not in hand[s]:
                        hand[s][0] = 14
                    hand[s] = sorted(set(hand[s]), reverse=True)
                if 13 not in hand[M]:
                    hand[M][-1] = 13
                    hand[M] = sorted(set(hand[M]), reverse=True)
                if sum(len(c) for c in hand.values()) != 13:
                    continue
                hp = sum({14: 4, 13: 3, 12: 2, 11: 1}.get(x, 0) for c in hand.values() for x in c)
                return hand, hp, sp
        return None
    return sample

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = dict(rkc1430.SITUATIONS), dict(rkc1430.CLASSIFIERS), dict(rkc1430.SAMPLERS), dict(rkc1430.PER_CALL)
for M, key in (('H', 'h'), ('S', 's')):
    sym = SUIT_SYM[M]
    opener_hand = lambda hp, M=M: tpl(hp, **{M: (5, 6), **{s: (2, 4) for s in SUITS if s != M}})
    sk = f"aab_4nt_1{key}"
    CLASSIFIERS[sk] = answer_4nt(M)
    SAMPLERS[sk] = dict(SAMPLERS[sk])
    SAMPLERS[sk]["5♥"] = either(SAMPLERS[sk]["5♥"], five_kc(M, opener_hand((14, 17))))
    SAMPLERS[sk]["5♠"] = either(SAMPLERS[sk]["5♠"], five_kc(M, opener_hand((14, 17))))
    CLASSIFIERS[f"svar_4nt_1{key}"] = answer_4nt(M)
    seq = [["Dig", f"1{sym}"], PAS, ["Makker", "2NT"], PAS, ["Dig", "3♦"], PAS, ["Makker", "4NT"], PAS]
    for shown, sk_ in (("5♣", "kl"), ("5♠", "sp")):
        sk = f"aab_konge_{sk_}_1{key}"
        reach = [f"6{SUIT_SYM[s]}" for s in ORDER if s != M and rank(f"6{SUIT_SYM[s]}") < rank(f"6{sym}")] + [f"6{sym}"]
        SITUATIONS[sk] = {"rolle": "Åbner", "auction": seq + [["Dig", shown], PAS, ["Makker", "5NT"], PAS],
                          "calls": reach + [f"7{sym}"], "bonus": BONUS_KONGE}
        CLASSIFIERS[sk] = answer_kings(M, shown)
        SAMPLERS[sk] = {c: opener_hand((16, 21)) for c in reach}
        PER_CALL[sk] = 3

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
