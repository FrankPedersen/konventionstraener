"""Tjekker puljen til Forsvar mod Multi 2♦ (Crowhurst) mod regeltabellerne i SPEC-crowhurst-traener.md.

Kør fra repoets rod:  python3 tools/tjek_crowhurst.py

Reglerne er skrevet her igen direkte fra specen, uafhængigt af dealer/crowhurst.py. Testen fejler, hvis en hånd i
pools/crowhurst.json har et andet svar end reglerne, hvis svaret ikke er en af situationens knapper, eller hvis
modulet og reglerne her giver forskellige svar på tilfældige hænder.
"""
import collections
import json
import pathlib
import random
import sys

ROD = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROD))
from dealer import crowhurst as modul  # noqa: E402  kun til sammenligningen på tilfældige hænder

HP = {14: 4, 13: 3, 12: 2, 11: 1}
SYM = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
TILFAELDIGE = 50000


def info(h):
    L = {s: len(h[s]) for s in 'SHDC'}
    hp = sum(HP.get(c, 0) for s in 'SHDC' for c in h[s])
    top = {s: sum(1 for c in h[s] if c >= 12) for s in 'SHDC'}
    jaevn = sorted(L.values(), reverse=True) in ([4, 3, 3, 3], [4, 4, 3, 2], [5, 3, 3, 2])
    return L, hp, top, jaevn


def mellem(x, a, b):
    return a <= x <= b


def laengste(farver, L):
    """Den længste farve; 'uafgjort', hvis to er lige lange."""
    if not farver:
        return None
    farver = sorted(farver, key=lambda s: -L[s])
    if len(farver) > 1 and L[farver[0]] == L[farver[1]]:
        return 'uafgjort'
    return farver[0]


def direkte(h):
    L, hp, top, jaevn = info(h)
    if mellem(hp, 17, 19) and jaevn:
        return '2NT'
    for m in 'CD':
        if L['H'] >= 5 and L[m] >= 5 and mellem(hp, 10, 16):
            return '4' + SYM[m]
    if L['C'] >= 5 and L['D'] >= 5 and mellem(hp, 14, 20):
        return '4NT'
    for M in 'SH':
        if L[M] >= 7 and top[M] >= 2 and mellem(hp, 12, 17):
            return '4' + SYM[M]
    if max(L['S'], L['H']) >= 5 and mellem(hp, 12, 16):
        return '2♠' if L['S'] >= L['H'] else '2♥'
    for m in 'CD':
        if L[m] >= 6 and top[m] >= 2 and mellem(hp, 16, 19) and max(L['S'], L['H']) < 5:
            return '3NT'
    if hp >= 17:
        return 'X'
    gode = [m for m in 'CD' if L[m] >= 6 or (L[m] == 5 and top[m] >= 2)]
    if gode and mellem(hp, 12, 16):
        m = laengste(gode, L)
        return None if m == 'uafgjort' else '3' + SYM[m]
    if mellem(hp, 12, 16) and jaevn:
        return 'X'
    if hp >= 12:
        trefarvet = sum(L[s] >= 4 for s in 'SHDC') == 3 and min(L['S'], L['H']) <= 1
        svag_minor = any(L[m] == 5 and top[m] < 2 for m in 'CD')
        return 'Pas' if trefarvet or svag_minor else None
    return 'Pas'


def genaabning(h):
    if direkte(h) != 'Pas':
        return None
    L, hp, top, jaevn = info(h)
    if L['S'] >= 4 and L['H'] <= 1 and hp >= 12:
        return 'X'
    lange = [m for m in 'CD' if L[m] >= 5]
    if lange and mellem(hp, 12, 16):
        m = laengste(lange, L)
        return None if m == 'uafgjort' else '3' + SYM[m]
    return 'Pas'


def svar_d(h):
    L, hp, top, jaevn = info(h)
    if L['H'] >= 4 and mellem(hp, 8, 15):
        return 'X'
    if L['S'] >= 5 and mellem(hp, 12, 17):
        return '3♠'
    lange = [m for m in 'CD' if L[m] >= 5]
    if lange and mellem(hp, 8, 11):
        m = laengste(lange, L)
        return None if m == 'uafgjort' else '3' + SYM[m]
    if L['S'] == 5 and mellem(hp, 8, 11):
        return '2NT'
    if mellem(hp, 8, 11) and L['S'] <= 4:
        return '2NT'  # invit uden farve; 3♥ efter 3♣ (Franks valg 27. oktober 2026)
    if L['S'] >= 4 and hp <= 7:
        return '2♠'
    if lange and hp <= 7:
        return '2NT'
    if hp <= 7:
        return 'Pas'
    return None


def svar_relae(h):
    if svar_d(h) != '2NT':
        return None
    L, hp, top, jaevn = info(h)
    if L['S'] == 5 and mellem(hp, 8, 11):
        return '3♠'
    if mellem(hp, 8, 11) and L['S'] <= 4 and max(L['C'], L['D']) < 5:
        return '3♥'
    if L['D'] >= 5 and hp <= 7:
        return '3♦'
    if L['C'] >= 5 and hp <= 7:
        return 'Pas'
    return None


def svar_4kl(h):
    L, hp, top, jaevn = info(h)
    if L['C'] >= 3 and L['C'] > L['H'] and mellem(hp, 14, 20):
        return '4♠'
    if L['H'] >= 3 and mellem(hp, 14, 20):
        return '4♦'
    if L['H'] >= 2:
        return '4♥'
    return None


def hjerterhold(h):
    """Es, konge med 1+ kort til, dame med 2+ eller knægt med 3+ (Claude Codes valg, Afklaret 17)."""
    mindst = {14: 1, 13: 2, 12: 3, 11: 4}
    return any(r in mindst and len(h['H']) >= mindst[r] for r in h['H'])


def dobler(h):
    """Dobleren efter (2♦) – X – (2♥) – 2NT – (pas) (Franks valg 27. oktober 2026, Afklaret 16)."""
    if direkte(h) != 'X':
        return None
    L, hp, top, jaevn = info(h)
    if mellem(hp, 12, 16):
        return '3♣'
    if jaevn and mellem(hp, 20, 21) and hjerterhold(h):
        return '3NT'
    if (jaevn and hp >= 22) or (not jaevn and L['H'] >= 5):
        return None
    farver = [s for s in 'SDC' if L[s] >= 5]
    if farver:
        s = laengste(farver, L)
        return None if s == 'uafgjort' else {'S': '3♠', 'D': '3♦', 'C': '4♣'}[s]
    return '3♥'


REGLER = {'direkte': direkte, 'genaabning': genaabning, 'svar_d': svar_d, 'svar_relae': svar_relae, 'svar_4kl': svar_4kl,
          'dobler': dobler}
SITUATIONER = {
    'dobler': ('Dobler', [['Modstander', '2♦'], ['Dig', 'X'], ['Modstander', '2♥'], ['Makker', '2NT'], ['Modstander', 'Pas']],
               ['3♣', '3♦', '3♥', '3♠', '3NT', '4♣']),
    'svar_relae': ('Svarer', [['Modstander', '2♦'], ['Makker', 'X'], ['Modstander', '2♥'], ['Dig', '2NT'], ['Modstander', 'Pas'],
                              ['Makker', '3♣'], ['Modstander', 'Pas']], ['Pas', '3♦', '3♥', '3♠']),
}


def main():
    pool = json.loads((ROD / 'pools' / 'crowhurst.json').read_text(encoding='utf-8'))
    fejl = []
    for s, (rolle, auction, calls) in SITUATIONER.items():
        sit = pool['situations'].get(s)
        if not sit or sit['rolle'] != rolle or sit['auction'] != auction or sit['calls'] != calls:
            fejl.append(f'situationen {s} skal have rollen {rolle}, meldeforløbet {auction} og knapperne {calls}')
        for c in calls:
            if not any(h['situation'] == s and h['correct'] == c for h in pool['hands']):
                fejl.append(f'situationen {s} har ingen hænder med svaret {c}')
    for i, h in enumerate(pool['hands'], 1):
        s, haand = h['situation'], h['hand']
        L, hp, _, _ = info(haand)
        if sum(L.values()) != 13 or hp != h['hp']:
            fejl.append(f'hånd {i}: {sum(L.values())} kort og {hp} hp (puljen siger {h["hp"]} hp)')
        if REGLER[s](haand) != h['correct']:
            fejl.append(f'hånd {i} ({s}): puljen siger {h["correct"]}, reglerne siger {REGLER[s](haand)}')
        if h['correct'] not in pool['situations'][s]['calls']:
            fejl.append(f'hånd {i} ({s}): {h["correct"]} er ikke en af situationens knapper')
        if not h.get('why') or not (h.get('en') or {}).get('why'):
            fejl.append(f'hånd {i} ({s}): mangler forklaring på dansk eller engelsk')

    rnd = random.Random(1)
    afvig = collections.Counter()
    kort = [(s, r) for s in 'SHDC' for r in range(2, 15)]
    for _ in range(TILFAELDIGE):
        valgt = rnd.sample(kort, 13)
        h = {s: sorted((r for x, r in valgt if x == s), reverse=True) for s in 'SHDC'}
        hp = info(h)[1]
        for s, regel in REGLER.items():
            svar = modul.CLASSIFIERS[s](h, hp)
            svar = svar[0] if svar else None
            if svar != regel(h):
                afvig[(s, svar, regel(h))] += 1
    for (s, svar, regel), n in sorted(afvig.items()):
        fejl.append(f'{s}: modulet siger {svar}, reglerne siger {regel} ({n} af {TILFAELDIGE} tilfældige hænder)')

    if fejl:
        print('\n'.join(fejl))
        return 1
    print(f'Crowhurst-puljen: i orden ({len(pool["hands"])} hænder; modulet og reglerne er enige på {TILFAELDIGE} tilfældige hænder).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
