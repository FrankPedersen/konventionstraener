"""
Markeringer i modspillet – to puljer til markering.html:

  markeringer – Makker 1 & mig, systemkortet 9.1–9.2:
    es_kald         makker spiller es ud: kald (lavt) med damen – mod farvekontrakt også med doubleton – ellers afvisning (højt)
    k_antal         makker spiller konge ud: antal efter Malmø – lavt = lige, højt = ulige
    ny_farve_antal  bordet vinder udspillet og spiller en ny farve: Malmø – lavt = lige, højt = ulige
    afkast_farve    første afkast mod farvekontrakt: lavt kort kalder farven, højt kort afviser den
    afkast_sans     første afkast mod sans: kast i den farve, du ikke er interesseret i
  lavinthal – forslag, trænes før det skrives ind i systemkortet (retning som hos Makker 2 & mig):
    ruff_retur      kortet til makkers trumfning viser returfarven
    doed_udspil     bordet har singleton i makkers es-udspil: kortet viser skiftefarven
    lav_afkast      afkast i en uønsket farve viser den ønskede af de to andre farver (mod sans og farvekontrakt)
  Højt beder om den højeste af de to farver, lavt om den laveste (♠ > ♥ > ♦ > ♣).

Spillet er realistisk: situationer efter 1. stik får de stik, der går forud, spillet efter reglerne (alle bekender,
den højeste i farven vinder). Hænderne vises med alle 13 kort, og »spillet« lister de kort, der er spillet – også i
stikket nu. Markeringen regnes på de kort, der er tilbage.
  1. stik            es_kald, k_antal, doed_udspil
  2. stik            ny_farve_antal (bordet vandt udspillet), afkast_farve, afkast_sans, lav_afkast (spilfører vandt udspillet)
  3. stik            ruff_retur: makker spiller ud, og du vinder; du indkasserer esset, og makker viser renonce; nu trumfning

Hver hånd er »giv« (vælg kortet) eller »læs« (hvad betyder makkers kort?). Antagelser, hvor kortet ikke er præcist:
kald = laveste kort; afvisning og »højt« = højeste kort, du har råd til (ikke en honnør), og mindst en 7'er;
lige antal = laveste, ulige antal = højeste. Et kort er tydeligt lavt, når læseren kan se alle lavere kort i farven
(egen hånd, bordet og de spillede kort), og tydeligt højt fra 8'eren og op; kun tydelige kort bruges i »læs«.
Spilfører er Syd, bordet Nord, du Øst (giv) eller Vest (læs). Kontrakten er 4 i en major med 8+ kort fit eller 3NT uden.
"""
import random

from .core import SUITS, SUIT_SYM, SUIT_NAME, export

ORDEN = {'S': 4, 'H': 3, 'D': 2, 'C': 1}
RN = {14: 'E', 13: 'K', 12: 'D', 11: 'B'}
HP = {14: 4, 13: 3, 12: 2, 11: 1}
SEAT = {'Nord': 'N', 'Øst': 'E', 'Syd': 'S', 'Vest': 'W'}

def rn(r): return RN.get(r, str(r))
def kort(s, r): return f"{SUIT_SYM[s]}{rn(r)}"
def code(s, r): return f"{s}{r}"
def uncode(c): return c[0], int(c[1:])
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

def copy(H): return {p: {s: list(H[p][s]) for s in SUITS} for p in H}
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
def interesting(cards): return any(r >= 12 for r in cards)
def pref(W, other):
    """True, når W er den højeste af de to farver."""
    return ORDEN[W] > ORDEN[other]

# ---------- spillet: tidligere stik og stikket nu ----------

class Spil:
    """Holder den oprindelige deling, de tidligere stik og de kort, der er tilbage (R)."""
    def __init__(self, H0):
        self.H0, self.R, self.hist = H0, copy(H0), []

    def play(self, seat, s, r):
        self.R[SEAT[seat]][s].remove(r)
        return [seat, code(s, r)]

    def trick(self, lead, cards):
        """cards: [(plads, farve, rang), …] i spilleorden. Vinderen er den højeste i udspilsfarven."""
        kort_ = [self.play(p, s, r) for p, s, r in cards]
        led = cards[0][1]
        winner = max((c for c in cards if c[1] == led), key=lambda c: c[2])[0]
        self.hist.append({"kort": kort_, "vinder": winner})
        return winner

    def udspil(self, winner, avoid):
        """1. stik: Vest spiller lavt ud fra en 3+ farve; vinderen tager med sit højeste kort, de andre lægger lavt."""
        order = ['Vest', 'Nord', 'Øst', 'Syd']
        As = [s for s in SUITS if s not in avoid and all(self.R[SEAT[p]][s] for p in order) and len(self.R['W'][s]) >= 3]
        random.shuffle(As)
        for A in As:
            cards = {p: (max if p == winner else min)(self.R[SEAT[p]][A]) for p in order}
            if all(cards[winner] > cards[p] for p in order if p != winner):
                self.trick('Vest', [(p, A, cards[p]) for p in order])
                return True
        return False

    def seen(self, seat, stik=()):
        """Det, pladsen kan se: egen hånd og bordet (fra start) og alle spillede kort."""
        s = {(x, r) for x in SUITS for r in self.H0[SEAT[seat]][x]} | {(x, r) for x in SUITS for r in self.H0['N'][x]}
        s |= {uncode(c) for t in self.hist for _, c in t['kort']}
        return s | {uncode(c) for _, c in stik}

    def rec(self, sit, mode, kon, T, du, stik, tekst, spm, valg, rigtige, hvorfor):
        spillet = [c for t in self.hist for _, c in t['kort']] + [c for _, c in stik]
        return {"situation": sit, "mode": mode, "kontrakt": kon, "trumf": T, "du": du,
                "bordet": self.H0['N'], "haand": self.H0[SEAT[du]], "historik": self.hist, "spillet": spillet,
                "stik": stik, "tekst": tekst, "spm": spm, "valg": valg, "rigtige": rigtige, "hvorfor": hvorfor}

def laesbar(card, suit, seen):
    lower = [r for r in range(2, card) if (suit, r) not in seen]
    if not lower:
        return 'lav'
    if card >= 8:
        return 'hoej'
    return None

def cards_of(h): return [code(s, r) for s in SUITS for r in h[s]]
def laes_tekst(t): return t.replace('du kan ikke bekende – det er dit', 'makker kan ikke bekende – det er makkers')

# ---------- Makker 1 & mig ----------

def es_kald(H0, mode):
    c = contract(H0, random.choice(['farve', 'sans']))
    if not c:
        return None
    T, kon = c
    sp = Spil(H0)
    H = sp.R
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
            why = f"Doubleton mod farvekontrakt – du kan trumfe i tredje runde: kald med det laveste kort, {kort(X, card)}."
        else:
            why = (f"Ingen dame{' og ingen doubleton' if T else ''} ({holding(H['E'], X)}): afvis med det højeste kort, "
                   f"du har råd til, {kort(X, card)} – højt = afvisning.")
        return sp.rec('es_kald', 'giv', kon, T, 'Øst', stik, tekst, "Hvilket kort lægger du?",
                      [code(X, r) for r in E], [code(X, card)], why)
    if laesbar(card, X, sp.seen('Vest', stik)) != ('lav' if grund else 'hoej'):
        return None
    valg = ["Kald – fortsæt farven", "Afvisning – skift farve"]
    if grund:
        why = (f"{kort(X, card)} er det laveste kort, du ikke selv kan se: lavt = kald. Makker har damen"
               f"{' eller en doubleton' if T else ''} – fortsæt med {kort(X, 13)}.")
    else:
        why = f"{kort(X, card)} er et højt kort: højt = afvisning. Makker har ikke damen{' og ingen doubleton' if T else ''} – skift farve."
    return sp.rec('es_kald', 'laes', kon, T, 'Vest', stik + [['Øst', code(X, card)]], tekst.replace('Makker spiller', 'Du spiller'),
                  f"Makker lægger {kort(X, card)}. Hvad viser kortet?", valg, [valg[0] if grund else valg[1]], why)

def antal(sp, sit, X, mode, kon, T, stik, tekst, laes_tekst_):
    E = sp.R['E'][X]
    n = len(E)
    lige = n % 2 == 0
    card = lav(E) if lige else hoej(E)
    if not lige and (card < 7 or card == lav(E)):
        return None
    valg = ["Lige antal (2 eller 4)", "Ulige antal (3 eller 5)"]
    if mode == 'giv':
        why = (f"Du har {n} {navn(X)} – lige antal: læg det laveste, {kort(X, card)} (lavt = lige)." if lige else
               f"Du har {n} {navn(X)} – ulige antal: læg det højeste, {kort(X, card)} (højt = ulige).")
        return sp.rec(sit, 'giv', kon, T, 'Øst', stik, tekst, "Hvilket kort lægger du?", [code(X, r) for r in E], [code(X, card)], why)
    if laesbar(card, X, sp.seen('Vest', stik)) != ('lav' if lige else 'hoej'):
        return None
    why = (f"{kort(X, card)} er det laveste kort, du ikke selv kan se: lavt = lige antal (2 eller 4)." if lige else
           f"{kort(X, card)} er et højt kort: højt = ulige antal (3 eller 5).")
    return sp.rec(sit, 'laes', kon, T, 'Vest', stik + [['Øst', code(X, card)]], laes_tekst_,
                  f"Makker lægger {kort(X, card)}. Hvad viser kortet?", valg, [valg[0] if lige else valg[1]], why)

def k_antal(H0, mode):
    c = contract(H0, random.choice(['farve', 'sans']))
    if not c:
        return None
    T, kon = c
    sp = Spil(H0)
    H = sp.R
    cands = [s for s in SUITS if s != T and H['W'][s][:2] == [13, 12] and (T or H['W'][s][:3] == [13, 12, 11])
             and len(H['W'][s]) >= 3 and 2 <= len(H['N'][s]) <= 4 and 14 not in H['N'][s]
             and 2 <= len(H['E'][s]) <= 5 and max(H['E'][s]) <= 10]
    if not cands:
        return None
    X = random.choice(cands)
    d = min(H['N'][X])
    stik = [['Vest', code(X, 13)], ['Nord', code(X, d)]]
    tekst = f"Kontrakten er {kon} af Syd. Makker spiller {kort(X, 13)} ud, og bordet lægger {kort(X, d)}. Konge-udspil beder om antal."
    return antal(sp, 'k_antal', X, mode, kon, T, stik, tekst, tekst.replace('Makker spiller', 'Du spiller'))

def ny_farve_antal(H0, mode):
    c = contract(H0, random.choice(['farve', 'sans']))
    if not c:
        return None
    T, kon = c
    cands = [s for s in SUITS if s != T and len(H0['N'][s]) >= 2 and 2 <= len(H0['E'][s]) <= 5 and max(H0['E'][s]) <= 10]
    if not cands:
        return None
    X = random.choice(cands)
    sp = Spil(H0)
    if not sp.udspil('Nord', {T, X}):
        return None
    d = min(sp.R['N'][X])
    stik = [['Nord', code(X, d)]]
    tekst = f"Kontrakten er {kon} af Syd. Bordet vandt udspillet og spiller nu en ny farve: {kort(X, d)}."
    return antal(sp, 'ny_farve_antal', X, mode, kon, T, stik, tekst, tekst)

def void_trick(R, L):
    return [['Syd', code(L, max(R['S'][L]))], ['Vest', code(L, min(R['W'][L]))], ['Nord', code(L, min(R['N'][L]))]]

def afkast_farve(H0, mode):
    c = contract(H0, 'farve')
    if not c:
        return None
    T, kon = c
    if H0['E'][T] or not H0['W'][T] or not H0['N'][T] or not H0['S'][T]:
        return None
    sp = Spil(H0)
    if not sp.udspil('Syd', {T}):
        return None
    H = sp.R
    side = [s for s in SUITS if s != T]
    W = [s for s in side if H['E'][s][:2] == [14, 13] and len(H['E'][s]) >= 3 and lav(H['E'][s]) <= 10]
    U = [s for s in side if not interesting(H['E'][s])]
    if len(W) != 1 or len(U) != 2:
        return None
    W = W[0]
    kald = code(W, lav(H['E'][W]))
    afvis = [code(u, hoej(H['E'][u])) for u in U if len(H['E'][u]) >= 2 and 8 <= hoej(H['E'][u]) <= 10]
    stik = void_trick(H, T)
    tekst = f"Kontrakten er {kon} af Syd. Spilfører vandt udspillet og spiller trumf, og du kan ikke bekende – det er dit første afkast."
    if mode == 'giv':
        why = f"Du vil have {navn(W)} spillet ({holding(H['E'], W)}): kald med et lavt kort i farven, {kort(W, lav(H['E'][W]))} – lavt = kald."
        if afvis:
            why += " Du kan også afvise en farve, du ikke vil have, med et højt kort, fx " + ' eller '.join(kort(*uncode(x)) for x in afvis) + "."
        return sp.rec('afkast_farve', 'giv', kon, T, 'Øst', stik, tekst, "Hvilket kort kaster du?", cards_of(H['E']), [kald] + afvis, why)
    pick = random.choice([kald] + afvis)
    s, r = uncode(pick)
    is_kald = pick == kald
    if laesbar(r, s, sp.seen('Vest', stik)) != ('lav' if is_kald else 'hoej'):
        return None
    valg = [f"Makker vil have {navn(s)} spillet", f"Makker vil ikke have {navn(s)}"]
    why = (f"{kort(s, r)} er lavt: lavt = kald – makker vil have {navn(s)}." if is_kald else
           f"{kort(s, r)} er højt: højt = afvisning – makker vil ikke have {navn(s)}.")
    return sp.rec('afkast_farve', 'laes', kon, T, 'Vest', stik + [['Øst', pick]], laes_tekst(tekst),
                  f"Makker kaster {kort(s, r)}. Hvad viser kortet?", valg, [valg[0] if is_kald else valg[1]], why)

def lang_farve(H0):
    """Spilførers lange farve mod sans: Øst er renonce, Syd har 4+, Vest og bordet har kort i den."""
    Ls = [s for s in SUITS if not H0['E'][s] and len(H0['S'][s]) >= 4 and H0['W'][s] and H0['N'][s]]
    return random.choice(Ls) if Ls else None

def afkast_sans(H0, mode):
    c = contract(H0, 'sans')
    if not c:
        return None
    T, kon = c
    L = lang_farve(H0)
    if not L:
        return None
    sp = Spil(H0)
    if not sp.udspil('Syd', {L}):
        return None
    H = sp.R
    others = [s for s in SUITS if s != L]
    U = [s for s in others if not interesting(H['E'][s])]
    if len(U) != 1 or len(H['E'][U[0]]) < 2:
        return None
    U = U[0]
    stik = void_trick(H, L)
    tekst = (f"Kontrakten er 3NT af Syd. Spilfører vandt udspillet og spiller sin lange farve, {navn(L)}, "
             f"og du kan ikke bekende – det er dit første afkast.")
    keep = [s for s in others if s != U]
    if mode == 'giv':
        why = (f"{navn(U).capitalize()} er din uinteressante farve – ingen honnører ({holding(H['E'], U)}). Mod sans kaster du i den, "
               f"og beholder {navn(keep[0])} og {navn(keep[1])}, hvor du har værdier.")
        return sp.rec('afkast_sans', 'giv', kon, T, 'Øst', stik, tekst, "Hvilket kort kaster du?", cards_of(H['E']),
                      [code(U, r) for r in H['E'][U]], why)
    r = random.choice(H['E'][U])
    valg = [f"Makker er ikke interesseret i {navn(U)}", f"Makker vil have {navn(U)} spillet"]
    why = f"Mod sans kaster makker i den farve, han ikke er interesseret i: {kort(U, r)} siger nej tak til {navn(U)}."
    return sp.rec('afkast_sans', 'laes', kon, T, 'Vest', stik + [['Øst', code(U, r)]], laes_tekst(tekst),
                  f"Makker kaster {kort(U, r)}. Hvad viser kortet?", valg, [valg[0]], why)

# ---------- Lavinthal (forslag) ----------

def ruff_retur(H0, mode):
    c = contract(H0, 'farve')
    if not c:
        return None
    T, kon = c
    Xs = [s for s in SUITS if s != T and not H0['W'][s] and 14 in H0['E'][s] and len(H0['E'][s]) >= 4
          and H0['N'][s] and H0['S'][s] and H0['W'][T]]
    if not Xs:
        return None
    X = random.choice(Xs)
    sp = Spil(H0)
    # 1. stik: makker spiller ud, og du vinder
    if not sp.udspil('Øst', {T, X}):
        return None
    # 2. stik: du indkasserer esset, og makker viser renonce (kaster det laveste kort i sin længste sidefarve)
    D = [s for s in SUITS if s not in (T, X) and sp.R['W'][s]]
    if not D:
        return None
    Dw = max(D, key=lambda s: len(sp.R['W'][s]))
    sp.trick('Øst', [('Øst', X, 14), ('Syd', X, min(sp.R['S'][X])), ('Vest', Dw, min(sp.R['W'][Dw])), ('Nord', X, min(sp.R['N'][X]))])
    H = sp.R
    O = [s for s in SUITS if s not in (T, X)]
    Rs = [s for s in O if 14 in H['E'][s]]
    if len(Rs) != 1:
        return None
    R = Rs[0]
    other = [s for s in O if s != R][0]
    hi = pref(R, other)
    E = H['E'][X]
    card = hoej(E) if hi else lav(E)
    if hi and (card < 7 or card == lav(E)):
        return None
    hl = 'højeste' if hi else 'laveste'
    if mode == 'giv':
        tekst = (f"Kontrakten er {kon} af Syd. Du vandt udspillet og indkasserede {kort(X, 14)}, og makker kunne ikke bekende. "
                 f"Nu spiller du {navn(X)}, så makker kan trumfe.")
        why = (f"Du har {kort(R, 14)} og vil have makker til at spille {navn(R)} tilbage, så du kommer ind og kan give makker en trumfning mere. "
               f"{navn(R).capitalize()} er den {hl} af de to sidefarver ({navn(O[0])} og {navn(O[1])}): spil et {'højt' if hi else 'lavt'} kort, {kort(X, card)}.")
        return sp.rec('ruff_retur', 'giv', kon, T, 'Øst', [], tekst, "Hvilket kort spiller du?", [code(X, r) for r in E], [code(X, card)], why)
    stik = [['Øst', code(X, card)]]
    if laesbar(card, X, sp.seen('Vest', stik)) != ('hoej' if hi else 'lav'):
        return None
    hiS, loS = sorted(O, key=lambda s: -ORDEN[s])
    valg = [f"Spil {navn(hiS)} tilbage", f"Spil {navn(loS)} tilbage"]
    why = (f"{kort(X, card)} er et {'højt' if hi else 'lavt'} kort: makker beder om den {hl} af de to sidefarver, {navn(R)} – "
           f"dér har makker sin indkomst til næste trumfning.")
    tekst = (f"Kontrakten er {kon} af Syd. Makker vandt udspillet og indkasserede {kort(X, 14)}, og du kunne ikke bekende. "
             f"Nu spiller makker {navn(X)}, så du kan trumfe.")
    return sp.rec('ruff_retur', 'laes', kon, T, 'Vest', stik, tekst,
                  f"Makker spiller {kort(X, card)}. Hvilken farve skal du spille tilbage, når du har trumfet?",
                  valg, [valg[0] if hi else valg[1]], why)

def doed_udspil(H0, mode):
    c = contract(H0, 'farve')
    if not c:
        return None
    T, kon = c
    sp = Spil(H0)
    H = sp.R
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
             f"At fortsætte farven giver spilfører en trumfning eller et gratis afkast, så kortet viser i stedet, hvilken farve makker skal skifte til.")
    hl = 'højeste' if hi else 'laveste'
    if mode == 'giv':
        why = (f"Du vil have {navn(W)} ({holding(H['E'], W)}). Den er den {hl} af de to sidefarver ({navn(O[0])} og {navn(O[1])}): "
               f"læg et {'højt' if hi else 'lavt'} kort, {kort(X, card)}.")
        return sp.rec('doed_udspil', 'giv', kon, T, 'Øst', stik, tekst, "Hvilket kort lægger du?", [code(X, r) for r in E], [code(X, card)], why)
    if laesbar(card, X, sp.seen('Vest', stik)) != ('hoej' if hi else 'lav'):
        return None
    hiS, loS = sorted(O, key=lambda s: -ORDEN[s])
    valg = [f"Skift til {navn(hiS)}", f"Skift til {navn(loS)}"]
    why = f"{kort(X, card)} er et {'højt' if hi else 'lavt'} kort: makker beder om den {hl} af de to sidefarver, {navn(W)}."
    return sp.rec('doed_udspil', 'laes', kon, T, 'Vest', stik + [['Øst', code(X, card)]], tekst.replace('Makker spiller', 'Du spiller'),
                  f"Makker lægger {kort(X, card)}. Hvilken farve skal du skifte til?", valg, [valg[0] if hi else valg[1]], why)

def lav_afkast(H0, mode):
    c = contract(H0, random.choice(['farve', 'sans']))
    if not c:
        return None
    T, kon = c
    if T:
        L = T
        if H0['E'][T] or not H0['W'][T] or not H0['N'][T] or not H0['S'][T]:
            return None
        tekst = f"Kontrakten er {kon} af Syd. Spilfører vandt udspillet og spiller trumf, og du kan ikke bekende – det er dit første afkast."
    else:
        L = lang_farve(H0)
        if not L:
            return None
        tekst = (f"Kontrakten er 3NT af Syd. Spilfører vandt udspillet og spiller sin lange farve, {navn(L)}, "
                 f"og du kan ikke bekende – det er dit første afkast.")
    sp = Spil(H0)
    if not sp.udspil('Syd', {L}):
        return None
    H = sp.R
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
        u2 = [s for s in others if s not in (u, W)][0]
        hi = pref(W, u2)
        card = hoej(Eu) if hi else lav(Eu)
        if hi and card < 7:
            continue
        rigtige.append(code(u, card))
        forklar.append((u, card, hi, u2))
    if not rigtige:
        return None
    stik = void_trick(H, L)
    if mode == 'giv':
        dele = [f"{kort(u, card)}: de to andre farver er {navn(W)} og {navn(u2)}, og {navn(W)} er den {'højeste' if hi else 'laveste'}"
                for u, card, hi, u2 in forklar]
        why = (f"Du vil have {navn(W)} ({holding(H['E'], W)}). Kast i en uønsket farve – et højt kort beder om den højeste "
               f"af de to andre farver, et lavt kort om den laveste: " + '; '.join(dele) + ".")
        return sp.rec('lav_afkast', 'giv', kon, T, 'Øst', stik, tekst, "Hvilket kort kaster du?", cards_of(H['E']), rigtige, why)
    u, card, hi, u2 = random.choice(forklar)
    if laesbar(card, u, sp.seen('Vest', stik)) != ('hoej' if hi else 'lav'):
        return None
    hiS, loS = sorted([W, u2], key=lambda s: -ORDEN[s])
    valg = [f"Makker beder om {navn(hiS)}", f"Makker beder om {navn(loS)}"]
    why = (f"Makker kaster i {navn(u)}, en uønsket farve. {kort(u, card)} er et {'højt' if hi else 'lavt'} kort: "
           f"det beder om den {'højeste' if hi else 'laveste'} af de to andre farver, {navn(W)}.")
    return sp.rec('lav_afkast', 'laes', kon, T, 'Vest', stik + [['Øst', code(u, card)]], laes_tekst(tekst),
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
        "ruff_retur": {"titel": "Trumfning og retur", "regel": "Kortet, du spiller til makkers trumfning, viser returfarven: højt = den højeste af de to sidefarver, lavt = den laveste."},
        "doed_udspil": {"titel": "Død udspilsfarve", "regel": "Har bordet singleton i makkers es-udspil, er dit kort ikke kald eller afvisning, men farvevalg: højt = den højeste af de to sidefarver, lavt = den laveste."},
        "lav_afkast": {"titel": "Lavinthal-afkast", "regel": "Første afkast i en uønsket farve: højt kort beder om den højeste af de to andre farver, lavt kort om den laveste. Aldrig til trumf."},
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
                while made < PER and tries < 300000:
                    tries += 1
                    r = GEN[sit](deal(), mode)
                    if r:
                        hands.append(r)
                        made += 1
                if made < PER:
                    print(f"Advarsel: kun {made}/{PER} hænder til {sit} {mode}")
        return export(path, SITUATIONER[pool], hands)
    return export_pool
