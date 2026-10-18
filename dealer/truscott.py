"""
Truscott 2NT – svarer efter modpartens oplysningsdobling af makkers åbning. Bygger på konventionskortet
data/kort/truscott.json (kilde: Kromann, Truscott 2 UT + redobling, 2012) og er uafhængig af makker
(SPEC-truscott-traener.md).

Situationer: 1♣/1♦/1♥/1♠ – (X) – ?. Reglerne gennemgås i rækkefølge, og den første, der passer, er svaret.
"Støtte" er antal kort i åbningsfarven.
  1  10+ hp og 3+ støtte                          → 2NT
  2  10+ hp og højst 2 støtte                     → XX
  3  0–9 hp og præcis 3 støtte                    → 2 i farven
  4  0–9 hp og præcis 4 støtte                    → 3 i farven
  5  0–9 hp og 5+ støtte                          → 4 i farven
  6  højst 2 støtte, 6+ farve og højst 6 hp       → spring i den lange farve (spærremelding)
  7  højst 2 støtte, 5+ farve og 5–8 hp           → ny farve på billigste trin (ikke krav)
  8  højst 2 støtte og 0–5 hp                     → pas
Alt andet (fx 6–9 hp uden støtte og uden 5-farve) beskriver kortet ikke; hånden kommer ikke med i puljen.
Er der flere mulige nye farver i regel 6 eller 7, vælges den længste og ved lige længde den højeste.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, build_pool, tx

# --- Grænser, som konventionskortet ikke giver tal for – ret dem her ------------
STOETTE_MIN = 3        # 2NT: "støtte" læses som 3+ kort, fordi kortet bruger 3-kortstøtte på 2-trinnet
SPRING_LAENGDE = 6     # spring i ny farve: 6+ farve
SPRING_HP_MAX = 6      # spring i ny farve: svag hånd; med 7–8 hp og 5+ farve meldes den billigt
HP_MAX = 15            # stærkere hænder genereres ikke

PER_CALL = 7
ORDER = ['C', 'D', 'H', 'S']
K = lambda c: (0, 0) if c in ("Pas", "X", "XX") else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))

def cheapest(O, s):
    """Billigste trin for farven s efter åbningen 1 i O (doblingen tager ikke plads)."""
    return 1 if ORDER.index(s) > ORDER.index(O) else 2

def new_suit(O, L, min_len):
    """Den længste nye farve med mindst min_len kort; ved lige længde den højeste."""
    cand = [s for s in SUITS if s != O and L[s] >= min_len]
    return max(cand, key=lambda s: (L[s], ORDER.index(s))) if cand else None

def classify_for(O):
    sym, navn, name = SUIT_SYM[O], SUIT_NAME[O], SUIT_NAME_EN[O]
    def classify(hand, hp):
        L = lengths_of(hand)
        n = L[O]
        if hp > HP_MAX:
            return None
        if hp >= 10 and n >= STOETTE_MIN:
            return "2NT", tx(f"{n} kort i {navn} og {hp} hp: 2NT – 10+ med støtte.",
                             f"{n} cards in {name} and {hp} HCP: 2NT – 10+ with support.")
        if hp >= 10:
            return "XX", tx(f"{hp} hp uden støtte: redobling – 10+, lægger op til straf.",
                            f"{hp} HCP without support: redouble – 10+, looking for a penalty.")
        if n == 3:
            return f"2{sym}", tx(f"3 kort i {navn} og {hp} hp: 2{sym} – 3-kortstøtte, svag efter doblingen.",
                                 f"3 cards in {name} and {hp} HCP: 2{sym} – three-card support, weak after the double.")
        if n == 4:
            return f"3{sym}", tx(f"4 kort i {navn} og {hp} hp: 3{sym} – spærrende efter doblingen.",
                                 f"4 cards in {name} and {hp} HCP: 3{sym} – preemptive after the double.")
        if n >= 5:
            return f"4{sym}", tx(f"{n} kort i {navn} og {hp} hp: 4{sym} – spærrende med 5+ støtte.",
                                 f"{n} cards in {name} and {hp} HCP: 4{sym} – preemptive with five-card support or more.")
        s = new_suit(O, L, SPRING_LAENGDE)
        if s and hp <= SPRING_HP_MAX:
            c = f"{cheapest(O, s) + 1}{SUIT_SYM[s]}"
            return c, tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: spring til {c} – spærrende uden støtte.",
                         f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: a jump to {c} – preemptive without support.")
        s = new_suit(O, L, 5)
        if s and 5 <= hp <= 8:
            c = f"{cheapest(O, s)}{SUIT_SYM[s]}"
            return c, tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: {c} – ny farve uden støtte, 5–8 hp, ikke krav.",
                         f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: {c} – a new suit without support, 5–8 HCP, non-forcing.")
        if hp <= 5:
            return "Pas", tx(f"{hp} hp uden støtte: pas.", f"{hp} HCP without support: pass.")
        return None
    return classify

C_2NT = tx("10+ hp med støtte", "10+ HCP with support")
C_XX = tx("10+ hp uden støtte", "10+ HCP without support")
C_3M = tx("4-kortstøtte, 0–9 hp, spærrende", "Four-card support, 0–9 HCP, preemptive")
BONUSER = [
    {"q": tx("Hvad viser 2NT efter modpartens oplysningsdobling?", "What does 2NT show after the opponents' takeout double?"),
     "correct": C_2NT, "options": [C_2NT, tx("Naturligt, 11–12 hp jævn", "Natural, 11–12 HCP balanced"), C_XX],
     "why": tx("Truscott: 2NT viser 10+ hp med støtte til åbningsfarven. Uden støtte redobler svarer med 10+.",
               "Truscott: 2NT shows 10+ HCP with support for opener's suit. Without support, responder redoubles with 10+.")},
    {"q": tx("Hvad viser redobling?", "What does a redouble show?"),
     "correct": C_XX, "options": [C_XX, C_2NT, tx("Ønske om at spille redoblet uanset hånd", "A wish to play redoubled whatever the hand")],
     "why": tx("Redoblingen viser 10+ hp uden støtte og lægger op til straf. Med støtte og 10+ meldes 2NT.",
               "The redouble shows 10+ HCP without support and looks for a penalty. With support and 10+, bid 2NT.")},
    {"q": tx("Hvad viser 3 i åbningsfarven efter doblingen?", "What does three of opener's suit show after the double?"),
     "correct": C_3M, "options": [C_3M, tx("Invit med 10–12 hp", "Invitational with 10–12 HCP"), tx("3-kortstøtte, 6–9 hp", "Three-card support, 6–9 HCP")],
     "why": tx("Direkte støtte er svag efter doblingen og viser antallet af trumf: 2 i farven 3 kort, 3 i farven 4 kort, 4 i farven 5+ – alle 0–9 hp.",
               "A direct raise is weak after the double and shows the number of trumps: two of the suit 3 cards, three of the suit 4 cards, "
               "four of the suit 5+ – all 0–9 HCP.")},
]

def t(hp, **b):
    return tpl(hp, **{**{s: (0, 5) for s in SUITS}, **b})

SITUATIONS, CLASSIFIERS, SAMPLERS, PER = {}, {}, {}, {}
for i, (O, key) in enumerate((('C', 'kl'), ('D', 'ru'), ('H', 'hj'), ('S', 'sp'))):
    sk, sym = f"od_{key}", SUIT_SYM[O]
    nye = [s for s in SUITS if s != O]
    calls = {"Pas", "XX", "2NT", f"2{sym}", f"3{sym}", f"4{sym}"}
    calls |= {f"{cheapest(O, s)}{SUIT_SYM[s]}" for s in nye} | {f"{cheapest(O, s) + 1}{SUIT_SYM[s]}" for s in nye}
    SITUATIONS[sk] = {"rolle": "Svarer", "auction": [["Makker", f"1{sym}"], ["Modstander", "X"]], "allowXX": True,
                      "calls": sorted(calls, key=K), "bonus": BONUSER[i % len(BONUSER)]}
    CLASSIFIERS[sk] = classify_for(O)
    SAMPLERS[sk] = {"2NT": t((10, HP_MAX), **{O: (3, 5)}), "XX": t((10, HP_MAX), **{O: (0, 2)}),
                    f"2{sym}": t((0, 9), **{O: (3, 3)}), f"3{sym}": t((0, 9), **{O: (4, 4)}), f"4{sym}": t((0, 9), **{O: (5, 6)}),
                    "Pas": t((0, 5), **{O: (0, 2), **{s: (0, 4) for s in nye}})}
    for s in nye:
        andre = {x: (0, 4) for x in nye if x != s}
        SAMPLERS[sk][f"{cheapest(O, s) + 1}{SUIT_SYM[s]}"] = t((0, SPRING_HP_MAX), **{O: (0, 2), s: (6, 7), **andre})
        SAMPLERS[sk][f"{cheapest(O, s)}{SUIT_SYM[s]}"] = either(t((5, 8), **{O: (0, 2), s: (5, 5), **andre}),
                                                              t((SPRING_HP_MAX + 1, 8), **{O: (0, 2), s: (6, 6), **andre}))
    PER[sk] = PER_CALL

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER)
