"""
Fjerde farve krav – fælles for begge systemer (afsnit 4.8 hos Makker 1 & mig, afsnit 5a hos Makker 2 & mig).

Forløbene 1♦ – 1♥ – 1♠ – ? og 1♣ – 1♥ – 1♠ – ?; den fjerde farve er klør hhv. ruder.
  svar_*  – svarer: fjerde farve på 2-trinnet er rundekrav, 11+ hp. Med hold i den fjerde farve meldes
            sans naturligt (2NT 11–12, 3NT 13+) – fjerde farve bruges ikke, når der er en naturlig melding
  aab_*   – åbner svarer i denne rækkefølge: 1. støtte til svarers farve (3 hjerter) · 2. sans med hold i
            den fjerde farve (billigst med minimum, spring med tillæg) · 3. gentag egen 6-farve ·
            4. meld den fjerde farve naturligt med fire kort
Antagelser: hold = es, K-x, D-x-x eller B-x-x-x; åbners minimum 12–14, tillæg 15–17; støtten meldes
billigst (2♥). Svarerhænder med 4 spar, 6+ hjerter eller 4+ i åbners minor er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx
from .lebensohl import stopper

PAS = ["Modstander", "Pas"]
C_AAB = tx("Intet – den er kunstig og krav", "Nothing – it is artificial and forcing")
C_SVAR = tx("Med 11+ hp uden fit og uden naturlig melding", "With 11+ HCP, no fit and no natural bid")
BONUS = {
    "aab": {"q": tx("Hvad siger makkers fjerde farve om farven?", "What does partner's fourth suit say about that suit?"),
            "correct": C_AAB,
            "options": [C_AAB, tx("Mindst 4 kort i farven", "At least 4 cards in the suit"), tx("Hold i farven", "A stopper in the suit")],
            "why": tx("Fjerde farve er kunstig og krav: rundekrav på 2-trinnet (11+), udgangskrav på 3-trinnet (13+). Den siger intet om farven.",
                      "The fourth suit is artificial and forcing: forcing for one round at the two level (11+), game forcing at the "
                      "three level (13+). It says nothing about the suit.")},
    "svar": {"q": tx("Hvornår bruger du fjerde farve krav?", "When do you use fourth suit forcing?"),
             "correct": C_SVAR,
             "options": [C_SVAR, tx("Altid med 4 kort i farven", "Always with 4 cards in the suit"), tx("Kun med svag hånd", "Only with a weak hand")],
             "why": tx("Fjerde farve skaber et krav, når der ikke er fundet fit, og der ikke er en naturlig kravmelding – fx sans med hold.",
                       "The fourth suit creates a force when no fit has been found and there is no natural forcing bid – "
                       "such as notrump with a stopper.")},
}

def responder(minor, fourth):
    fsym = SUIT_SYM[fourth]
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp < 11 or hp > 16 or L['H'] < 4 or L['H'] >= 6 or L['S'] >= 4 or L[minor] >= 4:
            return None
        if stopper(hand, fourth) and min(L.values()) >= 2:
            if hp <= 12:
                return "2NT", tx(f"Hold i {SUIT_NAME[fourth]} og {hp} hp: 2NT er naturligt (invit) – fjerde farve er ikke nødvendig.",
                                 f"A stopper in {SUIT_NAME_EN[fourth]} and {hp} HCP: 2NT is natural (invitational) – the fourth suit is not needed.")
            return "3NT", tx(f"Hold i {SUIT_NAME[fourth]} og {hp} hp: 3NT.", f"A stopper in {SUIT_NAME_EN[fourth]} and {hp} HCP: 3NT.")
        return f"2{fsym}", tx(f"{hp} hp, intet fit og intet hold i {SUIT_NAME[fourth]}: 2{fsym} – fjerde farve, rundekrav.",
                              f"{hp} HCP, no fit and no stopper in {SUIT_NAME_EN[fourth]}: 2{fsym} – fourth suit, forcing for one round.")
    return classify

def opener(minor, fourth):
    msym, fsym = SUIT_SYM[minor], SUIT_SYM[fourth]
    def classify(hand, hp):
        L = lengths_of(hand)
        if not (12 <= hp <= 17) or L['S'] != 4 or L['H'] >= 4 or L[minor] < (4 if minor == 'D' else 3):
            return None
        if minor == 'C' and L['D'] >= 4 or minor == 'D' and L['C'] > L['D']:
            return None
        if L['H'] == 3:
            return "2♥", tx("3 hjerter: støtten til svarers første farve går forud for alt andet – 2♥.",
                            "3 hearts: support for responder's first suit comes before everything else – 2♥.")
        if stopper(hand, fourth):
            if hp <= 14:
                return "2NT", tx(f"Hold i {SUIT_NAME[fourth]} og minimum ({hp} hp): 2NT.",
                                 f"A stopper in {SUIT_NAME_EN[fourth]} and a minimum ({hp} HCP): 2NT.")
            return "3NT", tx(f"Hold i {SUIT_NAME[fourth]} og tillæg ({hp} hp): spring til 3NT.",
                             f"A stopper in {SUIT_NAME_EN[fourth]} and extra values ({hp} HCP): jump to 3NT.")
        if L[minor] >= 6:
            call = f"2{msym}" if minor == 'D' else f"3{msym}"
            return call, tx(f"6 {SUIT_NAME[minor]}, intet hold og ingen støtte: gentag farven – {call}.",
                            f"6 {SUIT_NAME_EN[minor]}, no stopper and no support: rebid the suit – {call}.")
        if L[fourth] >= 4:
            return f"3{fsym}", tx(f"4 {SUIT_NAME[fourth]}: meld den fjerde farve naturligt – 3{fsym} (sidste udvej).",
                                  f"4 {SUIT_NAME_EN[fourth]}: bid the fourth suit naturally – 3{fsym} (last resort).")
        return None
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for minor, fourth, key in (('D', 'C', 'ru'), ('C', 'D', 'kl')):
    msym, fsym = SUIT_SYM[minor], SUIT_SYM[fourth]
    seq = [f"1{msym}", "1♥", "1♠"]
    SITUATIONS[f"svar_{key}"] = {"rolle": "Svarer",
                                 "auction": [["Makker", seq[0]], PAS, ["Dig", seq[1]], PAS, ["Makker", seq[2]], PAS],
                                 "calls": [f"2{fsym}", "2♥", "2♠", "2NT", f"3{msym}", "3NT"], "bonus": BONUS["svar"]}
    CLASSIFIERS[f"svar_{key}"] = responder(minor, fourth)
    r = lambda hp, **b: tpl(hp, **{'H': (4, 5), 'S': (2, 3), minor: (1, 3), fourth: (2, 5), **b})
    SAMPLERS[f"svar_{key}"] = {f"2{fsym}": r((11, 15), **{fourth: (2, 4)}), "2NT": r((11, 12)), "3NT": r((13, 16))}
    PER_CALL[f"svar_{key}"] = 17
    fourth_bid = f"2{fsym}"
    SITUATIONS[f"aab_{key}"] = {"rolle": "Åbner",
                                "auction": [["Dig", seq[0]], PAS, ["Makker", seq[1]], PAS, ["Dig", seq[2]], PAS, ["Makker", fourth_bid], PAS],
                                "calls": sorted({"2♥", "2♠", "2NT", f"3{fsym}", "3NT", f"2{msym}" if minor == 'D' else f"3{msym}"},
                                                key=lambda c: int(c[0]) * 5 + ['♣', '♦', '♥', '♠', 'NT'].index(c[1:])),
                                "bonus": BONUS["aab"]}
    CLASSIFIERS[f"aab_{key}"] = opener(minor, fourth)
    o = lambda hp, **b: tpl(hp, **{'S': (4, 4), 'H': (1, 3), minor: (4, 6) if minor == 'D' else (3, 6), fourth: (1, 4), **b})
    SAMPLERS[f"aab_{key}"] = {"2♥": o((12, 17), H=(3, 3)), "2NT": o((12, 14), H=(1, 2)), "3NT": o((15, 17), H=(1, 2)),
                              (f"2{msym}" if minor == 'D' else f"3{msym}"): o((12, 16), H=(1, 2), **{minor: (6, 6), fourth: (1, 2)}),
                              **({f"3{fsym}": o((12, 16), H=(1, 2), **{fourth: (4, 4), minor: (4, 4)})} if minor == 'D' else {})}
    PER_CALL[f"aab_{key}"] = 12

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
