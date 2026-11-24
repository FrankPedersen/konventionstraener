"""
Multi 2♦ – åbningen, svarene, fortsættelserne og indblanding efter Jyderup Bridgeklubs ark "Multi 2ru" (J), med
hullerne udfyldt efter dokumentet "Ruder Multi" (W). Bygger på konventionskortet data/kort/multi-2ru.json og er
uafhængig af makker (SPEC-multi-2ru.md, system "generel").

2♦ viser en seksfarve i hjerter eller spar, 5–10 hp, ingen firfarve i den anden major og højst ét es (J).

Situationer (traener.html tager meldeforløbet fra situationen, så ret og indmelding har én situation pr. svar og pr.
indmelding):
  aabning  – ?                                  2♦ efter J · 1♥/1♠ med seksfarve og 11–15 · pas med seksfarve og 0–4
  svar     – 2♦ – pas – ?                        første regel, der passer (Grænser nedenfor): 4♥/4♠, 3♣/3♦, 2NT, 4♦,
                                                 2♠, 3♠, 3♥ og til sidst 2♥ (resten under 16 hp)
  ret_*    – 2♦ – pas – (2♥ 2♠ 3♥ 3♠ 4♣ 4♦) – pas – ?   åbners melding efter tabellen i specen
  spm      – 2♦ – pas – 2NT – pas – ?            3♣ maksimum · 3♦ minimum og hjerter · 3♥ minimum og spar
  spm2     – … 2NT – pas – 3♣ – pas – 3♦ – pas – ?   krydsmeldingen: 3♥ = spar og 3♠ = hjerter
  dobling  – 2♦ – (X) – ?                        pas ruder · XX styrke · 2♥ svag med fit i begge majorer · ellers som svar
  ind_*    – 2♦ – (2♠ 3♣ 3♦ 4♥) – ?               over 2♠ efter J: X styrke, og efter W: 3♥ pas eller ret ·
                                                 over 3♣, 3♦ og 4♥ efter W: X straf, ♥/♠ pas eller ret, minor naturligt
Ikke med i puljen (Afklaret, punkt 4 og 5): 4♣ og 3NT som svar, pas uden indblanding, svage hænder uden ruder og uden
fit i begge majorer efter dobling, åbningshænder med 5–10 hp og to esser eller en firfarve i den anden major, spm2
med minimum og to lige lange gode minorer under svar.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, rnd, build_pool, tx, hp_of

# --- Grænser, som kilderne ikke giver tal for – ret dem her ------------
MIN_HP, MAX_HP = (5, 7), (8, 10)   # åbners minimum og maksimum inden for 5–10

# svar: 2♦ – Pas – ?  (første regel, der passer)
EGEN_MAJOR   = dict(laengde=7, top=2, hp=10)    # 4♥/4♠: 7+ i majoren, 2 af de 3 øverste, 10+ hp
EGEN_MINOR   = dict(laengde=6, top=2, hp=13)    # 3♣/3♦ krav: 6+ i minoren, 2 af de 3 øverste, 13+ hp, ikke 3+ i begge majorer
SPOERG_HP    = 16                               # 2NT: 16+ hp
UDGANG_HP    = (13, 15)                         # 4♦: 3+ i begge majorer og 13–15 hp
INVIT_HJ     = dict(hjerter=3, hp=(11, 12))     # 2♠: 3+ hjerter og 11–12 hp
SPAER_TRE_SP = dict(begge=4, hp=(6, 10))        # 3♠: 4+ i begge majorer, 6–10 hp
SPAER_TRE_HJ = dict(begge=3, hp=(6, 10))        # 3♥: 3+ i begge majorer, 6–10 hp
# 2♥: resten under 16 hp
# 4♣ og 3NT: kun som forkerte valgmuligheder (Afklaret, punkt 5)

# dobling: 2♦ – X – ?  (første regel, der passer)
PAS_RUDER    = dict(laengde=6, hp_max=10)       # Pas: 6+ ruder, højst 10 hp
STRAF_XX     = dict(hp=12, major_max=2)         # XX: 12+ hp og højst 2 kort i hver major
SVAG_FIT_X   = dict(begge=3, hp_max=5)          # 2♥: 3+ i begge majorer, højst 5 hp
# derefter som under svar (2♠, 2NT, 3♣/3♦, 3♥/3♠, 4♦, 4♥/4♠ med samme grænser)
# svage hænder uden ruder og uden fit i begge majorer genereres ikke (Afklaret, punkt 4)

# indmelding over 2♠: 2♦ – (2♠) – ?
NEGATIV_X    = dict(hp=10)                      # X: 10+ hp
# 3♥ (W): pas eller ret med grænsen PAS_RET nedenfor (3+ i begge majorer, 7+ hp)
# Pas: resten

# indmelding over 3♣, 3♦ og 4♥ (W)
STRAF        = dict(laengde=4, top4=2, hp=12)   # X: 4+ i modpartens farve, 2 af de 4 øverste, 12+ hp
PAS_RET      = dict(hp=7)                       # billigste major: 3+ i begge majorer (over 4♥: 4+ spar), 7+ hp
MINOR_NAT    = dict(laengde=6, top=2, hp=8)     # minor: god 6+ farve, kun på 3-trinnet
# Pas: resten

PER_CALL_N = 7
PAS = ["Modstander", "Pas"]
TRIN = ['♣', '♦', '♥', '♠', 'NT']
FARVE = {v: k for k, v in SUIT_SYM.items()}
K = lambda c: (0, 0) if c in ("Pas", "X", "XX") else (int(c[0]), TRIN.index(c[1:]))
inden = lambda hp, rng: rng[0] <= hp <= rng[1]
anden = lambda M: 'S' if M == 'H' else 'H'


def toppe(hand, s, n=3):
    """Antal af de n øverste honnører i farven (n=3: E, K og D; n=4: også B)."""
    return sum(1 for r in hand[s] if r > 14 - n)


def esser(hand):
    return sum(1 for s in SUITS if 14 in hand[s])


def antal(n, s):
    """'3 hjerter' / '3 hearts' – 'ingen hjerter' / 'no hearts' ved renonce og ental på engelsk ved ét kort."""
    if n == 0:
        return tx(f"ingen {SUIT_NAME[s]}", f"no {SUIT_NAME_EN[s]}")
    return tx(f"{n} {SUIT_NAME[s]}", f"{n} {SUIT_NAME_EN[s][:-1] if n == 1 else SUIT_NAME_EN[s]}")


def og(*dele):
    """Danske og engelske dele sat sammen med komma og 'og'/'and'."""
    da = [str(d) for d in dele]
    en = [getattr(d, 'en', str(d)) for d in dele]
    return tx(', '.join(da[:-1]) + ' og ' + da[-1] if len(da) > 1 else da[0],
              ', '.join(en[:-1]) + ' and ' + en[-1] if len(en) > 1 else en[0])


def hp_tx(hp):
    return tx(f"{hp} hp", f"{hp} HCP")


def gyldig(hand, hp):
    """J: præcis seks kort i én major, højst tre i den anden, 5–10 hp og højst ét es."""
    L = lengths_of(hand)
    return any(L[M] == 6 and L[anden(M)] <= 3 for M in 'HS') and 5 <= hp <= 10 and esser(hand) <= 1


def major(hand):
    return 'H' if len(hand['H']) == 6 else 'S'


def billigste(over, s):
    """Det billigste lovlige bud i farven s over buddet over."""
    t, i = K(over)
    j = TRIN.index(SUIT_SYM[s])
    return f"{t if j > i else t + 1}{SUIT_SYM[s]}"


# --- aabning ----------------------------------------------------------------------

def aabning(hand, hp):
    L = lengths_of(hand)
    seks = [M for M in 'HS' if L[M] == 6]
    if len(seks) != 1:
        return None
    M = seks[0]
    sym, da, en = SUIT_SYM[M], SUIT_NAME[M], SUIT_NAME_EN[M]
    if 11 <= hp <= 15:
        return f"1{sym}", tx(f"6 {da} og {hp} hp: 1{sym} – med 11–15 hp er hånden for stærk til Multi 2♦ (5–10 hp).",
                             f"6 {en} and {hp} HCP: 1{sym} – with 11–15 HCP the hand is too strong for Multi 2♦ (5–10 HCP).")
    if hp <= 4:
        return "Pas", tx(f"6 {da} og kun {hp} hp: pas – Multi 2♦ kræver mindst 5 hp.",
                         f"6 {en} and only {hp} HCP: pass – Multi 2♦ needs at least 5 HCP.")
    if not gyldig(hand, hp):
        return None
    A = anden(M)
    es = tx("intet es", "no ace") if esser(hand) == 0 else tx("ét es", "one ace")
    return "2♦", tx(f"6 {da} uden firfarve i {SUIT_NAME[A]}, {hp} hp og {es}: 2♦ – seksfarve i hjerter eller spar, "
                    "5–10 hp, ingen firfarve i den anden major og højst ét es.",
                    f"6 {en} without four {SUIT_NAME_EN[A]}, {hp} HCP and {es.en}: 2♦ – a six-card suit in hearts or spades, "
                    "5–10 HCP, no four-card suit in the other major and at most one ace.")


# --- svar: 2♦ – pas – ? ------------------------------------------------------------

def svar(hand, hp, med_rest=True):
    """Første regel, der passer. Uden med_rest er der ingen 2♥ for resten (efter dobling)."""
    L = lengths_of(hand)
    e = EGEN_MAJOR
    for M in 'HS':
        if L[M] >= e['laengde'] and toppe(hand, M) >= e['top'] and hp >= e['hp']:
            sym = SUIT_SYM[M]
            return f"4{sym}", tx(
                f"{L[M]} {SUIT_NAME[M]} med {toppe(hand, M)} af de tre øverste honnører og {hp} hp: 4{sym} – "
                "svarers egen farve, og åbner passer.",
                f"{L[M]} {SUIT_NAME_EN[M]} with {toppe(hand, M)} of the top three honours and {hp} HCP: 4{sym} – "
                "responder's own suit, and opener passes.")
    e = EGEN_MINOR
    minorer = [m for m in 'CD' if L[m] >= e['laengde'] and toppe(hand, m) >= e['top'] and hp >= e['hp']
               and not (L['H'] >= 3 and L['S'] >= 3)]
    if minorer:
        if len(minorer) == 2 and L['C'] == L['D']:
            return None
        m = max(minorer, key=lambda x: L[x])
        sym = SUIT_SYM[m]
        return f"3{sym}", tx(
            f"{L[m]} {SUIT_NAME[m]} med {toppe(hand, m)} af de tre øverste honnører og {hp} hp: 3{sym} – krav med egen farve.",
            f"{L[m]} {SUIT_NAME_EN[m]} with {toppe(hand, m)} of the top three honours and {hp} HCP: 3{sym} – "
            "forcing with responder's own suit.")
    if hp >= SPOERG_HP:
        return "2NT", tx(f"{hp} hp: 2NT – spørger om styrken. Åbner svarer 3♣ med maksimum, 3♦ med minimum og hjerter "
                         "og 3♥ med minimum og spar.",
                         f"{hp} HCP: 2NT – asks about strength. Opener bids 3♣ with a maximum, 3♦ with a minimum and "
                         "hearts and 3♥ with a minimum and spades.")
    begge = og(antal(L['H'], 'H'), antal(L['S'], 'S'), hp_tx(hp))
    if L['H'] >= 3 and L['S'] >= 3 and inden(hp, UDGANG_HP):
        return "4♦", tx(f"{begge}: 4♦ – åbner melder sin farve på 4-trinnet.",
                        f"{begge.en}: 4♦ – opener bids the suit at the four level.")
    if L['H'] >= INVIT_HJ['hjerter'] and inden(hp, INVIT_HJ['hp']):
        return "2♠", tx(f"{L['H']} hjerter og {hp} hp: 2♠ – invit med hjerter. Åbner passer med spar og melder 3♥ med "
                        "minimum og 4♥ med maksimum.",
                        f"{antal(L['H'], 'H').en} and {hp} HCP: 2♠ – invitational in hearts. Opener passes with spades and "
                        "bids 3♥ with a minimum and 4♥ with a maximum.")
    s = SPAER_TRE_SP
    if L['H'] >= s['begge'] and L['S'] >= s['begge'] and inden(hp, s['hp']):
        return "3♠", tx(f"{begge}: 3♠ – pas eller ret, en spærremelding i makkers farve. Åbner passer med spar og "
                        "melder 4♥ med hjerter.",
                        f"{begge.en}: 3♠ – pass or correct, a preempt in partner's suit. Opener passes with spades and "
                        "bids 4♥ with hearts.")
    s = SPAER_TRE_HJ
    if L['H'] >= s['begge'] and L['S'] >= s['begge'] and inden(hp, s['hp']):
        return "3♥", tx(f"{begge}: 3♥ – pas eller ret, en spærremelding i makkers farve. Åbner passer med hjerter og "
                        "melder 3♠ med spar.",
                        f"{begge.en}: 3♥ – pass or correct, a preempt in partner's suit. Opener passes with hearts and "
                        "bids 3♠ with spades.")
    if not med_rest:
        return None
    return "2♥", tx(f"{begge}: 2♥ – søger farven (pas eller ret). Åbner passer med hjerter og melder 2♠ med spar.",
                    f"{begge.en}: 2♥ – asks for the suit (pass or correct). Opener passes with hearts and bids 2♠ "
                    "with spades.")


# --- ret: 2♦ – pas – (svar) – pas – ? ----------------------------------------------

# svar → (melding med hjerter, melding med spar); 2♠ med hjerter afhænger af minimum eller maksimum
RET = {
    '2♥': ("Pas", "2♠"),
    '2♠': (None, "Pas"),
    '3♥': ("Pas", "3♠"),
    '3♠': ("4♥", "Pas"),
    '4♣': ("4♦", "4♥"),
    '4♦': ("4♥", "4♠"),
}
BETYDNING = {
    '2♥': tx("2♥ søger farven: åbner passer med hjerter og melder 2♠ med spar.",
             "2♥ asks for the suit: opener passes with hearts and bids 2♠ with spades."),
    '2♠': tx("2♠ er invit med hjerter: åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum.",
             "2♠ is invitational in hearts: opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum."),
    '3♥': tx("3♥ er pas eller ret: åbner passer med hjerter og melder 3♠ med spar.",
             "3♥ is pass or correct: opener passes with hearts and bids 3♠ with spades."),
    '3♠': tx("3♠ er pas eller ret: åbner passer med spar og melder 4♥ med hjerter.",
             "3♠ is pass or correct: opener passes with spades and bids 4♥ with hearts."),
    '4♣': tx("4♣ er transfer: åbner melder farven under sin egen, 4♦ med hjerter og 4♥ med spar.",
             "4♣ is a transfer: opener bids the suit below his own, 4♦ with hearts and 4♥ with spades."),
    '4♦': tx("Efter 4♦ melder åbner sin farve: 4♥ med hjerter og 4♠ med spar.",
             "After 4♦ opener bids his suit: 4♥ with hearts and 4♠ with spades."),
}


def ret_efter(makkers):
    def ret(hand, hp):
        if not gyldig(hand, hp):
            return None
        M = major(hand)
        call = RET[makkers][0 if M == 'H' else 1]
        if call is None:
            call = "4♥" if inden(hp, MAX_HP) else "3♥"
            styrke = tx(f"6 hjerter og {hp} hp (maksimum)", f"6 hearts and {hp} HCP (a maximum)") if call == "4♥" \
                else tx(f"6 hjerter og {hp} hp (minimum)", f"6 hearts and {hp} HCP (a minimum)")
        else:
            styrke = tx(f"6 {SUIT_NAME[M]}", f"6 {SUIT_NAME_EN[M]}")
        navn = tx("pas", "pass") if call == "Pas" else tx(call, call)
        return call, tx(f"{styrke}: {navn}. {BETYDNING[makkers]}", f"{styrke.en}: {navn.en}. {BETYDNING[makkers].en}")
    return ret


# --- spm og spm2: 2♦ – pas – 2NT – pas – ? -----------------------------------------

def spm(hand, hp):
    if not gyldig(hand, hp):
        return None
    M = major(hand)
    if inden(hp, MAX_HP):
        return "3♣", tx(f"6 {SUIT_NAME[M]} og {hp} hp (maksimum): 3♣ – maksimum. Farven vises bagefter med en krydsmelding.",
                        f"6 {SUIT_NAME_EN[M]} and {hp} HCP (a maximum): 3♣ – a maximum. The suit is shown afterwards "
                        "with a crossover bid.")
    if M == 'H':
        return "3♦", tx(f"6 hjerter og {hp} hp (minimum): 3♦ – minimum og hjerter.",
                        f"6 hearts and {hp} HCP (a minimum): 3♦ – a minimum and hearts.")
    return "3♥", tx(f"6 spar og {hp} hp (minimum): 3♥ – minimum og spar.",
                    f"6 spades and {hp} HCP (a minimum): 3♥ – a minimum and spades.")


KRYDS = tx("Efter 3♦ viser åbner farven med en krydsmelding: 3♥ = spar og 3♠ = hjerter.",
           "After 3♦ opener shows the suit with a crossover bid: 3♥ = spades and 3♠ = hearts.")


def spm2(hand, hp):
    if not gyldig(hand, hp) or not inden(hp, MAX_HP):
        return None  # med minimum har åbner ikke meldt 3♣
    if major(hand) == 'S':
        return "3♥", tx(f"6 spar: 3♥. {KRYDS}", f"6 spades: 3♥. {KRYDS.en}")
    return "3♠", tx(f"6 hjerter: 3♠. {KRYDS}", f"6 hearts: 3♠. {KRYDS.en}")


# --- dobling: 2♦ – (X) – ? ---------------------------------------------------------

IGNORER = tx("Doblingen ignoreres, og der meldes som uden dobling.",
             "The double is ignored, and responder bids as without the double.")


def dobling(hand, hp):
    L = lengths_of(hand)
    if L['D'] >= PAS_RUDER['laengde'] and hp <= PAS_RUDER['hp_max']:
        return "Pas", tx(f"{L['D']} ruder og {hp} hp: pas – en svag hånd med ruder, for at spille 2♦ doblet.",
                         f"{L['D']} diamonds and {hp} HCP: pass – a weak hand with diamonds, to play 2♦ doubled.")
    if hp >= STRAF_XX['hp'] and L['H'] <= STRAF_XX['major_max'] and L['S'] <= STRAF_XX['major_max']:
        b = og(antal(L['H'], 'H'), antal(L['S'], 'S'), hp_tx(hp))
        return "XX", tx(f"{b}: XX – styrke med interesse for straf.",
                        f"{b.en}: XX – strength with interest in a penalty.")
    if L['H'] >= SVAG_FIT_X['begge'] and L['S'] >= SVAG_FIT_X['begge'] and hp <= SVAG_FIT_X['hp_max']:
        b = og(antal(L['H'], 'H'), antal(L['S'], 'S'), hp_tx(hp))
        return "2♥", tx(f"{b}: 2♥ – en svag hånd med fit i begge majorer, pas eller ret.",
                        f"{b.en}: 2♥ – a weak hand with a fit in both majors, pass or correct.")
    r = svar(hand, hp, med_rest=False)
    if not r:
        return None
    return r[0], tx(f"{r[1]} {IGNORER}", f"{r[1].en} {IGNORER.en}")


# --- indmelding: 2♦ – (2♠ 3♣ 3♦ 4♥) – ? --------------------------------------------

def indmelding_over(deres):
    f = FARVE[deres[1]]

    def over_2s(hand, hp):
        L = lengths_of(hand)
        if hp >= NEGATIV_X['hp']:
            return "X", tx(f"{hp} hp: X – styrke (negativ dobling). Med spar passer åbner, så doblingen står som straf.",
                           f"{hp} HCP: X – strength (negative double). With spades opener passes, so the double stands "
                           "for penalty.")
        b = og(antal(L['H'], 'H'), antal(L['S'], 'S'), hp_tx(hp))
        if hp >= PAS_RET['hp'] and L['H'] >= 3 and L['S'] >= 3:
            return "3♥", tx(f"{b}: 3♥ – pas eller ret. Åbner passer med hjerter og melder 3♠ med spar.",
                            f"{b.en}: 3♥ – pass or correct. Opener passes with hearts and bids 3♠ with spades.")
        if hp < PAS_RET['hp']:
            return "Pas", tx(f"{hp} hp: pas – hånden er for svag til at doble, og der er intet at tilføje.",
                             f"{hp} HCP: pass – the hand is too weak to double, and there is nothing to add.")
        return "Pas", tx(f"{b}: pas – hånden er for svag til at doble, og uden tre kort i begge majorer er der intet at "
                         "tilføje.",
                         f"{b.en}: pass – the hand is too weak to double, and without three cards in both majors there is "
                         "nothing to add.")

    def over_andet(hand, hp):
        L = lengths_of(hand)
        s = STRAF
        if L[f] >= s['laengde'] and toppe(hand, f, 4) >= s['top4'] and hp >= s['hp']:
            return "X", tx(f"{L[f]} {SUIT_NAME[f]} med {toppe(hand, f, 4)} af de fire øverste honnører og {hp} hp: "
                           "X – straf.",
                           f"{L[f]} {SUIT_NAME_EN[f]} with {toppe(hand, f, 4)} of the top four honours and {hp} HCP: "
                           "X – penalty.")
        if hp >= PAS_RET['hp']:
            if deres == '4♥':
                if L['S'] >= 4:
                    return "4♠", tx(f"{L['S']} spar og {hp} hp: 4♠ – pas eller ret. Makker har sikkert spar, når "
                                    "modparten melder 4♥.",
                                    f"{L['S']} spades and {hp} HCP: 4♠ – pass or correct. Partner very likely has spades "
                                    "when the opponents bid 4♥.")
            elif L['H'] >= 3 and L['S'] >= 3:
                b = og(antal(L['H'], 'H'), antal(L['S'], 'S'), hp_tx(hp))
                return "3♥", tx(f"{b}: 3♥ – pas eller ret. Åbner passer med hjerter og melder 3♠ med spar.",
                                f"{b.en}: 3♥ – pass or correct. Opener passes with hearts and bids 3♠ with spades.")
        m_ = MINOR_NAT
        for m in 'CD':
            bud = billigste(deres, m)
            if m != f and bud[0] == '3' and L[m] >= m_['laengde'] and toppe(hand, m) >= m_['top'] and hp >= m_['hp']:
                return bud, tx(f"{L[m]} {SUIT_NAME[m]} med {toppe(hand, m)} af de tre øverste honnører og {hp} hp: "
                               f"{bud} – naturligt og ikke krav.",
                               f"{L[m]} {SUIT_NAME_EN[m]} with {toppe(hand, m)} of the top three honours and {hp} HCP: "
                               f"{bud} – natural and non-forcing.")
        if hp < PAS_RET['hp']:
            return "Pas", tx(f"{hp} hp: pas – intet at tilføje.", f"{hp} HCP: pass – nothing to add.")
        if deres == '4♥':
            return "Pas", tx(f"{antal(L['S'], 'S')} og {hp} hp: pas – uden fire spar er der intet at tilføje.",
                             f"{antal(L['S'], 'S').en} and {hp} HCP: pass – without four spades there is nothing to add.")
        b = og(antal(L['H'], 'H'), antal(L['S'], 'S'), hp_tx(hp))
        ekstra = tx(" Klør kan kun meldes på 4-trinnet.", " Clubs can only be bid at the four level.") \
            if deres == '3♦' and L['C'] >= MINOR_NAT['laengde'] else tx("", "")
        return "Pas", tx(f"{b}: pas – uden tre kort i begge majorer er der intet at tilføje.{ekstra}",
                         f"{b.en}: pass – without three cards in both majors there is nothing to add.{ekstra.en}")

    return over_2s if deres == '2♠' else over_andet


# --- bonusspørgsmål ---------------------------------------------------------------

def bonus(q, correct, andre, why):
    return {"q": q, "correct": correct, "options": [correct, *andre], "why": why}


B_AABNING = bonus(
    tx("Hvilke krav stiller Multi 2♦ til hånden?", "What does Multi 2♦ require of the hand?"),
    tx("5–10 hp, seksfarve i en major, ingen firfarve i den anden major og højst ét es",
       "5–10 HCP, a six-card major, no four-card suit in the other major and at most one ace"),
    [tx("5–10 hp og en seksfarve i en hvilken som helst farve", "5–10 HCP and a six-card suit in any suit"),
     tx("11–15 hp og en seksfarve i en major", "11–15 HCP and a six-card major")],
    tx("Multi 2♦ viser en svag 2 i hjerter eller spar: 5–10 hp og en seksfarve uden firfarve i den anden major og med "
       "højst ét es. Formålet er at frigøre 2♥ og 2♠.",
       "Multi 2♦ shows a weak two in hearts or spades: 5–10 HCP and a six-card suit without a four-card suit in the other "
       "major and with at most one ace. The purpose is to free 2♥ and 2♠."))
B_SVAR = bonus(
    tx("Hvad betyder 2♠ som svar på Multi?", "What does 2♠ mean in response to Multi?"),
    tx("Invit med hjerter", "Invitational in hearts"),
    [tx("Pas eller ret i makkers farve", "Pass or correct in partner's suit"),
     tx("Naturligt med egen sparfarve", "Natural with responder's own spade suit")],
    tx("2♠ er invit med hjerter: åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum. Det er 2♥, der "
       "søger farven (pas eller ret).",
       "2♠ is invitational in hearts: opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum. It is "
       "2♥ that asks for the suit (pass or correct)."))
B_RET = {
    '2♥': bonus(tx("Hvad betyder svarers 2♥ efter 2♦?", "What does responder's 2♥ mean after 2♦?"),
                tx("Søger farven: åbner passer med hjerter og melder 2♠ med spar",
                   "Asks for the suit: opener passes with hearts and bids 2♠ with spades"),
                [tx("Naturligt med egen hjertefarve", "Natural with responder's own heart suit"),
                 tx("Invit med hjerter", "Invitational in hearts")],
                tx("2♥ søger farven (pas eller ret): åbner passer med hjerter og melder 2♠ med spar. Det er 2♠, der er "
                   "invit med hjerter.",
                   "2♥ asks for the suit (pass or correct): opener passes with hearts and bids 2♠ with spades. It is 2♠ "
                   "that is invitational in hearts.")),
    '2♠': bonus(tx("Hvad melder åbner med hjerter efter 2♦ – 2♠?", "What does opener bid with hearts after 2♦ – 2♠?"),
                tx("3♥ med minimum og 4♥ med maksimum", "3♥ with a minimum and 4♥ with a maximum"),
                [tx("Pas, fordi 2♠ er pas eller ret", "Pass, because 2♠ is pass or correct"),
                 tx("Altid 4♥", "Always 4♥")],
                tx("2♠ er invit med hjerter: åbner passer med spar og melder 3♥ med minimum og 4♥ med maksimum.",
                   "2♠ is invitational in hearts: opener passes with spades and bids 3♥ with a minimum and 4♥ with a maximum.")),
    '3♥': bonus(tx("Hvad betyder svarers 3♥ efter 2♦?", "What does responder's 3♥ mean after 2♦?"),
                tx("Pas eller ret: spærremelding i makkers farve", "Pass or correct: a preempt in partner's suit"),
                [tx("Krav med egen hjertefarve", "Forcing with responder's own heart suit"),
                 tx("Invit med hjerter", "Invitational in hearts")],
                tx("3♥ og 3♠ er pas eller ret: svarer spærrer i makkers farve. Efter 3♥ passer åbner med hjerter og melder "
                   "3♠ med spar.",
                   "3♥ and 3♠ are pass or correct: responder preempts in partner's suit. After 3♥ opener passes with hearts "
                   "and bids 3♠ with spades.")),
    '3♠': bonus(tx("Hvad melder åbner med hjerter efter 2♦ – 3♠?", "What does opener bid with hearts after 2♦ – 3♠?"),
                tx("4♥, fordi 3♠ er pas eller ret", "4♥, because 3♠ is pass or correct"),
                [tx("Pas, fordi 3♠ er naturligt", "Pass, because 3♠ is natural"),
                 tx("4♦, farven under sin egen", "4♦, the suit below his own")],
                tx("3♠ er pas eller ret: åbner passer med spar og melder 4♥ med hjerter.",
                   "3♠ is pass or correct: opener passes with spades and bids 4♥ with hearts.")),
    '4♣': bonus(tx("Hvad melder åbner efter 4♣?", "What does opener bid after 4♣?"),
                tx("Farven under sin egen: 4♦ med hjerter og 4♥ med spar",
                   "The suit below his own: 4♦ with hearts and 4♥ with spades"),
                [tx("Sin egen farve: 4♥ eller 4♠", "His own suit: 4♥ or 4♠"),
                 tx("4♦ uanset farven", "4♦ whatever the suit")],
                tx("4♣ er transfer: åbner melder farven under sin egen, 4♦ med hjerter og 4♥ med spar. Efter 4♦ melder "
                   "åbner sin egen farve.",
                   "4♣ is a transfer: opener bids the suit below his own, 4♦ with hearts and 4♥ with spades. After 4♦ "
                   "opener bids his own suit.")),
    '4♦': bonus(tx("Hvad melder åbner efter 4♦?", "What does opener bid after 4♦?"),
                tx("Sin egen farve: 4♥ eller 4♠", "His own suit: 4♥ or 4♠"),
                [tx("Farven under sin egen", "The suit below his own"), tx("Pas", "Pass")],
                tx("Efter 4♦ melder åbner sin egen farve. Efter 4♣ (transfer) melder han farven under sin egen.",
                   "After 4♦ opener bids his own suit. After 4♣ (a transfer) he bids the suit below his own.")),
}
B_SPM = bonus(
    tx("Hvad viser åbners 3♣ efter 2♦ – 2NT?", "What does opener's 3♣ show after 2♦ – 2NT?"),
    tx("Maksimum", "A maximum"), [tx("Minimum og hjerter", "A minimum and hearts"), tx("Klør", "Clubs")],
    tx("Efter 2NT viser 3♣ maksimum, 3♦ minimum og hjerter og 3♥ minimum og spar. Efter 3♣ søger svarer farven med 3♦, "
       "og åbner viser den med en krydsmelding.",
       "After 2NT, 3♣ shows a maximum, 3♦ a minimum and hearts and 3♥ a minimum and spades. After 3♣ responder asks for "
       "the suit with 3♦, and opener shows it with a crossover bid."))
B_SPM2 = bonus(
    tx("Hvad betyder svarers 3♥ efter 2♦ – 2NT – 3♣?", "What does responder's 3♥ mean after 2♦ – 2NT – 3♣?"),
    tx("Krav med egen farve", "Forcing with responder's own suit"),
    [tx("Søger farven", "Asks for the suit"), tx("Pas eller ret", "Pass or correct")],
    tx("Efter 3♣ (maksimum) er det 3♦, der søger farven, og åbner viser den med en krydsmelding: 3♥ = spar og 3♠ = "
       "hjerter. Svarers 3♥ og 3♠ er krav med egen farve.",
       "After 3♣ (a maximum) it is 3♦ that asks for the suit, and opener shows it with a crossover bid: 3♥ = spades and "
       "3♠ = hearts. Responder's 3♥ and 3♠ are forcing with responder's own suit."))
B_DOBLING = bonus(
    tx("Hvad viser redobling, når modparten dobler 2♦?", "What does a redouble show when the opponents double 2♦?"),
    tx("Styrke med interesse for straf", "Strength with interest in a penalty"),
    [tx("Ruder, for at spille", "Diamonds, to play"), tx("En svag hånd med fit i begge majorer", "A weak hand with a fit in both majors")],
    tx("Når modparten dobler 2♦, er pas en svag hånd med ruder, XX styrke med interesse for straf og 2♥ en svag hånd med "
       "fit i begge majorer. Andre meldinger er som uden dobling.",
       "When the opponents double 2♦, pass is a weak hand with diamonds, XX strength with interest in a penalty and 2♥ a "
       "weak hand with a fit in both majors. Other bids are as without the double."))
W_IND = tx("Over 3♣, 3♦ og 4♥ er dobling straf, hjerter eller spar er pas eller ret, og en minor er naturlig og ikke "
           "krav. Over 2♠ er dobling styrke.",
           "Over 3♣, 3♦ and 4♥ a double is for penalty, hearts or spades are pass or correct, and a minor is natural and "
           "non-forcing. Over 2♠ a double shows strength.")
B_IND = {
    '2♠': bonus(tx("Hvad betyder dobling efter 2♦ – (2♠)?", "What does a double mean after 2♦ – (2♠)?"),
                tx("Styrke (negativ dobling)", "Strength (negative double)"),
                [tx("Straf med spar", "Penalty with spades"), tx("Pas eller ret med hjerter", "Pass or correct with hearts")],
                tx("Over 2♠ er dobling styrke (negativ dobling). Med spar passer åbner, så doblingen står som straf.",
                   "Over 2♠ a double shows strength (negative double). With spades opener passes, so the double stands for "
                   "penalty.")),
    '3♣': bonus(tx("Hvad betyder dobling efter 2♦ – (3♣)?", "What does a double mean after 2♦ – (3♣)?"),
                tx("Straf", "Penalty"), [tx("Styrke (negativ dobling)", "Strength (negative double)"),
                                         tx("Pas eller ret", "Pass or correct")], W_IND),
    '3♦': bonus(tx("Hvad betyder 3♥ efter 2♦ – (3♦)?", "What does 3♥ mean after 2♦ – (3♦)?"),
                tx("Pas eller ret", "Pass or correct"), [tx("Naturligt med egen hjertefarve", "Natural with responder's own heart suit"),
                                                        tx("Krav", "Forcing")], W_IND),
    '4♥': bonus(tx("Hvad betyder 4♠ efter 2♦ – (4♥)?", "What does 4♠ mean after 2♦ – (4♥)?"),
                tx("Pas eller ret", "Pass or correct"), [tx("Egen sparfarve og krav", "Responder's own spade suit, forcing"),
                                                        tx("Straf", "Penalty")],
                tx("Over 4♥ er 4♠ pas eller ret: makker har sikkert spar. Dobling er straf.",
                   "Over 4♥, 4♠ is pass or correct: partner very likely has spades. A double is for penalty.")),
}

# --- situationer og hænder --------------------------------------------------------

NAVN = {'♣': 'c', '♦': 'd', '♥': 'h', '♠': 's'}
RET_CALLS = ["Pas", "2♠", "3♥", "3♠", "4♦", "4♥", "4♠"]


def lovlige(calls, sidste):
    return [c for c in calls if not c[0].isdigit() or K(c) > K(sidste)]


SITUATIONS = {
    "aabning": {"rolle": "Åbner", "auction": [], "calls": ["Pas", "1♥", "1♠", "2♦"], "bonus": B_AABNING},
    "svar": {"rolle": "Svarer", "auction": [["Makker", "2♦"], PAS],
             "calls": ["Pas", "2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "3NT", "4♣", "4♦", "4♥", "4♠"], "bonus": B_SVAR},
}
for _s in RET:
    SITUATIONS[f"ret_{_s[0]}{NAVN[_s[1]]}"] = {
        "rolle": "Åbner", "auction": [["Dig", "2♦"], PAS, ["Makker", _s], PAS],
        "calls": lovlige(RET_CALLS, _s), "bonus": B_RET[_s]}
SITUATIONS["spm"] = {"rolle": "Åbner", "auction": [["Dig", "2♦"], PAS, ["Makker", "2NT"], PAS],
                     "calls": ["3♣", "3♦", "3♥", "3♠", "3NT"], "bonus": B_SPM}
SITUATIONS["spm2"] = {"rolle": "Åbner",
                      "auction": [["Dig", "2♦"], PAS, ["Makker", "2NT"], PAS, ["Dig", "3♣"], PAS, ["Makker", "3♦"], PAS],
                      "calls": ["3♥", "3♠", "3NT"], "bonus": B_SPM2}
SITUATIONS["dobling"] = {"rolle": "Svarer", "auction": [["Makker", "2♦"], ["Modstander", "X"]], "allowXX": True,
                         "calls": ["Pas", "XX", "2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "4♣", "4♦", "4♥", "4♠"],
                         "bonus": B_DOBLING}
for _d in B_IND:
    SITUATIONS[f"ind_{_d[0]}{NAVN[_d[1]]}"] = {
        "rolle": "Svarer", "auction": [["Makker", "2♦"], ["Modstander", _d]], "allowX": True,
        "calls": ["Pas", "X"] + sorted((billigste(_d, s) for s in SUITS if s != FARVE[_d[1]]), key=K),
        "bonus": B_IND[_d]}

CLASSIFIERS = {"aabning": aabning, "svar": svar, "spm": spm, "spm2": spm2, "dobling": dobling}
for _s in RET:
    CLASSIFIERS[f"ret_{_s[0]}{NAVN[_s[1]]}"] = ret_efter(_s)
for _d in B_IND:
    CLASSIFIERS[f"ind_{_d[0]}{NAVN[_d[1]]}"] = indmelding_over(_d)


def t(hp, **b):
    """Fordeling inden for grænserne (andre farver 0–5) og hp inden for hp."""
    return tpl(hp, **{**{s: (0, 5) for s in SUITS}, **b})


def aab(M, hp):
    """Åbnerens hånd: seks kort i M, højst tre i den anden major og højst fire i hver minor."""
    return t(hp, **{M: (6, 6), anden(M): (0, 3), 'D': (0, 4), 'C': (0, 4)})


ALLE = (MIN_HP[0], MAX_HP[1])
SVAR_SAMPLERS = {
    "4♥": t((10, 15), H=(7, 8), S=(0, 3), D=(0, 4), C=(0, 4)),
    "4♠": t((10, 15), S=(7, 8), H=(0, 3), D=(0, 4), C=(0, 4)),
    "3♣": either(t((13, 16), C=(6, 7), H=(3, 3), S=(0, 2), D=(0, 3)), t((13, 16), C=(6, 7), S=(3, 3), H=(0, 2), D=(0, 3)),
                 t((13, 16), C=(6, 7), H=(0, 2), S=(0, 2), D=(0, 4))),
    "3♦": either(t((13, 16), D=(6, 7), H=(3, 3), S=(0, 2), C=(0, 3)), t((13, 16), D=(6, 7), S=(3, 3), H=(0, 2), C=(0, 3)),
                 t((13, 16), D=(6, 7), H=(0, 2), S=(0, 2), C=(0, 4))),
    "2NT": t((16, 19), S=(2, 5), H=(2, 5), D=(2, 5), C=(2, 5)),
    "4♦": t(UDGANG_HP, H=(3, 4), S=(3, 4), D=(1, 5), C=(1, 5)),
    "2♠": t(INVIT_HJ['hp'], H=(3, 5), S=(0, 4)),
    "3♠": t(SPAER_TRE_SP['hp'], H=(4, 5), S=(4, 5), D=(0, 4), C=(0, 4)),
    "3♥": t(SPAER_TRE_HJ['hp'], H=(3, 4), S=(3, 4)),
}
SAMPLERS = {
    "aabning": {
        "2♦": either(aab('H', ALLE), aab('S', ALLE)),
        "1♥": aab('H', (11, 15)),
        "1♠": aab('S', (11, 15)),
        "Pas": either(aab('H', (0, 4)), aab('S', (0, 4))),
    },
    "svar": {**SVAR_SAMPLERS,
             "2♥": either(rnd((0, 12)), t(UDGANG_HP, H=(0, 2), S=(2, 5), D=(2, 5), C=(2, 5)),
                          t(UDGANG_HP, S=(0, 2), H=(3, 5), D=(2, 5), C=(2, 5)))},
    "ret_2h": {"Pas": aab('H', ALLE), "2♠": aab('S', ALLE)},
    "ret_2s": {"Pas": aab('S', ALLE), "3♥": aab('H', MIN_HP), "4♥": aab('H', MAX_HP)},
    "ret_3h": {"Pas": aab('H', ALLE), "3♠": aab('S', ALLE)},
    "ret_3s": {"Pas": aab('S', ALLE), "4♥": aab('H', ALLE)},
    "ret_4c": {"4♦": aab('H', ALLE), "4♥": aab('S', ALLE)},
    "ret_4d": {"4♥": aab('H', ALLE), "4♠": aab('S', ALLE)},
    "spm": {"3♣": either(aab('H', MAX_HP), aab('S', MAX_HP)), "3♦": aab('H', MIN_HP), "3♥": aab('S', MIN_HP)},
    "spm2": {"3♥": aab('S', MAX_HP), "3♠": aab('H', MAX_HP)},
    "dobling": {
        "Pas": t((0, 10), D=(6, 7), S=(0, 4), H=(0, 4), C=(0, 4)),
        "XX": t((12, 17), H=(0, 2), S=(0, 2), D=(3, 6), C=(3, 6)),
        "2♥": t((0, 5), H=(3, 4), S=(3, 4)),
        "2♠": SVAR_SAMPLERS["2♠"],
        "2NT": either(t((16, 19), H=(3, 5), S=(2, 5), D=(2, 5), C=(2, 5)), t((16, 19), S=(3, 5), H=(2, 5), D=(2, 5), C=(2, 5))),
        "3♣": either(t((13, 16), C=(6, 7), H=(3, 3), S=(0, 2), D=(0, 2)), t((13, 16), C=(6, 7), S=(3, 3), H=(0, 2), D=(0, 2))),
        "3♦": either(t((13, 16), D=(6, 7), H=(3, 3), S=(0, 2), C=(0, 2)), t((13, 16), D=(6, 7), S=(3, 3), H=(0, 2), C=(0, 2))),
        "3♥": SVAR_SAMPLERS["3♥"],
        "3♠": SVAR_SAMPLERS["3♠"],
        "4♦": SVAR_SAMPLERS["4♦"],
        "4♥": SVAR_SAMPLERS["4♥"],
        "4♠": SVAR_SAMPLERS["4♠"],
    },
    "ind_2s": {
        "X": t((10, 16), S=(0, 4)),
        "3♥": t((PAS_RET['hp'], NEGATIV_X['hp'] - 1), H=(3, 4), S=(3, 4)),
        "Pas": either(t((0, PAS_RET['hp'] - 1), S=(0, 4)), t((PAS_RET['hp'], NEGATIV_X['hp'] - 1), H=(0, 2), S=(0, 4)),
                      t((PAS_RET['hp'], NEGATIV_X['hp'] - 1), S=(0, 2), H=(0, 5))),
    },
    "ind_3c": {
        "X": t((12, 17), C=(4, 5), S=(0, 4), H=(0, 4), D=(0, 4)),
        "3♥": t((7, 12), H=(3, 4), S=(3, 4), C=(0, 3), D=(0, 4)),
        "3♦": either(t((8, 12), D=(6, 7), H=(0, 2), S=(0, 3), C=(0, 3)), t((8, 12), D=(6, 7), S=(0, 2), H=(0, 3), C=(0, 3))),
        "Pas": either(t((0, 6), C=(0, 4)), t((7, 11), H=(0, 2), S=(0, 5), D=(0, 5), C=(0, 4)),
                      t((7, 11), S=(0, 2), H=(0, 5), D=(0, 5), C=(0, 4))),
    },
    "ind_3d": {
        "X": t((12, 17), D=(4, 5), S=(0, 4), H=(0, 4), C=(0, 4)),
        "3♥": t((7, 12), H=(3, 4), S=(3, 4), D=(0, 3), C=(0, 4)),
        "Pas": either(t((0, 6), D=(0, 4)), t((7, 11), H=(0, 2), S=(0, 5), C=(0, 7), D=(0, 4)),
                      t((7, 11), S=(0, 2), H=(0, 5), C=(0, 7), D=(0, 4))),
    },
    "ind_4h": {
        "X": t((12, 17), H=(4, 5), S=(0, 4), D=(0, 4), C=(0, 4)),
        "4♠": t((7, 12), S=(4, 5), H=(0, 4)),
        "Pas": either(t((0, 6), H=(0, 4)), t((7, 11), S=(0, 3), H=(0, 3))),
    },
}
PER_CALL = {k: PER_CALL_N for k in SITUATIONS}

# Facit fra specen (hånd, situation, facit) – kortgiveren skal give samme melding
_V = {'E': 14, 'K': 13, 'D': 12, 'B': 11, 'T': 10}


def _h(s):
    return {f: sorted((_V.get(c) or int(c) for c in x if c != '–'), reverse=True) for f, x in zip('SHDC', s.split())}


EKSEMPLER = [
    (_h('E72 984 KD743 86'), "svar", "3♥"),
    (_h('– KDBT874 KD92 E4'), "svar", "4♥"),
    (_h('DBT EK4 942 EKD2'), "svar", "2NT"),
    (_h('8 D743 EDT9742 B'), "dobling", "Pas"),
    (_h('9 KB93 EK86 KDT8'), "ind_3c", "X"),
    (_h('2 KB3 DT3 EK7542'), "ind_3d", "Pas"),
    (_h('KT72 862 KD952 8'), "ind_4h", "4♠"),
    (_h('KD9653 7 D76 863'), "aabning", "2♦"),
    (_h('KBT975 8 873 985'), "aabning", "Pas"),
    (_h('95 KDB973 KB 874'), "aabning", "2♦"),
]


def export_pool(path):
    for hand, sit, facit in EKSEMPLER:
        hp = hp_of([r for s in SUITS for r in hand[s]])
        got = CLASSIFIERS[sit](hand, hp)
        assert got and got[0] == facit, (sit, facit, got)
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
