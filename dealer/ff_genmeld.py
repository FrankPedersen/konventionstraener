"""
Åbners stærke genmeldinger og 3♣ checkback – Makker 2 & mig, afsnit 4 og 8.

  aab_*   – åbner efter 1♦ – 1♠ (uden 4 spar):
            1NT jævn 12–14 · 2NT jævn 18–19 · 2♦ 6-farve 12–15 · 3♦ god 6-farve 16–18 ·
            2♣ 5-4 med klør 12–18 · 3♣ spring 19–21 (udgangskrav) · 2♥ 5-4 med hjerter 12–15 (naturlig, ikke
            krav) · 3♥ spring 16–21 (krav i én runde; med 19+ viser åbner udgangskraft i næste melding). Kun den nye
            højere farve har de nye grænser: en ny lavere farve koster ikke plads, fordi svarer kan give præference på
            2-trinnet (Franks valg 31. oktober 2026)
  svar_*  – svarer efter 1♦ – 1♠ – 2NT (18–19): 3♣ checkback med 5 spar eller 4 hjerter · 3NT ellers
            (efter 1♣ – 1♥ – 2NT: 5 hjerter eller 4 spar)
  check_* – åbner svarer på 3♣: 3 i svarers major = 3 korts støtte · 3 i den anden major = 4-farve ·
            3♦ ingen af delene · 3NT som 3♦ med maksimum (19)
Antagelser: »god 6-farve« = to af de tre øverste honnører; jævn = 4-3-3-3, 4-4-3-2 eller 5-3-3-2; svarer
med 6+ spar eller 13+ er ikke med. Revers spilles ikke: den er overvejet og fravalgt (Bilag G).
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx

PAS = ["Modstander", "Pas"]
C_AAB = tx("Ny højere farve 12–15 ikke krav, spring 16+ krav i én runde", "New higher suit 12–15 non-forcing, jump 16+ forcing for one round")
C_CHECK = tx("Åbners majorfordeling – krav til udgang", "Opener's major-suit holding – forcing to game")
BONUS = {
    "aab": {"q": tx("Hvad er grænsen mellem ny højere farve og spring i ny højere farve?", "Where is the boundary between a new higher suit and a jump in a new higher suit?"),
            "correct": C_AAB,
            "options": [C_AAB, tx("Ny højere farve 12–18, spring 19+ udgangskrav", "New higher suit 12–18, jump 19+ game forcing"), tx("Spring er altid spærrende", "A jump is always preemptive")],
            "why": tx("Med 12–15 og 5-4 meldes den nye højere farve uden spring – naturlig og ikke krav; med 16+ springes. Springet er krav i én runde, og med 19+ viser åbner udgangskraft i næste melding. "
                      "En ny lavere farve koster ikke plads, fordi svarer kan give præference på 2-trinnet: den er 12–18, og springet dér er 19+ og udgangskrav.",
                      "With 12–15 and 5-4, the new higher suit is bid without a jump – natural and non-forcing; with 16+ you jump. "
                      "The jump is forcing for one round, and with 19+ opener shows game-forcing values with the next bid. "
                      "A new lower suit costs no space, because responder can give preference at the two level: it is 12–18, "
                      "and the jump there is 19+ and game forcing.")},
    "check": {"q": tx("Hvad spørger 3♣ efter åbners 2NT-genmelding om?", "What does 3♣ after opener's 2NT rebid ask?"),
              "correct": C_CHECK,
              "options": [C_CHECK, tx("Naturlig klør", "Natural clubs"), tx("Esser", "Aces")],
              "why": tx("3♣ checkback er kunstig: 3 i svarers major = 3 korts støtte, 3 i den anden major = 4-farve, 3♦ = ingen af delene.",
                        "3♣ checkback is artificial: three of responder's major = three-card support, three of the other major = "
                        "a four-card suit, 3♦ = neither.")},
}

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def good(cards):
    return sum(1 for r in cards[:3] if r >= 12) >= 2

def rebid(hand, hp):
    L = lengths_of(hand)
    if L['S'] >= 4 or L['D'] < 4 or L['C'] > L['D'] or not (12 <= hp <= 21):
        return None
    if balanced(L):
        if hp <= 14:
            return "1NT", tx(f"Jævn hånd, {hp} hp: 1NT (12–14).", f"Balanced hand, {hp} HCP: 1NT (12–14).")
        if 18 <= hp <= 19:
            return "2NT", tx(f"Jævn hånd, {hp} hp: 2NT (18–19).", f"Balanced hand, {hp} HCP: 2NT (18–19).")
        return None
    if L['D'] >= 6 and L['H'] < 4 and L['C'] < 4:
        if hp <= 15:
            return "2♦", tx(f"{L['D']} ruder og {hp} hp: 2♦ (12–15).", f"{L['D']} diamonds and {hp} HCP: 2♦ (12–15).")
        if hp <= 18 and good(hand['D']):
            return "3♦", tx(f"God {L['D']}-farve ruder og {hp} hp: 3♦ – inviterende (16–18).",
                            f"A good {L['D']}-card diamond suit and {hp} HCP: 3♦ – invitational (16–18).")
        return None
    if L['D'] >= 5 and L['H'] == 4 and L['C'] < 4:
        if hp <= 15:
            return "2♥", tx(f"5-4 med hjerter og {hp} hp: 2♥ – naturlig, ikke krav (12–15).",
                            f"5-4 with hearts and {hp} HCP: 2♥ – natural, non-forcing (12–15).")
        if hp <= 18:
            return "3♥", tx(f"5-4 med hjerter og {hp} hp: spring til 3♥ – krav i én runde (16+).",
                            f"5-4 with hearts and {hp} HCP: jump to 3♥ – forcing for one round (16+).")
        return "3♥", tx(f"5-4 med hjerter og {hp} hp: spring til 3♥ – krav i én runde; med 19+ viser du udgangskraft i næste melding.",
                        f"5-4 with hearts and {hp} HCP: jump to 3♥ – forcing for one round; with 19+ you show game-forcing values "
                        f"with your next bid.")
    if L['D'] >= 5 and L['C'] == 4 and L['H'] < 4:
        if hp <= 18:
            return "2♣", tx(f"5-4 med klør og {hp} hp: 2♣ – ny lavere farve (12–18).", f"5-4 with clubs and {hp} HCP: 2♣ – a new lower suit (12–18).")
        return "3♣", tx(f"5-4 med klør og {hp} hp: spring til 3♣ – udgangskrav (19–21).",
                        f"5-4 with clubs and {hp} HCP: jump to 3♣ – game forcing (19–21).")
    return None

def checkback(M):
    O = 'S' if M == 'H' else 'H'
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 4 or L[M] > 5 or hp < 6 or hp > 12:
            return None
        if L[M] >= 5 or L[O] >= 4:
            why = f"{L[M]} {SUIT_NAME[M]}" if L[M] >= 5 else f"4 {SUIT_NAME[O]}"
            why_en = f"{L[M]} {SUIT_NAME_EN[M]}" if L[M] >= 5 else f"4 {SUIT_NAME_EN[O]}"
            return "3♣", tx(f"{why} og {hp} hp: 3♣ checkback – spørg om åbners majorfordeling.",
                            f"{why_en} and {hp} HCP: 3♣ checkback – ask about opener's major-suit holding.")
        return "3NT", tx(f"Kun 4 {SUIT_NAME[M]} og ingen 4 {SUIT_NAME[O]}: intet at spørge om – 3NT.",
                         f"Only 4 {SUIT_NAME_EN[M]} and not 4 {SUIT_NAME_EN[O]}: nothing to ask about – 3NT.")
    return classify

def answer(M):
    O, sym, osym = ('S' if M == 'H' else 'H'), SUIT_SYM[M], SUIT_SYM['S' if M == 'H' else 'H']
    def classify(hand, hp):
        L = lengths_of(hand)
        if not balanced(L) or not (18 <= hp <= 19) or L[M] >= 4:
            return None
        if L[M] == 3:
            return f"3{sym}", tx(f"3 {SUIT_NAME[M]}: 3{sym} – 3 korts støtte, fittet er fundet.",
                                 f"3 {SUIT_NAME_EN[M]}: 3{sym} – three-card support, the fit is found.")
        if L[O] >= 4:
            return f"3{osym}", tx(f"4 {SUIT_NAME[O]}, men ikke 3 {SUIT_NAME[M]}: 3{osym}.", f"4 {SUIT_NAME_EN[O]}, but not 3 {SUIT_NAME_EN[M]}: 3{osym}.")
        if hp == 18:
            return "3♦", tx("Hverken 3 korts støtte eller 4-farve i den anden major: 3♦.",
                            "Neither three-card support nor four cards in the other major: 3♦.")
        return "3NT", tx("Hverken støtte eller 4-farve, men maksimum (19): 3NT.", "Neither support nor a four-card suit, but a maximum (19): 3NT.")
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
SITUATIONS["aab_1ru"] = {"rolle": "Åbner", "auction": [["Dig", "1♦"], PAS, ["Makker", "1♠"], PAS],
                         "calls": ["1NT", "2♣", "2♦", "2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3NT"], "bonus": BONUS["aab"]}
CLASSIFIERS["aab_1ru"] = rebid
t = lambda hp, **b: tpl(hp, **{'S': (1, 3), 'H': (1, 3), 'D': (4, 5), 'C': (1, 3), **b})
SAMPLERS["aab_1ru"] = {"1NT": t((12, 14)), "2NT": t((18, 19)), "2♦": t((12, 15), D=(6, 7)), "3♦": t((16, 18), D=(6, 6)),
                       "2♣": t((12, 18), D=(5, 6), C=(4, 4)), "3♣": t((19, 21), D=(5, 6), C=(4, 4)),
                       "2♥": t((12, 15), D=(5, 6), H=(4, 4)), "3♥": t((16, 21), D=(5, 6), H=(4, 4))}
PER_CALL["aab_1ru"] = 9
for M, op, mk in (('S', 'D', 'sp'), ('H', 'C', 'hj')):
    sym, osym = SUIT_SYM[M], SUIT_SYM[op]
    sk = f"svar_{mk}"
    SITUATIONS[sk] = {"rolle": "Svarer",
                      "auction": [["Makker", f"1{osym}"], PAS, ["Dig", f"1{sym}"], PAS, ["Makker", "2NT"], PAS],
                      "calls": ["Pas", "3♣", "3♦", f"3{sym}", "3NT", f"4{sym}"], "bonus": BONUS["check"]}
    CLASSIFIERS[sk] = checkback(M)
    O = 'S' if M == 'H' else 'H'
    s = lambda hp, M=M, O=O, **b: tpl(hp, **{M: (4, 4), O: (0, 3), 'D': (1, 5), 'C': (1, 5), **b})
    SAMPLERS[sk] = {"3♣": either(s((6, 12), **{M: (5, 5)}), s((6, 12), **{O: (4, 4)})), "3NT": s((6, 12))}
    PER_CALL[sk] = 28
    sk = f"check_{mk}"
    SITUATIONS[sk] = {"rolle": "Åbner",
                      "auction": [["Dig", f"1{osym}"], PAS, ["Makker", f"1{sym}"], PAS, ["Dig", "2NT"], PAS, ["Makker", "3♣"], PAS],
                      "calls": ["3♦", "3♥", "3♠", "3NT", f"4{sym}"], "bonus": BONUS["check"]}
    CLASSIFIERS[sk] = answer(M)
    a = lambda hp, M=M, O=O, op=op, **b: tpl(hp, **{M: (2, 3), O: (2, 3), 'D': (2, 5), 'C': (2, 5), op: (4, 5), **b})
    SAMPLERS[sk] = {f"3{sym}": a((18, 19), **{M: (3, 3)}), f"3{SUIT_SYM[O]}": a((18, 19), **{M: (2, 2), O: (4, 4)}),
                    "3♦": a((18, 18), **{M: (2, 2), O: (2, 3)}), "3NT": a((19, 19), **{M: (2, 2), O: (2, 3)})}
    PER_CALL[sk] = 8

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
