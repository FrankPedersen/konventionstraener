"""
xy sans – fælles for begge systemer, efter afsnit 6a hos Makker 2 & mig.

Forløbet 1♣/1♦ – 1♠ – 1NT (12–14 jævn). Puljen dækker:
  svar_1x   – svarers melding over 1NT: pas (svag, 4 spar, ingen lang farve) · 2♠ / 3♣ stop (svag, egen
              lang farve) · 2♣ relæ (invit, 10–11 hp) · 2♦ udgangskrav (13+ hp)
  relae_1x  – efter 2♣ – 2♦ beskriver svarer: 2♠ 5-farve, invit · 2NT invit uden 5-farve · 3 i ny farve 5-5
  aabner_1x – åbners svar på 2♦: 2♥ fire hjerter (måske også tre spar) · 2♠ tre spar, ikke fire hjerter ·
              2NT hverken tre spar eller fire hjerter
12 hp er ikke med: dokumentet overlapper dér (relæ 10–12, udgangskrav 12+). Direkte 2NT og 3NT er heller
ikke med, fordi de konkurrerer med relæet på samme hænder.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, build_pool, tx

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
            extra_en = " – you also have three spades, but the hearts come first" if L['S'] == 3 else ""
            return "2♥", tx(f"Fire hjerter{extra}: 2♥.", f"Four hearts{extra_en}: 2♥.")
        if L['S'] == 3:
            return "2♠", tx("Tre spar og ikke fire hjerter: 2♠.", "Three spades and not four hearts: 2♠.")
        return "2NT", tx(f"Hverken tre spar ({L['S']}) eller fire hjerter ({L['H']}): 2NT.",
                         f"Neither three spades ({L['S']}) nor four hearts ({L['H']}): 2NT.")
    return classify

def responder_first(hand, hp):
    L = lengths_of(hand)
    if L['S'] < 4 or L['H'] >= 4:
        return None          # med 4 hjerter havde svarer meldt 1♥ først
    if WEAK_HP[0] <= hp <= WEAK_HP[1]:
        if L['S'] >= 6 and max(L['H'], L['D'], L['C']) <= 3:
            return "2♠", tx(f"Svag hånd med {L['S']} spar: 2♠ – stop, du afslutter i din lange farve.",
                            f"Weak hand with {L['S']} spades: 2♠ – to play, you sign off in your long suit.")
        if L['S'] == 4 and L['C'] >= 6:
            return "3♣", tx(f"Svag hånd med {L['C']} klør: 3♣ – stop, du afslutter i din lange farve.",
                            f"Weak hand with {L['C']} clubs: 3♣ – to play, you sign off in your long suit.")
        if L['S'] == 4 and max(L.values()) <= 4:
            return "Pas", tx(f"{hp} hp og ingen lang farve: pas – 1NT er en fin kontrakt.",
                             f"{hp} HCP and no long suit: pass – 1NT is a fine contract.")
        return None
    if INVITE_HP[0] <= hp <= INVITE_HP[1]:
        return "2♣", tx(f"{hp} hp er en invitationshånd: 2♣ relæ – åbner melder 2♦, og du beskriver hånden bagefter.",
                        f"{hp} HCP is an invitational hand: 2♣ relay – opener bids 2♦, and you describe the hand afterwards.")
    if hp >= GF_HP:
        return "2♦", tx(f"{hp} hp er udgangskrav: 2♦ – åbner beskriver sin fordeling i trin.",
                        f"{hp} HCP is game forcing: 2♦ – opener describes the shape in steps.")
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
        return call, tx(f"5 spar og 5 {SUIT_NAME[s]}: {call} viser 5-5, invit eller bedre.",
                        f"5 spades and 5 {SUIT_NAME_EN[s]}: {call} shows 5-5, invitational or better.")
    if L['S'] >= 5:
        return "2♠", tx(f"{L['S']} spar og {hp} hp: 2♠ viser 5-farven, invit.", f"{L['S']} spades and {hp} HCP: 2♠ shows the five-card suit, invitational.")
    if not fives:
        return "2NT", tx(f"{hp} hp uden 5-farve: 2NT er invit.", f"{hp} HCP without a five-card suit: 2NT is invitational.")
    return None

C_AAB = tx("Udgangskrav – beder dig vise fordelingen i trin", "Game forcing – asks you to show your shape in steps")
C_RELAE = tx("Tvunget relæsvar – siger intet om hånden", "A forced relay response – says nothing about the hand")
C_SVAR = tx("12–14 hp, jævn", "12–14 HCP, balanced")
BONUS = {
    "aabner": {"q": tx("Hvad viser makkers 2♦?", "What does partner's 2♦ show?"),
               "correct": C_AAB,
               "options": [C_AAB, tx("Naturligt, ruderfarve", "Natural, a diamond suit"), tx("Relæ – beder dig melde 2♥", "A relay – asks you to bid 2♥")],
               "why": tx("Efter 1-farve – 1-farve – 1NT er 2♦ udgangskrav og alerteres. Åbner beskriver fordelingen i trin.",
                         "After one of a suit – one of a suit – 1NT, 2♦ is game forcing and alerted. Opener describes the shape in steps.")},
    "relae": {"q": tx("Hvad viste åbners 2♦?", "What did opener's 2♦ show?"),
              "correct": C_RELAE,
              "options": [C_RELAE, tx("Naturlig ruderfarve", "A natural diamond suit"), tx("Udgangskrav", "Game forcing")],
              "why": tx("2♣ er relæ og tvinger åbner til 2♦, som intet siger. Nu beskriver svarer sin invitationshånd på lavt niveau.",
                        "2♣ is a relay and forces opener to bid 2♦, which says nothing. Now responder describes the invitational hand at a low level.")},
    "svar": {"q": tx("Hvad viser åbners 1NT-genmelding?", "What does opener's 1NT rebid show?"),
             "correct": C_SVAR,
             "options": [C_SVAR, tx("15–17 hp, jævn", "15–17 HCP, balanced"), tx("18–19 hp, jævn", "18–19 HCP, balanced")],
             "why": tx("1NT-genmeldingen viser 12–14 jævn – med 15–17 havde åbner åbnet 1NT. Det brede interval er grunden til relæet.",
                       "The 1NT rebid shows 12–14 balanced – with 15–17 opener would have opened 1NT. The wide range is the reason for the relay.")},
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
