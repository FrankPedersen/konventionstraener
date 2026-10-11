"""
Markeringer i modspillet – to puljer til markering.html:

  markeringer – Makker 1 & mig, systemkortet 9.1–9.2:
    es_kald         makker spiller es ud: kald (lavt) med damen – mod farvekontrakt også med doubleton – ellers afvisning (højt)
    k_antal         makker spiller konge ud: antal efter Malmø – lavt = lige, højt = ulige
    ny_farve_antal  spilfører spiller en ny farve fra bordet: Malmø – lavt = lige, højt = ulige
    afkast_farve    første afkast mod farvekontrakt: lavt kort kalder farven, højt kort afviser den
    afkast_sans     første afkast mod sans: kast i den farve, du ikke er interesseret i
  lavinthal – forslag, trænes før det skrives ind i systemkortet (retning som hos Makker 2 & mig):
    ruff_retur      kortet til makkers stjæler viser returfarven
    doed_udspil     bordet har singleton i makkers es-udspil: kortet viser skiftefarven
    lav_afkast      afkast i en uønsket farve viser den ønskede af de to andre farver (mod sans og farvekontrakt)
  Højt beder om den højeste af de to farver, lavt om den laveste (♠ > ♥ > ♦ > ♣).

Hver hånd er »giv« (vælg kortet) eller »læs« (hvad betyder makkers kort?). Antagelser, hvor kortet ikke er præcist:
kald = laveste kort; afvisning og »højt« = højeste kort, du har råd til (ikke en honnør), og mindst en 7'er;
lige antal = laveste, ulige antal = højeste. Et kort er tydeligt lavt, når læseren kan se alle lavere kort i farven,
og tydeligt højt fra 8'eren og op; kun tydelige kort bruges i »læs«. Spilfører er Syd, bordet Nord, du Øst (giv)
eller Vest (læs). Kontrakten er 4 i en major med 8+ kort fit eller 3NT uden.
"""
import random

from .core import SUITS, SUIT_SYM, SUIT_NAME, export

ORDEN = {'S': 4, 'H': 3, 'D': 2, 'C': 1}
RN = {14: 'E', 13: 'K', 12: 'D', 11: 'B'}
HP = {14: 4, 13: 3, 12: 2, 11: 1}

def rn(r): return RN.get(r, str(r))
def kort(s, r): return f"{SUIT_SYM[s]}{rn(r)}"
def code(s, r): return f"{s}{r}"
def holding(h, s): return SUIT_SYM[s] + ' ' + ' '.join(rn(r) for r in h[s])
def navn(s): return SUIT_NAME[s]

def deal():
    deck = [(s, r) for s in SUITS for r in range(2, 15)]
    random.shuffle(deck)
    hands = {}
    for i, seat in enumerate('NESW'):
        h = {s: [] for s in SUITS}
        for s, r in deck[i * 13:(i + 1) * 13]:
            h[s].append(r)
        for s in SUITS:
            h[s].sort(reverse=True)
        hands[seat] = h
    return hands

def hp(h): return sum(HP.get(r, 0) for s in SUITS for r in h[s])

def contract(H, want):
    ns = {s: len(H['N'][s]) + len(H['S'][s]) for s in SUITS}
    nshp = hp(H['N']) + hp(H['S'])
    if want == 'farve':
        majors = [s for s in ('S', 'H') if ns[s] >= 8]
        if not majors or nshp < 20:
            return None
        T = max(majors, key=lambda s: ns[s])
        return T, f"4{SUIT_SYM[T]}"
    if nshp < 24 or any(ns[s] >= 8 for s in ('S', 'H')):
        return None
    return None, '3NT'

def lav(cards): return min(cards)
def hoej(cards):
    small = [r for r in cards if r <= 10]
    return max(small) if small else max(cards)

def seen_by(H, seat, extra=()):
    s = {(x, r) for x in SUITS for r in H[seat][x]} | {(x, r) for x in SUITS for r in H['N'][x]}
    return s | set(extra)

def laesbar(card, suit, seen):
    lower = [r for r in range(2, card) if (suit, r) not in seen]
    if not lower:
        return 'lav'
    if card >= 8:
        return 'hoej'
    return None

def without(h, *cards):
    out = {s: list(h[s]) for s in SUITS}
    for s, r in cards:
        out[s].remove(r)
    return out

def trumf_tekst(T): return f"trumf er {navn(T)}" if T else "sans"

def rec(sit, mode, kontrakt, T, du, bordet, haand, stik, tekst, spm, valg, rigtige, hvorfor):
    return {"situation": sit, "mode": mode, "kontrakt": kontrakt, "trumf": T, "du": du,
            "bordet": bordet, "haand": haand, "stik": stik, "tekst": tekst, "spm": spm,
            "valg": valg, "rigtige": rigtige, "hvorfor": hvorfor}

# ---------- Makker 1 & mig ----------

def es_kald(H, mode):
    c = contract(H, random.choice(['farve', 'sans']))
    if not c:
        return None
    T, kon = c
    cands = [s for s in SUITS if s != T and H['W'][s][:2] == [14, 13] and len(H['W'][s]) >= 3
             and 2 <= len(H['N'][s]) <= 4 and 12 not in H['N'][s] and 2 <= len(H['E'][s]) <= 4]
    if not cands:
        return None
    X = random.choice(cands)
    E = H['E'][X]
    grund = 'damen' if 12 in E else ('doubleton' if T and len(E) == 2 else None)
    card = lav(E) if grund else hoej(E)
    if not grund and (card < 7 or card == lav(E)):
        return None
    d = min(H['N'][X])
    stik = [['Vest', code(X, 14)], ['Nord', code(X, d)]]
    tekst = f"Kontrakten er {kon} af Syd. Makker spiller {kort(X, 14)} ud, og bordet lægger {kort(X, d)}."
    if mode == 'giv':
        if grund == 'damen':
            why = f"Du har damen ({holding(H['E'], X)}): kald med det laveste kort, {kort(X, card)} – lavt = kald."
        elif grund == 'doubleton':
            why = f"Doubleton mod farvekontrakt – du kan stjæle i tredje runde: kald med det laveste kort, {kort(X, card)}."
        else:
            why = (f"Ingen dame{' og ingen doubleton' if T else ''} ({holding(H['E'], X)}): afvis med det højeste kort, "
                   f"du har råd til, {kort(X, card)} – højt = afvisning.")
        return rec('es_kald', 'giv', kon, T, 'Øst', without(H['N'], (X, d)), H['E'], stik, tekst,
                   "Hvilket kort lægger du?", [code(X, r) for r in E], [code(X, card)], why)
    l = laesbar(card, X, seen_by(H, 'W'))
    if l != ('lav' if grund else 'hoej'):
        return None
    valg = ["Kald – fortsæt farven", "Afvisning – skift farve"]
    if grund:
        why = (f"{kort(X, card)} er det laveste kort, du ikke selv kan se: lavt = kald. Makker har damen"
               f"{' eller en doubleton' if T else ''} – fortsæt med {kort(X, 13)}.")
    else:
        why = f"{kort(X, card)} er et højt kort: højt = afvisning. Makker har ikke damen{' og ingen doubleton' if T else ''} – skift farve."
    return rec('es_kald', 'laes', kon, T, 'Vest', without(H['N'], (X, d)), without(H['W'], (X, 14)),
               stik + [['Øst', code(X, card)]], tekst.replace('Makker spiller', 'Du spiller'),
               f"Makker lægger {kort(X, card)}. Hvad viser kortet?", valg, [valg[0] if grund else valg[1]], why)

def antal(sit, X, E, mode, H, kon, T, stik, tekst, leader_card=None):
    n = len(E)
    lige = n % 2 == 0
    card = lav(E) if lige else hoej(E)
    if not lige and (card < 7 or card == lav(E)):
        return None
    valg = ["Lige antal (2 eller 4)", "Ulige antal (3 eller 5)"]
    if mode == 'giv':
        why = (f"Du har {n} {navn(X)} – lige antal: læg det laveste, {kort(X, card)} (lavt = lige)." if lige else
               f"Du har {n} {navn(X)} – ulige antal: læg det højeste, {kort(X, card)} (højt = ulige).")
        bordet = without(H['N'], *[(c[0], int(c[1:])) for p, c in stik if p == 'Nord'])
        return rec(sit, 'giv', kon, T, 'Øst', bordet, H['E'], stik, tekst, "Hvilket kort lægger du?",
                   [code(X, r) for r in E], [code(X, card)], why)
    played = [(c[0], int(c[1:])) for p, c in stik]
    l = laesbar(card, X, seen_by(H, 'W', played))
    if l != ('lav' if lige else 'hoej'):
        return None
    why = (f"{kort(X, card)} er det laveste kort, du ikke selv kan se: lavt = lige antal (2 eller 4)." if lige else
           f"{kort(X, card)} er et højt kort: højt = ulige antal (3 eller 5).")
    haand = without(H['W'], *[(c[0], int(c[1:])) for p, c in stik if p == 'Vest'])
    bordet = without(H['N'], *[(c[0], int(c[1:])) for p, c in stik if p == 'Nord'])
    return rec(sit, 'laes', kon, T, 'Vest', bordet, haand, stik + [['Øst', code(X, card)]],
               tekst.replace('Makker spiller', 'Du spiller'), f"Makker lægger {kort(X, card)}. Hvad viser kortet?",
               valg, [valg[0] if lige else valg[1]], why)

def k_antal(H, mode):
    c = contract(H, random.choice(['farve', 'sans']))
    if not c:
        return None
    T, kon = c
    cands = [s for s in SUITS if s != T and H['W'][s][:2] == [13, 12] and (T or H['W'][s][:3] == [13, 12, 11])
             and len(H['W'][s]) >= 3 and 2 <= len(H['N'][s]) <= 4 and 14 not in H['N'][s]
             and 2 <= len(H['E'][s]) <= 5 and max(H['E'][s]) <= 10]
    if not cands:
        return None
    X = random.choice(cands)
    d = min(H['N'][X])
    stik = [['Vest', code(X, 13)], ['Nord', code(X, d)]]
    tekst = f"Kontrakten er {kon} af Syd. Makker spiller {kort(X, 13)} ud, og bordet lægger {kort(X, d)}. Konge-udspil beder om antal."
    return antal('k_antal', X, H['E'][X], mode, H, kon, T, stik, tekst)

def ny_farve_antal(H, mode):
    c = contract(H, random.choice(['farve', 'sans']))
    if not c:
        return None
    T, kon = c
    cands = [s for s in SUITS if s != T and len(H['N'][s]) >= 2 and 2 <= len(H['E'][s]) <= 5 and max(H['E'][s]) <= 10]
    if not cands:
        return None
    X = random.choice(cands)
    d = min(H['N'][X])
    stik = [['Nord', code(X, d)]]
    tekst = f"Kontrakten er {kon} af Syd. Spilfører er inde og spiller en ny farve fra bordet: {kort(X, d)}."
    return antal('ny_farve_antal', X, H['E'][X], mode, H, kon, T, stik, tekst)

def interesting(cards): return any(r >= 12 for r in cards)

def void_trick(H, L):
    return [['Syd', code(L, max(H['S'][L]))], ['Vest', code(L, min(H['W'][L]))], ['Nord', code(L, min(H['N'][L]))]]

def afkast_farve(H, mode):
    c = contract(H, 'farve')
    if not c:
        return None
    T, kon = c
    if H['E'][T] or not H['W'][T] or not H['N'][T]:
        return None
    side = [s for s in SUITS if s != T]
    W = [s for s in side if H['E'][s][:2] == [14, 13] and len(H['E'][s]) >= 3 and lav(H['E'][s]) <= 10]
    U = [s for s in side if not interesting(H['E'][s])]
    if len(W) != 1 or len(U) != 2:
        return None
    W = W[0]
    kald = code(W, lav(H['E'][W]))
    afvis = [code(u, hoej(H['E'][u])) for u in U if len(H['E'][u]) >= 2 and 8 <= hoej(H['E'][u]) <= 10]
    stik = void_trick(H, T)
    tekst = f"Kontrakten er {kon} af Syd. Spilfører spiller trumf, og du kan ikke bekende – det er dit første afkast."
    played = [(x[0], int(x[1:])) for p, x in stik]
    if mode == 'giv':
        why = f"Du vil have {navn(W)} spillet ({holding(H['E'], W)}): kald med et lavt kort i farven, {kort(W, lav(H['E'][W]))} – lavt = kald."
        if afvis:
            why += " Du kan også afvise en farve, du ikke vil have, med et højt kort, fx " + ' eller '.join(kort(x[0], int(x[1:])) for x in afvis) + "."
        return rec('afkast_farve', 'giv', kon, T, 'Øst', without(H['N'], played[2]), H['E'], stik, tekst, "Hvilket kort kaster du?",
                   [code(s, r) for s in SUITS for r in H['E'][s]], [kald] + afvis, why)
    pick = random.choice([kald] + afvis)
    s, r = pick[0], int(pick[1:])
    is_kald = pick == kald
    if laesbar(r, s, seen_by(H, 'W', played)) != ('lav' if is_kald else 'hoej'):
        return None
    valg = [f"Makker vil have {navn(s)} spillet", f"Makker vil ikke have {navn(s)}"]
    why = (f"{kort(s, r)} er lavt: lavt = kald – makker vil have {navn(s)}." if is_kald else
           f"{kort(s, r)} er højt: højt = afvisning – makker vil ikke have {navn(s)}.")
    return rec('afkast_farve', 'laes', kon, T, 'Vest', without(H['N'], played[2]), without(H['W'], played[1]),
               stik + [['Øst', pick]], tekst.replace('du kan ikke bekende – det er dit', 'makker kan ikke bekende – det er makkers'),
               f"Makker kaster {kort(s, r)}. Hvad viser kortet?", valg, [valg[0] if is_kald else valg[1]], why)

def afkast_sans(H, mode):
    c = contract(H, 'sans')
    if not c:
        return None
    T, kon = c
    Ls = [s for s in SUITS if not H['E'][s] and len(H['S'][s]) >= 4 and H['W'][s] and H['N'][s]]
    if not Ls:
        return None
    L = random.choice(Ls)
    others = [s for s in SUITS if s != L]
    U = [s for s in others if not interesting(H['E'][s])]
    if len(U) != 1 or len(H['E'][U[0]]) < 2:
        return None
    U = U[0]
    stik = void_trick(H, L)
    played = [(x[0], int(x[1:])) for p, x in stik]
    tekst = f"Kontrakten er 3NT af Syd. Spilfører spiller sin lange farve, {navn(L)}, og du kan ikke bekende – det er dit første afkast."
    keep = [s for s in others if s != U]
    if mode == 'giv':
        why = (f"{navn(U).capitalize()} er din uinteressante farve – ingen honnører ({holding(H['E'], U)}). Mod sans kaster du i den, "
               f"og beholder {navn(keep[0])} og {navn(keep[1])}, hvor du har værdier.")
        return rec('afkast_sans', 'giv', kon, T, 'Øst', without(H['N'], played[2]), H['E'], stik, tekst, "Hvilket kort kaster du?",
                   [code(s, r) for s in SUITS for r in H['E'][s]], [code(U, r) for r in H['E'][U]], why)
    r = random.choice(H['E'][U])
    valg = [f"Makker er ikke interesseret i {navn(U)}", f"Makker vil have {navn(U)} spillet"]
    why = f"Mod sans kaster makker i den farve, han ikke er interesseret i: {kort(U, r)} siger nej tak til {navn(U)}."
    return rec('afkast_sans', 'laes', kon, T, 'Vest', without(H['N'], played[2]), without(H['W'], played[1]),
               stik + [['Øst', code(U, r)]], tekst.replace('du kan ikke bekende – det er dit', 'makker kan ikke bekende – det er makkers'),
               f"Makker kaster {kort(U, r)}. Hvad viser kortet?", valg, [valg[0]], why)

# ---------- Lavinthal (forslag) ----------

def pref(W, other):
    """True, når W er den højeste af de to farver."""
    return ORDEN[W] > ORDEN[other]

def ruff_retur(H, mode):
    c = contract(H, 'farve')
    if not c:
        return None
    T, kon = c
    Xs = [s for s in SUITS if s != T and not H['W'][s] and len(H['E'][s]) >= 3]
    if not Xs or not H['W'][T]:
        return None
    X = random.choice(Xs)
    O = [s for s in SUITS if s not in (T, X)]
    R = [s for s in O if 14 in H['E'][s]]
    if len(R) != 1:
        return None
    R = R[0]
    other = [s for s in O if s != R][0]
    hi = pref(R, other)
    E = H['E'][X]
    card = hoej(E) if hi else lav(E)
    if hi and (card < 7 or card == lav(E)):
        return None
    tekst = (f"Kontrakten er {kon} af Syd. Makker har vist renonce i {navn(X)}, og du er inde. "
             f"Du spiller {navn(X)}, så makker kan stjæle.")
    hl = 'højeste' if hi else 'laveste'
    if mode == 'giv':
        why = (f"Du har {kort(R, 14)} og vil have makker til at spille {navn(R)} tilbage, så du kommer ind og kan give en stjæler mere. "
               f"{navn(R).capitalize()} er den {hl} af de to sidefarver ({navn(O[0])} og {navn(O[1])}): spil et {'højt' if hi else 'lavt'} kort, {kort(X, card)}.")
        return rec('ruff_retur', 'giv', kon, T, 'Øst', H['N'], H['E'], [], tekst, "Hvilket kort spiller du?",
                   [code(X, r) for r in E], [code(X, card)], why)
    if laesbar(card, X, seen_by(H, 'W')) != ('hoej' if hi else 'lav'):
        return None
    hiS, loS = sorted(O, key=lambda s: -ORDEN[s])
    valg = [f"Spil {navn(hiS)} tilbage", f"Spil {navn(loS)} tilbage"]
    why = (f"{kort(X, card)} er et {'højt' if hi else 'lavt'} kort: makker beder om den {hl} af de to sidefarver, {navn(R)} – "
           f"dér har makker sin indkomst til næste stjæler.")
    return rec('ruff_retur', 'laes', kon, T, 'Vest', H['N'], H['W'], [['Øst', code(X, card)]],
               f"Kontrakten er {kon} af Syd. Du har vist renonce i {navn(X)}, og makker spiller farven, så du kan stjæle.",
               f"Makker spiller {kort(X, card)}. Hvilken farve skal du spille tilbage, når du har stjålet?",
               valg, [valg[0] if hi else valg[1]], why)

def doed_udspil(H, mode):
    c = contract(H, 'farve')
    if not c:
        return None
    T, kon = c
    Xs = [s for s in SUITS if s != T and H['W'][s][:2] == [14, 13] and len(H['W'][s]) >= 3 and len(H['N'][s]) == 1 and len(H['E'][s]) >= 2]
    if not Xs:
        return None
    X = random.choice(Xs)
    O = [s for s in SUITS if s not in (T, X)]
    Wn = [s for s in O if 14 in H['E'][s] or (13 in H['E'][s] and 12 in H['E'][s])]
    if len(Wn) != 1:
        return None
    W = Wn[0]
    other = [s for s in O if s != W][0]
    if any(r >= 13 for r in H['E'][other]):
        return None
    hi = pref(W, other)
    E = H['E'][X]
    card = hoej(E) if hi else lav(E)
    if card == (lav(E) if hi else hoej(E)) or (hi and card < 7):
        return None
    d = H['N'][X][0]
    stik = [['Vest', code(X, 14)], ['Nord', code(X, d)]]
    tekst = (f"Kontrakten er {kon} af Syd. Makker spiller {kort(X, 14)} ud, og bordet har singleton {kort(X, d)}. "
             f"At fortsætte farven giver spilfører en stjæler, så kortet viser, hvilken farve makker skal skifte til.")
    hl = 'højeste' if hi else 'laveste'
    if mode == 'giv':
        why = (f"Du vil have {navn(W)} ({holding(H['E'], W)}). Den er den {hl} af de to sidefarver ({navn(O[0])} og {navn(O[1])}): "
               f"læg et {'højt' if hi else 'lavt'} kort, {kort(X, card)}.")
        return rec('doed_udspil', 'giv', kon, T, 'Øst', without(H['N'], (X, d)), H['E'], stik, tekst, "Hvilket kort lægger du?",
                   [code(X, r) for r in E], [code(X, card)], why)
    if laesbar(card, X, seen_by(H, 'W')) != ('hoej' if hi else 'lav'):
        return None
    hiS, loS = sorted(O, key=lambda s: -ORDEN[s])
    valg = [f"Skift til {navn(hiS)}", f"Skift til {navn(loS)}"]
    why = f"{kort(X, card)} er et {'højt' if hi else 'lavt'} kort: makker beder om den {hl} af de to sidefarver, {navn(W)}."
    return rec('doed_udspil', 'laes', kon, T, 'Vest', without(H['N'], (X, d)), without(H['W'], (X, 14)),
               stik + [['Øst', code(X, card)]], tekst.replace('Makker spiller', 'Du spiller'),
               f"Makker lægger {kort(X, card)}. Hvilken farve skal du skifte til?", valg, [valg[0] if hi else valg[1]], why)

def lav_afkast(H, mode):
    want = random.choice(['farve', 'sans'])
    c = contract(H, want)
    if not c:
        return None
    T, kon = c
    if T:
        L = T
        if H['E'][T] or not H['W'][T] or not H['N'][T]:
            return None
        tekst = f"Kontrakten er {kon} af Syd. Spilfører spiller trumf, og du kan ikke bekende – det er dit første afkast."
    else:
        Ls = [s for s in SUITS if not H['E'][s] and len(H['S'][s]) >= 4 and H['W'][s] and H['N'][s]]
        if not Ls:
            return None
        L = random.choice(Ls)
        tekst = f"Kontrakten er 3NT af Syd. Spilfører spiller sin lange farve, {navn(L)}, og du kan ikke bekende – det er dit første afkast."
    others = [s for s in SUITS if s != L]
    Wn = [s for s in others if 14 in H['E'][s] or (13 in H['E'][s] and 12 in H['E'][s])]
    U = [s for s in others if not interesting(H['E'][s])]
    if len(Wn) != 1 or len(U) != 2:
        return None
    W = Wn[0]
    rigtige, forklar = [], []
    for u in U:
        Eu = H['E'][u]
        if len(Eu) < 2:
            continue
        rest = [s for s in others if s != u]
        u2 = [s for s in rest if s != W][0]
        hi = pref(W, u2)
        card = hoej(Eu) if hi else lav(Eu)
        if hi and card < 7:
            continue
        rigtige.append(code(u, card))
        forklar.append((u, card, hi, u2))
    if not rigtige:
        return None
    stik = void_trick(H, L)
    played = [(x[0], int(x[1:])) for p, x in stik]
    if mode == 'giv':
        dele = [f"{kort(u, card)}: de to andre farver er {navn(W)} og {navn(u2)}, og {navn(W)} er den {'højeste' if hi else 'laveste'}"
                for u, card, hi, u2 in forklar]
        why = (f"Du vil have {navn(W)} ({holding(H['E'], W)}). Kast i en farve, du ikke vil have, med et højt kort for den højeste "
               f"af de to andre farver og et lavt for den laveste – " + '; '.join(dele) + ".")
        return rec('lav_afkast', 'giv', kon, T, 'Øst', without(H['N'], played[2]), H['E'], stik, tekst, "Hvilket kort kaster du?",
                   [code(s, r) for s in SUITS for r in H['E'][s]], rigtige, why)
    u, card, hi, u2 = random.choice(forklar)
    if laesbar(card, u, seen_by(H, 'W', played)) != ('hoej' if hi else 'lav'):
        return None
    hiS, loS = sorted([W, u2], key=lambda s: -ORDEN[s])
    valg = [f"Makker beder om {navn(hiS)}", f"Makker beder om {navn(loS)}"]
    why = (f"Makker kaster i {navn(u)}, som han ikke vil have. {kort(u, card)} er et {'højt' if hi else 'lavt'} kort: "
           f"det beder om den {'højeste' if hi else 'laveste'} af de to andre farver, {navn(W)}.")
    return rec('lav_afkast', 'laes', kon, T, 'Vest', without(H['N'], played[2]), without(H['W'], played[1]),
               stik + [['Øst', code(u, card)]], tekst.replace('du kan ikke bekende – det er dit', 'makker kan ikke bekende – det er makkers'),
               f"Makker kaster {kort(u, card)}. Hvad beder makker om?", valg, [valg[0] if hi else valg[1]], why)

# ---------- puljer ----------

SITUATIONER = {
    "markeringer": {
        "es_kald": {"titel": "Es-udspil", "regel": "Es-udspil beder om kald: lavt kort = kald (fortsæt), højt kort = afvisning. Kald med damen – mod farvekontrakt også med doubleton."},
        "k_antal": {"titel": "Konge-udspil", "regel": "Konge-udspil beder om antal (Malmø): lavt kort = lige antal, højt kort = ulige antal."},
        "ny_farve_antal": {"titel": "Spilfører spiller ny farve", "regel": "Spilfører spiller en ny farve: Malmø – lavt kort = lige antal, højt kort = ulige antal."},
        "afkast_farve": {"titel": "Første afkast mod farve", "regel": "Første afkast mod farvekontrakt: kald/afvisning – et lavt kort kalder farven, et højt kort afviser den."},
        "afkast_sans": {"titel": "Første afkast mod sans", "regel": "Første afkast mod sans: kast i den farve, du ikke er interesseret i."},
    },
    "lavinthal": {
        "ruff_retur": {"titel": "Stjæler og retur", "regel": "Kortet, du spiller til makkers stjæler, viser returfarven: højt = den højeste af de to sidefarver, lavt = den laveste."},
        "doed_udspil": {"titel": "Død udspilsfarve", "regel": "Har bordet singleton i makkers es-udspil, er dit kort farveskift: højt = den højeste af de to sidefarver, lavt = den laveste."},
        "lav_afkast": {"titel": "Lavinthal-afkast", "regel": "Kast i en farve, du ikke vil have: højt kort beder om den højeste af de to andre farver, lavt kort om den laveste. Aldrig til trumf."},
    },
}
GEN = {"es_kald": es_kald, "k_antal": k_antal, "ny_farve_antal": ny_farve_antal, "afkast_farve": afkast_farve,
       "afkast_sans": afkast_sans, "ruff_retur": ruff_retur, "doed_udspil": doed_udspil, "lav_afkast": lav_afkast}
PER = 12   # hænder pr. situation og øvelsestype

def exporter(pool):
    def export_pool(path):
        hands = []
        for sit in SITUATIONER[pool]:
            for mode in ('giv', 'laes'):
                made = tries = 0
                while made < PER and tries < 200000:
                    tries += 1
                    r = GEN[sit](deal(), mode)
                    if r:
                        hands.append(r)
                        made += 1
                if made < PER:
                    print(f"Advarsel: kun {made}/{PER} hænder til {sit} {mode}")
        return export(path, SITUATIONER[pool], hands)
    return export_pool
