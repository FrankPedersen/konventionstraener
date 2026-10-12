"""
Multiforsvar mod 1NT – Makker 1 & mig, systemkortet v1.7 afsnit 8.1.

Indmelder (1NT – ?): D = stærk jævn hånd 15–17(+), forslag til straf · 2♣ = begge majorer 5-4 ·
2♦ = multi, 6+ i en major, ca. 6–10 hp · 2♥/2♠ = 5 i majoren + 4–5 i en ukendt minor ·
2NT = begge minorer · 3♣/3♦ = naturligt, spærrende. 2♣, 2♥/2♠ og 2NT er 10–16 hp.
Indmelders næste melding: 2♣ – 2♦ (spørger efter femfarven), 2♥/2♠ – 2NT (spørger efter minoren),
2♦ – 2♥ og 2♦ – 4♥ (pas eller korriger), 2♦ – 2NT (Plauken: 3♣ god multi, 3♦/3♥ dårlig multi som
transfer) og 2♦ – 2NT – 3♣ – 3♦ (transfer: 3♠ = hjerter, 3♥ = spar).
Svarer: på 2♣ præference eller 2♦ · på 2♦ 2♥ (pas eller korriger), 2♠ (udgangsopfordring, hvis makker
har hjerter), 2NT (Plauken), 3♥/3♠ (egen major) og 4♥ (spærrende) · på 2♥/2♠ pas eller 2NT ·
på 2NT præference · på D (mod svag sans) strafpas, scramble eller spring.

Grænser, som systemkortet ikke angiver, står som konstanter herunder. Hænder, kortet ikke beskriver
(fx 6+ major med 11–16 hp, 5-4-4-0 med begge majorer, stærke svarere efter 2♣ og 2♥/2♠), er ikke med.
"""
import random

from .core import (SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, deal_suit_lengths, fill_hand, lengths_of,
                   rnd, tpl, either, build_pool, tx)

# --- Grænser, som systemkortet ikke giver tal for – ret dem her ------------------
DOUBLE_HP = (15, 18)       # D: "15–17 hp eller lidt stærkere", jævn
MULTI_HP = (6, 10)         # 2♦: "ca. 6–10 hp"
MULTI_MAX = 8              # Plauken: 3♣ = god multi 8–10, 3♦/3♥ = dårlig multi 6–7
OVERCALL_HP = (10, 16)     # 2♣, 2♥/2♠ og 2NT
PREEMPT_MINOR_HP = (6, 11) # 3♣/3♦: naturligt og spærrende, 6+ farve
ADV_2KL_MAX = 11           # svarer på 2♣: præference eller 2♦; stærkere hænder beskriver kortet ikke
ADV_2M_MAX = 12            # svarer på 2♥/2♠: pas eller 2NT
ADV_GAME = 14              # svarer på 2♦: udgangsinteresse
ADV_4HJ_MAX = 9            # svarer på 2♦: 4♥ spærrende med fit i begge majorer
ADV_2NT_MAX = 10           # svarer på 2NT: præference
SCRAMBLE_MAX = 7           # svarer på D: 0–7 hp scrambler
STRAF_MIN = 8              # svarer på D: strafpas med 8+ hp
JUMP_HP = (9, 11)          # svarer på D: spring i farve med 5+ farve

BALANCED = {(4, 3, 3, 3), (4, 4, 3, 2), (5, 3, 3, 2)}

def shape(L):
    return tuple(sorted(L.values(), reverse=True))

def top_honours(cards):
    return sum(1 for r in cards if r >= 12)

def minor_of(L):
    """Den entydige 4–5-korts minor, eller None."""
    m = [x for x in ('D', 'C') if L[x] >= 4]
    return m[0] if len(m) == 1 else None

# --- Generatorer -------------------------------------------------------------------

def gen_5_4_majors(hp_range=OVERCALL_HP):
    """2♣: begge majorer 5-4 (den ene eller den anden vej), minorerne højst 3."""
    for _ in range(20):
        long_s, short_s = random.choice([('S', 'H'), ('H', 'S')])
        lengths = deal_suit_lengths({long_s: (5, 5), short_s: (4, 4), 'D': (0, 3), 'C': (0, 3)})
        if lengths:
            r = fill_hand(lengths, hp_range, (0, 40))
            if r:
                return r
    return None

def gen_multi(hp_range=MULTI_HP, major=None):
    """2♦: 6–7 kort i en major, ingen anden 4+ farve i majorerne."""
    for _ in range(20):
        M = major or random.choice(['S', 'H'])
        fixed = {x: (0, 3) for x in SUITS}
        fixed[M] = (6, 7)
        lengths = deal_suit_lengths(fixed)
        if lengths:
            r = fill_hand(lengths, hp_range, (0, 40))
            if r:
                return r
    return None

def multi_major(L):
    return 'S' if L['S'] >= 6 else 'H'

# --- Indmelder: 1NT – ? ------------------------------------------------------------

def classify_overcall(hand, hp):
    L = lengths_of(hand)
    S, H, D, C = L['S'], L['H'], L['D'], L['C']
    if shape(L) in BALANCED and DOUBLE_HP[0] <= hp <= DOUBLE_HP[1]:
        return "X", tx(f"{hp} hp og jævn hånd: D er forslag til straf – mindst samme styrke som sansåbneren.",
                       f"{hp} HCP and a balanced hand: X suggests penalty – at least the same strength as the notrump opener.")
    if hp > OVERCALL_HP[1]:
        return None
    major6 = [M for M in ('S', 'H') if L[M] >= 6]
    if major6 and max(S, H) <= 7 and min(S, H) <= 3:
        if MULTI_HP[0] <= hp <= MULTI_HP[1]:
            M = major6[0]
            return "2♦", tx(f"{L[M]} {SUIT_NAME[M]} og {hp} hp: 2♦ (multi) viser en 6-farve i en major, ca. 6–10 hp.",
                            f"{L[M]} {SUIT_NAME_EN[M]} and {hp} HCP: 2♦ (multi) shows a six-card major, about 6–10 HCP.")
        if hp > MULTI_HP[1]:
            return None
    minor6 = [m for m in ('D', 'C') if L[m] >= 6]
    if minor6 and max(S, H) <= 3 and PREEMPT_MINOR_HP[0] <= hp <= PREEMPT_MINOR_HP[1]:
        m = minor6[0]
        return f"3{SUIT_SYM[m]}", tx(f"{L[m]} {SUIT_NAME[m]} og {hp} hp: 3{SUIT_SYM[m]} er naturligt og spærrende.",
                                     f"{L[m]} {SUIT_NAME_EN[m]} and {hp} HCP: 3{SUIT_SYM[m]} is natural and preemptive.")
    if hp >= OVERCALL_HP[0]:
        if sorted((S, H)) == [4, 5]:
            if max(D, C) >= 4:
                return None   # 5-4-4-0 med begge majorer beskriver kortet ikke
            return "2♣", tx(f"{hp} hp med {S} spar og {H} hjerter: 2♣ viser begge majorer, 5-4.",
                            f"{hp} HCP with {S} spades and {H} hearts: 2♣ shows both majors, 5-4.")
        for M, O in (('H', 'S'), ('S', 'H')):
            m = minor_of(L)
            if L[M] == 5 and L[O] <= 3 and m:
                return f"2{SUIT_SYM[M]}", tx(f"5 {SUIT_NAME[M]} og {L[m]} {SUIT_NAME[m]}: 2{SUIT_SYM[M]} viser femfarven "
                                             f"og 4–5 kort i en ukendt minor.",
                                             f"5 {SUIT_NAME_EN[M]} and {L[m]} {SUIT_NAME_EN[m]}: 2{SUIT_SYM[M]} shows the five-card suit "
                                             f"and 4–5 cards in an unknown minor.")
        if D >= 4 and C >= 4 and max(D, C) >= 5 and max(S, H) <= 3:
            return "2NT", tx(f"{D} ruder og {C} klør: 2NT viser begge minorer.", f"{D} diamonds and {C} clubs: 2NT shows both minors.")
        if minor6 or major6:
            return None
    return "Pas", tx(f"{hp} hp og ingen fordeling, der passer til en indmelding – og ikke en stærk jævn hånd til D.",
                     f"{hp} HCP and no shape that suits an overcall – and not a strong balanced hand for X.")

# --- Indmelders næste melding ------------------------------------------------------

def rebid_2kl_2ru(hand, hp):
    """1NT – 2♣ – pas – 2♦ – pas – ? : makker spørger efter femfarven."""
    L = lengths_of(hand)
    M = 'S' if L['S'] == 5 else 'H'
    return f"2{SUIT_SYM[M]}", tx(f"2♦ spørger efter femfarven: du har 5 {SUIT_NAME[M]} og melder 2{SUIT_SYM[M]}.",
                                 f"2♦ asks for the five-card suit: you have 5 {SUIT_NAME_EN[M]} and bid 2{SUIT_SYM[M]}.")

def rebid_2m_2nt(hand, hp):
    """1NT – 2♥/2♠ – pas – 2NT – pas – ? : makker spørger efter minoren."""
    L = lengths_of(hand)
    m = minor_of(L)
    return f"3{SUIT_SYM[m]}", tx(f"2NT spørger efter minorfarven: du har {L[m]} {SUIT_NAME[m]} og melder 3{SUIT_SYM[m]}.",
                                 f"2NT asks for the minor: you have {L[m]} {SUIT_NAME_EN[m]} and bid 3{SUIT_SYM[m]}.")

def rebid_2ru_2hj(hand, hp):
    """1NT – 2♦ – pas – 2♥ – pas – ? : pas eller korriger."""
    M = multi_major(lengths_of(hand))
    if M == 'H':
        return "Pas", tx("2♥ er pas eller korriger. Din farve er hjerter, så du passer.", "2♥ is pass or correct. Your suit is hearts, so you pass.")
    return "2♠", tx("2♥ er pas eller korriger. Din farve er spar, så du retter til 2♠.", "2♥ is pass or correct. Your suit is spades, so you correct to 2♠.")

def rebid_2ru_4hj(hand, hp):
    """1NT – 2♦ – pas – 4♥ – pas – ? : pas eller korriger, spærrende."""
    M = multi_major(lengths_of(hand))
    if M == 'H':
        return "Pas", tx("4♥ er pas eller korriger (spærrende). Din farve er hjerter, så du passer.",
                         "4♥ is pass or correct (preemptive). Your suit is hearts, so you pass.")
    return "4♠", tx("4♥ er pas eller korriger (spærrende). Din farve er spar, så du retter til 4♠.",
                    "4♥ is pass or correct (preemptive). Your suit is spades, so you correct to 4♠.")

def rebid_plauken(hand, hp):
    """1NT – 2♦ – pas – 2NT – pas – ? : Plauken."""
    M = multi_major(lengths_of(hand))
    if hp >= MULTI_MAX:
        return "3♣", tx(f"{hp} hp er god multi (8–10): 3♣. Makker kan spørge efter farven med 3♦.",
                        f"{hp} HCP is a good multi (8–10): 3♣. Partner can ask for the suit with 3♦.")
    call = "3♦" if M == 'H' else "3♥"
    return call, tx(f"{hp} hp er dårlig multi (6–7): {call} er transfer til {SUIT_NAME[M]} – "
                    f"3♦ viser hjerter, 3♥ viser spar.",
                    f"{hp} HCP is a poor multi (6–7): {call} is a transfer to {SUIT_NAME_EN[M]} – "
                    f"3♦ shows hearts, 3♥ shows spades.")

def rebid_plauken_relay(hand, hp):
    """1NT – 2♦ – pas – 2NT – pas – 3♣ – pas – 3♦ – pas – ? : transfer."""
    M = multi_major(lengths_of(hand))
    call = "3♠" if M == 'H' else "3♥"
    return call, tx(f"3♦ beder om farven. Svaret er transfer: 3♠ = hjerter, 3♥ = spar. Din farve er {SUIT_NAME[M]}: {call}.",
                    f"3♦ asks for the suit. The answer is a transfer: 3♠ = hearts, 3♥ = spades. Your suit is {SUIT_NAME_EN[M]}: {call}.")

# --- Svarer --------------------------------------------------------------------------

def classify_after_2kl(hand, hp):
    """1NT – 2♣ – pas – ? : begge majorer 5-4."""
    if hp > ADV_2KL_MAX:
        return None
    L = lengths_of(hand)
    S, H = L['S'], L['H']
    if S == H:
        return "2♦", tx(f"Lige mange spar og hjerter ({S}-{H}): 2♦ spørger efter makkers femfarve, så I lander i 5-{S}-fittet.",
                        f"As many spades as hearts ({S}-{H}): 2♦ asks for partner's five-card suit, so you land in the 5-{S} fit.")
    M = 'S' if S > H else 'H'
    return f"2{SUIT_SYM[M]}", tx(f"Flest {SUIT_NAME[M]} ({S} spar, {H} hjerter): 2{SUIT_SYM[M]} er præference til den "
                                 f"bedste major – det sædvanlige svar.",
                                 f"More {SUIT_NAME_EN[M]} ({S} spades, {H} hearts): 2{SUIT_SYM[M]} is a preference for the "
                                 f"better major – the usual response.")

def classify_after_2ru(hand, hp):
    """1NT – 2♦ – pas – ? : multi, 6+ i en ukendt major, ca. 6–10 hp."""
    L = lengths_of(hand)
    S, H = L['S'], L['H']
    if hp >= ADV_GAME:
        for M, O in (('H', 'S'), ('S', 'H')):
            if L[M] >= 6 and top_honours(hand[M]) >= 2 and L[O] <= 2:
                sym = SUIT_SYM[M]
                return f"3{sym}", tx(f"{hp} hp og egen {SUIT_NAME[M]}farve ({L[M]} kort): 3{sym} viser styrke i farven, ingen "
                                     f"interesse for den anden major og udgangsinteresse. Makker støtter med xxx eller Hx.",
                                     f"{hp} HCP and your own {SUIT_NAME_EN[M][:-1]} suit ({L[M]} cards): 3{sym} shows strength in the suit, no "
                                     f"interest in the other major and game interest. Partner raises with xxx or Hx.")
        if S >= 3 and H >= 3:
            return "2NT", tx(f"{hp} hp og plads i begge majorer: 2NT (Plauken) er stærkt relæ – udgangsinteresse, uanset hvilken major makker har.",
                             f"{hp} HCP and room in both majors: 2NT (Plauken) is a strong relay – game interest whichever major partner holds.")
        if H >= 3:
            return "2♠", tx(f"{hp} hp med {H} hjerter, men kun {S} spar: 2♠ er udgangsopfordring, hvis makker har hjerter. "
                            f"Har makker spar, passer han.",
                            f"{hp} HCP with {H} hearts, but only {S} spades: 2♠ invites game if partner has hearts. "
                            f"If partner has spades, partner passes.")
        if S >= 3:
            return "2♥", tx(f"{hp} hp med {S} spar, men kun {H} hjerter: 2♥ er pas eller korriger. Retter makker til 2♠, "
                            f"kan du støtte til udgang.",
                            f"{hp} HCP with {S} spades, but only {H} hearts: 2♥ is pass or correct. If partner corrects to 2♠, "
                            f"you can raise to game.")
        return None
    if hp <= ADV_4HJ_MAX and S >= 3 and H >= 3 and max(S, H) >= 4:
        return "4♥", tx(f"Svag hånd med fit til begge majorer ({S} spar, {H} hjerter): 4♥ er pas eller korriger og spærrende.",
                        f"Weak hand with a fit for both majors ({S} spades, {H} hearts): 4♥ is pass or correct and preemptive.")
    return "2♥", tx(f"Svag hånd ({hp} hp): 2♥ er pas eller korriger – makker passer med hjerter og retter til 2♠ "
                    f"med spar. Alle svage hænder melder 2♥.",
                    f"Weak hand ({hp} HCP): 2♥ is pass or correct – partner passes with hearts and corrects to 2♠ "
                    f"with spades. Every weak hand bids 2♥.")

def after_major_minor(M):
    """1NT – 2♥/2♠ – pas – ? : 5 i majoren + 4–5 i en ukendt minor."""
    sym, name, en = SUIT_SYM[M], SUIT_NAME[M], SUIT_NAME_EN[M]
    def classify(hand, hp):
        if hp > ADV_2M_MAX:
            return None
        L = lengths_of(hand)
        if L[M] >= 2:
            return "Pas", tx(f"{L[M]} {name}: pas er det sædvanlige svar – I spiller 2{sym}.", f"{L[M]} {en}: pass is the usual response – you play 2{sym}.")
        if L['D'] >= 3 and L['C'] >= 3:
            return "2NT", tx(f"Kun {L[M]} {name}, men {L['D']} ruder og {L['C']} klør: 2NT spørger efter makkers minor, "
                             f"så I lander i et sikkert fit.",
                             f"Only {L[M]} {en}, but {L['D']} diamonds and {L['C']} clubs: 2NT asks for partner's minor, "
                             f"so you land in a safe fit.")
        return None
    return classify

def classify_after_2nt(hand, hp):
    """1NT – 2NT – pas – ? : begge minorer. Kortet beskriver ikke svarene – præference til den længste."""
    if hp > ADV_2NT_MAX:
        return None
    L = lengths_of(hand)
    if L['D'] > L['C']:
        return "3♦", tx(f"Flest ruder ({L['D']} ruder, {L['C']} klør): 3♦ – præference til den længste minor.",
                        f"More diamonds ({L['D']} diamonds, {L['C']} clubs): 3♦ – preference for the longer minor.")
    return "3♣", tx(f"{L['C']} klør og {L['D']} ruder: 3♣ – præference til klør, når den er mindst lige så lang.",
                    f"{L['C']} clubs and {L['D']} diamonds: 3♣ – preference for clubs when they are at least as long.")

def classify_after_double(hand, hp):
    """1NT – D – pas – ? : modstanderne spiller svag sans (12–14)."""
    L = lengths_of(hand)
    long5 = [s for s in SUITS if L[s] >= 5]
    if JUMP_HP[0] <= hp <= JUMP_HP[1] and len(long5) > 1:
        return None   # to 5-farver: kortet siger ikke, hvilken der springes i
    if JUMP_HP[0] <= hp <= JUMP_HP[1] and long5:
        s = long5[0]
        return f"3{SUIT_SYM[s]}", tx(f"{hp} hp og {L[s]} {SUIT_NAME[s]}: spring til 3{SUIT_SYM[s]} er udgangsforslag i farven "
                                     f"eller sans (mindst 5-farve, ca. 9–11 hp).",
                                     f"{hp} HCP and {L[s]} {SUIT_NAME_EN[s]}: the jump to 3{SUIT_SYM[s]} invites game in the suit "
                                     f"or notrump (at least a five-card suit, about 9–11 HCP).")
    if hp >= STRAF_MIN:
        if long5 and hp > JUMP_HP[1]:
            return None
        return "Pas", tx(f"{hp} hp: strafpas (8+). Over for makkers stærke jævne hånd står 1NT doblet sandsynligvis flere ned.",
                         f"{hp} HCP: pass for penalty (8+). Opposite partner's strong balanced hand, 1NT doubled will probably go several down.")
    for s in ('C', 'D', 'H', 'S'):
        if L[s] >= 4:
            return f"2{SUIT_SYM[s]}", tx(f"{hp} hp: med 0–7 hp scrambles der – meld din laveste 4-farve (2{SUIT_SYM[s]}). "
                                         f"Uden 3-kortstøtte melder makker sin laveste 4-farve over, til I har et 4-3-fit.",
                                         f"{hp} HCP: with 0–7 HCP you scramble – bid your lowest four-card suit (2{SUIT_SYM[s]}). "
                                         f"Without three-card support, partner bids the next four-card suit up until you have a 4-3 fit.")
    return None

# --- Situationer ---------------------------------------------------------------------

M54 = tx("Begge majorer 5–4, 10–16 hp", "Both majors 5–4, 10–16 HCP")
MULTI = tx("6+ i en major, ca. 6–10 hp", "6+ cards in a major, about 6–10 HCP")
MM54 = tx("Major + minor 5–4, 10–16 hp", "Major + minor 5–4, 10–16 HCP")
RELAE = tx("Stærkt relæ med udgangsinteresse", "A strong relay with game interest")
HJ = tx("5 hjerter + 4–5 i en ukendt minor, 10–16 hp", "5 hearts + 4–5 cards in an unknown minor, 10–16 HCP")
SP = tx("5 spar + 4–5 i en ukendt minor, 10–16 hp", "5 spades + 4–5 cards in an unknown minor, 10–16 HCP")
BM = tx("Begge minorer, 10–16 hp", "Both minors, 10–16 HCP")
DBL = tx("15–17+ hp jævn – forslag til straf", "15–17+ HCP balanced – suggests penalty")
FRI = tx("Mindst 15 hp, fri fordeling – semikrav", "At least 15 HCP, any shape – semi-forcing")
BM5 = tx("Begge majorer 5–4", "Both majors 5–4")
MM_WHY = tx("2♥/2♠ viser femfarven i den meldte major og en 4–5-farve i en minor, som 2NT kan spørge efter.",
            "2♥/2♠ shows five cards in the major bid and a 4–5-card minor, which 2NT can ask for.")
BONUS = {
    "2kl": {"q": tx("Hvad viser makkers 2♣?", "What does partner's 2♣ show?"), "correct": M54,
            "options": [M54, MULTI, MM54],
            "why": tx("2♣ viser begge majorer, 5–4. Svarer ved ikke, hvilken der er femfarven – derfor findes 2♦ som spørgsmål.",
                      "2♣ shows both majors, 5–4. The advancer does not know which is the five-card suit – hence 2♦ as an ask.")},
    "2ru": {"q": tx("Hvad viser 2♦ i Multiforsvar?", "What does 2♦ show in the Multi defence?"), "correct": MULTI,
            "options": [MULTI, M54, tx("Naturlig ruderfarve", "A natural diamond suit")],
            "why": tx("2♦ er multi: en 6-farve i en ukendt major og svagere end de øvrige indmeldinger, ca. 6–10 hp.",
                      "2♦ is multi: a six-card suit in an unknown major, weaker than the other overcalls, about 6–10 HCP.")},
    "plauken": {"q": tx("Hvad er 2NT efter makkers 2♦ (Plauken)?", "What is 2NT after partner's 2♦ (Plauken)?"), "correct": RELAE,
                "options": [RELAE, tx("Naturligt, 11–12 hp", "Natural, 11–12 HCP"), tx("Spørger efter minoren", "Asks for the minor")],
                "why": tx("2NT er stærkt relæ: udgangsinteresse, uanset hvilken major multi-melderen har. 3♣ viser god multi, 3♦/3♥ dårlig multi som transfer.",
                          "2NT is a strong relay: game interest whichever major the multi bidder holds. "
                          "3♣ shows a good multi, 3♦/3♥ a poor multi as a transfer.")},
    "2hj": {"q": tx("Hvad viser 2♥ i Multiforsvar?", "What does 2♥ show in the Multi defence?"), "correct": HJ,
            "options": [HJ, tx("6+ hjerter, svag hånd", "6+ hearts, a weak hand"), BM5],
            "why": MM_WHY},
    "2sp": {"q": tx("Hvad viser 2♠ i Multiforsvar?", "What does 2♠ show in the Multi defence?"), "correct": SP,
            "options": [SP, tx("6+ spar, svag hånd", "6+ spades, a weak hand"), BM5],
            "why": MM_WHY},
    "2nt": {"q": tx("Hvad viser 2NT i Multiforsvar?", "What does 2NT show in the Multi defence?"), "correct": BM,
            "options": [BM, tx("Jævn hånd, 15–17 hp", "A balanced hand, 15–17 HCP"), BM5],
            "why": tx("2NT er usædvanlig 2NT: begge minorer, 10–16 hp.", "2NT is the Unusual 2NT: both minors, 10–16 HCP.")},
    "indmelding": {"q": tx("Hvad viser doblingen af modstandernes 1NT?", "What does the double of the opponents' 1NT show?"), "correct": DBL,
                   "options": [DBL, FRI, tx("Begge majorer, 10–16 hp", "Both majors, 10–16 HCP")],
                   "why": tx("Doblingen er forslag til straf med en jævn hånd af mindst samme styrke som åbningen. 2♣, 2♥/2♠ og 2NT viser 10–16 hp, 2♦ ca. 6–10.",
                             "The double suggests penalty with a balanced hand at least as strong as the opening. "
                             "2♣, 2♥/2♠ and 2NT show 10–16 HCP, 2♦ about 6–10.")},
    "dobling": {"q": tx("Hvad viser makkers dobling af 1NT?", "What does partner's double of 1NT show?"), "correct": DBL,
                "options": [DBL, FRI, tx("Begge majorer, 10–16 hp", "Both majors, 10–16 HCP")],
                "why": tx("Doblingen er forslag til straf. Derfor er strafpas med 8+ hp oftest det rigtige svar; med 0–7 hp scrambles der.",
                          "The double suggests penalty. So passing for penalty with 8+ HCP is usually right; with 0–7 HCP you scramble.")},
}

PAS = ["Modstander", "Pas"]
SVAG_SANS = tx("1NT = 12–14 hp (svag sans)", "1NT = 12–14 HCP (weak notrump)")
SITUATIONS = {
    "indmelding": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"]], "allowX": True,
                   "calls": ["X", "Pas", "2♣", "2♦", "2♥", "2♠", "2NT", "3♣", "3♦"], "bonus": BONUS["indmelding"]},
    "gen_2kl": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♣"], PAS, ["Makker", "2♦"], PAS],
                "calls": ["2♥", "2♠", "2NT", "3♣"], "bonus": BONUS["2kl"]},
    "gen_2hj": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♥"], PAS, ["Makker", "2NT"], PAS],
                "calls": ["3♣", "3♦", "3♥", "3NT"], "bonus": BONUS["2hj"]},
    "gen_2sp": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♠"], PAS, ["Makker", "2NT"], PAS],
                "calls": ["3♣", "3♦", "3♠", "3NT"], "bonus": BONUS["2sp"]},
    "gen_2ru_2hj": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♦"], PAS, ["Makker", "2♥"], PAS],
                    "calls": ["Pas", "2♠", "2NT", "3♥"], "bonus": BONUS["2ru"]},
    "gen_2ru_4hj": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♦"], PAS, ["Makker", "4♥"], PAS],
                    "calls": ["Pas", "4♠", "4NT", "5♥"], "bonus": BONUS["2ru"]},
    "gen_plauken": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♦"], PAS, ["Makker", "2NT"], PAS],
                    "calls": ["3♣", "3♦", "3♥", "3♠", "3NT"], "bonus": BONUS["plauken"]},
    "gen_plauken_relae": {"rolle": "Indmelder", "auction": [["Modstander", "1NT"], ["Dig", "2♦"], PAS, ["Makker", "2NT"], PAS,
                                                            ["Dig", "3♣"], PAS, ["Makker", "3♦"], PAS],
                          "calls": ["3♥", "3♠", "3NT", "4♥"], "bonus": BONUS["plauken"]},
    "svar_2kl": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♣"], PAS],
                 "calls": ["Pas", "2♦", "2♥", "2♠", "2NT", "3♥", "3♠"], "bonus": BONUS["2kl"]},
    "svar_2ru": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♦"], PAS],
                 "calls": ["Pas", "2♥", "2♠", "2NT", "3♥", "3♠", "3NT", "4♥"], "bonus": BONUS["2ru"]},
    "svar_2hj": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♥"], PAS],
                 "calls": ["Pas", "2♠", "2NT", "3♣", "3♥"], "bonus": BONUS["2hj"]},
    "svar_2sp": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2♠"], PAS],
                 "calls": ["Pas", "2NT", "3♣", "3♦", "3♠"], "bonus": BONUS["2sp"]},
    "svar_2nt": {"rolle": "Svarer", "auction": [["Modstander", "1NT"], ["Makker", "2NT"], PAS],
                 "calls": ["3♣", "3♦", "3♥", "3NT"], "bonus": BONUS["2nt"]},
    "svar_dobling": {"rolle": "Svarer", "note": SVAG_SANS, "auction": [["Modstander", "1NT"], ["Makker", "X"], PAS],
                     "calls": ["Pas", "2♣", "2♦", "2♥", "2♠", "3♣", "3♦", "3♥", "3♠", "2NT"], "bonus": BONUS["dobling"]},
}

CLASSIFIERS = {
    "indmelding": classify_overcall,
    "gen_2kl": rebid_2kl_2ru, "gen_2hj": rebid_2m_2nt, "gen_2sp": rebid_2m_2nt,
    "gen_2ru_2hj": rebid_2ru_2hj, "gen_2ru_4hj": rebid_2ru_4hj,
    "gen_plauken": rebid_plauken, "gen_plauken_relae": rebid_plauken_relay,
    "svar_2kl": classify_after_2kl, "svar_2ru": classify_after_2ru,
    "svar_2hj": after_major_minor('H'), "svar_2sp": after_major_minor('S'),
    "svar_2nt": classify_after_2nt, "svar_dobling": classify_after_double,
}

def major_minor(M, hp=OVERCALL_HP):
    return either(tpl(hp, **{M: (5, 5), 'D': (4, 5)}), tpl(hp, **{M: (5, 5), 'C': (4, 5)}))

SAMPLERS = {
    "indmelding": {
        "X": either(tpl(DOUBLE_HP, S=(2, 4), H=(2, 4), D=(2, 4), C=(2, 4)),
                    *[tpl(DOUBLE_HP, **{x: (5, 5) if x == s else (2, 3) for x in SUITS}) for s in SUITS]),
        "Pas": rnd((3, 14)), "2♣": gen_5_4_majors, "2♦": gen_multi,
        "2♥": major_minor('H'), "2♠": major_minor('S'),
        "2NT": tpl(OVERCALL_HP, D=(4, 6), C=(4, 6)),
        "3♣": tpl(PREEMPT_MINOR_HP, C=(6, 7)), "3♦": tpl(PREEMPT_MINOR_HP, D=(6, 7)),
    },
    "gen_2kl": {"2♥": lambda: gen_5_4_majors(), "2♠": lambda: gen_5_4_majors()},
    "gen_2hj": {"3♣": tpl(OVERCALL_HP, H=(5, 5), C=(4, 5)), "3♦": tpl(OVERCALL_HP, H=(5, 5), D=(4, 5))},
    "gen_2sp": {"3♣": tpl(OVERCALL_HP, S=(5, 5), C=(4, 5)), "3♦": tpl(OVERCALL_HP, S=(5, 5), D=(4, 5))},
    "gen_2ru_2hj": {"Pas": lambda: gen_multi(major='H'), "2♠": lambda: gen_multi(major='S')},
    "gen_2ru_4hj": {"Pas": lambda: gen_multi(major='H'), "4♠": lambda: gen_multi(major='S')},
    "gen_plauken": {"3♣": lambda: gen_multi((MULTI_MAX, MULTI_HP[1])),
                    "3♦": lambda: gen_multi((MULTI_HP[0], MULTI_MAX - 1), 'H'),
                    "3♥": lambda: gen_multi((MULTI_HP[0], MULTI_MAX - 1), 'S')},
    "gen_plauken_relae": {"3♠": lambda: gen_multi((MULTI_MAX, MULTI_HP[1]), 'H'),
                          "3♥": lambda: gen_multi((MULTI_MAX, MULTI_HP[1]), 'S')},
    "svar_2kl": {"2♦": tpl((0, ADV_2KL_MAX), S=(2, 4), H=(2, 4), D=(1, 5), C=(1, 5)),
                 "2♥": rnd((0, ADV_2KL_MAX)), "2♠": rnd((0, ADV_2KL_MAX))},
    "svar_2ru": {"2♥": either(rnd((0, 13)), tpl((ADV_GAME, 17), S=(3, 5), H=(0, 2), D=(1, 5), C=(1, 5))),
                 "2♠": tpl((ADV_GAME, 17), H=(3, 5), S=(0, 2), D=(1, 5), C=(1, 5)),
                 "2NT": tpl((ADV_GAME, 18), S=(3, 4), H=(3, 4), D=(2, 4), C=(2, 4)),
                 "3♥": tpl((ADV_GAME + 1, 19), H=(6, 7), S=(0, 2), D=(1, 4), C=(1, 4)),
                 "3♠": tpl((ADV_GAME + 1, 19), S=(6, 7), H=(0, 2), D=(1, 4), C=(1, 4)),
                 "4♥": tpl((0, ADV_4HJ_MAX), S=(3, 4), H=(3, 4), D=(0, 5), C=(0, 5))},
    "svar_2hj": {"Pas": rnd((0, ADV_2M_MAX)), "2NT": tpl((0, ADV_2M_MAX), H=(0, 1), D=(3, 6), C=(3, 6), S=(0, 5))},
    "svar_2sp": {"Pas": rnd((0, ADV_2M_MAX)), "2NT": tpl((0, ADV_2M_MAX), S=(0, 1), D=(3, 6), C=(3, 6), H=(0, 5))},
    "svar_2nt": {"3♣": rnd((0, ADV_2NT_MAX)), "3♦": tpl((0, ADV_2NT_MAX), D=(3, 6), C=(0, 3), S=(0, 5), H=(0, 5))},
    "svar_dobling": {
        "Pas": rnd((STRAF_MIN, 14)),
        "2♣": tpl((0, SCRAMBLE_MAX), C=(4, 6), D=(0, 4), H=(0, 4), S=(0, 4)),
        "2♦": tpl((0, SCRAMBLE_MAX), D=(4, 6), C=(0, 3), H=(0, 4), S=(0, 4)),
        "2♥": tpl((0, SCRAMBLE_MAX), H=(4, 6), C=(0, 3), D=(0, 3), S=(0, 4)),
        "2♠": tpl((0, SCRAMBLE_MAX), S=(4, 6), C=(0, 3), D=(0, 3), H=(0, 3)),
        **{f"3{SUIT_SYM[s]}": tpl(JUMP_HP, **{x: (5, 6) if x == s else (0, 4) for x in SUITS}) for s in SUITS},
    },
}

PER_CALL = {"indmelding": 6, "gen_2kl": 5, "gen_2hj": 5, "gen_2sp": 5, "gen_2ru_2hj": 4, "gen_2ru_4hj": 4,
            "gen_plauken": 4, "gen_plauken_relae": 4, "svar_2kl": 5, "svar_2ru": 4, "svar_2hj": 5,
            "svar_2sp": 5, "svar_2nt": 4, "svar_dobling": 3}

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
