"""Tjekker konventionskortenes meldeeksempler mod trænerens pulje (CLAUDE.md, Nye kort).

Kør fra repoets rod:  python3 tools/tjek_kort_eksempler.py [id ...]
For hvert meldeeksempel på et kort med traener.pool søges en hånd i puljen med samme meldeforløb og samme hånd.
- Fejl: hånden findes, men puljens svar er et andet, eller "N hp" i forklaringen passer ikke med hånden.
- Advarsel: hånden findes ikke i puljen (tilladt, men nye kort henter eksemplerne derfra).
"""
import json
import pathlib
import re
import sys

ROD = pathlib.Path(__file__).resolve().parent.parent
HP = {14: 4, 13: 3, 12: 2, 11: 1}
norm = lambda h: {f: sorted(h.get(f, []), reverse=True) for f in 'SHDC'}

index = json.loads((ROD / 'data/kort/index.json').read_text(encoding='utf-8'))
ids = sys.argv[1:] or [f[:-5] for f in index]
fejl, advarsler, tjekket = [], [], 0
for kid in ids:
    k = json.loads((ROD / 'data/kort' / f'{kid}.json').read_text(encoding='utf-8'))
    pool_sti = (k.get('traener') or {}).get('pool')
    if k.get('type') != 'melding' or not pool_sti:
        continue
    pool = json.loads((ROD / pool_sti).read_text(encoding='utf-8'))
    if 'situations' not in pool or 'hands' not in pool:
        continue
    for i, e in enumerate(k.get('eksempler', []), 1):
        tjekket += 1
        navn = f'{kid} eksempel {i}'
        hp = sum(HP.get(c, 0) for f in 'SHDC' for c in e['haand'][f])
        # "(16–17)" og lignende er grænser, ikke hændens point
        for n in re.findall(r'(?<![–(\d])(\d+) hp', e['forklaring']):
            if int(n) != hp:
                fejl.append(f'{navn}: forklaringen siger {n} hp, hånden har {hp} hp')
        forloeb = [list(x) for x in e['auction'][:-1]]
        sit = [s for s, v in pool['situations'].items() if [list(x) for x in v['auction']] == forloeb]
        match = [h for h in pool['hands'] if h.get('situation') in sit and norm(h['hand']) == norm(e['haand'])]
        if not match:
            advarsler.append(f'{navn}: hånden findes ikke i {pool_sti}')
        elif match[0].get('correct') != e['svar']:
            fejl.append(f"{navn}: kortet siger {e['svar']}, puljen siger {match[0].get('correct')}")

for a in advarsler:
    print('Advarsel:', a)
if fejl:
    print('\n'.join(fejl))
    sys.exit(1)
print(f'{tjekket} meldeeksempler er i orden ({len(advarsler)} advarsler).')
