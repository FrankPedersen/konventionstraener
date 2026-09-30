"""
xy sans – fælles for begge systemer (Karina & Franks afsnit 4.7, Flemming & Franks afsnit 6a).

Forløbet 1♣/1♦ – 1♠ – 1NT (12–14 jævn). Puljen dækker kun det, begge dokumenter er enige om:
  svar_1x  – svarers melding over 1NT: pas med en svag 4-korts sparhånd, 2♣ relæ med invitationshånd
             (10–11 hp), 2♦ udgangskrav (13+ hp)
  aabner_1x – åbners svar på 2♦: 2♥ fire hjerter (måske også tre spar) · 2♠ tre spar, ikke fire hjerter ·
             2NT hverken tre spar eller fire hjerter
Svarers videre meldinger efter 2♣ – 2♦ er ikke med: de to dokumenter er uenige om 2♥/2♠ dér
(svag hos Karina & Frank, invit hos Flemming & Frank). 12 hp er heller ikke med – dokumenterne
overlapper dér (relæ 10–12, udgangskrav 12+).
"""
from .core import SUITS, SUIT_NAME, lengths_of, tpl, build_pool

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
        if L['S'] == 4 and max(L.values()) <= 4:
            return "Pas", f"{hp} hp og ingen lang farve: pas – 1NT er en fin kontrakt."
        return None          # svag hånd med 5+ farve behandler dokumenterne forskelligt
    if INVITE_HP[0] <= hp <= INVITE_HP[1]:
        return "2♣", f"{hp} hp er en invitationshånd: 2♣ relæ – åbner melder 2♦, og du beskriver hånden bagefter."
    if hp >= GF_HP:
        return "2♦", f"{hp} hp er udgangskrav: 2♦ – åbner beskriver sin fordeling i trin."
    return None

BONUS = {
    "aabner": {"q": "Hvad viser makkers 2♦?",
               "correct": "Udgangskrav – beder dig vise fordelingen i trin",
               "options": ["Udgangskrav – beder dig vise fordelingen i trin", "Naturligt, ruderfarve", "Relæ – beder dig melde 2♥"],
               "why": "Efter 1-farve – 1-farve – 1NT er 2♦ udgangskrav og alerteres. Åbner beskriver fordelingen i trin."},
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
        "calls": ["Pas", "2♣", "2♦", "2♠", "2NT", "3NT"], "bonus": BONUS["svar"]}
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
    }
    PER_CALL[f"aabner_1{key}"] = 15
    PER_CALL[f"svar_1{key}"] = 15

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
