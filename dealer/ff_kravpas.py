"""
Kravpas og Loven – Flemming & Frank, afsnit 18 og 18a.

  lov_svar_* – svarer efter makkers 1♥ – (1♠) eller 1♠ – (2♥): støt efter Loven – 3 trumf (8 i alt) på
               2-trinnet · 4 trumf (9) på 3-trinnet · 5 trumf (10) på 4-trinnet · pas under 6 sp
  lov_aab_*  – åbner efter 1M – (indmelding) – 2M – (deres 2-/3-melding): makker har vist 3 trumf;
               med minimum meldes til trumfantallet – 5 trumf (8) pas · 6 trumf (9) 3M
  naese_*    – næsekravpas: 1♥ – (1♠) – pas – (pas) – ?: åbner med højst 2 spar genåbner med dobling
               (makker kan stå med gode spar og strafpasse); med 4+ spar passer han
Antagelser: zonen er neutral og der justeres ikke for dobbeltfit og korthed; støttepoint 5/3/1 med
4+ trumf og 3/2/1 med 3; åbner har minimum (12–14); næsekravpas med præcis 3 spar er ikke med.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, either, build_pool
from .omvendt_bergen import support_points

PAS = ["Modstander", "Pas"]
BONUS = {
    "lov": {"q": "Hvor højt melder du efter Loven med 9 trumf tilsammen?",
            "correct": "Til 3-trinnet",
            "options": ["Til 3-trinnet", "Til 2-trinnet", "Til 4-trinnet"],
            "why": "Loven: meld til det antal stik, der svarer til antallet af trumf – 8 trumf 2-trinnet, 9 trumf 3-trinnet, 10 trumf 4-trinnet."},
    "naese": {"q": "Hvorfor genåbner åbner med dobling i 1♥ – (1♠) – pas – (pas)?",
              "correct": "Makker kan have gode spar og ville strafdoble",
              "options": ["Makker kan have gode spar og ville strafdoble", "Åbner har 18+", "Åbner viser spar"],
              "why": "Med negative doblinger kan makker ikke selv strafdoble 1♠. Er åbner kort i spar, genåbner han med dobling, så makker kan strafpasse."},
}

def law_responder(M, O):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[O] > 2 or hp > 9:
            return None
        n = L[M]
        if n < 3:
            return None
        sp = support_points(hand, hp, M)
        if sp < 6:
            return ("Pas", f"{sp} sp: pas.") if hp <= 5 else None
        if sp > 9:
            return None
        call = {3: f"2{sym}", 4: f"3{sym}"}.get(n, f"4{sym}")
        return call, f"{n} {SUIT_NAME[M]} + makkers 5 = {n + 5} trumf: Loven siger {call[0]}-trinnet – {call}."
    return classify

def law_opener(M):
    sym = SUIT_SYM[M]
    def classify(hand, hp):
        L = lengths_of(hand)
        if not (12 <= hp <= 14) or L[M] not in (5, 6) or any(L[s] >= 5 for s in SUITS if s != M):
            return None
        total = L[M] + 3
        if total == 8:
            return "Pas", f"{L[M]} trumf + makkers 3 = 8: Loven siger 2-trinnet – pas."
        return f"3{sym}", f"{L[M]} trumf + makkers 3 = 9: Loven siger 3-trinnet – 3{sym}."
    return classify

def nose(hand, hp):
    L = lengths_of(hand)
    if not (12 <= hp <= 14) or L['H'] != 5 or L['S'] == 3:
        return None
    if L['S'] <= 2:
        return "X", f"{L['S']} spar: genåbn med dobling – makker kan sidde med gode spar og strafpasse."
    return "Pas", f"{L['S']} spar: du er selv lang i deres farve – pas."

SITUATIONS = {
    "lov_svar_sp": {"rolle": "Svarer", "auction": [["Makker", "1♠"], ["Modstander", "2♥"]], "allowX": True,
                    "calls": ["Pas", "2♠", "2NT", "3♥", "3♠", "4♠"], "bonus": BONUS["lov"]},
    "lov_svar_hj": {"rolle": "Svarer", "auction": [["Makker", "1♥"], ["Modstander", "1♠"]], "allowX": True,
                    "calls": ["Pas", "1NT", "2♥", "2♠", "3♥", "4♥"], "bonus": BONUS["lov"]},
    "naese_hj": {"rolle": "Åbner", "auction": [["Dig", "1♥"], ["Modstander", "1♠"], ["Makker", "Pas"], PAS], "allowX": True,
                 "calls": ["Pas", "X", "1NT", "2♣", "2♦", "2♥"], "bonus": BONUS["naese"]},
}
CLASSIFIERS = {"lov_svar_sp": law_responder('S', 'H'), "lov_svar_hj": law_responder('H', 'S'), "naese_hj": nose}
r = lambda hp, M, O, n: tpl(hp, **{O: (0, 2), 'D': (1, 5), 'C': (1, 5), M: (n, n)})
lov = lambda M, O: {f"2{SUIT_SYM[M]}": r((5, 9), M, O, 3), f"3{SUIT_SYM[M]}": r((3, 8), M, O, 4), f"4{SUIT_SYM[M]}": r((2, 7), M, O, 5), "Pas": r((0, 4), M, O, 3)}
SAMPLERS = {"lov_svar_sp": lov('S', 'H'), "lov_svar_hj": lov('H', 'S'),
            "naese_hj": {"X": tpl((12, 14), H=(5, 5), S=(0, 2), D=(1, 5), C=(1, 5)), "Pas": tpl((12, 14), H=(5, 5), S=(4, 4), D=(1, 3), C=(1, 3))}}
PER_CALL = {"lov_svar_sp": 13, "lov_svar_hj": 13, "naese_hj": 20}
for M, key, over, theirs in (('H', 'hj', "1♠", "2♠"), ('S', 'sp', "2♥", "3♥")):
    sym = SUIT_SYM[M]
    sk = f"lov_aab_{key}"
    SITUATIONS[sk] = {"rolle": "Åbner", "auction": [["Dig", f"1{sym}"], ["Modstander", over], ["Makker", f"2{sym}"], ["Modstander", theirs]],
                      "allowX": True, "calls": ["Pas", "3♣", "3♦", f"3{sym}", "3NT", f"4{sym}"] if M == 'H' else ["Pas", "3♠", "3NT", "4♣", "4♦", "4♠"],
                      "bonus": BONUS["lov"]}
    CLASSIFIERS[sk] = law_opener(M)
    o = lambda hp, n, M=M: tpl(hp, **{**{s: (1, 4) for s in SUITS}, M: (n, n)})
    SAMPLERS[sk] = {"Pas": o((12, 14), 5), f"3{sym}": o((12, 14), 6)}
    PER_CALL[sk] = 20

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
