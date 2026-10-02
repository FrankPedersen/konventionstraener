"""
Fælles byggesten til »Kampen om kontrakten« (20-20, efter referencedokumentet 01-principper.md).

Forskelle fra core.build_pool:
  * hver hånd får en tilfældig zone (ingen / ns / ov / alle); Dig sidder altid Syd, så »vi« er Nord-Syd
  * klassifikatoren kaldes som classify(hand, hp, zone) og kan returnere (call, why) eller
    (call, why, extra), hvor extra lægges på hånden i puljen:
      aftale: True            – facit hviler på vores aftale, ikke bogens regel (vises ikke i profil Grund)
      only:   [profiler]       – hånden vises kun i disse profiler
      grund / turnering: {"correct", "why"} – afvigende facit i den profil (fx Stenberg, Lebensohl)
"""
import random
from .core import SUITS, export

ZONES = ["ingen", "ns", "ov", "alle"]

def we_vul(zone):
    return zone in ("ns", "alle")

def they_vul(zone):
    return zone in ("ov", "alle")

def zone_word(zone):
    return {"ingen": "ingen i zonen", "ns": "I er i zonen", "ov": "de er i zonen", "alle": "alle i zonen"}[zone]

def build_pool(path, situations, classifiers, samplers, per_call):
    hands, seen = [], set()
    for situation, n in per_call.items():
        for call, sampler in samplers[situation].items():
            made = tries = 0
            while made < n and tries < 20000:
                tries += 1
                r = sampler()
                if not r:
                    continue
                hand, hp, sp = r
                key = tuple(tuple(hand[s]) for s in SUITS)
                zone = random.choice(ZONES)
                res = classifiers[situation](hand, hp, zone)
                if key in seen or not res or res[0] != call:
                    continue
                seen.add(key)
                entry = {"situation": situation, "hand": {s: hand[s] for s in SUITS},
                         "hp": hp, "sp": sp, "zone": zone, "correct": res[0], "why": res[1]}
                if len(res) > 2 and res[2]:
                    entry.update(res[2])
                hands.append(entry)
                made += 1
            if made < n:
                print(f"Advarsel: kun {made}/{n} hænder til {situation} {call}")
    return export(path, situations, hands)

def zoneless(classify):
    """Gør en klassifikator uden zone-parameter brugbar her."""
    return lambda hand, hp, zone: classify(hand, hp)
