"""
Muiderberg (Bikini) 2♥ og 2♠ – åbningen, svarene, pas eller ret efter 3♣ og 2NT-relæet efter Franks tekst af
21. november 2026 (F), med hullerne udfyldt efter dokumentet "Ruder Multi" (W). Bygger på konventionskortet
data/kort/muiderberg.json og er uafhængig af makker (SPEC-muiderberg.md, system "generel"). Muiderberg forudsætter, at
Multi 2♦ (dealer/multi_2ru.py) tager de svage hænder med en seksfarve i en major.

2♥/2♠ viser præcis fem kort i majoren, 4–5 kort i en ukendt minor, højst tre i den anden major og ca. 5–10 hp (F).

Situationer (traener.html tager meldeforløbet fra situationen, så svar, ret og spm har én situation pr. åbning):
  aabning      – ?                          2♥/2♠ efter F · 2♦ (Multi) med seksfarve · 1♥/1♠ med 11–15 · pas med 0–4
  svar_2h/_2s  – 2M – pas – ?               første regel, der passer (Grænser nedenfor): 4M, 2NT, 3M, 3♣ og pas
  ret_2h/_2s   – 2M – pas – 3♣ – pas – ?    pas med klør, 3♦ med ruder
  spm_2h/_2s   – 2M – pas – 2NT – pas – ?   3♣ min/klør · 3♦ min/ruder · 3♥ maks/klør · 3♠ maks/ruder
Ikke med i puljen (Afklaret, punkt 3, 4 og 9): ny farve og 2♠ efter 2♥ som svar, zonestilling, svarhænder uden regel
og åbningshænder med to minorer på 4+ kort (minoren er ikke entydig).
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx, hp_of, sp_of
from .multi_2ru import gyldig as gyldig_multi, aab as aab_multi, antal, og, hp_tx

# --- Grænser, som kilderne ikke giver tal for – ret dem her ------------
MIN_HP, MAX_HP = (5, 7), (8, 10)            # åbners minimum og maksimum inden for 5–10

# svar: 2M – Pas – ?  (første regel, der passer)
UDGANG       = dict(stoette=3, hp=(13, 16))  # 4M: 3+ i åbners major, 13–16 hp
SPAER_UDGANG = dict(stoette=4, hp=(0, 10))   # 4M: 4+ i åbners major, højst 10 hp (spærrende)
SPOERG       = dict(hp=17)                   # 2NT: 17+ hp,
SPOERG_INVIT = dict(stoette=3, hp=(11, 12))  #      eller 3+ støtte og 11–12 hp
ENKELTLOEFT  = dict(stoette=3, hp=(6, 10))   # 3M: præcis 3 i åbners major, 6–10 hp (RONF)
MINOR_RET    = dict(major_max=1, minor=3, hp_max=10)  # 3♣: højst 1 i åbners major, 3+ i begge minorer, højst 10 hp
# Pas: 2+ i åbners major og højst 10 hp
# Ny farve (W: naturlig og krav) og 2♠ efter 2♥ genereres ikke (Afklaret, punkt 3)
# En svarhånd, der ikke rammer en regel, genereres ikke (Afklaret, punkt 9)

PER_CALL_N = 7
PAS = ["Modstander", "Pas"]
inden = lambda hp, rng: rng[0] <= hp <= rng[1]
anden = lambda M: 'S' if M == 'H' else 'H'
NAVN = {'H': 'h', 'S': 's'}


def fordeling(hand):
    """(major, minor) for en Muiderberg-fordeling, ellers None: præcis fem i majoren, højst tre i den anden major og
    4–5 kort i én minor; den anden minor har højst tre, så minoren er entydig."""
    L = lengths_of(hand)
    for M in 'HS':
        if L[M] == 5 and L[anden(M)] <= 3:
            minorer = [m for m in 'CD' if L[m] >= 4]
            if len(minorer) == 1 and L[minorer[0]] <= 5:
                return M, minorer[0]
    return None


def gyldig(hand, hp):
    """En gyldig Muiderberg-åbning: fordelingen ovenfor og 5–10 hp."""
    return fordeling(hand) is not None and 5 <= hp <= 10


def fem(hand):
    """'5 hjerter og 4 klør' / '5 hearts and 4 clubs'."""
    M, m = fordeling(hand)
    n = len(hand[m])
    return tx(f"5 {SUIT_NAME[M]} og {n} {SUIT_NAME[m]}", f"5 {SUIT_NAME_EN[M]} and {n} {SUIT_NAME_EN[m]}")


def fem_hp(hand, hp):
    """'5 hjerter, 4 klør og 8 hp' / '5 hearts, 4 clubs and 8 HCP'."""
    M, m = fordeling(hand)
    n = len(hand[m])
    return og(tx(f"5 {SUIT_NAME[M]}", f"5 {SUIT_NAME_EN[M]}"), tx(f"{n} {SUIT_NAME[m]}", f"{n} {SUIT_NAME_EN[m]}"),
              hp_tx(hp))


# --- aabning ----------------------------------------------------------------------

def aabning(hand, hp):
    if gyldig_multi(hand, hp):
        L = lengths_of(hand)
        M = 'H' if L['H'] == 6 else 'S'
        es = tx("intet es", "no ace") if not any(14 in hand[s] for s in SUITS) else tx("ét es", "one ace")
        return "2♦", tx(f"6 {SUIT_NAME[M]}, {hp} hp og {es}: 2♦ – med en seksfarve i majoren åbnes Multi 2♦. "
                        "Muiderberg 2♥/2♠ viser en femfarve.",
                        f"6 {SUIT_NAME_EN[M]}, {hp} HCP and {es.en}: 2♦ – with a six-card major the opening is Multi 2♦. "
                        "Muiderberg 2♥/2♠ shows a five-card suit.")
    f = fordeling(hand)
    if not f:
        return None
    M, sym, b = f[0], SUIT_SYM[f[0]], fem_hp(hand, hp)
    if hp <= 4:
        m = fordeling(hand)[1]
        kun = og(tx(f"5 {SUIT_NAME[M]}", f"5 {SUIT_NAME_EN[M]}"),
                 tx(f"{len(hand[m])} {SUIT_NAME[m]}", f"{len(hand[m])} {SUIT_NAME_EN[m]}"),
                 tx(f"kun {hp} hp", f"only {hp} HCP"))
        return "Pas", tx(f"{kun}: pas – Muiderberg kræver ca. 5–10 hp.",
                         f"{kun.en}: pass – Muiderberg needs about 5–10 HCP.")
    if hp <= 10:
        return f"2{sym}", tx(f"{b}: 2{sym} – Muiderberg: en femfarve i {SUIT_NAME[M]} og mindst fire kort i en ukendt "
                             "minor med ca. 5–10 hp.",
                             f"{b.en}: 2{sym} – Muiderberg: a five-card {SUIT_NAME_EN[M][:-1]} suit and at least four "
                             "cards in an unknown minor with about 5–10 HCP.")
    if hp <= 15:
        return f"1{sym}", tx(f"{b}: 1{sym} – med 11–15 hp er hånden for stærk til Muiderberg (ca. 5–10 hp).",
                             f"{b.en}: 1{sym} – with 11–15 HCP the hand is too strong for Muiderberg (about 5–10 HCP).")
    return None


# --- svar: 2M – pas – ? ------------------------------------------------------------

SPOERG_TX = tx("Åbner viser minor og styrke: 3♣ minimum med klør, 3♦ minimum med ruder, 3♥ maksimum med klør og 3♠ "
               "maksimum med ruder.",
               "Opener shows the minor and strength: 3♣ a minimum with clubs, 3♦ a minimum with diamonds, 3♥ a maximum "
               "with clubs and 3♠ a maximum with diamonds.")


def svar_paa(M):
    sym = SUIT_SYM[M]

    def svar(hand, hp):
        L = lengths_of(hand)
        st = L[M]
        s = og(antal(st, M), hp_tx(hp))
        u = UDGANG
        if st >= u['stoette'] and inden(hp, u['hp']):
            return f"4{sym}", tx(f"{s}: 4{sym} – slutkontrakt i åbners major.",
                                 f"{s.en}: 4{sym} – sign-off in opener's major.")
        u = SPAER_UDGANG
        if st >= u['stoette'] and inden(hp, u['hp']):
            return f"4{sym}", tx(f"{s}: 4{sym} – slutkontrakt i åbners major. Med mindst fire trumf er udgangen spærrende.",
                                 f"{s.en}: 4{sym} – sign-off in opener's major. With at least four trumps the game bid is "
                                 "preemptive.")
        if hp >= SPOERG['hp']:
            return "2NT", tx(f"{hp} hp: 2NT – kunstigt, stærkt spørgebud. {SPOERG_TX}",
                             f"{hp} HCP: 2NT – artificial, strong enquiry. {SPOERG_TX.en}")
        u = SPOERG_INVIT
        if st >= u['stoette'] and inden(hp, u['hp']):
            return "2NT", tx(f"{s}: 2NT – kunstigt, stærkt spørgebud. Efter åbners svar vælger svarer mellem "
                             "delkontrakt og udgang.",
                             f"{s.en}: 2NT – artificial, strong enquiry. After opener's answer responder chooses "
                             "between a partscore and game.")
        u = ENKELTLOEFT
        if st == u['stoette'] and inden(hp, u['hp']):
            return f"3{sym}", tx(f"{s}: 3{sym} – enkeltløft i åbners major: spærrepræget og ikke krav.",
                                 f"{s.en}: 3{sym} – a single raise in opener's major: preemptive and non-forcing.")
        u = MINOR_RET
        if st <= u['major_max'] and L['C'] >= u['minor'] and L['D'] >= u['minor'] and hp <= u['hp_max']:
            b = og(antal(st, M), antal(L['C'], 'C'), antal(L['D'], 'D'), hp_tx(hp))
            return "3♣", tx(f"{b}: 3♣ – pas eller ret: ønske om at spille i åbners minor. Åbner passer med klør og "
                            "melder 3♦ med ruder.",
                            f"{b.en}: 3♣ – pass or correct: to play in opener's minor. Opener passes with clubs and "
                            "bids 3♦ with diamonds.")
        if st >= 2 and hp <= 10:
            if st >= ENKELTLOEFT['stoette'] and hp < ENKELTLOEFT['hp'][0]:
                return "Pas", tx(f"{s}: pas – præference til åbners major. Hånden er for svag til enkeltløftet.",
                                 f"{s.en}: pass – preference for opener's major. The hand is too weak for the single "
                                 "raise.")
            return "Pas", tx(f"{s}: pas – præference til åbners major.",
                             f"{s.en}: pass – preference for opener's major.")
        return None
    return svar


# --- ret: 2M – pas – 3♣ – pas – ? --------------------------------------------------

def ret_paa(M):
    def ret(hand, hp):
        if not gyldig(hand, hp) or fordeling(hand)[0] != M:
            return None
        b = fem(hand)
        if fordeling(hand)[1] == 'C':
            return "Pas", tx(f"{b}: pas – 3♣ er pas eller ret, og med klør passer åbner.",
                             f"{b.en}: pass – 3♣ is pass or correct, and with clubs opener passes.")
        return "3♦", tx(f"{b}: 3♦ – 3♣ er pas eller ret, og med ruder retter åbner til 3♦.",
                        f"{b.en}: 3♦ – 3♣ is pass or correct, and with diamonds opener corrects to 3♦.")
    return ret


# --- spm: 2M – pas – 2NT – pas – ? -------------------------------------------------

SPM = {  # (minor, maksimum) → (melding, dansk, engelsk)
    ('C', False): ("3♣", "minimum med klør", "a minimum with clubs"),
    ('D', False): ("3♦", "minimum med ruder", "a minimum with diamonds"),
    ('C', True): ("3♥", "maksimum med klør", "a maximum with clubs"),
    ('D', True): ("3♠", "maksimum med ruder", "a maximum with diamonds"),
}


def spm_paa(M):
    def spm(hand, hp):
        if not gyldig(hand, hp) or fordeling(hand)[0] != M:
            return None
        mx = inden(hp, MAX_HP)
        call, da, en = SPM[(fordeling(hand)[1], mx)]
        b = fem_hp(hand, hp)
        styrke = tx("maksimum", "a maximum") if mx else tx("minimum", "a minimum")
        return call, tx(f"{b} ({styrke}): {call} – {da}.", f"{b.en} ({styrke.en}): {call} – {en}.")
    return spm


# --- bonusspørgsmål ---------------------------------------------------------------

def bonus(q, correct, andre, why):
    return {"q": q, "correct": correct, "options": [correct, *andre], "why": why}


B_AABNING = bonus(
    tx("Hvad viser en Muiderberg-åbning på 2♥ eller 2♠?", "What does a Muiderberg opening of 2♥ or 2♠ show?"),
    tx("En femfarve i majoren, mindst fire kort i en ukendt minor og ca. 5–10 hp",
       "A five-card major, at least four cards in an unknown minor and about 5–10 HCP"),
    [tx("En seksfarve i majoren og ca. 5–10 hp", "A six-card major and about 5–10 HCP"),
     tx("En femfarve i majoren, mindst fire kort i en ukendt minor og 11–15 hp",
        "A five-card major, at least four cards in an unknown minor and 11–15 HCP")],
    tx("2♥/2♠ viser en femfarve i majoren og mindst fire kort i en ukendt minor med ca. 5–10 hp. Med en seksfarve i "
       "majoren åbnes Multi 2♦.",
       "2♥/2♠ shows a five-card major and at least four cards in an unknown minor with about 5–10 HCP. With a six-card "
       "major the opening is Multi 2♦."))
B_SVAR = {
    'H': bonus(tx("Hvad betyder 3♣ som svar på Muiderberg?", "What does 3♣ mean in response to Muiderberg?"),
               tx("Pas eller ret: ønske om at spille i åbners minor", "Pass or correct: to play in opener's minor"),
               [tx("Naturligt med egen klørfarve", "Natural with responder's own club suit"),
                tx("Kunstigt, stærkt spørgebud", "Artificial, strong enquiry")],
               tx("3♣ er pas eller ret: svarer vil spille i åbners minor. Åbner passer med klør og melder 3♦ med ruder. "
                  "Det stærke spørgebud er 2NT.",
                  "3♣ is pass or correct: responder wants to play in opener's minor. Opener passes with clubs and bids "
                  "3♦ with diamonds. The strong enquiry is 2NT.")),
    'S': bonus(tx("Hvad betyder 3♠ efter 2♠ – pas?", "What does 3♠ mean after 2♠ – pass?"),
               tx("Enkeltløft: spærrepræget og ikke krav", "A single raise: preemptive and non-forcing"),
               [tx("Invit til udgang", "An invitation to game"),
                tx("Kunstigt, stærkt spørgebud", "Artificial, strong enquiry")],
               tx("3♥/3♠ er et enkeltløft i åbners major: spærrepræget og ikke krav (RONF). Det stærke spørgebud er 2NT.",
                  "3♥/3♠ is a single raise in opener's major: preemptive and non-forcing (RONF). The strong enquiry is "
                  "2NT.")),
}
B_RET = {
    M: bonus(tx(f"Hvad melder åbner med ruder efter 2{SUIT_SYM[M]} – 3♣?",
                f"What does opener bid with diamonds after 2{SUIT_SYM[M]} – 3♣?"),
             tx("3♦, fordi 3♣ er pas eller ret", "3♦, because 3♣ is pass or correct"),
             [tx("Pas, fordi 3♣ er svarers egen farve", "Pass, because 3♣ is responder's own suit"),
              tx(f"3{SUIT_SYM[M]}, åbners egen major", f"3{SUIT_SYM[M]}, opener's own major")],
             tx("3♣ er pas eller ret: svarer vil spille i åbners minor. Åbner passer med klør og melder 3♦ med ruder.",
                "3♣ is pass or correct: responder wants to play in opener's minor. Opener passes with clubs and bids "
                "3♦ with diamonds."))
    for M in 'HS'
}
SPM_WHY = tx("Efter 2NT viser 3♣ minimum med klør, 3♦ minimum med ruder, 3♥ maksimum med klør og 3♠ maksimum med "
             "ruder.",
             "After 2NT, 3♣ shows a minimum with clubs, 3♦ a minimum with diamonds, 3♥ a maximum with clubs and 3♠ a "
             "maximum with diamonds.")
B_SPM = {
    'H': bonus(tx("Hvad viser åbners 3♥ efter 2♥ – 2NT?", "What does opener's 3♥ show after 2♥ – 2NT?"),
               tx("Maksimum med klør", "A maximum with clubs"),
               [tx("Minimum med klør", "A minimum with clubs"), tx("Maksimum med ruder", "A maximum with diamonds")],
               SPM_WHY),
    'S': bonus(tx("Hvad viser åbners 3♦ efter 2♠ – 2NT?", "What does opener's 3♦ show after 2♠ – 2NT?"),
               tx("Minimum med ruder", "A minimum with diamonds"),
               [tx("Maksimum med ruder", "A maximum with diamonds"), tx("Minimum med klør", "A minimum with clubs")],
               SPM_WHY),
}

# --- situationer og hænder --------------------------------------------------------

SVAR_CALLS = ["Pas", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "4♥", "4♠"]

SITUATIONS = {"aabning": {"rolle": "Åbner", "auction": [], "calls": ["Pas", "1♥", "1♠", "2♦", "2♥", "2♠"],
                          "bonus": B_AABNING}}
CLASSIFIERS = {"aabning": aabning}
for _M in 'HS':
    _a, _n = f"2{SUIT_SYM[_M]}", NAVN[_M]
    SITUATIONS[f"svar_2{_n}"] = {"rolle": "Svarer", "auction": [["Makker", _a], PAS],
                                 "calls": [c for c in SVAR_CALLS if not (_M == 'S' and c == "2♠")], "bonus": B_SVAR[_M]}
    SITUATIONS[f"ret_2{_n}"] = {"rolle": "Åbner", "auction": [["Dig", _a], PAS, ["Makker", "3♣"], PAS],
                                "calls": ["Pas", "3♦", f"3{SUIT_SYM[_M]}"], "bonus": B_RET[_M]}
    SITUATIONS[f"spm_2{_n}"] = {"rolle": "Åbner", "auction": [["Dig", _a], PAS, ["Makker", "2NT"], PAS],
                                "calls": ["3♣", "3♦", "3♥", "3♠", "3NT"], "bonus": B_SPM[_M]}
    CLASSIFIERS[f"svar_2{_n}"] = svar_paa(_M)
    CLASSIFIERS[f"ret_2{_n}"] = ret_paa(_M)
    CLASSIFIERS[f"spm_2{_n}"] = spm_paa(_M)


def t(hp, **b):
    """Fordeling inden for grænserne (andre farver 0–5) og hp inden for hp."""
    return tpl(hp, **{**{s: (0, 5) for s in SUITS}, **b})


def aab(M, hp, minor=None):
    """Åbnerens hånd: fem kort i M, højst tre i den anden major, 4–5 kort i minoren og højst tre i den anden minor."""
    def en(m):
        return t(hp, **{M: (5, 5), anden(M): (0, 3), m: (4, 5), ('D' if m == 'C' else 'C'): (0, 3)})
    return en(minor) if minor else either(en('C'), en('D'))


class Foerst:
    """Giver først en fast hånd (Franks eksempel), derefter hænder fra sampleren. Nulstilles ved hver export_pool."""
    def __init__(self, hand, sampler):
        self.hand, self.sampler, self.brugt = hand, sampler, False

    def __call__(self):
        if self.brugt:
            return self.sampler()
        self.brugt = True
        hp = hp_of([r for s in SUITS for r in self.hand[s]])
        return self.hand, hp, sp_of(lengths_of(self.hand), hp)


# Facit fra specen: Franks eksempel ♠KBT75 ♥73 ♦98 ♣KD65 åbner 2♠
FRANK = {'S': [13, 11, 10, 7, 5], 'H': [7, 3], 'D': [9, 8], 'C': [13, 12, 6, 5]}
FRANK_2S = Foerst(FRANK, aab('S', (MIN_HP[0], MAX_HP[1])))

ALLE = (MIN_HP[0], MAX_HP[1])
SAMPLERS = {
    "aabning": {
        "2♥": aab('H', ALLE),
        "2♠": FRANK_2S,
        "1♥": aab('H', (11, 15)),
        "1♠": aab('S', (11, 15)),
        "Pas": either(aab('H', (0, 4)), aab('S', (0, 4))),
        "2♦": either(aab_multi('H', ALLE), aab_multi('S', ALLE)),
    },
}
for _M in 'HS':
    _s, _n = SUIT_SYM[_M], NAVN[_M]
    SAMPLERS[f"svar_2{_n}"] = {
        f"4{_s}": either(t(UDGANG['hp'], **{_M: (3, 5)}), t(SPAER_UDGANG['hp'], **{_M: (4, 5)})),
        "2NT": either(t((SPOERG['hp'], 20)), t(SPOERG_INVIT['hp'], **{_M: (3, 5)})),
        f"3{_s}": t(ENKELTLOEFT['hp'], **{_M: (3, 3)}),
        "3♣": t((0, MINOR_RET['hp_max']), **{_M: (0, 1), 'C': (3, 6), 'D': (3, 6)}),
        "Pas": either(t((0, 10), **{_M: (2, 2)}), t((0, ENKELTLOEFT['hp'][0] - 1), **{_M: (3, 3)})),
    }
    SAMPLERS[f"ret_2{_n}"] = {"Pas": aab(_M, ALLE, 'C'), "3♦": aab(_M, ALLE, 'D')}
    SAMPLERS[f"spm_2{_n}"] = {"3♣": aab(_M, MIN_HP, 'C'), "3♦": aab(_M, MIN_HP, 'D'),
                              "3♥": aab(_M, MAX_HP, 'C'), "3♠": aab(_M, MAX_HP, 'D')}
PER_CALL = {k: PER_CALL_N for k in SITUATIONS}


def export_pool(path):
    hp = hp_of([r for s in SUITS for r in FRANK[s]])
    got = aabning(FRANK, hp)
    assert got and got[0] == "2♠", got
    FRANK_2S.brugt = False
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
