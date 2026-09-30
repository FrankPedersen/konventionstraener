"""
xy sans – fælles for begge systemer, efter Flemming & Franks afsnit 6a.

Forløbet 1♣/1♦ – 1♠ – 1NT (12–14 jævn). Puljen dækker:
  svar_1x   – svarers melding over 1NT: pas (svag, 4 spar, ingen lang farve) · 2♠ / 3♣ stop (svag, egen
              lang farve) · 2♣ relæ (invit, 10–11 hp) · 2♦ udgangskrav (13+ hp)
  relae_1x  – efter 2♣ – 2♦ beskriver svarer: 2♠ 5-farve, invit · 2NT invit uden 5-farve · 3 i ny farve 5-5
  aabner_1x – åbners svar på 2♦: 2♥ fire hjerter (måske også tre spar) · 2♠ tre spar, ikke fire hjerter ·
              2NT hverken tre spar eller fire hjerter
12 hp er ikke med: dokumentet overlapper dér (relæ 10–12, udgangskrav 12+). Direkte 2NT og 3NT er heller
ikke med, fordi de konkurrerer med relæet på samme hænder.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, build_pool

WEAK_HP = (6, 9)
INVITE_HP = (10, 11)
GF_HP = 13

def opening_minor(L):
    """1♦ med 4+ ruder og højst 3 klør, 1♣ med 3+ klør og højst 3 ruder – ellers ingen entydig åbning."""
    if L['D'] >= 4 and L['C'] <= 3:
        return 'D'
    if L['C'] >= 3 and L['D'] <= 3:
        return 'C'
    return None

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def opener_answer(minor):
    def classify(hand, hp):
        L = lengths_of(hand)
        if not (12 <= hp <= 14) or not balanced(L) or opening_minor(L) != minor:
            return None
        if L['S'] >= 4 or L['H'] >= 5:
            return None      # 4 spar havde støttet; 5 hjerter havde åbnet 1♥
        if L['H'] == 4:
            extra = " – du har også tre spar, men hjerterne kommer først" if L['S'] == 3 else ""
            return "2♥", f"Fire hjerter{extra}: 2♥."
        if L['S'] == 3:
            return "2♠", "Tre spar og ikke fire hjerter: 2♠."
        return "2NT", f"Hverken tre spar ({L['S']}) eller fire hjerter ({L['H']}): 2NT."
    return classify

def responder_first(hand, hp):
    L = lengths_of(hand)
    if L['S'] < 4 or L['H'] >= 4:
        return None          # med 4 hjerter havde svarer meldt 1♥ først
    if WEAK_HP[0] <= hp <= WEAK_HP[1]:
        if L['S'] >= 6 and max(L['H'], L['D'], L['C']) <= 3:
            return "2♠", f"Svag hånd med {L['S']} spar: 2♠ – stop, du afslutter i din lange farve."
        if L['S'] == 4 and L['C'] >= 6:
            return "3♣", f"Svag hånd med {L['C']} klør: 3♣ – stop, du afslutter i din lange farve."
        if L['S'] == 4 and max(L.values()) <= 4:
            return "Pas", f"{hp} hp og ingen lang farve: pas – 1NT er en fin kontrakt."
        return None
    if INVITE_HP[0] <= hp <= INVITE_HP[1]:
        return "2♣", f"{hp} hp er en invitationshånd: 2♣ relæ – åbner melder 2♦, og du beskriver hånden bagefter."
    if hp >= GF_HP:
        return "2♦", f"{hp} hp er udgangskrav: 2♦ – åbner beskriver sin fordeling i trin."
    return None

def responder_after_relay(hand, hp):
    """1m – 1♠ – 1NT – 2♣ – 2♦ – ?: invitationshånden beskriver sig."""
    L = lengths_of(hand)
    if L['S'] < 4 or L['H'] >= 4 and L['S'] == 4 or not (INVITE_HP[0] <= hp <= INVITE_HP[1]):
        return None
    fives = [s for s in ('C', 'D', 'H') if L[s] >= 5]
    if L['S'] >= 5 and fives:
        s = fives[0]
        call = f"3{SUIT_SYM[s]}"
        return call, f"5 spar og 5 {SUIT_NAME[s]}: {call} viser 5-5, invit eller bedre."
    if L['S'] >= 5:
        return "2♠", f"{L['S']} spar og {hp} hp: 2♠ viser 5-farven, invit."
    if not fives:
        return "2NT", f"{hp} hp uden 5-farve: 2NT er invit."
    return None

BONUS = {
    "aabner": {"q": "Hvad viser makkers 2♦?",
               "correct": "Udgangskrav – beder dig vise fordelingen i trin",
               "options": ["Udgangskrav – beder dig vise fordelingen i trin", "Naturligt, ruderfarve", "Relæ – beder dig melde 2♥"],
               "why": "Efter 1-farve – 1-farve – 1NT er 2♦ udgangskrav og alerteres. Åbner beskriver fordelingen i trin."},
    "relae": {"q": "Hvad viste åbners 2♦?",
              "correct": "Tvunget relæsvar – siger intet om hånden",
              "options": ["Tvunget relæsvar – siger intet om hånden", "Naturlig ruderfarve", "Udgangskrav"],
              "why": "2♣ er relæ og tvinger åbner til 2♦, som intet siger. Nu beskriver svarer sin invitationshånd på lavt niveau."},
    "svar": {"q": "Hvad viser åbners 1NT-genmelding?",
             "correct": "12–14 hp, jævn",
             "options": ["12–14 hp, jævn", "15–17 hp, jævn", "18–19 hp, jævn"],
             "why": "1NT-genmeldingen viser 12–14 jævn – med 15–17 havde åbner åbnet 1NT. Det brede interval er grunden til relæet."},
}

PAS = ["Modstander", "Pas"]
SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for minor, sym, key in (('C', '♣', 'kl'), ('D', '♦', 'ru')):
    other = 'D' if minor == 'C' else 'C'
    SITUATIONS[f"aabner_1{key}"] = {
        "rolle": "Åbner",
        "auction": [["Dig", f"1{sym}"], PAS, ["Makker", "1♠"], PAS, ["Dig", "1NT"], PAS, ["Makker", "2♦"], PAS],
        "calls": ["2♥", "2♠", "2NT", "3♣", "3♦", "3NT"], "bonus": BONUS["aabner"]}
    SITUATIONS[f"svar_1{key}"] = {
        "rolle": "Svarer",
        "auction": [["Makker", f"1{sym}"], PAS, ["Dig", "1♠"], PAS, ["Makker", "1NT"], PAS],
        "calls": ["Pas", "2♣", "2♦", "2♠", "2NT", "3♣", "3NT"], "bonus": BONUS["svar"]}
    SITUATIONS[f"relae_1{key}"] = {
        "rolle": "Svarer",
        "auction": [["Makker", f"1{sym}"], PAS, ["Dig", "1♠"], PAS, ["Makker", "1NT"], PAS, ["Dig", "2♣"], PAS, ["Makker", "2♦"], PAS],
        "calls": ["2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3NT"], "bonus": BONUS["relae"]}
    CLASSIFIERS[f"relae_1{key}"] = responder_after_relay
    CLASSIFIERS[f"aabner_1{key}"] = opener_answer(minor)
    CLASSIFIERS[f"svar_1{key}"] = responder_first
    base = {minor: (4, 5) if minor == 'D' else (3, 5), other: (2, 3)}
    SAMPLERS[f"aabner_1{key}"] = {
        "2♥": tpl((12, 14), H=(4, 4), S=(2, 3), **base),
        "2♠": tpl((12, 14), H=(2, 3), S=(3, 3), **base),
        "2NT": tpl((12, 14), H=(2, 3), S=(2, 2), **base),
    }
    SAMPLERS[f"svar_1{key}"] = {
        "Pas": tpl(WEAK_HP, S=(4, 4), H=(2, 3), D=(2, 4), C=(2, 4)),
        "2♣": tpl(INVITE_HP, S=(4, 6), H=(0, 3), D=(0, 5), C=(0, 5)),
        "2♦": tpl((GF_HP, 17), S=(4, 6), H=(0, 3), D=(0, 5), C=(0, 5)),
        "2♠": tpl(WEAK_HP, S=(6, 7), H=(0, 3), D=(0, 3), C=(0, 3)),
        "3♣": tpl(WEAK_HP, S=(4, 4), C=(6, 6), H=(0, 2), D=(0, 2)),
    }
    SAMPLERS[f"relae_1{key}"] = {
        "2♠": tpl(INVITE_HP, S=(5, 6), H=(0, 3), D=(0, 4), C=(0, 4)),
        "2NT": tpl(INVITE_HP, S=(4, 4), H=(2, 3), D=(2, 4), C=(2, 4)),
        "3♣": tpl(INVITE_HP, S=(5, 5), C=(5, 5), H=(0, 3), D=(0, 3)),
        "3♦": tpl(INVITE_HP, S=(5, 5), D=(5, 5), H=(0, 3), C=(0, 3)),
        "3♥": tpl(INVITE_HP, S=(5, 5), H=(5, 5), D=(0, 3), C=(0, 3)),
    }
    PER_CALL[f"aabner_1{key}"] = 20
    PER_CALL[f"svar_1{key}"] = 8
    PER_CALL[f"relae_1{key}"] = 4

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
