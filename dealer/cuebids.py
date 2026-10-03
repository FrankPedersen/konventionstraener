"""
Cuebids – fælles for begge systemer, efter afsnit 7 hos Makker 2 & mig.

Kontrol = es, konge, singleton eller renonce. Billigste kontrolfarve først; en oversprunget farve
benægter kontrol. Makkerne cuebidder på skift, indtil én afmelder i trumf.
Forløbet er Bekkasin: 1M – 2NT – 3♦ (åbners tillæg uden korthed):
  svar_*  – svarer: cuebid i billigste kontrolfarve med slemambition (17+ sp), ellers 4M (som i Bekkasin)
  aab_*   – åbner efter svarers cuebid: billigste egen kontrol over cuebiddet og under 4M; 4M, hvis
            ingen af jer har kontrol i en farve, svarer sprang over, eller hvis du ingen kontrol kan vise
Antagelse: åbner med tillæg samarbejder altid om slemundersøgelsen.
"""
from .core import SUITS, SUIT_SYM, SUIT_NAME, lengths_of, tpl, build_pool
from .bekkasin import cue_bids, has_control, control_word, responder_after_extra, rank

PAS = ["Modstander", "Pas"]
BONUS = {"q": "Hvad betyder det, når makker springer en farve over i sit cuebid?",
         "correct": "Makker har ikke kontrol i den farve",
         "options": ["Makker har ikke kontrol i den farve", "Makker har renonce dér", "Ingenting – cuebids kan meldes i vilkårlig rækkefølge"],
         "why": "Man cuebidder billigst muligt; springer man en farve over, benægter man kontrol dér. Kontrol = es, konge, singleton eller renonce."}

def opener_after_cue(M, cue):
    sym = SUIT_SYM[M]
    bids = cue_bids(M, "3♦")
    skipped = [s for c, s in bids if rank(c) < rank(cue)]
    def classify(hand, hp):
        L = lengths_of(hand)
        if L[M] < 5 or hp < 16 or any(L[s] <= 1 for s in SUITS if s != M):
            return None
        lacking = [s for s in skipped if not has_control(hand, s)]
        if lacking:
            names = ", ".join(SUIT_NAME[s] for s in lacking)
            return f"4{sym}", f"Makker sprang {names} over, og du har heller ikke kontrol dér: afmeld i 4{sym}."
        for c, s in cue_bids(M, cue):
            if has_control(hand, s):
                return c, f"Billigste egen kontrol over makkers {cue}: {c} viser {control_word(hand, s)} i {SUIT_NAME[s]}."
        return f"4{sym}", f"Ingen kontrol at vise under 4{sym}: afmeld."
    return classify

SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL = {}, {}, {}, {}
for M, key in (('H', 'h'), ('S', 's')):
    sym, om = SUIT_SYM[M], ('S' if M == 'H' else 'H')
    for cue, s in cue_bids(M, "3♦"):
        later = [c for c, _ in cue_bids(M, cue)]
        if not later:
            continue
        sk = f"aab_{key}_{s.lower()}"
        SITUATIONS[sk] = {"rolle": "Åbner",
                          "auction": [["Dig", f"1{sym}"], PAS, ["Makker", "2NT"], PAS, ["Dig", "3♦"], PAS, ["Makker", cue], PAS],
                          "calls": (["Pas"] if len(later) < 2 else []) + later + [f"4{sym}", "4NT"], "bonus": BONUS}
        CLASSIFIERS[sk] = opener_after_cue(M, cue)
        gen = tpl((16, 20), **{M: (5, 6), **{x: (2, 4) for x in SUITS if x != M}})
        SAMPLERS[sk] = {c: gen for c in later + [f"4{sym}"]}
        PER_CALL[sk] = 8
    sk = f"svar_{key}"
    SITUATIONS[sk] = {"rolle": "Svarer",
                      "auction": [["Makker", f"1{sym}"], PAS, ["Dig", "2NT"], PAS, ["Makker", "3♦"], PAS],
                      "calls": [c for c, _ in cue_bids(M, "3♦")] + ["3NT", f"4{sym}"], "bonus": BONUS}
    CLASSIFIERS[sk] = responder_after_extra(M, "3♦")
    resp = tpl((14, 20), **{M: (4, 5), om: (0, 3), 'D': (0, 5), 'C': (0, 5)})
    SAMPLERS[sk] = {c: resp for c, _ in cue_bids(M, "3♦")}
    SAMPLERS[sk][f"4{sym}"] = tpl((10, 14), **{M: (4, 5), om: (0, 3), 'D': (0, 5), 'C': (0, 5)})
    PER_CALL[sk] = 12

def export_pool(path):
    return build_pool(path, SITUATIONS, CLASSIFIERS, SAMPLERS, PER_CALL)
