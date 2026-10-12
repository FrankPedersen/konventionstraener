"""
DONT mod modstandernes 1NT – Makker 2 & mig, afsnit 15a.

  indmelding – 1NT – ?: D én ukendt farve 6+ (10–16) · 2♣ klør + højere 5-4 · 2♦ ruder + højere 5-4 ·
               2♥ hjerter + spar 5-4 · 2♠ spar alene 6+ · 2NT begge minorer 5-5 (8–15) · pas ellers
  gen_*      – indmelder efter makkers relæ: vis farven / den anden farve – pas, hvis relæet ramte den
  svar_*     – svarer efter 2♣/2♦/2♥: pas med støtte · billigste relæ uden · 2NT invit 11+ ·
               3 i den viste farve spærrende med god støtte
Antagelser, som dokumentet ikke giver tal for: god støtte = 5+ kort, støtte til pas = 3–4 kort;
efter 2♥ (begge farver kendt) er pas/2♠ præference. Svarerhænder med 13+ hp eller egen 6-farve er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, rnd, either, build_pool, tx

ORDER = ['C', 'D', 'H', 'S']

def shape(L):
    """('two', a, b) med a lavest, ('one', s) eller None."""
    long4 = [s for s in ORDER if L[s] >= 4]
    if len(long4) == 2 and max(L[s] for s in long4) >= 5:
        return ('two', long4[0], long4[1])
    six = [s for s in ORDER if L[s] >= 6]
    if len(six) == 1 and len(long4) == 1:
        return ('one', six[0])
    return None

def classify_overcall(hand, hp):
    L = lengths_of(hand)
    if hp < 8:
        return "Pas", tx(f"{hp} hp – under 8 hp er der ingen grund til at blande sig.", f"{hp} HCP – below 8 HCP there is no reason to come in.")
    if hp > 16:
        return None
    sh = shape(L)
    if sh and sh[0] == 'two':
        _, a, b = sh
        if hp > 15:
            return None
        desc = f"{L[a]} {SUIT_NAME[a]} og {L[b]} {SUIT_NAME[b]}"
        desc_en = f"{L[a]} {SUIT_NAME_EN[a]} and {L[b]} {SUIT_NAME_EN[b]}"
        if (a, b) == ('C', 'D') and L['C'] >= 5 and L['D'] >= 5:
            return "2NT", tx(f"{desc}: 2NT viser begge minorer, mindst 5-5.", f"{desc_en}: 2NT shows both minors, at least 5-5.")
        if (a, b) == ('H', 'S'):
            return "2♥", tx(f"{desc}: 2♥ viser hjerter og spar – begge farver er kendt med det samme.",
                            f"{desc_en}: 2♥ shows hearts and spades – both suits are known at once.")
        call = f"2{SUIT_SYM[a]}"
        return call, tx(f"{desc}: {call} viser {SUIT_NAME[a]} og en højere farve, mindst 5-4.",
                        f"{desc_en}: {call} shows {SUIT_NAME_EN[a]} and a higher suit, at least 5-4.")
    if sh and sh[0] == 'one':
        s = sh[1]
        if s == 'S':
            if hp > 15:
                return None
            return "2♠", tx(f"{L['S']} spar alene: 2♠ – naturlig slutmelding.", f"{L['S']} spades alone: 2♠ – natural, to play.")
        if hp >= 10:
            return "X", tx(f"Én lang farve ({L[s]} {SUIT_NAME[s]}) og {hp} hp: D viser én ukendt farve, mindst 6 kort.",
                           f"One long suit ({L[s]} {SUIT_NAME_EN[s]}) and {hp} HCP: X shows one unknown suit, at least 6 cards.")
        return "Pas", tx(f"{L[s]} {SUIT_NAME[s]}, men kun {hp} hp – D kræver 10–16 hp.", f"{L[s]} {SUIT_NAME_EN[s]}, but only {hp} HCP – X needs 10–16 HCP.")
    return "Pas", tx(f"{hp} hp, men ingen DONT-fordeling (én 6-farve eller to farver 5-4).",
                     f"{hp} HCP, but no DONT shape (one six-card suit or two suits 5-4).")

def rebid_after_relay(overcall, relay):
    """Indmelder viser farven / den anden farve efter makkers relæ – pas, hvis relæet ramte den."""
    def classify(hand, hp):
        res = classify_overcall(hand, hp)
        if not res or res[0] != overcall:
            return None
        sh = shape(lengths_of(hand))
        target = sh[1] if overcall == "X" else sh[2]
        what = "din farve" if overcall == "X" else "din anden farve"
        what_en = "your suit" if overcall == "X" else "your second suit"
        if f"2{SUIT_SYM[target]}" == relay:
            return "Pas", tx(f"Makker bad om {what}, og relæet {relay} ramte netop {SUIT_NAME[target]}: pas.",
                             f"Partner asked for {what_en}, and the relay {relay} hit exactly {SUIT_NAME_EN[target]}: pass.")
        call = f"2{SUIT_SYM[target]}"
        return call, tx(f"Makker bad om {what}: {call} viser {SUIT_NAME[target]}.", f"Partner asked for {what_en}: {call} shows {SUIT_NAME_EN[target]}.")
    return classify

def advance_one_known(shown, relay):
    """Svar på 2♣/2♦: den viste farve plus en ukendt højere."""
    sym, name, en = SUIT_SYM[shown], SUIT_NAME[shown], SUIT_NAME_EN[shown]
    def classify(hand, hp):
        L = lengths_of(hand)
        if hp >= 13 or any(L[s] >= 6 for s in SUITS if s != shown):
            return None
        if hp >= 11:
            return "2NT", tx(f"{hp} hp: 2NT er invit og spørger indmelder om styrke og fordeling.",
                             f"{hp} HCP: 2NT is invitational and asks the overcaller about strength and shape.")
        if L[shown] >= 5:
            return f"3{sym}", tx(f"{L[shown]} {name} – god støtte: 3{sym} er spærrende.", f"{L[shown]} {en} – good support: 3{sym} is preemptive.")
        if L[shown] >= 3:
            return "Pas", tx(f"{L[shown]} {name} er støtte nok: pas – vi har fundet et sted at spille.",
                             f"{L[shown]} {en} is enough support: pass – we have found a place to play.")
        return relay, tx(f"Kun {L[shown]} {name}: {relay} er relæ og beder indmelder vise sin anden farve.",
                         f"Only {L[shown]} {en}: {relay} is a relay and asks the overcaller to show the second suit.")
    return classify

def advance_majors(hand, hp):
    """Svar på 2♥: hjerter og spar er begge kendt."""
    L = lengths_of(hand)
    H, S = L['H'], L['S']
    if hp >= 13 or any(L[s] >= 6 for s in ('C', 'D')):
        return None
    if hp >= 11:
        return "2NT", tx(f"{hp} hp: 2NT er invit og spørger indmelder om styrke og fordeling.",
                         f"{hp} HCP: 2NT is invitational and asks the overcaller about strength and shape.")
    if max(H, S) >= 5:
        M = 'H' if H >= S else 'S'
        return f"3{SUIT_SYM[M]}", tx(f"{L[M]} {SUIT_NAME[M]} – god støtte: 3{SUIT_SYM[M]} er spærrende.",
                                     f"{L[M]} {SUIT_NAME_EN[M]} – good support: 3{SUIT_SYM[M]} is preemptive.")
    if H >= S:
        return "Pas", tx(f"{H} hjerter og {S} spar: pas og spil 2♥.", f"{H} hearts and {S} spades: pass and play 2♥.")
    return "2♠", tx(f"{S} spar mod {H} hjerter: 2♠ – præference for spar.", f"{S} spades against {H} hearts: 2♠ – preference for spades.")

C_IND = tx("Én ukendt farve, mindst 6 kort", "One unknown suit, at least 6 cards")
C_RELAE = tx("At du viser din (anden) farve", "That you show your (second) suit")
C_2KL = tx("Klør og en højere farve, mindst 5-4", "Clubs and a higher suit, at least 5-4")
C_2RU = tx("Ruder og en højere farve, mindst 5-4", "Diamonds and a higher suit, at least 5-4")
C_2HJ = tx("Hjerter og spar, mindst 5-4", "Hearts and spades, at least 5-4")
BONUS = {
    "indmelding": {"q": tx("Hvad viser en DONT-dobling af 1NT?", "What does a DONT double of 1NT show?"),
                   "correct": C_IND,
                   "options": [C_IND, tx("Straf – mindst 15 hp", "Penalty – at least 15 HCP"), tx("Begge majorer", "Both majors")],
                   "why": tx("I DONT er doblingen ikke straf: den viser én ukendt farve med mindst 6 kort og 10–16 hp. Makker melder 2♣ som relæ.",
                             "In DONT the double is not for penalty: it shows one unknown suit of at least 6 cards and 10–16 HCP. "
                             "Partner bids 2♣ as a relay.")},
    "relae": {"q": tx("Hvad beder makkers relæ om?", "What does partner's relay ask for?"),
              "correct": C_RELAE,
              "options": [C_RELAE, tx("At du viser din styrke", "That you show your strength"),
                          tx("At du melder sans med hold", "That you bid notrump with a stopper")],
              "why": tx("Relæet – den billigste melding – beder indmelder vise farven. Rammer relæet netop indmelderens farve, passer han.",
                        "The relay – the cheapest bid – asks the overcaller to show the suit. If the relay hits the overcaller's suit, "
                        "the overcaller passes.")},
    "2kl": {"q": tx("Hvad viser makkers 2♣?", "What does partner's 2♣ show?"),
            "correct": C_2KL,
            "options": [C_2KL, tx("Naturlig klørfarve, 6+ kort", "A natural club suit, 6+ cards"), "Stayman"],
            "why": tx("2♣ viser klør og en højere farve, mindst 5-4, 8–15 hp. Den højere farve er ukendt, indtil du spørger.",
                      "2♣ shows clubs and a higher suit, at least 5-4, 8–15 HCP. The higher suit is unknown until you ask.")},
    "2ru": {"q": tx("Hvad viser makkers 2♦?", "What does partner's 2♦ show?"),
            "correct": C_2RU,
            "options": [C_2RU, tx("Énfarvet major", "A one-suited major"), tx("Naturlig ruderfarve, 6+ kort", "A natural diamond suit, 6+ cards")],
            "why": tx("2♦ viser ruder og en højere farve, mindst 5-4, 8–15 hp.", "2♦ shows diamonds and a higher suit, at least 5-4, 8–15 HCP.")},
    "2hj": {"q": tx("Hvad viser makkers 2♥?", "What does partner's 2♥ show?"),
            "correct": C_2HJ,
            "options": [C_2HJ, tx("Hjerter og en minor", "Hearts and a minor"), tx("Naturlig hjerterfarve, 6+ kort", "A natural heart suit, 6+ cards")],
            "why": tx("2♥ viser hjerter og spar, mindst 5-4 – den eneste DONT-melding, hvor begge farver er kendt med det samme.",
                      "2♥ shows hearts and spades, at least 5-4 – the only DONT bid where both suits are known at once.")},
}

PAS = ["Modstander", "Pas"]
SITUATIONS = {
    "indmelding": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"]], "allowX": True,
                   "calls": ["X", "Pas", "2♣", "2♦", "2♥", "2♠", "2NT"], "bonus": BONUS["indmelding"]},
    "gen_dobling": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "X"], PAS, ["Makker", "2♣"], PAS],
                    "calls": ["Pas", "2♦", "2♥", "2♠"], "bonus": BONUS["relae"]},
    "gen_2kl": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♣"], PAS, ["Makker", "2♦"], PAS],
                "calls": ["Pas", "2♥", "2♠", "2NT"], "bonus": BONUS["relae"]},
    "gen_2ru": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♦"], PAS, ["Makker", "2♥"], PAS],
                "calls": ["Pas", "2♠", "2NT", "3♣"], "bonus": BONUS["relae"]},
    "svar_2kl": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♣"], PAS],
                 "calls": ["Pas", "2♦", "2♥", "2NT", "3♣"], "bonus": BONUS["2kl"]},
    "svar_2ru": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♦"], PAS],
                 "calls": ["Pas", "2♥", "2♠", "2NT", "3♦"], "bonus": BONUS["2ru"]},
    "svar_2hj": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♥"], PAS],
                 "calls": ["Pas", "2♠", "2NT", "3♥", "3♠"], "bonus": BONUS["2hj"]},
}
CLASSIFIERS = {
    "indmelding": classify_overcall,
    "gen_dobling": rebid_after_relay("X", "2♣"),
    "gen_2kl": rebid_after_relay("2♣", "2♦"),
    "gen_2ru": rebid_after_relay("2♦", "2♥"),
    "svar_2kl": advance_one_known('C', "2♦"),
    "svar_2ru": advance_one_known('D', "2♥"),
    "svar_2hj": advance_majors,
}

def two(a, b, hp=(8, 15)):
    return tpl(hp, **{a: (4, 6), b: (4, 6)})

def one(s, hp=(10, 16)):
    return tpl(hp, **{s: (6, 7)})

SAMPLERS = {
    "indmelding": {
        "Pas": rnd((3, 14)), "X": either(one('C'), one('D'), one('H')),
        "2♣": either(two('C', 'D'), two('C', 'H'), two('C', 'S')), "2♦": either(two('D', 'H'), two('D', 'S')),
        "2♥": two('H', 'S'), "2♠": one('S', (8, 15)), "2NT": tpl((8, 15), C=(5, 6), D=(5, 6)),
    },
    "gen_dobling": {"Pas": one('C'), "2♦": one('D'), "2♥": one('H')},
    "gen_2kl": {"Pas": two('C', 'D'), "2♥": two('C', 'H'), "2♠": two('C', 'S')},
    "gen_2ru": {"Pas": two('D', 'H'), "2♠": two('D', 'S')},
    "svar_2kl": {"2NT": rnd((11, 12)), "Pas": tpl((4, 10), C=(3, 4), D=(0, 5), H=(0, 5), S=(0, 5)),
                 "2♦": tpl((0, 10), C=(0, 2), D=(2, 5), H=(2, 5), S=(2, 5)), "3♣": tpl((3, 10), C=(5, 6), D=(0, 5), H=(0, 5), S=(0, 5))},
    "svar_2ru": {"2NT": rnd((11, 12)), "Pas": tpl((4, 10), D=(3, 4), C=(0, 5), H=(0, 5), S=(0, 5)),
                 "2♥": tpl((0, 10), D=(0, 2), C=(2, 5), H=(2, 5), S=(2, 5)), "3♦": tpl((3, 10), D=(5, 6), C=(0, 5), H=(0, 5), S=(0, 5))},
    "svar_2hj": {"2NT": rnd((11, 12)), "Pas": tpl((0, 10), H=(2, 4), S=(0, 3), D=(0, 5), C=(0, 5)),
                 "2♠": tpl((0, 10), S=(3, 4), H=(0, 2), D=(0, 5), C=(0, 5)),
                 "3♥": tpl((0, 10), H=(5, 6), S=(0, 4), D=(0, 5), C=(0, 5)), "3♠": tpl((0, 10), S=(5, 6), H=(0, 3), D=(0, 5), C=(0, 5))},
}
PER_CALL = {"indmelding": 8, "gen_dobling": 6, "gen_2kl": 6, "gen_2ru": 6,
            "svar_2kl": 8, "svar_2ru": 8, "svar_2hj": 7}

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
