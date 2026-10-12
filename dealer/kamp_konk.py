"""
Konkurrencemeldinger – Kampen om kontrakten §2, §4, §6, §7, §8, §9 og §11.

  gif   §7   – (1♦/1♥/1♠) pas (pas) ?: jævn: pas under 11 (aftale) · 1NT 11–14 · X 15–18 · 2NT 19–21.
               Ujævn: X 9+ uden femfarve og med højst to i deres farve · X 15+ (derefter ny farve) ·
               farve 7–14 med femfarve (billigst) · spring på 2-trinnet = konstruktivt, 11–14 med seksfarve
  2020  §4/§2/§11 – (1♥/1♦) pas (2♥/2♦) pas (pas) ?: sælg ikke ud – højst to i deres farve: femfarve meldes,
               ellers X · tre eller flere i deres farve: pas.
               1♠ (2♥) 2♠ (3♥) ?: åbner med minimum melder efter trumfreglen: 9 trumf 3♠, 8 trumf pas.
               Klub/Turnering (zonejustering + små offermeldinger, aftale): uden for zonen også 3♠ på 8 trumf
  dobl  §6   – (1♦) ? anden hånd: X kræver 12–17 · (1♠) pas (4♠) ?: X oplysende med kort spar og 12+ ·
               (1♣) 1♥ (1♠) ?: én umeldt farve – X = ruder og Hx i hjerter · 2♦ = egen farve uden medløb · 2♥ støtte
  ut8   §8   – makker 1♥ (1NT) ?: X 9+ (stærkest, straf) · 2♥ 3 trumf 6–8 · 3♥ 4+ trumf og korthed (destruktiv) ·
               ny farve svag seksfarve · 2NT 5-5 i minor · pas
  ut9   §9   – makker 1NT (2♥) ?: 2♠ femfarve, ønske om at spille · 3♠ femfarve 10+, krav · 3♣/3♦ seksfarve, svag ·
               2NT invit 8–9 med hold · 3NT 10+ med hold · 3♥ 10+ uden hold (søger hold) · X oplysende, 4 spar 6–9.
               Turnering (Lebensohl): svag minor via 2NT · direkte 3♣/3♦ = krav 10+ · 2NT er ikke invit.
               Makker 1NT (X) ?: XX 7+ · 0–6 med femfarve: flygt i femfarven · ellers pas
Antagelser: hold = es, K-x, D-x-x eller B-x-x-x; hænder, hvor dokumentet ikke giver én melding, er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, SUIT_NAME_EN, lengths_of, tpl, either, tx
from .kamp import build_pool as kbuild, we_vul
from .lebensohl import stopper

ORDER = ['C', 'D', 'H', 'S']
PAS = ["Modstander", "Pas"]
K = lambda c: (0, 0) if c in ("Pas", "X", "XX") else (int(c[0]), ['♣', '♦', '♥', '♠', 'NT'].index(c[1:]))
AFT = {"aftale": True}

def balanced(L):
    return sorted(L.values()) in ([3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5])

def cheapest(after, s):
    for lv in (1, 2, 3, 4):
        if (lv, ORDER.index(s)) > K(after):
            return f"{lv}{SUIT_SYM[s]}"

def sort_calls(calls):
    return sorted(set(calls), key=K)

# ---------------- GIF ----------------
C_GIF = tx("3–4 hp af makker – men ikke på jævne hænder", "3–4 HCP from partner – but not with balanced hands")
B_GIF = {"q": tx("Hvad låner du ved genåbning i fjerde hånd?", "What do you borrow when balancing in fourth seat?"),
         "correct": C_GIF,
         "options": [C_GIF, tx("Intet – samme krav som direkte", "Nothing – the same requirements as in direct seat"),
                     tx("3–4 hp, også på jævne hænder", "3–4 HCP, also with balanced hands")],
         "why": tx("Lånet kompenserer for fordeling, ikke for point. Jævne hænder melder efter rene hp: pas under 11, 1NT 11–14, X 15–18, 2NT 19–21.",
                   "The loan compensates for shape, not for points. Balanced hands bid on plain HCP: pass below 11, 1NT 11–14, X 15–18, 2NT 19–21.")}

def gif(O):
    def classify(hand, hp, zone):
        L = lengths_of(hand)
        if hp > 21:
            return None
        if balanced(L) and max(L[s] for s in ('H', 'S') if s != O) <= 4:
            if hp < 11:
                if hp < 8:
                    return "Pas", tx(f"Jævn hånd med {hp} hp: pas – for lidt til at genåbne.", f"Balanced hand with {hp} HCP: pass – too little to balance.")
                return "Pas", tx(f"Jævn hånd med {hp} hp: pas – ved GIF låner du ikke på jævne hænder (under 11).",
                                 f"Balanced hand with {hp} HCP: pass – when balancing you do not borrow with balanced hands (below 11)."), AFT
            if hp <= 14:
                return "1NT", tx(f"Jævn hånd med {hp} hp: 1NT (11–14).", f"Balanced hand with {hp} HCP: 1NT (11–14).")
            if hp <= 18:
                return "X", tx(f"Jævn hånd med {hp} hp: dobling – og sans billigst bagefter (15–18).",
                               f"Balanced hand with {hp} HCP: double – and the cheapest notrump afterwards (15–18).")
            return "2NT", tx(f"Jævn hånd med {hp} hp: 2NT (19–21).", f"Balanced hand with {hp} HCP: 2NT (19–21).")
        if balanced(L):
            return None
        five = [s for s in ORDER if s != O and L[s] >= 5]
        if hp >= 15:
            return ("X", tx(f"{hp} hp: dobling – med ny farve bagefter viser du 15+.",
                            f"{hp} HCP: double – a new suit afterwards shows 15+.")) if hp <= 18 else None
        if five:
            s = max(five, key=lambda x: (L[x], ORDER.index(x)))
            c = cheapest(f"1{SUIT_SYM[O]}", s)
            if L[s] >= 6 and 11 <= hp <= 14:
                j = f"{int(c[0]) + 1}{c[1:]}"
                if j[0] == '2':
                    return j, tx(f"Seksfarve og {hp} hp: spring til {j} – efter to passer er spring konstruktive (11–14).",
                                 f"A six-card suit and {hp} HCP: jump to {j} – after two passes, jumps are constructive (11–14).")
                return None
            if 7 <= hp <= 14:
                return c, tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: {c} – farvemelding i fjerde hånd (ca. 7–14).",
                             f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: {c} – a suit bid in fourth seat (about 7–14).")
            return ("Pas", tx(f"Kun {hp} hp: pas.", f"Only {hp} HCP: pass.")) if hp < 7 else None
        if L[O] <= 2 and hp >= 9:
            return "X", tx(f"{hp} hp og kort i {SUIT_NAME[O]}: dobling – du låner 3–4 hp af makker (nedre grænse ca. 9).",
                           f"{hp} HCP and short in {SUIT_NAME_EN[O]}: double – you borrow 3–4 HCP from partner (lower limit about 9).")
        if hp < 9:
            return "Pas", tx(f"{hp} hp uden femfarve: pas.", f"{hp} HCP without a five-card suit: pass.")
        return None
    return classify

# ---------------- 20-20 ----------------
C_2020 = tx("Lige så mange som jeres fælles trumf", "As many as your combined trumps")
B_2020 = {"q": tx("Hvor mange stik forpligter I jer til i en delkontraktkamp?", "How many tricks do you contract for in a part-score battle?"),
          "correct": C_2020,
          "options": [C_2020, tx("Det afhænger af honnørpointene", "It depends on the high-card points"), tx("Altid kun to-trinnet", "Always only the two level")],
          "why": tx("Trumfreglen: 8 trumf – 2-trinnet, 9 – 3-trinnet, 10 – 4-trinnet. Og sælg aldrig ud under 2♠, når modparten har fundet tilpasning.",
                    "The trump rule: 8 trumps – the two level, 9 – the three level, 10 – the four level. And never sell out below 2♠ "
                    "when the opponents have found a fit.")}

def balance(O):
    osym = SUIT_SYM[O]
    def classify(hand, hp, zone):
        L = lengths_of(hand)
        if hp > 11:
            return None
        if L[O] >= 3:
            return ("Pas", tx(f"{L[O]} {SUIT_NAME[O]}: makker er kort, og du har ingen fordeling at kæmpe med – pas.",
                              f"{L[O]} {SUIT_NAME_EN[O]}: partner is short, and you have no shape to compete with – pass.")) if balanced(L) else None
        five = [s for s in ORDER if s != O and L[s] >= 5]
        if len(five) == 1:
            s = five[0]
            c = cheapest(f"2{osym}", s)
            return c, tx(f"{L[s]} {SUIT_NAME[s]} og kort i {SUIT_NAME[O]}: {c} – sælg ikke ud på 2-trinnet, de har fundet tilpasning.",
                         f"{L[s]} {SUIT_NAME_EN[s]} and short in {SUIT_NAME_EN[O]}: {c} – do not sell out at the two level, they have found a fit.")
        if not five and all(L[s] >= 3 for s in ORDER if s != O):
            return "X", tx(f"Kort i {SUIT_NAME[O]} og plads til alle de andre: dobling – tag makker med på råd. I har omtrent halvdelen af pointene.",
                           f"Short in {SUIT_NAME_EN[O]} with room for all the others: double – consult partner. You have about half the points.")
        return None
    return classify

def compete(hand, hp, zone):
    L = lengths_of(hand)
    if not (12 <= hp <= 14) or L['S'] not in (5, 6) or L['H'] > 2 or max(L['C'], L['D']) >= 5:
        return None
    t = L['S'] + 3
    vul = we_vul(zone)
    zw = "I er i zonen" if vul else "I er uden for zonen"
    zw_en = "you are vulnerable" if vul else "you are not vulnerable"
    grund = (("3♠", tx(f"{t} trumf: trumfreglen siger 3-trinnet – 3♠.", f"{t} trumps: the trump rule says the three level – 3♠.")) if t == 9
             else ("Pas", tx("8 trumf: trumfreglen siger 2-trinnet – pas.", "8 trumps: the trump rule says the two level – pass.")))
    if t == 9:
        klub = ("3♠", tx(f"9 trumf: 3♠ – {zw}, og ni trumf bærer 3-trinnet.", f"9 trumps: 3♠ – {zw_en}, and nine trumps carry the three level."))
    elif vul:
        klub = ("Pas", tx("8 trumf og I er i zonen: pas – i zonen kræves én trumf mere for det sidste trin.",
                          "8 trumps and you are vulnerable: pass – vulnerable, you need one more trump for the last level."))
    else:
        klub = ("3♠", tx("8 trumf, men uden for zonen og mod deres tilpasning på 2-trinnet: 3♠ – en lille offermelding (−50 slår −140).",
                         "8 trumps, but not vulnerable and against their fit at the two level: 3♠ – a small sacrifice (−50 beats −140)."))
    extra = {"aftale": True} if klub[0] != grund[0] else {}
    if klub[0] != grund[0]:
        extra["grund"] = {"correct": grund[0], "why": grund[1]}
    return klub[0], klub[1], extra

# ---------------- doblinger ----------------
C_DOB = tx("Oplysende – tag makker med på råd", "Takeout – consult partner")
B_DOB = {"q": tx("Hvad betyder en dobling, når modparten har meldt og støttet hinanden?", "What does a double mean when the opponents have bid and raised?"),
         "correct": C_DOB,
         "options": [C_DOB, tx("Straf", "Penalty"), tx("Viser en stærk jævn hånd", "Shows a strong balanced hand")],
         "why": tx("Så snart modparten har fundet tilpasning, er alle doblinger i de tidlige runder oplysende – også højt oppe. Grænsen går over 4 i major.",
                   "As soon as the opponents have found a fit, all doubles in the early rounds are for takeout – even at a high level. "
                   "The limit is above four of a major.")}

def od_direct(hand, hp, zone):
    L = lengths_of(hand)
    if L['D'] > 2 or min(L['C'], L['H'], L['S']) < 3 or max(L.values()) >= 5:
        return None
    if 12 <= hp <= 17:
        return "X", tx(f"{hp} hp og kort i ruder: oplysningsdobling – i anden hånd skal du selv have værdierne (12–17).",
                       f"{hp} HCP and short in diamonds: takeout double – in second seat you need the values yourself (12–17).")
    if 8 <= hp <= 11:
        return "Pas", tx(f"Kun {hp} hp: pas – direkte i anden hånd kræver dobling 12–17. (I fjerde hånd efter to passer kunne du låne.)",
                         f"Only {hp} HCP: pass – a direct double in second seat needs 12–17. (In fourth seat after two passes you could borrow.)")
    return None

def od_high(hand, hp, zone):
    L = lengths_of(hand)
    if max(L.values()) >= 6 or hp > 17:
        return None
    if L['S'] <= 1 and min(L['C'], L['D'], L['H']) >= 3 and hp >= 12:
        return "X", tx(f"Kort i spar og plads til de tre andre farver ({hp} hp): dobling er oplysende – de har meldt og støttet.",
                       f"Short in spades with room for the other three suits ({hp} HCP): the double is for takeout – they have bid and raised.")
    if hp <= 9:
        return "Pas", tx(f"{hp} hp: pas.", f"{hp} HCP: pass.")
    return None

def one_unbid(hand, hp, zone):
    L = lengths_of(hand)
    if not (6 <= hp <= 11) or L['C'] >= 4 or L['S'] >= 4:
        return None
    h = hand['H']
    if L['H'] >= 3 and hp <= 9:
        return "2♥", tx(f"{L['H']} hjerter og {hp} hp: 2♥ – støt med støtte.", f"{L['H']} hearts and {hp} HCP: 2♥ – raise with support.")
    if L['D'] >= 4 and L['H'] == 2 and h[0] >= 11:
        return "X", tx(f"Ruder og H-x i hjerter: dobling viser den sidste farve med lidt medløb i makkers farve.",
                       f"Diamonds and H-x in hearts: the double shows the last suit with some tolerance for partner's suit.")
    if L['D'] >= 6 and L['H'] <= 1:
        return "2♦", tx(f"{L['D']} ruder uden medløb i hjerter: 2♦ – meld din egen farve naturligt.",
                        f"{L['D']} diamonds without tolerance for hearts: 2♦ – bid your own suit naturally.")
    return None

# ---------------- §8 fjenden melder 1NT ind ----------------
C_UT8 = tx("Dobling – straf, 9+", "Double – penalty, 9+")
B_UT8 = {"q": tx("Hvad er den stærkeste melding, når fjenden melder 1NT ind over makkers åbning?",
                 "What is the strongest bid when the opponents overcall 1NT over partner's opening?"),
         "correct": C_UT8,
         "options": [C_UT8, tx("Ny farve – krav", "A new suit – forcing"), tx("2NT – invit", "2NT – invitational")],
         "why": tx("Dobling er straf og den stærkeste melding (9+). Ny farve er den svageste – 2 over 1 gælder ikke her.",
                   "Double is for penalty and the strongest bid (9+). A new suit is the weakest – 2 over 1 does not apply here.")}

def ut8(hand, hp, zone):
    L = lengths_of(hand)
    if hp > 15:
        return None
    if hp >= 9:
        return "X", tx(f"{hp} hp: dobling – straf og den stærkeste melding (9+).", f"{hp} HCP: double – penalty and the strongest bid (9+).")
    short = min(L[s] for s in SUITS if s != 'H')
    if L['H'] >= 4 and short <= 1 and 4 <= hp <= 8:
        return "3♥", tx(f"{L['H']} trumf og korthed: 3♥ – springstøtten er destruktiv.", f"{L['H']} trumps and shortness: 3♥ – the jump raise is preemptive.")
    if L['H'] >= 3 and 6 <= hp <= 8:
        return ("2♥", tx(f"{L['H']} hjerter og {hp} hp: 2♥ – naturlig støtte.",
                         f"{L['H']} hearts and {hp} HCP: 2♥ – natural support.")) if not (L['H'] >= 4 and short <= 1) else None
    if L['C'] >= 5 and L['D'] >= 5 and L['H'] <= 1 and hp <= 8:
        return "2NT", tx(f"{L['C']}-{L['D']} i minorerne: 2NT – spillestærk, men honnørsvag.",
                         f"{L['C']}-{L['D']} in the minors: 2NT – strong in playing tricks, but weak in honours.")
    six = [s for s in ('C', 'D', 'S') if L[s] >= 6]
    if six and L['H'] <= 2 and 4 <= hp <= 8:
        s = six[0]
        return f"2{SUIT_SYM[s]}", tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: 2{SUIT_SYM[s]} – svag og ikke krav (ny farve er den svageste melding her).",
                                     f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: 2{SUIT_SYM[s]} – weak and non-forcing (a new suit is the weakest bid here).")
    if L['H'] <= 2 and max(L.values()) <= 4 and hp <= 8:
        return "Pas", tx(f"{hp} hp uden støtte og uden lang farve: pas.", f"{hp} HCP without support and without a long suit: pass.")
    return None

# ---------------- §9 de melder ind over vores 1NT ----------------
C_UT9 = tx("Nej – de bortfalder", "No – they are off")
B_UT9 = {"q": tx("Gælder Stayman og overføringer, når modparten melder ind over makkers 1NT?",
                 "Do Stayman and transfers apply when the opponents overcall partner's 1NT?"),
         "correct": C_UT9,
         "options": [C_UT9, tx("Ja, uændret", "Yes, unchanged"), tx("Kun Stayman", "Only Stayman")],
         "why": tx("Stayman og transfers bortfalder efter en indmelding. Ny farve billigst er ønske om at spille, spring er krav, og overmelding i fjendens farve søger hold.",
                   "Stayman and transfers are off after an overcall. A new suit at the cheapest level is to play, a jump is forcing, "
                   "and a cue-bid in the opponents' suit asks for a stopper.")}

def ut9(hand, hp, zone):
    L = lengths_of(hand)
    if hp > 15 or L['H'] >= 4:
        return None
    if L['S'] >= 5:
        if 5 <= hp <= 9:
            return "2♠", tx(f"{L['S']} spar og {hp} hp: 2♠ – ønske om at spille.", f"{L['S']} spades and {hp} HCP: 2♠ – to play.")
        if hp >= 10:
            return "3♠", tx(f"{L['S']} spar og {hp} hp: 3♠ – spring er krav, mindst femfarve.",
                            f"{L['S']} spades and {hp} HCP: 3♠ – the jump is forcing, at least a five-card suit.")
        return None
    six = [s for s in ('C', 'D') if L[s] >= 6]
    if six:
        s = six[0]
        c = f"3{SUIT_SYM[s]}"
        if 5 <= hp <= 9:
            return (c, tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: {c} – ønske om at spille.", f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: {c} – to play."),
                    {"turnering": {"correct": "2NT", "why": tx(f"Svag hånd med {L[s]} {SUIT_NAME[s]}: 2NT – Lebensohl-relæ til 3♣, så du stopper i {c}.",
                                                               f"Weak hand with {L[s]} {SUIT_NAME_EN[s]}: 2NT – the Lebensohl relay to 3♣, so you stop in {c}.")}})
        if hp >= 10:
            return (c, tx(f"{L[s]} {SUIT_NAME[s]} og {hp} hp: {c} direkte – i Lebensohl er den direkte 3-melding krav.",
                          f"{L[s]} {SUIT_NAME_EN[s]} and {hp} HCP: {c} directly – in Lebensohl the direct three-level bid is forcing."),
                    {"only": ["turnering"]})
        return None
    if L['S'] == 4 and L['H'] <= 2 and 6 <= hp <= 9 and max(L.values()) <= 4:
        return "X", tx(f"4 spar og kort i hjerter ({hp} hp): dobling – oplysende.", f"4 spades and short in hearts ({hp} HCP): double – takeout.")
    if balanced(L) and L['S'] <= 3:
        st = stopper(hand, 'H')
        if 8 <= hp <= 9 and st:
            return "2NT", tx(f"{hp} hp og hold i hjerter: 2NT – invit.", f"{hp} HCP and a heart stopper: 2NT – invitational."), {"only": ["grund", "klub"]}
        if hp >= 10:
            if st:
                return "3NT", tx(f"{hp} hp og hold i hjerter: 3NT.", f"{hp} HCP and a heart stopper: 3NT.")
            return "3♥", tx(f"{hp} hp uden hold i hjerter: 3♥ – overmelding i fjendens farve, udgangskrav og søger hold.",
                            f"{hp} HCP without a heart stopper: 3♥ – a cue-bid in the opponents' suit, game forcing and asking for a stopper.")
    if hp <= 5 and max(L.values()) <= 4:
        return "Pas", tx(f"{hp} hp: pas.", f"{hp} HCP: pass.")
    return None

def ut9x(hand, hp, zone):
    L = lengths_of(hand)
    if hp > 12:
        return None
    if hp >= 7:
        return "XX", tx(f"{hp} hp: redobling – vi har flest point, og flygter de, kan vi strafdoble.",
                        f"{hp} HCP: redouble – we have the majority of the points, and if they run we can double for penalty.")
    five = [s for s in ORDER if L[s] >= 5]
    if len(five) == 1:
        s = five[0]
        return f"2{SUIT_SYM[s]}", tx(f"{hp} hp og {L[s]} {SUIT_NAME[s]}: 2{SUIT_SYM[s]} – flygt altid i femfarven.",
                                     f"{hp} HCP and {L[s]} {SUIT_NAME_EN[s]}: 2{SUIT_SYM[s]} – always run to the five-card suit.")
    if not five and max(L.values()) <= 4:
        return "Pas", tx(f"{hp} hp uden femfarve: pas.", f"{hp} HCP without a five-card suit: pass.")
    return None

t = lambda hp, **b: tpl(hp, **{**{s: (1, 4) for s in SUITS}, **b})

def build(kind):
    SIT, CL, SAM, PER = {}, {}, {}, {}
    if kind == "gif":
        for O, key in (('D', 'ru'), ('H', 'hj'), ('S', 'sp')):
            osym = SUIT_SYM[O]
            sk = f"gif_{key}"
            others = [s for s in ORDER if s != O]
            calls = ["Pas", "X", "1NT", "2NT"] + [cheapest(f"1{osym}", s) for s in others]
            calls += [f"{int(cheapest(f'1{osym}', s)[0]) + 1}{SUIT_SYM[s]}" for s in others if cheapest(f"1{osym}", s)[0] == '1']
            SIT[sk] = {"rolle": "Genåbner", "auction": [["Modstander", f"1{osym}"], ["Makker", "Pas"], ["Modstander", "Pas"]],
                       "allowX": True, "calls": sort_calls(calls), "bonus": B_GIF}
            CL[sk] = gif(O)
            bal = lambda hp, O=O: tpl(hp, **{**{s: (3, 4) for s in SUITS}, O: (2, 3)})
            SAM[sk] = {"Pas": either(bal((7, 10)), t((3, 6))), "1NT": bal((11, 14)), "X": either(bal((15, 18)), t((9, 14), **{O: (0, 1)})),
                       "2NT": bal((19, 21))}
            for s in others:
                c = cheapest(f"1{osym}", s)
                SAM[sk][c] = t((7, 13), **{s: (5, 5), O: (1, 3)})
                if c[0] == '1':
                    SAM[sk][f"2{SUIT_SYM[s]}"] = t((11, 14), **{s: (6, 6), O: (1, 3)})
            PER[sk] = 5
    if kind == "2020":
        for O, key in (('H', 'hj'), ('D', 'ru')):
            osym = SUIT_SYM[O]
            sk = f"bal_{key}"
            others = [s for s in ORDER if s != O]
            calls = ["Pas", "X"] + [cheapest(f"2{osym}", s) for s in others] + ["2NT"]
            SIT[sk] = {"rolle": "Fjerde hånd", "auction": [["Modstander", f"1{osym}"], ["Dig", "Pas"], ["Modstander", f"2{osym}"], ["Makker", "Pas"], PAS],
                       "allowX": True, "calls": sort_calls(calls), "bonus": B_2020}
            CL[sk] = balance(O)
            SAM[sk] = {"Pas": t((4, 10), **{O: (3, 4), **{s: (3, 4) for s in others}}),
                       "X": t((5, 11), **{O: (0, 2), **{s: (3, 4) for s in others}})}
            for s in others:
                SAM[sk][cheapest(f"2{osym}", s)] = t((5, 11), **{O: (0, 2), s: (5, 6)})
            PER[sk] = 9
        SIT["kamp_sp"] = {"rolle": "Åbner", "auction": [["Dig", "1♠"], ["Modstander", "2♥"], ["Makker", "2♠"], ["Modstander", "3♥"]],
                          "allowX": True, "calls": ["Pas", "X", "3♠", "4♠", "3NT"], "bonus": B_2020}
        CL["kamp_sp"] = compete
        SAM["kamp_sp"] = {"Pas": t((12, 14), S=(5, 5), H=(0, 2), C=(1, 4), D=(1, 4)), "3♠": t((12, 14), S=(5, 6), H=(0, 2), C=(1, 4), D=(1, 4))}
        PER["kamp_sp"] = 22
    if kind == "dobl":
        SIT["direkte"] = {"rolle": "Anden hånd", "auction": [["Modstander", "1♦"]], "allowX": True,
                          "calls": ["Pas", "X", "1♥", "1♠", "1NT", "2♣"], "bonus": B_DOB}
        CL["direkte"] = od_direct
        SAM["direkte"] = {"X": t((12, 17), D=(0, 2), C=(3, 4), H=(3, 4), S=(3, 4)), "Pas": t((8, 11), D=(0, 2), C=(3, 4), H=(3, 4), S=(3, 4))}
        PER["direkte"] = 16
        SIT["hoejt"] = {"rolle": "Fjerde hånd", "auction": [["Modstander", "1♠"], ["Makker", "Pas"], ["Modstander", "4♠"]], "allowX": True,
                        "calls": ["Pas", "X", "4NT", "5♣", "5♦", "5♥"], "bonus": B_DOB}
        CL["hoejt"] = od_high
        SAM["hoejt"] = {"X": t((12, 17), S=(0, 1), C=(3, 5), D=(3, 5), H=(3, 5)), "Pas": t((3, 9), S=(1, 4))}
        PER["hoejt"] = 16
        SIT["umeldt"] = {"rolle": "Fortsætter", "auction": [["Modstander", "1♣"], ["Makker", "1♥"], ["Modstander", "1♠"]], "allowX": True,
                         "calls": ["Pas", "X", "1NT", "2♣", "2♦", "2♥"], "bonus": B_DOB}
        CL["umeldt"] = one_unbid
        SAM["umeldt"] = {"2♥": t((6, 9), H=(3, 4), C=(1, 3), S=(1, 3)), "X": t((6, 11), D=(4, 5), H=(2, 2), C=(1, 3), S=(1, 3)),
                         "2♦": t((6, 11), D=(6, 7), H=(0, 1), C=(1, 3), S=(1, 3))}
        PER["umeldt"] = 12
    if kind == "ut8":
        SIT["ut8"] = {"rolle": "Svarer", "auction": [["Makker", "1♥"], ["Modstander", "1NT"]], "allowX": True,
                      "calls": ["Pas", "X", "2♣", "2♦", "2♥", "2♠", "2NT", "3♥"], "bonus": B_UT8}
        CL["ut8"] = ut8
        SAM["ut8"] = {"X": t((9, 14)), "3♥": t((4, 8), H=(4, 5), S=(0, 1)), "2♥": t((6, 8), H=(3, 3), **{s: (2, 4) for s in ('C', 'D', 'S')}),
                      "2NT": t((4, 8), C=(5, 6), D=(5, 6), H=(0, 1), S=(0, 2)), "2♣": t((4, 8), C=(6, 7), H=(0, 2)),
                      "2♦": t((4, 8), D=(6, 7), H=(0, 2)), "2♠": t((4, 8), S=(6, 7), H=(0, 2)),
                      "Pas": t((0, 8), H=(0, 2), **{s: (3, 4) for s in ('C', 'D', 'S')})}
        PER["ut8"] = 13
    if kind == "ut9":
        SIT["ut9"] = {"rolle": "Svarer", "auction": [["Makker", "1NT"], ["Modstander", "2♥"]], "allowX": True,
                      "calls": ["Pas", "X", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "3NT"], "bonus": B_UT9}
        CL["ut9"] = ut9
        SAM["ut9"] = {"2♠": t((5, 9), S=(5, 6), H=(0, 3)), "3♠": t((10, 14), S=(5, 6), H=(0, 3)),
                      "3♣": either(t((5, 9), C=(6, 7), H=(0, 3), S=(0, 3)), t((10, 13), C=(6, 7), H=(0, 3), S=(0, 3))),
                      "3♦": either(t((5, 9), D=(6, 7), H=(0, 3), S=(0, 3)), t((10, 13), D=(6, 7), H=(0, 3), S=(0, 3))),
                      "X": t((6, 9), S=(4, 4), H=(0, 2)), "2NT": t((8, 9), H=(3, 3), S=(2, 3), C=(2, 4), D=(2, 4)),
                      "3NT": t((10, 14), H=(3, 3), S=(2, 3), C=(2, 4), D=(2, 4)), "3♥": t((10, 14), H=(2, 3), S=(2, 3), C=(2, 4), D=(2, 4)),
                      "Pas": t((0, 5), H=(2, 3), S=(2, 3), C=(2, 4), D=(2, 4))}
        PER["ut9"] = 11
        SIT["ut9x"] = {"rolle": "Svarer", "auction": [["Makker", "1NT"], ["Modstander", "X"]], "allowXX": True,
                       "calls": ["Pas", "XX", "2♣", "2♦", "2♥", "2♠"], "bonus": B_UT9}
        CL["ut9x"] = ut9x
        SAM["ut9x"] = {"XX": t((7, 12)), "Pas": t((0, 6), **{s: (3, 4) for s in SUITS})}
        for s in ORDER:
            SAM["ut9x"][f"2{SUIT_SYM[s]}"] = t((0, 6), **{s: (5, 6)})
        PER["ut9x"] = 9
    return SIT, CL, SAM, PER

def exporter(kind):
    return lambda path: kbuild(path, *build(kind))
