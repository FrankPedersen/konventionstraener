"""
Revers – forslag til Makker 2 & mig, bilag G (diskussionsoplæg, ikke vedtaget).

Revers = ny højere farve fra åbner, meldt billigst muligt på nyt niveau: 16+ hp og rundekrav efter 1-over-1 og efter
1NT-svaret (i dag: naturlig, 5-4, 12–18 hp, ikke krav).
  aab_kl / aab_ru / aab_hj – åbner efter 1♣ – 1♠, 1♦ – 1♠ og 1♥ – 1NT: 5-4 med 16–18 → revers (2♥ / 2♥ / 2♠) ·
                            6-4 med minimum → gentag åbningsfarven (minimum kan ikke reversere)
  svar_kl / svar_ru         – svarer efter 1♣ – 1♠ – 2♥ og 1♦ – 1♠ – 2♥ (G2): pas findes ikke · 2♠ svag med 5-farve ·
                            3 i åbningsfarven svag præference (også med 2) · 2NT udgangskrav med hold i fjerde farve,
                            stærkere end 3NT · 3 i fjerde farve = fjerde farve, udgangskrav · 3♥ støtte, slow arrival
                            (stærkere) · 4♥ støtte, fast arrival (svagere) · 3♠ udgangskrav med 6-farve · 3NT for at
                            spille med hold i fjerde farve, svagere · 4 i åbningsfarven sleminvit med støtte
G2 giver 1♣ – 1♠ – 2♥ som eksempel; 1♦ – 1♠ – 2♥ følger samme skema med klør som fjerde farve.
Antagelser, som bilaget ikke giver tal for: svag = 6–8 hp, udgangskrav = 9–15 (bilaget: »ca. 8« og »ca. 9«);
den stærkere melding (2NT, 3♥, 4 i minoren) = 13+, den svagere (3NT, 4♥) = 9–12; revers = 16–18, fordi 19+ springer
(afsnit 4); støtte = 4+ kort; hold = es, K-x, D-x-x eller B-x-x-x. Ikke med: 5-4 med minimum og 6-4 med 16+ (bilaget
siger ikke hvad – 6-4 kan også være dobbeltspring i egen farve), 5-4-2-2 (kan være sansåbning eller 2NT), åbner med 3
spar efter 1♠-svaret, svag svarer med 4 hjerter eller 6 spar, 6 spar med hold i fjerde farve (3♠ eller 3NT) og
sanshænder med renonce.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, build_pool, tx
from .lebensohl import stopper

PAS = ["Modstander", "Pas"]

def q(da, en, correct, wrong, why_da, why_en):
    return {"q": tx(da, en), "correct": correct, "options": [correct, *wrong], "why": tx(why_da, why_en)}

STYRKE = tx("16+ hp og rundekrav", "16+ HCP and forcing for one round")
SAMME = tx("Nej – spar meldes på samme niveau", "No – spades are bid at the same level")
FORDELING = tx("Kun fordeling – udgangskravet er der allerede", "Only shape – the auction is already game forcing")
SANS = tx("3NT er den svagere udgangshånd, 2NT den stærkere", "3NT is the weaker game hand, 2NT the stronger")
SVAGT = tx("Svagt – ikke kravpas", "Weak – not a forcing pass")
BONUS = {
    "aab_kl": q("Hvad viser en revers i forslaget?", "What does a reverse show in the proposal?", STYRKE,
                [tx("12–18 hp, ikke krav", "12–18 HCP, non-forcing"), tx("19–21 hp, udgangskrav", "19–21 HCP, game forcing")],
                "Forslaget giver reversen en fast styrke: 16+ og rundekrav. I dag er den naturlig, 5-4, 12–18 hp og ikke krav. "
                "Med 19+ og 5-4 springer åbner i ny farve.",
                "The proposal gives the reverse a fixed strength: 16+ and forcing for one round. Today it is natural, 5-4, "
                "12–18 HCP and non-forcing. With 19+ and 5-4 opener jumps in a new suit."),
    "aab_ru": q("Er 1♣ – 1♥ – 1♠ en revers?", "Is 1♣ – 1♥ – 1♠ a reverse?", SAMME,
                [tx("Ja – spar er højere end klør", "Yes – spades rank above clubs"),
                 tx("Ja, hvis åbner har 16+ hp", "Yes, if opener has 16+ HCP")],
                "En revers meldes billigst muligt på et nyt niveau: 1♣ – 1♥ – 2♦, 1♦ – 1♠ – 2♥ og 1♥ – 1NT – 2♠. "
                "1♠ er på samme niveau som 1♥ og er derfor ikke revers.",
                "A reverse is bid at the cheapest level on a new level: 1♣ – 1♥ – 2♦, 1♦ – 1♠ – 2♥ and 1♥ – 1NT – 2♠. "
                "1♠ is on the same level as 1♥, so it is not a reverse."),
    "aab_hj": q("Hvad viser en revers efter 2 over 1?", "What does a reverse show after a 2-over-1?", FORDELING,
                [STYRKE, tx("Ikke krav", "Non-forcing")],
                "Efter 2 over 1 er der allerede udgangskrav, så reversen viser kun fordeling – følg afsnit 5 (15+ for ny farve "
                "på 3-trinnet). Efter forhåndspas er reversen ikke krav.",
                "After a 2-over-1 the auction is already game forcing, so the reverse shows only shape – follow section 5 "
                "(15+ for a new suit at the three level). After a passed hand the reverse is non-forcing."),
    "svar_kl": q("Hvad er forskellen på 2NT og 3NT efter reversen?", "What is the difference between 2NT and 3NT after the reverse?",
                 SANS, [tx("2NT er den svagere udgangshånd, 3NT den stærkere", "2NT is the weaker game hand, 3NT the stronger"),
                        tx("2NT er svag og beder om 3♣", "2NT is weak and asks for 3♣")],
                 "Begge lover hold i fjerde farve. 3NT er for at spille med en svagere udgangshånd uden slemambition; 2NT er "
                 "stærkere og lader åbner vise sin fordeling. Ingberman (2NT som svagt relæ) er kun et alternativ til drøftelse.",
                 "Both promise a stopper in the fourth suit. 3NT is to play with a weaker game hand without slam interest; 2NT "
                 "is stronger and lets opener show their shape. Ingberman (2NT as a weak relay) is only an alternative for discussion."),
    "svar_ru": q("1♣ – 1♠ – 2♥ – (3♦): hvad betyder svarers pas?", "1♣ – 1♠ – 2♥ – (3♦): what does responder's pass mean?",
                 SVAGT, [tx("Kravpas – åbner skal melde", "A forcing pass – opener must bid"),
                         tx("Ønske om at straffe", "A wish to penalise")],
                 "Efter indmelding over reversen er pas svagt (ikke kravpas), og dobling er straf.",
                 "After an overcall over the reverse, pass is weak (not a forcing pass), and double is for penalties."),
}

def is_5422(L):
    return sorted(L.values()) == [2, 2, 4, 5]

def opener(m, R):
    """Åbner har åbnet 1 i m; R er reversfarven (hjerter efter 1♣/1♦ – 1♠, spar efter 1♥ – 1NT)."""
    ms, rs = SUIT_SYM[m], SUIT_SYM[R]
    rest = [s for s in SUITS if s not in (m, R)]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[R] != 4 or any(L[s] >= 4 for s in rest) or (R == 'H' and L['S'] >= 3):
            return None
        if L[m] == 5 and 16 <= hp <= 18 and not is_5422(L):
            return f"2{rs}", tx(f"5 {SUIT_NAME[m]}, 4 {SUIT_NAME[R]} og {hp} hp: revers 2{rs} – 16+ og rundekrav, så makker ved, "
                                "at du har ekstra værdier.",
                                f"5 {SUIT_NAME_EN[m]}, 4 {SUIT_NAME_EN[R]} and {hp} HCP: reverse with 2{rs} – 16+ and forcing for "
                                "one round, so partner knows you have extra values.")
        if L[m] == 6 and 12 <= hp <= 15:
            return f"2{ms}", tx(f"6 {SUIT_NAME[m]}, 4 {SUIT_NAME[R]} og kun {hp} hp: 2{ms} – med minimum må du ikke reversere, "
                                "så du gentager din 6-farve.",
                                f"6 {SUIT_NAME_EN[m]}, 4 {SUIT_NAME_EN[R]} and only {hp} HCP: 2{ms} – with a minimum you may not "
                                "reverse, so you rebid your six-card suit.")
        return None
    return classify

def responder(m, F):
    """Forløbet 1m – 1♠ – 2♥; F er den fjerde farve."""
    ms, fs = SUIT_SYM[m], SUIT_SYM[F]
    md, me, fd, fe = SUIT_NAME[m], SUIT_NAME_EN[m], SUIT_NAME[F], SUIT_NAME_EN[F]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L['S'] < 4 or not (6 <= hp <= 15) or (L['H'] >= 4 and L['S'] < 5):
            return None
        if hp <= 8:
            if L['H'] >= 4 or L['S'] >= 6:
                return None
            if L['S'] == 5 and L[m] <= 3:
                return "2♠", tx(f"5 spar og kun {hp} hp: 2♠ – svag med 5-farve. Pas findes ikke, for reversen er rundekrav.",
                                f"5 spades and only {hp} HCP: 2♠ – weak with a five-card suit. Pass does not exist, because "
                                "the reverse is forcing for one round.")
            if L['S'] == 4 and L[m] >= 2:
                return f"3{ms}", tx(f"4 spar, {L[m]} {md} og kun {hp} hp: 3{ms} – svag præference, også med 2 {md}.",
                                    f"4 spades, {L[m]} {me} and only {hp} HCP: 3{ms} – weak preference, even with 2 {me}.")
            return None
        if L['H'] >= 4:
            if hp >= 13:
                return "3♥", tx(f"{L['H']} hjerter og {hp} hp: 3♥ – støtte, slow arrival. Stærkere end 4♥ og giver plads "
                                "til slemundersøgelse.",
                                f"{L['H']} hearts and {hp} HCP: 3♥ – support, slow arrival. Stronger than 4♥ and leaves room "
                                "to explore for slam.")
            return "4♥", tx(f"{L['H']} hjerter og {hp} hp: 4♥ – støtte, fast arrival. Den svagere støttemelding.",
                            f"{L['H']} hearts and {hp} HCP: 4♥ – support, fast arrival. The weaker raise.")
        stop = stopper(hand, F)
        if L['S'] >= 6:
            if stop:
                return None
            return "3♠", tx(f"{L['S']} spar, {hp} hp og intet hold i {fd}: 3♠ – udgangskrav med 6-farve.",
                            f"{L['S']} spades, {hp} HCP and no stopper in {fe}: 3♠ – game forcing with a six-card suit.")
        if L[m] >= 4 and hp >= 13:
            return f"4{ms}", tx(f"{L[m]} {md} og {hp} hp: 4{ms} – sleminvit med {md}støtte.",
                                f"{L[m]} {me} and {hp} HCP: 4{ms} – a slam try with {me[:-1]} support.")
        if stop:
            if min(L.values()) == 0:
                return None
            if hp >= 13:
                return "2NT", tx(f"Hold i {fd}, ingen fit og {hp} hp: 2NT – udgangskrav og stærkere end 3NT, så åbner kan "
                                 "vise sin fordeling.",
                                 f"A stopper in {fe}, no fit and {hp} HCP: 2NT – game forcing and stronger than 3NT, so opener "
                                 "can show their shape.")
            return "3NT", tx(f"Hold i {fd}, ingen fit og {hp} hp: 3NT – for at spille. Den svagere udgangshånd uden slemambition.",
                             f"A stopper in {fe}, no fit and {hp} HCP: 3NT – to play. The weaker game hand without slam interest.")
        return f"3{fs}", tx(f"Intet hold i {fd}, ingen fit og {hp} hp: 3{fs} – fjerde farve og udgangskrav (efter en revers er "
                            "fjerde farve altid udgangskrav).",
                            f"No stopper in {fe}, no fit and {hp} HCP: 3{fs} – fourth suit and game forcing (after a reverse "
                            "the fourth suit is always game forcing).")
    return classify

SVAR_CALLS = ["Pas", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "3NT", "4♣", "4♦", "4♥"]
SITUATIONS = {
    "aab_kl": {"rolle": "Åbner", "auction": [["Dig", "1♣"], PAS, ["Makker", "1♠"], PAS],
               "calls": ["1NT", "2♣", "2♦", "2♥", "2♠", "2NT", "3♣"], "bonus": BONUS["aab_kl"]},
    "aab_ru": {"rolle": "Åbner", "auction": [["Dig", "1♦"], PAS, ["Makker", "1♠"], PAS],
               "calls": ["1NT", "2♣", "2♦", "2♥", "2♠", "2NT", "3♦"], "bonus": BONUS["aab_ru"]},
    "aab_hj": {"rolle": "Åbner", "auction": [["Dig", "1♥"], PAS, ["Makker", "1NT"], PAS],
               "calls": ["Pas", "2♣", "2♦", "2♥", "2♠", "2NT", "3♥"], "bonus": BONUS["aab_hj"]},
    "svar_kl": {"rolle": "Svarer", "auction": [["Makker", "1♣"], PAS, ["Dig", "1♠"], PAS, ["Makker", "2♥"], PAS],
                "calls": SVAR_CALLS, "bonus": BONUS["svar_kl"]},
    "svar_ru": {"rolle": "Svarer", "auction": [["Makker", "1♦"], PAS, ["Dig", "1♠"], PAS, ["Makker", "2♥"], PAS],
                "calls": SVAR_CALLS, "bonus": BONUS["svar_ru"]},
}
CLASSIFIERS = {"aab_kl": opener('C', 'H'), "aab_ru": opener('D', 'H'), "aab_hj": opener('H', 'S'),
               "svar_kl": responder('C', 'D'), "svar_ru": responder('D', 'C')}

def aab_samplers(m, R):
    rest = {s: (0, 3) for s in SUITS if s not in (m, R)}
    if R == 'H':
        rest['S'] = (0, 2)
    return {f"2{SUIT_SYM[R]}": tpl((16, 18), **{**rest, m: (5, 5), R: (4, 4)}),
            f"2{SUIT_SYM[m]}": tpl((12, 15), **{**rest, m: (6, 6), R: (4, 4)})}

def svar_samplers(m, F):
    ms, fs = SUIT_SYM[m], SUIT_SYM[F]
    t = lambda hp, S, H, M, Fb: tpl(hp, S=S, H=H, **{m: M, F: Fb})
    return {"2♠": t((6, 8), (5, 5), (0, 3), (0, 3), (0, 4)), f"3{ms}": t((6, 8), (4, 4), (0, 3), (2, 5), (0, 5)),
            "4♥": t((9, 12), (5, 6), (4, 4), (0, 3), (0, 3)), "3♥": t((13, 15), (5, 6), (4, 4), (0, 3), (0, 3)),
            "3♠": t((9, 15), (6, 7), (0, 3), (0, 3), (0, 2)), f"4{ms}": t((13, 15), (4, 5), (0, 3), (4, 5), (0, 3)),
            "3NT": t((9, 12), (4, 5), (0, 3), (0, 3), (2, 5)), "2NT": t((13, 15), (4, 5), (0, 3), (0, 3), (2, 5)),
            f"3{fs}": t((9, 15), (4, 5), (0, 3), (0, 3), (0, 3))}

SAMPLERS = {"aab_kl": aab_samplers('C', 'H'), "aab_ru": aab_samplers('D', 'H'), "aab_hj": aab_samplers('H', 'S'),
            "svar_kl": svar_samplers('C', 'D'), "svar_ru": svar_samplers('D', 'C')}
PER_CALL = {"aab_kl": 15, "aab_ru": 15, "aab_hj": 15, "svar_kl": 6, "svar_ru": 6}

# Håndlavede eksempler (hånd, situation, facit) – kortgiveren skal give samme melding
EKSEMPLER = [
    ({'S': [5], 'H': [14, 13, 11, 4], 'D': [13, 8, 2], 'C': [14, 12, 9, 7, 3]}, "aab_kl", "2♥"),
    ({'S': [5], 'H': [13, 11, 4, 2], 'D': [13, 8], 'C': [14, 12, 9, 7, 3, 2]}, "aab_kl", "2♣"),
    ({'S': [14, 12, 8, 4], 'H': [14, 13, 11, 5, 2], 'D': [13, 8, 3], 'C': [7]}, "aab_hj", "2♠"),
    ({'S': [13, 12, 9, 8, 4], 'H': [7, 3], 'D': [8, 5, 4], 'C': [11, 6, 2]}, "svar_kl", "2♠"),
    ({'S': [14, 11, 8, 4], 'H': [12, 3], 'D': [13, 11, 5], 'C': [9, 8, 4, 2]}, "svar_kl", "3NT"),
    ({'S': [14, 12, 8, 4], 'H': [13, 7, 3], 'D': [13, 5], 'C': [9, 8, 6, 4]}, "svar_ru", "3♣"),
]

def export_pool(path):
    from .core import hp_of
    for hand, sit, facit in EKSEMPLER:
        hp = hp_of([r for s in SUITS for r in hand[s]])
        got = CLASSIFIERS[sit](hand, hp)
        assert got and got[0] == facit, (sit, facit, got)
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
