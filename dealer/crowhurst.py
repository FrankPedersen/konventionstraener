"""
Forsvar mod Multi 2♦ (Crowhurst) – forsvaret mod modpartens 2♦, når den er Multi eller Ekren, med Lebensohl efter
makkers dobling. Bygger på konventionskortet data/kort/crowhurst.json (kilde: Jyderup Bridgeklub, "Crowhurst med
Lebensohl", docs/kilder/crowhurst_med_lebensohl.pdf) og er uafhængig af makker (SPEC-crowhurst-traener.md).

Reglerne gennemgås i rækkefølge, og den første, der passer, er svaret. Hænder, der ikke passer nogen regel, kommer
ikke med i puljen.

direkte – (2♦) – ?
  1  17–19 hp, jævn                                          → 2NT
  2  5+ hjerter og 5+ i en minor, TOFARVE_HP                 → 4 i minoren
  3  5-5 eller længere i minorerne, MINOR_4NT_HP             → 4NT
  4  7+ i en major med MAJOR_4M_KVALITET, MAJOR_4M_HP        → 4 i majoren
  5  5+ i en major, 12–16 hp                                 → 2 i den længste major; ved lige længde spar
  6  6+ i en minor med MINOR_3NT_KVALITET, MINOR_3NT_HP, uden 5-farve major → 3NT
  7  17+ hp                                                  → X
  8  5+ i en minor med MINOR_KVALITET, 12–16 hp              → 3 i minoren
  9  12–16 hp, jævn                                          → X
 10  12+ hp, trefarvet med korthed i en major, eller en 5-farve minor uden MINOR_KVALITET → pas
 11  højst 11 hp                                             → pas
genaabning – (2♦) – pas – (2♥) – pas – (pas) – ?   (hånden har passet efter reglerne for direkte)
  1  4+ spar, højst 1 hjerter, 12+ hp → X;  2  5+ i en minor, 12–16 hp → 3 i minoren;  3  ellers → pas
svar_d – (2♦) – X – (2♥) – ?   og svar_d_sp – (2♦) – X – (2♠) – ?   (M = deres major, A = den anden; over 2♠ er det
samme struktur med farverne byttet om, Franks valg 28. oktober 2026)
  1  4+ i M og STRAF_HP → X;  2  6+ i A og KRAV_HP → 4A;  3  5 i A og KRAV_HP → 3A;  4  5+ i en minor og INVIT_HP → 3 i
  minoren;  5  ellers INVIT_HP → 2NT;  6  over 2♥: 4+ spar og højst SVAG_HP → 2♠;  7  5+ i en minor og højst SVAG_HP →
  2NT;  8  ellers, højst SVAG_HP → pas
svar_relae og svar_relae_sp – (2♦) – X – (2M) – 2NT – (pas) – 3♣ – (pas) – ?   (hånden har meldt 2NT efter reglerne ovenfor)
  1  5+ i A og INVIT_HP → 3A (invit);  2  ellers INVIT_HP → 3M (holdspørgsmål til 3NT);  3  5+ ruder og højst SVAG_HP → 3♦;
  4  5+ klør og højst SVAG_HP → pas
svar_pas – (2♦) – X – (pas) – ?   (Franks valg 28. oktober 2026)
  1  RUDER_STRAF+ ruder og højst STRAF_HP[1] → pas (straf);  2  5+ i spar, hjerter eller klør og KRAV_HP → 3 i farven (krav);
  3  4+ i en major og højst SVAG_HP → 2 i majoren;  4  5+ klør og højst SVAG_HP → 2NT
svar_4kl – (2♦) – 4♣ – (pas) – ?   (makker har 5+ hjerter og 5+ klør)
  1  3+ klør, flere klør end hjerter, SLEM_HP → 4♠;  2  3+ hjerter, SLEM_HP → 4♦;  3  ellers med 2+ hjerter → 4♥
dobler – (2♦) – X – (2♥) – 2NT – (pas) – ?   og dobler_sp – (2♦) – X – (2♠) – 2NT – (pas) – ?   (hånden har doblet efter
reglerne for direkte; M = deres major, A = den anden; Franks valg 27. og 28. oktober 2026)
  1  12–16 hp, jævn → 3♣;  2  20–21 hp, jævn, med HOLD i M → 3NT;  3  17+ og 5+ i A → 3A;  4  17+ og 5+ ruder → 3♦;
  5  17+ og 5+ klør → 4♣;  6  17+ uden egen farve → 3M

Har en hånd to lige lange minorer, der begge giver 3 i minoren (direkte regel 8 og svar_d regel 3), siger reglerne
ikke, hvilken der meldes, og hånden kommer ikke med i puljen. Det samme gælder dobleren med to lige lange 5-farver
blandt A, ruder og klør, med 17+ og 5+ i M uden at være jævn og med 22+ jævn, og svaret over pas med to lige
lange majorer eller to lige lange 5-farver; invitationer og hænder, som reglerne over pas ikke nævner, er heller ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, rnd, build_pool, tx

# --- Grænser, som kilden ikke giver tal for – ret dem her ------------------------
TOFARVE_HP = (10, 16)        # 4♣/4♦: 5+ hjerter og 5+ minor
MINOR_4NT_HP = (14, 20)      # 4NT: begge minorer, "styrke"
MAJOR_4M_HP = (12, 17)       # 4♥/4♠: for at spille
MAJOR_4M_KVALITET = 2        # 4M: mindst 2 af E, K, D i farven
MINOR_3NT_HP = (16, 19)      # 3NT: "typisk minorlængde/styrke"
MINOR_3NT_KVALITET = 2       # 3NT: mindst 2 af E, K, D i minoren
MINOR_KVALITET = 2           # 3♣/3♦: mindst 2 af E, K, D, ellers 6+ kort; ellers "tvivlsom" → pas
STRAF_HP = (8, 15)           # svar_d: X straf med 4+ i deres major
SVAG_HP = 7                  # svar_d, svar_relae og svar_pas: højst 7 hp er svag
INVIT_HP = (8, 11)           # svar_d: konstruktiv invit
KRAV_HP = (12, 17)           # svar_d: 3 i den anden major krav (4 med 6+); svar_pas: ny farve på 3-trinnet krav
RUDER_STRAF = 5              # svar_pas: pas er straf med 5+ ruder og højst STRAF_HP[1] hp
SLEM_HP = (14, 20)           # svar_4kl: krav (4♦/4♠) med sleminteresse
DOBLER_HP_MAX = 22           # dobler: stærkere hænder genereres ikke
# dobler: hold i deres major er es, konge med 1+ kort til, dame med 2+ eller knægt med 3+ (laveste længde for hver honnør)
HOLD = {14: 1, 13: 2, 12: 3, 11: 4}
PER_CALL = 7

MINORER = ('C', 'D')
MAJORER = ('S', 'H')
JAEVN = {(4, 3, 3, 3), (4, 4, 3, 2), (5, 3, 3, 2)}
K = lambda c: (0, 0) if c in ("Pas", "X", "XX") else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))
inden = lambda hp, rng: rng[0] <= hp <= rng[1]

def jaevn(L):
    return tuple(sorted(L.values(), reverse=True)) in JAEVN

def toppe(hand, s):
    """Antal af E, K og D i farven."""
    return sum(1 for r in hand[s] if r >= 12)

def god_minor(hand, L, m):
    """3♣/3♦: en 5-farve med mindst MINOR_KVALITET af E, K og D, eller 6+ kort."""
    return L[m] >= 6 or (L[m] == 5 and toppe(hand, m) >= MINOR_KVALITET)

def entydig(farver, L):
    """Den længste af farverne; None, hvis to er lige lange (reglerne siger ikke, hvilken der meldes)."""
    if not farver:
        return None
    farver = sorted(farver, key=lambda s: L[s], reverse=True)
    return farver[0] if len(farver) == 1 or L[farver[0]] > L[farver[1]] else None

# --- direkte ----------------------------------------------------------------------

def direkte(hand, hp):
    L = lengths_of(hand)
    if 17 <= hp <= 19 and jaevn(L):
        return "2NT", tx(f"{hp} hp og jævn: 2NT – 17–19 jævn; herpå amerikansk Stayman.",
                         f"{hp} HCP and balanced: 2NT – 17–19 balanced; then American Stayman.")
    m = next((m for m in MINORER if L[m] >= 5), None)
    if L['H'] >= 5 and m and inden(hp, TOFARVE_HP):
        return f"4{SUIT_SYM[m]}", tx(
            f"{L['H']} hjerter, {L[m]} {SUIT_NAME[m]} og {hp} hp: 4{SUIT_SYM[m]} – 5+ hjerter og 5+ {SUIT_NAME[m]}.",
            f"{L['H']} hearts, {L[m]} {SUIT_NAME_EN[m]} and {hp} HCP: 4{SUIT_SYM[m]} – 5+ hearts and 5+ {SUIT_NAME_EN[m]}.")
    if L['C'] >= 5 and L['D'] >= 5 and inden(hp, MINOR_4NT_HP):
        return "4NT", tx(f"{L['D']} ruder, {L['C']} klør og {hp} hp: 4NT – begge minorer med styrke.",
                         f"{L['D']} diamonds, {L['C']} clubs and {hp} HCP: 4NT – both minors with strength.")
    M = next((M for M in MAJORER if L[M] >= 7 and toppe(hand, M) >= MAJOR_4M_KVALITET), None)
    if M and inden(hp, MAJOR_4M_HP):
        return f"4{SUIT_SYM[M]}", tx(f"{L[M]} gode {SUIT_NAME[M]} og {hp} hp: 4{SUIT_SYM[M]} – for at spille.",
                                     f"{L[M]} good {SUIT_NAME_EN[M]} and {hp} HCP: 4{SUIT_SYM[M]} – to play.")
    if 12 <= hp <= 16 and max(L['S'], L['H']) >= 5:
        M = 'S' if L['S'] >= L['H'] else 'H'
        return f"2{SUIT_SYM[M]}", tx(f"{L[M]} {SUIT_NAME[M]} og {hp} hp: 2{SUIT_SYM[M]} – naturligt, 5+ farve, 12–16.",
                                     f"{L[M]} {SUIT_NAME_EN[M]} and {hp} HCP: 2{SUIT_SYM[M]} – natural, 5+ suit, 12–16.")
    m = next((m for m in MINORER if L[m] >= 6 and toppe(hand, m) >= MINOR_3NT_KVALITET), None)
    if m and inden(hp, MINOR_3NT_HP) and max(L['S'], L['H']) < 5:
        return "3NT", tx(f"{L[m]} gode {SUIT_NAME[m]} og {hp} hp: 3NT – for at spille med minorlængde og styrke.",
                         f"{L[m]} good {SUIT_NAME_EN[m]} and {hp} HCP: 3NT – to play with minor length and strength.")
    if hp >= 17:
        return "X", tx(f"{hp} hp: X – 12–16 jævn eller 17+.",
                       f"{hp} HCP: X – 12–16 balanced or 17+.")
    if 12 <= hp <= 16:
        gode = [m for m in MINORER if god_minor(hand, L, m)]
        if gode:
            m = entydig(gode, L)
            if not m:
                return None
            return f"3{SUIT_SYM[m]}", tx(
                f"{L[m]} {SUIT_NAME[m]} og {hp} hp: 3{SUIT_SYM[m]} – naturligt, 5+ farve, 12–16.",
                f"{L[m]} {SUIT_NAME_EN[m]} and {hp} HCP: 3{SUIT_SYM[m]} – natural, 5+ suit, 12–16.")
    if 12 <= hp <= 16 and jaevn(L):
        return "X", tx(f"{hp} hp og jævn: X – 12–16 jævn eller 17+.",
                       f"{hp} HCP and balanced: X – 12–16 balanced or 17+.")
    if hp >= 12:
        kort_major = next((M for M in MAJORER if L[M] <= 1), None)
        if sum(1 for s in SUITS if L[s] >= 4) == 3 and kort_major:
            return "Pas", tx(
                f"Trefarvet med {L[kort_major]} {SUIT_NAME[kort_major]} og {hp} hp: pas – du kommer om muligt igen senere med en oplysningsdobling.",
                f"Three-suited with {L[kort_major]} {SUIT_NAME_EN[kort_major]} and {hp} HCP: pass – if possible, you come back later with a takeout double.")
        m = next((m for m in MINORER if L[m] == 5 and not god_minor(hand, L, m)), None)
        if m:
            return "Pas", tx(
                f"{hp} hp, men kun en tvivlsom 5-farve i {SUIT_NAME[m]}: pas – du kommer om muligt igen senere med minorfarven.",
                f"{hp} HCP, but only a doubtful five-card {SUIT_NAME_EN[m]} suit: pass – if possible, you come back later with the minor.")
        return None
    return "Pas", tx(f"{hp} hp: pas.", f"{hp} HCP: pass.")

# --- genåbning --------------------------------------------------------------------

def genaabning(hand, hp):
    r = direkte(hand, hp)
    if not r or r[0] != "Pas":
        return None
    L = lengths_of(hand)
    if L['S'] >= 4 and L['H'] <= 1 and hp >= 12:
        hj, hj_en = ('en hjerter', 'one heart') if L['H'] == 1 else ('renonce i hjerter', 'a heart void')
        return "X", tx(f"{L['S']} spar og {hj} i genåbningen: X – oplysning, typisk 4 spar og korthed i hjerter.",
                       f"{L['S']} spades and {hj_en} in the balancing seat: X – takeout, typically 4 spades and shortness in hearts.")
    m = entydig([m for m in MINORER if L[m] >= 5], L)
    if m and 12 <= hp <= 16:
        return f"3{SUIT_SYM[m]}", tx(f"{L[m]} {SUIT_NAME[m]} og {hp} hp: 3{SUIT_SYM[m]} – den minorfarve, du ventede med.",
                                     f"{L[m]} {SUIT_NAME_EN[m]} and {hp} HCP: 3{SUIT_SYM[m]} – the minor you waited with.")
    if any(L[m] >= 5 for m in MINORER) and 12 <= hp <= 16:
        return None
    if hp < 12:
        return "Pas", tx(f"{hp} hp: pas.", f"{hp} HCP: pass.")
    return "Pas", tx(f"{hp} hp uden 4 spar og korthed i hjerter og uden 5-farve i en minor: pas.",
                     f"{hp} HCP without 4 spades and short hearts and without a five-card minor: pass.")

# --- svar på makkers dobling ------------------------------------------------------

HOLD_NAVN = {'H': ("hjerterhold", "a heart stopper"), 'S': ("sparhold", "a spade stopper")}

def svar_efter(hand, hp, M):
    """(2♦) – X – (2M) – ?  M er deres major og A den anden."""
    A = 'S' if M == 'H' else 'H'
    sM, sA = SUIT_SYM[M], SUIT_SYM[A]
    L = lengths_of(hand)
    if L[M] >= 4 and inden(hp, STRAF_HP):
        return "X", tx(f"{L[M]} {SUIT_NAME[M]} og {hp} hp: X – straf.", f"{L[M]} {SUIT_NAME_EN[M]} and {hp} HCP: X – penalty.")
    if L[A] >= 6 and inden(hp, KRAV_HP):
        return f"4{sA}", tx(f"{L[A]} {SUIT_NAME[A]} og {hp} hp: 4{sA} – for at spille med 6+ kort og udgangsstyrke.",
                            f"{L[A]} {SUIT_NAME_EN[A]} and {hp} HCP: 4{sA} – to play with 6+ cards and game values.")
    if L[A] >= 5 and inden(hp, KRAV_HP):
        return f"3{sA}", tx(f"{L[A]} {SUIT_NAME[A]} og {hp} hp: 3{sA} – krav, 5+ farve.",
                            f"{L[A]} {SUIT_NAME_EN[A]} and {hp} HCP: 3{sA} – forcing, 5+ suit.")
    if inden(hp, INVIT_HP):
        lange = [m for m in MINORER if L[m] >= 5]
        if lange:
            m = entydig(lange, L)
            if not m:
                return None
            return f"3{SUIT_SYM[m]}", tx(f"{L[m]} {SUIT_NAME[m]} og {hp} hp: 3{SUIT_SYM[m]} – konstruktiv, invit.",
                                         f"{L[m]} {SUIT_NAME_EN[m]} and {hp} HCP: 3{SUIT_SYM[m]} – constructive, invitational.")
        if L[A] >= 5:
            return "2NT", tx(f"{L[A]} {SUIT_NAME[A]} og {hp} hp: 2NT – Lebensohl; efter makkers 3♣ inviterer du med 3{sA}.",
                             f"{L[A]} {SUIT_NAME_EN[A]} and {hp} HCP: 2NT – Lebensohl; after partner's 3♣ you invite with 3{sA}.")
        return "2NT", tx(f"{hp} hp uden 5-farve: 2NT – Lebensohl; efter makkers 3♣ inviterer du til 3NT med 3{sM}.",
                         f"{hp} HCP without a five-card suit: 2NT – Lebensohl; after partner's 3♣ you invite to 3NT with 3{sM}.")
    if hp > SVAG_HP:
        return None
    if M == 'H' and L['S'] >= 4:
        return "2♠", tx(f"{L['S']} spar og {hp} hp: 2♠ – for at spille.", f"{L['S']} spades and {hp} HCP: 2♠ – to play.")
    m = next((m for m in MINORER if L[m] >= 5), None)
    if m:
        return "2NT", tx(f"{L[m]} {SUIT_NAME[m]} og {hp} hp: 2NT – Lebensohl; du vil spille 3♣ eller 3♦.",
                         f"{L[m]} {SUIT_NAME_EN[m]} and {hp} HCP: 2NT – Lebensohl; you want to play 3♣ or 3♦.")
    if M == 'H':
        return "Pas", tx(f"{hp} hp uden 4 spar og uden 5-farve i en minor: pas.",
                         f"{hp} HCP without 4 spades and without a five-card minor: pass.")
    return "Pas", tx(f"{hp} hp uden 5-farve i en minor: pas.", f"{hp} HCP without a five-card minor: pass.")

def relae_efter(hand, hp, M):
    """(2♦) – X – (2M) – 2NT – (pas) – 3♣ – (pas) – ?"""
    r = svar_efter(hand, hp, M)
    if not r or r[0] != "2NT":
        return None
    A = 'S' if M == 'H' else 'H'
    sM, sA = SUIT_SYM[M], SUIT_SYM[A]
    L = lengths_of(hand)
    if L[A] >= 5 and inden(hp, INVIT_HP):
        return f"3{sA}", tx(f"{L[A]} {SUIT_NAME[A]} og {hp} hp: 3{sA} – invit med 5+ kort.",
                            f"{L[A]} {SUIT_NAME_EN[A]} and {hp} HCP: 3{sA} – invitational with 5+ cards.")
    if inden(hp, INVIT_HP):
        hold, hold_en = HOLD_NAVN[M]
        return f"3{sM}", tx(f"{hp} hp uden 5-farve: 3{sM} – invit til 3NT, beder om {hold}. Med 4+ {SUIT_NAME[M]} havde du doblet 2{sM}.",
                            f"{hp} HCP without a five-card suit: 3{sM} – invitation to 3NT, asks for {hold_en}. "
                            f"With 4+ {SUIT_NAME_EN[M]} you would have doubled 2{sM}.")
    if L['D'] >= 5 and hp <= SVAG_HP:
        return "3♦", tx(f"{L['D']} ruder og {hp} hp: 3♦ – svag med minorfarven.",
                        f"{L['D']} diamonds and {hp} HCP: 3♦ – weak with the minor.")
    if L['C'] >= 5 and hp <= SVAG_HP:
        return "Pas", tx(f"{L['C']} klør og {hp} hp: pas – svag med minorfarven.",
                         f"{L['C']} clubs and {hp} HCP: pass – weak with the minor.")
    return None

def svar_pas(hand, hp):
    """(2♦) – X – (pas) – ?"""
    L = lengths_of(hand)
    if L['D'] >= RUDER_STRAF and hp <= STRAF_HP[1]:
        return "Pas", tx(f"{L['D']} ruder og {hp} hp: pas – straf med lange ruder.",
                         f"{L['D']} diamonds and {hp} HCP: pass – penalty with long diamonds.")
    if inden(hp, KRAV_HP):
        farver = [s for s in ('S', 'H', 'C') if L[s] >= 5]
        if not farver:
            return None
        s = entydig(farver, L)
        if not s:
            return None
        return f"3{SUIT_SYM[s]}", tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: 3{SUIT_SYM[s]} – krav, ny farve på 3-trinnet.",
                                     f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: 3{SUIT_SYM[s]} – forcing, a new suit at the three level.")
    if hp > SVAG_HP:
        return None
    major = [s for s in MAJORER if L[s] >= 4]
    if major:
        s = entydig(major, L)
        if not s:
            return None
        return f"2{SUIT_SYM[s]}", tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: 2{SUIT_SYM[s]} – for at spille.",
                                     f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: 2{SUIT_SYM[s]} – to play.")
    if L['C'] >= 5:
        return "2NT", tx(f"{L['C']} klør og {hp} hp: 2NT – Lebensohl; du vil spille 3♣.",
                         f"{L['C']} clubs and {hp} HCP: 2NT – Lebensohl; you want to play 3♣.")
    return None

def svar_4kl(hand, hp):
    L = lengths_of(hand)
    if L['C'] >= 3 and L['C'] > L['H'] and inden(hp, SLEM_HP):
        return "4♠", tx(f"{L['C']} klør, {L['H']} hjerter og {hp} hp: 4♠ – krav med klør som trumf.",
                        f"{L['C']} clubs, {L['H']} hearts and {hp} HCP: 4♠ – forcing with clubs as trumps.")
    if L['H'] >= 3 and inden(hp, SLEM_HP):
        return "4♦", tx(f"{L['H']} hjerter og {hp} hp: 4♦ – krav med hjerter som trumf.",
                        f"{L['H']} hearts and {hp} HCP: 4♦ – forcing with hearts as trumps.")
    if L['H'] >= 2:
        return "4♥", tx(f"{L['H']} hjerter og {hp} hp: 4♥ – for at spille.", f"{L['H']} hearts and {hp} HCP: 4♥ – to play.")
    return None

# --- dobleren efter makkers 2NT (Franks valg 27. og 28. oktober 2026) -------------

def hold(hand, M):
    """Es, konge med 1+ kort til, dame med 2+ eller knægt med 3+ i farve M (HOLD)."""
    return any(r in HOLD and len(hand[M]) >= HOLD[r] for r in hand[M])

def dobler_efter(hand, hp, M):
    """(2♦) – X – (2M) – 2NT – (pas) – ?  M er deres major og A den anden."""
    r = direkte(hand, hp)
    if not r or r[0] != "X":
        return None
    A = 'S' if M == 'H' else 'H'
    sM = SUIT_SYM[M]
    navn, navn_en = HOLD_NAVN[M]
    L = lengths_of(hand)
    if 12 <= hp <= 16:
        return "3♣", tx(f"{hp} hp og jævn: 3♣ – som makker beder om; du har 12–16 jævn.",
                        f"{hp} HCP and balanced: 3♣ – as partner asks; you have 12–16 balanced.")
    if jaevn(L) and 20 <= hp <= 21 and hold(hand, M):
        return "3NT", tx(f"{hp} hp, jævn og {navn}: 3NT – 20–21 jævn med {navn}.",
                         f"{hp} HCP, balanced with {navn_en}: 3NT – 20–21 balanced with {navn_en}.")
    if (jaevn(L) and hp >= 22) or (not jaevn(L) and L[M] >= 5):
        return None
    farver = [s for s in (A, 'D', 'C') if L[s] >= 5]
    if farver:
        s = entydig(farver, L)
        if not s:
            return None
        bud = "4♣" if s == 'C' else f"3{SUIT_SYM[s]}"
        krav, krav_en = (", krav", ", forcing") if s != 'C' else ("", "")
        return bud, tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: {bud} – 5+ {SUIT_NAME[s]}, 17+{krav}.",
                       f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: {bud} – 5+ {SUIT_NAME_EN[s]}, 17+{krav_en}.")
    if jaevn(L):
        return f"3{sM}", tx(f"{hp} hp og jævn, men uden {navn}: 3{sM} – 17+ uden egen farve; beder om {navn}.",
                            f"{hp} HCP and balanced, but without {navn_en}: 3{sM} – 17+ without a suit of your own; asks for {navn_en}.")
    return f"3{sM}", tx(f"{hp} hp uden egen farve: 3{sM} – 17+ uden egen farve; beder om {navn}.",
                        f"{hp} HCP without a suit of your own: 3{sM} – 17+ without a suit of your own; asks for {navn_en}.")

# --- bonusspørgsmål ---------------------------------------------------------------

C_X = tx("12–16 jævn eller 17+", "12–16 balanced or 17+")
C_2NT = tx("Lebensohl: beder om 3♣", "Lebensohl: asks for 3♣")
C_4NT = tx("Esspørgsmål med 6 esser", "Ace ask with 6 aces")
C_BRUD = tx("Bryder i stedet for at melde 3♣", "Breaks instead of bidding 3♣")
B_X = {"q": tx("Hvad viser X direkte over 2♦?", "What does X show directly over 2♦?"),
       "correct": C_X, "options": [C_X, tx("Straf af ruder", "Penalty of diamonds"),
                                   tx("Oplysning med korthed i ruder", "Takeout with shortness in diamonds")],
       "why": tx("Doblingen af 2♦ viser 12–16 jævn eller 17+. Den er hverken straf eller oplysning af ruder.",
                 "The double of 2♦ shows 12–16 balanced or 17+. It is neither a penalty nor a takeout double of diamonds.")}
B_2NT = {"q": tx("Hvad viser 2NT fra makker efter (2♦) – X – (2♥)?", "What does 2NT from partner show after (2♦) – X – (2♥)?"),
         "correct": C_2NT, "options": [C_2NT, tx("Naturligt, 10–12 jævn", "Natural, 10–12 balanced"),
                                       tx("Krav til udgang", "Game forcing")],
         "why": tx("2NT er Lebensohl og beder dobleren melde 3♣: enten en svag hånd med en minor eller en invit, med 5+ spar "
                   "3♠ bagefter og uden farve 3♥ (holdspørgsmål til 3NT). 3♣ og 3♦ direkte er invit.",
                   "2NT is Lebensohl and asks the doubler to bid 3♣: either a weak hand with a minor or an invitation, with 5+ spades "
                   "3♠ afterwards and without a suit 3♥ (asking for a stopper for 3NT). 3♣ and 3♦ directly are invitational.")}
B_4NT = {"q": tx("Hvad viser 4NT efter (2♦) – 4♣?", "What does 4NT show after (2♦) – 4♣?"),
         "correct": C_4NT, "options": [C_4NT, tx("Begge minorer", "Both minors"), tx("For at spille", "To play")],
         "why": tx("Efter 4♣ (5+ hjerter og 5+ klør) er 4NT esspørgsmål med 6 esser, normalt de fire esser og kongerne i hjerter og klør.",
                   "After 4♣ (5+ hearts and 5+ clubs), 4NT is an ace ask with 6 aces, normally the four aces and the kings of hearts and clubs.")}
B_BRUD = {"q": tx("Hvad gør dobleren efter makkers 2NT med 17+?", "What does the doubler do after partner's 2NT with 17+?"),
          "correct": C_BRUD, "options": [C_BRUD, tx("Melder 3♣ og passer bagefter", "Bids 3♣ and passes afterwards"),
                                         tx("Melder altid 3NT", "Always bids 3NT")],
          "why": tx("2NT beder om 3♣, men med 17+ bryder dobleren i stedet for at melde 3♣: 3♦ og 3♠ med 5+ farve (krav), "
                    "4♣ med 5+ klør, 3♥ uden egen farve (beder om hjerterhold) og 3NT med 20–21 jævn og hjerterhold.",
                    "2NT asks for 3♣, but with 17+ the doubler breaks instead of bidding 3♣: 3♦ and 3♠ with a 5+ suit (forcing), "
                    "4♣ with 5+ clubs, 3♥ without a suit of your own (asks for a heart stopper) and 3NT with 20–21 balanced "
                    "and a heart stopper.")}
C_3H = tx("Invit til 3NT, beder om hjerterhold", "Invitation to 3NT, asks for a heart stopper")
B_3H = {"q": tx("Hvad viser svarerens 3♥ efter 2NT – 3♣?", "What does responder's 3♥ show after 2NT – 3♣?"),
        "correct": C_3H, "options": [C_3H, tx("Naturligt med 5 hjerter", "Natural with 5 hearts"),
                                     tx("Krav til udgang", "Game forcing")],
        "why": tx("3♥ kan ikke være naturlig, fordi svareren dobler 2♥ for straf med 4+ hjerter. Den inviterer til 3NT "
                  "og beder om hjerterhold.",
                  "3♥ cannot be natural, because responder doubles 2♥ for penalty with 4+ hearts. It invites to 3NT "
                  "and asks for a heart stopper.")}
B_BRUD_SP = {"q": tx("Hvad gør dobleren efter (2♦) – X – (2♠) – 2NT med 17+?",
                     "What does the doubler do after (2♦) – X – (2♠) – 2NT with 17+?"),
             "correct": C_BRUD, "options": [C_BRUD, tx("Melder 3♣ og passer bagefter", "Bids 3♣ and passes afterwards"),
                                            tx("Melder altid 3NT", "Always bids 3NT")],
             "why": tx("Over 2♠ er det samme struktur som over 2♥ med farverne byttet om: 3♦ og 3♥ med 5+ farve (krav), 4♣ med "
                       "5+ klør, 3♠ uden egen farve (beder om sparhold) og 3NT med 20–21 jævn og sparhold.",
                       "Over 2♠ the structure is the same as over 2♥ with the suits swapped: 3♦ and 3♥ with a 5+ suit (forcing), "
                       "4♣ with 5+ clubs, 3♠ without a suit of your own (asks for a spade stopper) and 3NT with 20–21 balanced "
                       "and a spade stopper.")}
C_X_SP = tx("Straf med 4+ spar", "Penalty with 4+ spades")
B_X_SP = {"q": tx("Hvad viser svarerens X i (2♦) – X – (2♠)?", "What does responder's X show in (2♦) – X – (2♠)?"),
          "correct": C_X_SP, "options": [C_X_SP, tx("Oplysning med hjerter", "Takeout with hearts"),
                                         tx("12+ uden farve", "12+ without a suit")],
          "why": tx("Over 2♠ er strukturen den samme som over 2♥ med farverne byttet om: X er straf med 4+ spar, 2NT er "
                    "Lebensohl, 3♥ er krav med 5+ hjerter, og 3♣ og 3♦ er konstruktive og invit.",
                    "Over 2♠ the structure is the same as over 2♥ with the suits swapped: X is penalty with 4+ spades, 2NT is "
                    "Lebensohl, 3♥ is forcing with 5+ hearts, and 3♣ and 3♦ are constructive and invitational.")}
C_3S_SP = tx("Invit til 3NT, beder om sparhold", "Invitation to 3NT, asks for a spade stopper")
B_3S_SP = {"q": tx("Hvad viser svarerens 3♠ i (2♦) – X – (2♠) – 2NT – 3♣?", "What does responder's 3♠ show in (2♦) – X – (2♠) – 2NT – 3♣?"),
           "correct": C_3S_SP, "options": [C_3S_SP, tx("Naturligt med 5 spar", "Natural with 5 spades"),
                                           tx("Krav til udgang", "Game forcing")],
           "why": tx("Efter 2NT – 3♣ er 3 i modpartens major et holdspørgsmål til 3NT: med 4+ spar havde svareren doblet 2♠ "
                     "for straf. 3♥ er invit med 5+ hjerter.",
                     "After 2NT – 3♣, three of the opponents' major asks for a stopper for 3NT: with 4+ spades responder would "
                     "have doubled 2♠ for penalty. 3♥ is invitational with 5+ hearts.")}
C_PAS = tx("Straf med lange ruder", "Penalty with long diamonds")
B_PAS = {"q": tx("Hvad viser svarerens pas i (2♦) – X – (pas)?", "What does responder's pass show in (2♦) – X – (pass)?"),
         "correct": C_PAS, "options": [C_PAS, tx("Svag hånd uden farve", "A weak hand without a suit"),
                                       tx("Venter på makkers næste melding", "Waits for partner's next bid")],
         "why": tx("Over pas er 2♥ og 2♠ for at spille, 2NT er Lebensohl, nye farver på 3-trinnet er krav, og pas er straf "
                   "med lange ruder.",
                   "Over a pass, 2♥ and 2♠ are to play, 2NT is Lebensohl, new suits at the three level are forcing, and pass is "
                   "penalty with long diamonds.")}

# --- situationer og hænder --------------------------------------------------------

NOTE = tx("2♦ (Multi eller Ekren)", "2♦ (Multi or Ekren)")

def t(hp, **b):
    return tpl(hp, **{**{s: (0, 5) for s in SUITS}, **b})

SITUATIONS = {
    "direkte": {"rolle": "Indmelder", "note": NOTE, "auction": [["Modstander", "2♦"]], "allowX": True,
                "calls": ["Pas", "X", "2♥", "2♠", "2NT", "3♣", "3♦", "3NT", "4♣", "4♦", "4♥", "4♠", "4NT"], "bonus": B_X},
    "genaabning": {"rolle": "Genåbner", "note": NOTE,
                   "auction": [["Modstander", "2♦"], ["Dig", "Pas"], ["Modstander", "2♥"], ["Makker", "Pas"], ["Modstander", "Pas"]],
                   "allowX": True, "calls": ["Pas", "X", "2♠", "3♣", "3♦"], "bonus": B_X},
    "svar_d": {"rolle": "Svarer", "note": NOTE, "auction": [["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "2♥"]],
               "allowX": True, "calls": ["Pas", "X", "2♠", "2NT", "3♣", "3♦", "3♠", "4♠"], "bonus": B_2NT},
    "svar_relae": {"rolle": "Svarer", "note": NOTE,
                   "auction": [["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "2♥"], ["Dig", "2NT"], ["Modstander", "Pas"],
                               ["Makker", "3♣"], ["Modstander", "Pas"]],
                   "calls": ["Pas", "3♦", "3♥", "3♠"], "bonus": B_3H},
    "svar_4kl": {"rolle": "Svarer", "note": NOTE, "auction": [["Modstander", "2♦"], ["Makker", "4♣"], ["Modstander", "Pas"]],
                 "calls": ["4♦", "4♥", "4♠"], "bonus": B_4NT},
    "dobler": {"rolle": "Dobler", "note": NOTE,
               "auction": [["Modstander", "2♦"], ["Dig", "X"], ["Modstander", "2♥"], ["Makker", "2NT"], ["Modstander", "Pas"]],
               "calls": ["3♣", "3♦", "3♥", "3♠", "3NT", "4♣"], "bonus": B_BRUD},
    "svar_d_sp": {"rolle": "Svarer", "note": NOTE, "auction": [["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "2♠"]],
                  "allowX": True, "calls": ["Pas", "X", "2NT", "3♣", "3♦", "3♥", "4♥"], "bonus": B_X_SP},
    "svar_relae_sp": {"rolle": "Svarer", "note": NOTE,
                      "auction": [["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "2♠"], ["Dig", "2NT"], ["Modstander", "Pas"],
                                  ["Makker", "3♣"], ["Modstander", "Pas"]],
                      "calls": ["Pas", "3♦", "3♥", "3♠"], "bonus": B_3S_SP},
    "svar_pas": {"rolle": "Svarer", "note": NOTE, "auction": [["Modstander", "2♦"], ["Makker", "X"], ["Modstander", "Pas"]],
                 "calls": ["Pas", "2♥", "2♠", "2NT", "3♣", "3♥", "3♠"], "bonus": B_PAS},
    "dobler_sp": {"rolle": "Dobler", "note": NOTE,
                  "auction": [["Modstander", "2♦"], ["Dig", "X"], ["Modstander", "2♠"], ["Makker", "2NT"], ["Modstander", "Pas"]],
                  "calls": ["3♣", "3♦", "3♥", "3♠", "3NT", "4♣"], "bonus": B_BRUD_SP},
}
for s in SITUATIONS.values():
    s["calls"] = sorted(s["calls"], key=K)

CLASSIFIERS = {"direkte": direkte, "genaabning": genaabning, "svar_d": lambda h, hp: svar_efter(h, hp, 'H'),
               "svar_relae": lambda h, hp: relae_efter(h, hp, 'H'), "svar_4kl": svar_4kl, "dobler": lambda h, hp: dobler_efter(h, hp, 'H'),
               "svar_d_sp": lambda h, hp: svar_efter(h, hp, 'S'), "svar_relae_sp": lambda h, hp: relae_efter(h, hp, 'S'),
               "svar_pas": svar_pas, "dobler_sp": lambda h, hp: dobler_efter(h, hp, 'S')}

SAMPLERS = {
    "direkte": {
        "2NT": t((17, 19), S=(2, 5), H=(2, 5), D=(2, 5), C=(2, 5)),
        "4♣": t(TOFARVE_HP, H=(5, 6), C=(5, 6), S=(0, 3), D=(0, 3)),
        "4♦": t(TOFARVE_HP, H=(5, 6), D=(5, 6), S=(0, 3), C=(0, 3)),
        "4NT": t(MINOR_4NT_HP, C=(5, 7), D=(5, 7), S=(0, 3), H=(0, 3)),
        "4♥": t(MAJOR_4M_HP, H=(7, 8), S=(0, 3), D=(0, 3), C=(0, 3)),
        "4♠": t(MAJOR_4M_HP, S=(7, 8), H=(0, 3), D=(0, 3), C=(0, 3)),
        "3NT": either(t(MINOR_3NT_HP, C=(6, 7), S=(0, 4), H=(0, 4), D=(0, 4)),
                      t(MINOR_3NT_HP, D=(6, 7), S=(0, 4), H=(0, 4), C=(0, 4))),
        "X": either(t((12, 16), S=(2, 5), H=(2, 5), D=(2, 5), C=(2, 5)), t((17, 21), S=(0, 6), H=(0, 6), D=(0, 6), C=(0, 6))),
        "2♥": t((12, 16), H=(5, 6), S=(0, 4)),
        "2♠": t((12, 16), S=(5, 6), H=(0, 5)),
        "3♣": t((12, 16), C=(5, 7), S=(0, 4), H=(0, 4), D=(0, 4)),
        "3♦": t((12, 16), D=(5, 7), S=(0, 4), H=(0, 4), C=(0, 4)),
        "Pas": either(rnd((0, 11)),
                      t((12, 16), S=(0, 1), H=(4, 5), D=(4, 5), C=(4, 5)),
                      t((12, 16), H=(0, 1), S=(4, 5), D=(4, 5), C=(4, 5)),
                      t((12, 16), C=(5, 5), S=(0, 4), H=(0, 4), D=(0, 4)),
                      t((12, 16), D=(5, 5), S=(0, 4), H=(0, 4), C=(0, 4))),
    },
    "genaabning": {
        "X": t((12, 16), S=(4, 5), H=(0, 1), D=(3, 5), C=(3, 5)),
        "3♣": t((12, 16), C=(5, 5), S=(0, 4), H=(2, 4), D=(0, 4)),
        "3♦": t((12, 16), D=(5, 5), S=(0, 4), H=(2, 4), C=(0, 4)),
        "Pas": either(rnd((0, 11)), t((12, 16), S=(0, 1), H=(4, 5), D=(4, 5), C=(4, 5))),
    },
    "svar_d": {
        "X": t(STRAF_HP, H=(4, 5)),
        "3♠": t(KRAV_HP, S=(5, 5), H=(0, 3)),
        "4♠": t(KRAV_HP, S=(6, 7), H=(0, 3)),
        "3♣": t(INVIT_HP, C=(5, 6), H=(0, 3), D=(0, 4)),
        "3♦": t(INVIT_HP, D=(5, 6), H=(0, 3), C=(0, 4)),
        "2NT": either(t(INVIT_HP, S=(5, 5), H=(0, 3), D=(0, 4), C=(0, 4)), t(INVIT_HP, S=(6, 7), H=(0, 3), D=(0, 3), C=(0, 3)),
                      t(INVIT_HP, S=(0, 4), H=(0, 3), D=(0, 4), C=(0, 4)),
                      t((0, SVAG_HP), C=(5, 7), S=(0, 3)), t((0, SVAG_HP), D=(5, 7), S=(0, 3))),
        "2♠": t((0, SVAG_HP), S=(4, 6)),
        "Pas": t((0, SVAG_HP), S=(0, 3), D=(0, 4), C=(0, 4)),
    },
    "svar_relae": {
        "3♠": either(t(INVIT_HP, S=(5, 5), H=(0, 3), D=(0, 4), C=(0, 4)), t(INVIT_HP, S=(6, 7), H=(0, 3), D=(0, 3), C=(0, 3))),
        "3♥": t(INVIT_HP, S=(0, 4), H=(0, 3), D=(0, 4), C=(0, 4)),
        "3♦": t((0, SVAG_HP), D=(5, 7), S=(0, 3)),
        "Pas": t((0, SVAG_HP), C=(5, 7), S=(0, 3), D=(0, 4)),
    },
    "svar_4kl": {
        "4♠": t(SLEM_HP, C=(3, 5), H=(0, 2)),
        "4♦": t(SLEM_HP, H=(3, 4), C=(0, 3)),
        "4♥": t((0, SLEM_HP[0] - 1), H=(2, 4)),
    },
    "dobler": {
        "3♣": t((12, 16), S=(2, 4), H=(2, 4), D=(2, 5), C=(2, 5)),
        "3NT": t((20, 21), S=(2, 5), H=(3, 5), D=(2, 5), C=(2, 5)),
        "3♠": t((17, DOBLER_HP_MAX), S=(5, 6), H=(0, 4), D=(0, 4), C=(0, 4)),
        "3♦": t((17, DOBLER_HP_MAX), D=(5, 7), S=(0, 4), H=(0, 4), C=(0, 4)),
        "4♣": t((17, DOBLER_HP_MAX), C=(5, 7), S=(0, 4), H=(0, 4), D=(0, 4)),
        "3♥": either(t((17, DOBLER_HP_MAX), S=(0, 4), H=(0, 4), D=(0, 4), C=(0, 4)),
                     t((20, 21), S=(2, 4), H=(2, 3), D=(2, 4), C=(2, 4))),
    },
    "svar_d_sp": {
        "X": t(STRAF_HP, S=(4, 5)),
        "3♥": t(KRAV_HP, H=(5, 5), S=(0, 3)),
        "4♥": t(KRAV_HP, H=(6, 7), S=(0, 3)),
        "3♣": t(INVIT_HP, C=(5, 6), S=(0, 3), D=(0, 4)),
        "3♦": t(INVIT_HP, D=(5, 6), S=(0, 3), C=(0, 4)),
        "2NT": either(t(INVIT_HP, H=(5, 5), S=(0, 3), D=(0, 4), C=(0, 4)), t(INVIT_HP, H=(6, 7), S=(0, 3), D=(0, 3), C=(0, 3)),
                      t(INVIT_HP, H=(0, 4), S=(0, 3), D=(0, 4), C=(0, 4)),
                      t((0, SVAG_HP), C=(5, 7), S=(0, 3)), t((0, SVAG_HP), D=(5, 7), S=(0, 3))),
        "Pas": t((0, SVAG_HP), D=(0, 4), C=(0, 4)),
    },
    "svar_relae_sp": {
        "3♥": either(t(INVIT_HP, H=(5, 5), S=(0, 3), D=(0, 4), C=(0, 4)), t(INVIT_HP, H=(6, 7), S=(0, 3), D=(0, 3), C=(0, 3))),
        "3♠": t(INVIT_HP, H=(0, 4), S=(0, 3), D=(0, 4), C=(0, 4)),
        "3♦": t((0, SVAG_HP), D=(5, 7), S=(0, 3)),
        "Pas": t((0, SVAG_HP), C=(5, 7), S=(0, 3), D=(0, 4)),
    },
    "svar_pas": {
        "Pas": t((0, STRAF_HP[1]), D=(RUDER_STRAF, 7)),
        "3♣": t(KRAV_HP, C=(5, 7), S=(0, 4), H=(0, 4), D=(0, 4)),
        "3♥": t(KRAV_HP, H=(5, 7), S=(0, 4), D=(0, 4), C=(0, 4)),
        "3♠": t(KRAV_HP, S=(5, 7), H=(0, 4), D=(0, 4), C=(0, 4)),
        "2♥": t((0, SVAG_HP), H=(4, 6), S=(0, 3), D=(0, 4)),
        "2♠": t((0, SVAG_HP), S=(4, 6), H=(0, 3), D=(0, 4)),
        "2NT": t((0, SVAG_HP), C=(5, 7), S=(0, 3), H=(0, 3), D=(0, 4)),
    },
    "dobler_sp": {
        "3♣": t((12, 16), S=(2, 4), H=(2, 4), D=(2, 5), C=(2, 5)),
        "3NT": t((20, 21), S=(3, 5), H=(2, 5), D=(2, 5), C=(2, 5)),
        "3♥": t((17, DOBLER_HP_MAX), H=(5, 6), S=(0, 4), D=(0, 4), C=(0, 4)),
        "3♦": t((17, DOBLER_HP_MAX), D=(5, 7), S=(0, 4), H=(0, 4), C=(0, 4)),
        "4♣": t((17, DOBLER_HP_MAX), C=(5, 7), S=(0, 4), H=(0, 4), D=(0, 4)),
        "3♠": either(t((17, DOBLER_HP_MAX), S=(0, 4), H=(0, 4), D=(0, 4), C=(0, 4)),
                     t((20, 21), S=(2, 3), H=(2, 4), D=(2, 4), C=(2, 4))),
    },
}
PER = {k: PER_CALL for k in SITUATIONS}

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER)
