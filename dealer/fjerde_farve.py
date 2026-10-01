"""
Fjerde farve krav – fælles for begge systemer (Karina & Franks afsnit 4.8, Flemming & Franks afsnit 5a).

Forløbene 1♦ – 1♥ – 1♠ – ? og 1♣ – 1♥ – 1♠ – ?; den fjerde farve er klør hhv. ruder.
  svar_*  – svarer: fjerde farve på 2-trinnet er rundekrav, 11+ hp. Med hold i den fjerde farve meldes
            sans naturligt (2NT 11–12, 3NT 13+) – fjerde farve bruges ikke, når der er en naturlig melding
  aab_*   – åbner svarer i denne rækkefølge: 1. støtte til svarers farve (3 hjerter) · 2. sans med hold i
            den fjerde farve (billigst med minimum, spring med tillæg) · 3. gentag egen 6-farve ·
            4. meld den fjerde farve naturligt med fire kort
Antagelser: hold = es, K-x, D-x-x eller B-x-x-x; åbners minimum 12–14, tillæg 15–17; støtten meldes
billigst (2♥). Svarerhænder med 4 spar, 6+ hjerter eller 4+ i åbners minor er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from .lebensohl import stopper

PAS = ["Modstander", "Pas"]
BONUS = {
    "aab": {"q": "Hvad siger makkers fjerde farve om farven?",
            "correct": "Intet – den er kunstig og krav",
            "options": ["Intet – den er kunstig og krav", "Mindst 4 kort i farven", "Hold i farven"],
            "why": "Fjerde farve er kunstig og krav: rundekrav på 2-trinnet (11+), udgangskrav på 3-trinnet (13+). Den siger intet om farven."},
    "svar": {"q": "Hvornår bruger du fjerde farve krav?",
             "correct": "Med 11+ hp uden fit og uden naturlig melding",
             "options": ["Med 11+ hp uden fit og uden naturlig melding", "Altid med 4 kort i farven", "Kun med svag hånd"],
             "why": "Fjerde farve skaber et krav, når der ikke er fundet fit, og der ikke er en naturlig kravmelding – fx sans med hold."},
}

def responder(minor, fourth):
    fsym = SUIT_SYM[fourth]
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp < 11 or hp > 16 or L['H'] < 4 or L['H'] >= 6 or L['S'] >= 4 or L[minor] >= 4:
            return None
        if stopper(hand, fourth) and min(L.values()) >= 2:
            if hp <= 12:
                return "2NT", f"Hold i {SUIT_NAME[fourth]} og {hp} hp: 2NT er naturligt (invit) – fjerde farve er ikke nødvendig."
            return "3NT", f"Hold i {SUIT_NAME[fourth]} og {hp} hp: 3NT."
        return f"2{fsym}", f"{hp} hp, intet fit og intet hold i {SUIT_NAME[fourth]}: 2{fsym} – fjerde farve, rundekrav."
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
            return "2♥", "3 hjerter: støtten til svarers første farve går forud for alt andet – 2♥."
        if stopper(hand, fourth):
            if hp <= 14:
                return "2NT", f"Hold i {SUIT_NAME[fourth]} og minimum ({hp} hp): 2NT."
            return "3NT", f"Hold i {SUIT_NAME[fourth]} og tillæg ({hp} hp): spring til 3NT."
        if L[minor] >= 6:
            call = f"2{msym}" if minor == 'D' else f"3{msym}"
            return call, f"6 {SUIT_NAME[minor]}, intet hold og ingen støtte: gentag farven – {call}."
        if L[fourth] >= 4:
            return f"3{fsym}", f"4 {SUIT_NAME[fourth]}: meld den fjerde farve naturligt – 3{fsym} (sidste udvej)."
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
