"""Accepttest for SPEC-multi-2ru.md: træneren Multi 2♦ efter Jyderups ark, med hullerne udfyldt fra W.

Kør fra repoets rod:  python3 tools/tjek_multi_2ru.py

Testen tjekker specens otte punkter og skriver for hvert, om det er i orden eller rødt:
1. Facit-eksemplerne 2, 3, 4, 5, 7, 8 og 9 og de tre første åbningshænder giver tabellernes svar med
   dealer/multi_2ru.py's bedømmelse og med reglerne her. Grænserne i modulet er de samme som i specens kodeblok og står
   under overskriften "# --- Grænser, som kilderne ikke giver tal for – ret dem her".
2. ret, spm og spm2 giver tabellens svar for alle kombinationer af svar, åbners major og minimum eller maksimum.
3. Puljen har alle syv situationer med specens meldeforløb, roller, meldinger og bonusspørgsmål; hver melding, reglerne
   giver, har mindst 7 hænder (PER_CALL), og build_pools.py skriver ingen "Advarsel: kun …".
4. For hver hånd i puljen er correct det svar, reglerne her giver (og modulet giver), og ingen hånd ligger uden for de
   regler, situationen har.
5. Alle åbnerhænder er gyldige 2♦-åbninger efter J (og Nords hånd, når puljen har hele spil).
6. Posten multi-2ru står i data/konventioner.json som i specen, ff-multi-2ru er væk, og de øvrige poster og de filer,
   specen ikke tillader ændret, er som i tagget v-foer-multi-2ru.
7. tools/tjek_konventionskort.py melder "i orden", og tools/tjek_kort_eksempler.py multi-2ru giver ingen advarsler;
   kortet har alle seks afsnit, traener-feltet og eksempler med samme meldeforløb og svar som eksempel 3, 4, 5 og 9.
8. tools/tjek_fagord.py, tools/tjek_bydeform.py og tools/tjek_sprog.py er grønne.

Reglerne er skrevet her igen direkte fra specen, uafhængigt af modulet; tallene kommer fra specens kodeblok under
Grænser. traener.html tager meldeforløbet fra situationen, så ret og indmelding har én situation pr. svar og pr.
indmelding i puljen. Testen finder situationerne ud fra meldeforløbet, ikke ud fra navnene.
"""
import contextlib
import io
import json
import os
import pathlib
import random
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8')
ROD = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROD))

TAG = 'v-foer-multi-2ru'
FLETTET = '9ce90ee'  # flettecommit for multi-2ru; punkt 6 sammenligner tagget med den, ikke med arbejdsmappen
HP = {14: 4, 13: 3, 12: 2, 11: 1}
SYM = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
FARVE = {v: k for k, v in SYM.items()}
OVERSKRIFT = '# --- Grænser, som kilderne ikke giver tal for – ret dem her'
PER_CALL_MIN = 7
FREDET = ['viden/2-over-1-makker2.html', 'traener.html', 'dealer/core.py', 'dealer/crowhurst.py']


# ---------- Specen: grænserne og posten ----------

def spec_tekst():
    for sti in (ROD / 'SPEC-multi-2ru.md', ROD / 'docs' / 'specs' / 'SPEC-multi-2ru.md'):
        if sti.exists():
            return sti.read_text(encoding='utf-8')
    raise FileNotFoundError('SPEC-multi-2ru.md findes hverken i roden eller i docs/specs/')


SPEC = spec_tekst()
_blok = re.search(r'```python\n(# --- Grænser.*?)```', SPEC, re.S).group(1)
G = {}
exec(_blok, {}, G)  # noqa: S102  specens egen kodeblok med grænserne
NAVNE = sorted(G)
POST = json.loads(re.search(r'## Post i data/konventioner.json\s*```json\n(.*?)```', SPEC, re.S).group(1))


def g(navn, felt=None):
    return G[navn] if felt is None else G[navn][felt]


# ---------- Hænder ----------

def haand(s):
    """'E72 984 KD743 86' (♠ ♥ ♦ ♣) → {'S': [14, 7, 2], …}. – er en renonce."""
    vaerdi = {'E': 14, 'K': 13, 'D': 12, 'B': 11, 'T': 10}
    farver = s.split()
    assert len(farver) == 4, s
    return {f: sorted((vaerdi.get(c) or int(c) for c in x if c not in '–-'), reverse=True) for f, x in zip('SHDC', farver)}


def info(h):
    L = {s: len(h[s]) for s in 'SHDC'}
    hp = sum(HP.get(c, 0) for s in 'SHDC' for c in h[s])
    return L, hp


def top(h, s, n):
    """Antal af de n øverste honnører (n=3: E K D, n=4: E K D B) i farven."""
    return sum(1 for c in h[s] if c > 14 - n)


def esser(h):
    return sum(1 for s in 'SHDC' if 14 in h[s])


def mellem(x, ab):
    return ab[0] <= x <= ab[1]


def anden(M):
    return 'S' if M == 'H' else 'H'


# ---------- Reglerne (specen, Regler og Grænser) ----------

def gyldig_2ru(h):
    """J: præcis seks kort i én major, højst tre i den anden, 5–10 hp og højst ét es."""
    L, hp = info(h)
    return any(L[M] == 6 and L[anden(M)] <= 3 for M in 'HS') and 5 <= hp <= 10 and esser(h) <= 1


def major(h):
    L, _ = info(h)
    return 'H' if L['H'] == 6 else 'S'


def aabning(h):
    L, hp = info(h)
    seks = [M for M in 'HS' if L[M] == 6]
    if len(seks) != 1:
        return None
    M = seks[0]
    if 11 <= hp <= 15:
        return '1' + SYM[M]
    if hp <= 4:
        return 'Pas'
    if gyldig_2ru(h):
        return '2♦'
    return None  # 5–10 hp med to esser eller en firfarve i den anden major: kilderne siger ikke hvad


def svar(h, med_rest=True):
    """2♦ – Pas – ?  Første regel, der passer. Uden med_rest falder 2♥ (resten) væk, som efter dobling."""
    L, hp = info(h)
    for M in 'HS':
        e = g('EGEN_MAJOR')
        if L[M] >= e['laengde'] and top(h, M, 3) >= e['top'] and hp >= e['hp']:
            return '4' + SYM[M]
    e = g('EGEN_MINOR')
    minorer = [m for m in 'CD' if L[m] >= e['laengde'] and top(h, m, 3) >= e['top'] and hp >= e['hp']
               and not (L['H'] >= 3 and L['S'] >= 3)]
    if minorer:
        if len(minorer) == 2 and L['C'] == L['D']:
            return None  # to lige lange minorer: specen siger ikke hvilken
        return '3' + SYM[max(minorer, key=lambda m: L[m])]
    if hp >= g('SPOERG_HP'):
        return '2NT'
    if L['H'] >= 3 and L['S'] >= 3 and mellem(hp, g('UDGANG_HP')):
        return '4♦'
    if L['H'] >= g('INVIT_HJ', 'hjerter') and mellem(hp, g('INVIT_HJ', 'hp')):
        return '2♠'
    s = g('SPAER_TRE_SP')
    if L['H'] >= s['begge'] and L['S'] >= s['begge'] and mellem(hp, s['hp']):
        return '3♠'
    s = g('SPAER_TRE_HJ')
    if L['H'] >= s['begge'] and L['S'] >= s['begge'] and mellem(hp, s['hp']):
        return '3♥'
    return '2♥' if med_rest else None  # 2♥: resten (under SPOERG_HP)


def dobling(h):
    """2♦ – X – ?"""
    L, hp = info(h)
    if L['D'] >= g('PAS_RUDER', 'laengde') and hp <= g('PAS_RUDER', 'hp_max'):
        return 'Pas'
    if hp >= g('STRAF_XX', 'hp') and L['H'] <= g('STRAF_XX', 'major_max') and L['S'] <= g('STRAF_XX', 'major_max'):
        return 'XX'
    if L['H'] >= g('SVAG_FIT_X', 'begge') and L['S'] >= g('SVAG_FIT_X', 'begge') and hp <= g('SVAG_FIT_X', 'hp_max'):
        return '2♥'
    return svar(h, med_rest=False)  # svage hænder uden ruder og uden fit i begge majorer: ikke med (Afklaret, punkt 4)


def indmelding(h, deres):
    """2♦ – (deres) – ?  Over 2♠ dobling efter J og 3♥ (pas eller ret) efter W, over 3♣, 3♦ og 4♥ efter W."""
    L, hp = info(h)
    if deres == '2♠':
        if hp >= g('NEGATIV_X', 'hp'):
            return 'X'
        if hp >= g('PAS_RET', 'hp') and L['H'] >= 3 and L['S'] >= 3:
            return '3♥'
        return 'Pas'
    trin, f = int(deres[0]), FARVE[deres[1]]
    s = g('STRAF')
    if L[f] >= s['laengde'] and top(h, f, 4) >= s['top4'] and hp >= s['hp']:
        return 'X'
    if hp >= g('PAS_RET', 'hp'):
        if deres == '4♥':
            if L['S'] >= 4:
                return '4♠'
        elif L['H'] >= 3 and L['S'] >= 3:
            return '3♥'
    m = g('MINOR_NAT')
    for minor in 'CD':
        bud = billigste(deres, minor)
        if minor != f and bud and bud[0] == '3' and L[minor] >= m['laengde'] and top(h, minor, 3) >= m['top'] \
                and hp >= m['hp']:
            return bud
    return 'Pas'


RET = {
    '2♥': lambda M, mx: 'Pas' if M == 'H' else '2♠',
    '2♠': lambda M, mx: 'Pas' if M == 'S' else ('4♥' if mx else '3♥'),
    '3♥': lambda M, mx: 'Pas' if M == 'H' else '3♠',
    '3♠': lambda M, mx: 'Pas' if M == 'S' else '4♥',
    '4♣': lambda M, mx: '4♦' if M == 'H' else '4♥',
    '4♦': lambda M, mx: '4♥' if M == 'H' else '4♠',
}


def ret(h, makkers):
    if not gyldig_2ru(h):
        return None
    _, hp = info(h)
    return RET[makkers](major(h), mellem(hp, g('MAX_HP')))


def spm(h):
    if not gyldig_2ru(h):
        return None
    _, hp = info(h)
    if mellem(hp, g('MAX_HP')):
        return '3♣'
    return '3♦' if major(h) == 'H' else '3♥'


def spm2(h):
    if not gyldig_2ru(h):
        return None
    _, hp = info(h)
    if not mellem(hp, g('MAX_HP')):
        return None  # åbner har vist maksimum med 3♣
    return '3♥' if major(h) == 'S' else '3♠'


# ---------- Meldeforløbene (specen, Situationer) ----------

PAS = ['Modstander', 'Pas']
TRIN = ['♣', '♦', '♥', '♠', 'NT']


def rang(bud):
    return (int(bud[0]), TRIN.index(bud[1:])) if bud[0].isdigit() else None


def billigste(over, farve):
    """Det billigste lovlige bud i farven over buddet over."""
    t, i = rang(over)
    j = TRIN.index(SYM[farve])
    return f'{t if j > i else t + 1}{SYM[farve]}'


def lovlig(calls, sidste):
    return [c for c in calls if not c[0].isdigit() or rang(c) > rang(sidste)]


RET_SVAR = ['2♥', '2♠', '3♥', '3♠', '4♣', '4♦']
IND = ['2♠', '3♣', '3♦', '4♥']
RET_CALLS = ['Pas', '2♠', '3♥', '3♠', '4♦', '4♥', '4♠']


def ind_calls(deres):
    f = FARVE[deres[1]]
    return ['Pas', 'X'] + sorted((billigste(deres, s) for s in 'CDHS' if s != f), key=rang)


SITUATIONER = {}  # meldeforløb (som tuple) → (familie, rolle, meldinger, svar reglerne kan give, regel)
SITUATIONER[()] = ('aabning', 'Åbner', ['Pas', '1♥', '1♠', '2♦'], {'Pas', '1♥', '1♠', '2♦'}, aabning)
SITUATIONER[(('Makker', '2♦'), tuple(PAS))] = (
    'svar', 'Svarer', ['Pas', '2♥', '2♠', '2NT', '3♣', '3♦', '3♥', '3♠', '3NT', '4♣', '4♦', '4♥', '4♠'],
    {'2♥', '2♠', '2NT', '3♣', '3♦', '3♥', '3♠', '4♦', '4♥', '4♠'}, svar)
for _s in RET_SVAR:
    SITUATIONER[(('Dig', '2♦'), tuple(PAS), ('Makker', _s), tuple(PAS))] = (
        'ret', 'Åbner', lovlig(RET_CALLS, _s), {RET[_s](M, mx) for M in 'HS' for mx in (False, True)},
        (lambda s: lambda h: ret(h, s))(_s))
SITUATIONER[(('Dig', '2♦'), tuple(PAS), ('Makker', '2NT'), tuple(PAS))] = (
    'spm', 'Åbner', ['3♣', '3♦', '3♥', '3♠', '3NT'], {'3♣', '3♦', '3♥'}, spm)
SITUATIONER[(('Dig', '2♦'), tuple(PAS), ('Makker', '2NT'), tuple(PAS), ('Dig', '3♣'), tuple(PAS),
             ('Makker', '3♦'), tuple(PAS))] = ('spm2', 'Åbner', ['3♥', '3♠', '3NT'], {'3♥', '3♠'}, spm2)
SITUATIONER[(('Makker', '2♦'), ('Modstander', 'X'))] = (
    'dobling', 'Svarer', ['Pas', 'XX', '2♥', '2♠', '2NT', '3♣', '3♦', '3♥', '3♠', '4♣', '4♦', '4♥', '4♠'],
    {'Pas', 'XX', '2♥', '2♠', '2NT', '3♣', '3♦', '3♥', '3♠', '4♦', '4♥', '4♠'}, dobling)
_IND_SVAR = {'2♠': {'Pas', 'X', '3♥'}, '3♣': {'Pas', 'X', '3♦', '3♥'}, '3♦': {'Pas', 'X', '3♥'}, '4♥': {'Pas', 'X', '4♠'}}
for _d in IND:
    SITUATIONER[(('Makker', '2♦'), ('Modstander', _d))] = (
        'indmelding', 'Svarer', ind_calls(_d), _IND_SVAR[_d], (lambda d: lambda h: indmelding(h, d))(_d))
FAMILIER = ['aabning', 'svar', 'ret', 'spm', 'spm2', 'dobling', 'indmelding']
BONUS = {
    'aabning': 'Hvilke krav stiller Multi 2♦ til hånden?',
    'svar': 'Hvad betyder 2♠ som svar på Multi?',
    'ret': 'Hvad melder åbner efter 4♣?',
    'spm2': 'Hvad betyder svarers 3♥ efter 2♦ – 2NT – 3♣?',
    'dobling': 'Hvad viser redobling, når modparten dobler 2♦?',
    'indmelding': 'Hvad betyder dobling efter 2♦ – (2♠)?',
}


def forloeb(auction):
    return tuple(tuple(x) for x in auction)


# ---------- Facit (specen, Eksemplerne) ----------

SVAR = (('Makker', '2♦'), tuple(PAS))
FACIT = [
    ('eksempel 2', SVAR, 'E72 984 KD743 86', '3♥'),
    ('eksempel 3', SVAR, '– KDBT874 KD92 E4', '4♥'),
    ('eksempel 4', SVAR, 'DBT EK4 942 EKD2', '2NT'),
    ('eksempel 5', (('Makker', '2♦'), ('Modstander', 'X')), '8 D743 EDT9742 B', 'Pas'),
    ('eksempel 7', (('Makker', '2♦'), ('Modstander', '3♣')), '9 KB93 EK86 KDT8', 'X'),
    ('eksempel 8', (('Makker', '2♦'), ('Modstander', '3♦')), '2 KB3 DT3 EK7542', 'Pas'),
    ('eksempel 9', (('Makker', '2♦'), ('Modstander', '4♥')), 'KT72 862 KD952 8', '4♠'),
    ('åbningshånd 1', (), 'KD9653 7 D76 863', '2♦'),
    ('åbningshånd 2', (), 'KBT975 8 873 985', 'Pas'),
    ('åbningshånd 3', (), '95 KDB973 KB 874', '2♦'),
]
KORT_EKSEMPLER = [  # kortets eksempler: samme meldeforløb og svar som eksempel 3, 4, 5 og 9
    ('eksempel 3', SVAR, '4♥'),
    ('eksempel 4', SVAR, '2NT'),
    ('eksempel 5', (('Makker', '2♦'), ('Modstander', 'X')), 'Pas'),
    ('eksempel 9', (('Makker', '2♦'), ('Modstander', '4♥')), '4♠'),
]


# ---------- Modulet og puljen ----------

_modul = None


def modul():
    global _modul
    if _modul is None:
        if not (ROD / 'dealer' / 'multi_2ru.py').exists():
            raise RuntimeError('dealer/multi_2ru.py findes ikke endnu')
        from dealer import multi_2ru
        _modul = multi_2ru
    return _modul


def noegle(forl):
    """Modulets situation med dette meldeforløb."""
    ns = [k for k, v in modul().SITUATIONS.items() if forloeb(v['auction']) == forl]
    if len(ns) != 1:
        raise RuntimeError(f'modulet har {len(ns)} situationer med meldeforløbet {vis(forl)}')
    return ns[0]


def bedoem(forl, h):
    """Modulets svar på hånden i situationen med dette meldeforløb."""
    res = modul().CLASSIFIERS[noegle(forl)](h, info(h)[1])
    return res[0] if res else None


def pulje():
    sti = ROD / 'pools' / 'multi-2ru.json'
    if not sti.exists():
        raise RuntimeError('pools/multi-2ru.json findes ikke endnu')
    return json.loads(sti.read_text(encoding='utf-8'))


def vis(forl):
    return ' – '.join(c for _, c in forl) + (' – ?' if forl else '?')


def vis_haand(h):
    navn = {14: 'E', 13: 'K', 12: 'D', 11: 'B', 10: 'T'}
    return ' '.join(SYM[s] + (''.join(navn.get(c, str(c)) for c in h[s]) or '–') for s in 'SHDC')


def koer(*args):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    r = subprocess.run([sys.executable, *args], cwd=ROD, capture_output=True, text=True, encoding='utf-8', env=env)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


# ---------- De otte punkter ----------

def punkt1():
    fejl = []
    for navn, forl, kort, facit in FACIT:  # reglerne her skal give facit, ellers er testen forkert
        h = haand(kort)
        regel = SITUATIONER[forl][4](h)
        if regel != facit:
            fejl.append(f'{navn}: reglerne i testen giver {regel}, facit er {facit} (testen eller grænserne er forkerte)')
    m = modul()
    kilde = (ROD / 'dealer' / 'multi_2ru.py').read_text(encoding='utf-8')
    if OVERSKRIFT not in kilde:
        fejl.append(f'dealer/multi_2ru.py: overskriften "{OVERSKRIFT}" mangler')
    for n in NAVNE:
        if not hasattr(m, n):
            fejl.append(f'dealer/multi_2ru.py: konstanten {n} mangler')
        elif getattr(m, n) != G[n]:
            fejl.append(f'dealer/multi_2ru.py: {n} = {getattr(m, n)!r}, specen siger {G[n]!r}')
    for navn, forl, kort, facit in FACIT:
        svar_ = bedoem(forl, haand(kort))
        if svar_ != facit:
            fejl.append(f'{navn} ({vis(forl)}, {kort}): modulet giver {svar_}, facit er {facit}')
    return fejl


def aabnerhaender():
    """To gyldige 2♦-åbninger for hver major og hvert hp fra 5 til 10 (faste hænder, samme frø hver gang)."""
    rnd = random.Random(2026)
    ud = []
    for M in 'HS':
        A = anden(M)
        for maal in range(5, 11):
            fundet = 0
            while fundet < 2:
                k = rnd.randint(0, 3)
                minor = rnd.sample([(s, r) for s in 'CD' for r in range(2, 15)], 7 - k)
                h = {M: sorted(rnd.sample(range(2, 15), 6), reverse=True), A: sorted(rnd.sample(range(2, 15), k), reverse=True)}
                for s in 'CD':
                    h[s] = sorted((r for x, r in minor if x == s), reverse=True)
                if info(h)[1] == maal and gyldig_2ru(h):
                    ud.append(h)
                    fundet += 1
    return ud


def punkt2():
    fejl = []
    haender = aabnerhaender()
    sit = [f for f, v in SITUATIONER.items() if v[0] in ('ret', 'spm', 'spm2')]
    sete = set()
    for forl in sit:
        familie, _, _, _, regel = SITUATIONER[forl]
        for h in haender:
            M, hp = major(h), info(h)[1]
            mx = 'maksimum' if mellem(hp, g('MAX_HP')) else 'minimum'
            forventet, faktisk = regel(h), bedoem(forl, h)
            if forventet != faktisk and (forl, M, mx) not in sete:
                sete.add((forl, M, mx))
                fejl.append(f'{familie} ({vis(forl)}), {"hjerter" if M == "H" else "spar"} og {mx} ({vis_haand(h)}, {hp} hp): '
                            f'modulet giver {faktisk}, tabellen siger {forventet}')
    return fejl


def punkt3():
    fejl = []
    m, p = modul(), pulje()
    import build_pools
    if build_pools.CONVENTIONS.get('multi-2ru') is not m:
        fejl.append('build_pools.py: "multi-2ru": multi_2ru mangler i CONVENTIONS')
    for k, n in m.PER_CALL.items():
        if n < PER_CALL_MIN:
            fejl.append(f'PER_CALL[{k!r}] er {n}, mindst {PER_CALL_MIN}')
    sit = {forloeb(v['auction']): (k, v) for k, v in p['situations'].items()}
    if len(sit) != len(p['situations']):
        fejl.append('puljen har to situationer med samme meldeforløb')
    for forl in sit:
        if forl not in SITUATIONER:
            fejl.append(f'puljen har en situation, specen ikke har: {sit[forl][0]} ({vis(forl)})')
    familier = set()
    for forl, (familie, rolle, calls, svarene, _) in SITUATIONER.items():
        if forl not in sit:
            fejl.append(f'{familie}: puljen mangler meldeforløbet {vis(forl)}')
            continue
        familier.add(familie)
        k, v = sit[forl]
        if v.get('rolle') != rolle:
            fejl.append(f'{k}: rollen er {v.get("rolle")}, specen siger {rolle}')
        if set(v.get('calls', [])) != set(calls) or len(v.get('calls', [])) != len(calls):
            fejl.append(f'{k} ({vis(forl)}): meldingerne er {v.get("calls")}, specen siger {calls}')
        if 'X' in calls and not v.get('allowX'):
            fejl.append(f'{k}: X er en af meldingerne, men allowX mangler')
        if 'XX' in calls and not v.get('allowXX'):
            fejl.append(f'{k}: XX er en af meldingerne, men allowXX mangler')
        b, be = v.get('bonus') or {}, (v.get('en') or {}).get('bonus') or {}
        if not (b.get('q') and b.get('why') and len(b.get('options', [])) == 3 and b.get('correct') in b['options']):
            fejl.append(f'{k}: bonusspørgsmålet skal have spørgsmål, forklaring og tre svarmuligheder med det rigtige')
        if not (be.get('q') and be.get('why') and len(be.get('options', [])) == 3 and be.get('correct') in be['options']):
            fejl.append(f'{k}: bonusspørgsmålet mangler på engelsk')
        antal = {}
        for h in p['hands']:
            if h['situation'] == k:
                antal[h['correct']] = antal.get(h['correct'], 0) + 1
        if set(antal) != svarene:
            fejl.append(f'{k} ({vis(forl)}): puljens svar er {sorted(antal)}, reglerne giver {sorted(svarene)}')
        for c, n in sorted(antal.items()):
            if n < PER_CALL_MIN:
                fejl.append(f'{k} ({vis(forl)}): {c} har {n} {"hånd" if n == 1 else "hænder"}, mindst {PER_CALL_MIN}')
    if familier != set(FAMILIER):
        fejl.append(f'puljen mangler situationerne {sorted(set(FAMILIER) - familier)}')
    for familie, q in BONUS.items():
        if not any(v.get('bonus', {}).get('q') == q for forl, (k, v) in sit.items()
                   if forl in SITUATIONER and SITUATIONER[forl][0] == familie):
            fejl.append(f'{familie}: bonusspørgsmålet "{q}" mangler')
    with tempfile.TemporaryDirectory() as mappe:
        ud = io.StringIO()
        with contextlib.redirect_stdout(ud):
            build_pools.CONVENTIONS['multi-2ru'].export_pool(os.path.join(mappe, 'multi-2ru.json'))
        for linje in ud.getvalue().splitlines():
            if 'Advarsel: kun' in linje:
                fejl.append(f'build_pools.py: {linje.strip()}')
    return fejl


def punkt4():
    fejl = []
    m, p = modul(), pulje()
    for i, h in enumerate(p['hands'], 1):
        k = h.get('situation')
        v = p['situations'].get(k)
        if not v:
            fejl.append(f'hånd {i}: situationen {k} findes ikke')
            continue
        forl = forloeb(v['auction'])
        if forl not in SITUATIONER:
            continue  # meldt under punkt 3
        L, hp = info(h['hand'])
        if sum(L.values()) != 13 or hp != h.get('hp'):
            fejl.append(f'hånd {i} ({k}): {sum(L.values())} kort og {hp} hp (puljen siger {h.get("hp")} hp)')
        regel = SITUATIONER[forl][4](h['hand'])
        if regel is None:
            fejl.append(f'hånd {i} ({k}, {vis_haand(h["hand"])}): ligger uden for situationens regler (puljen siger {h["correct"]})')
        elif regel != h['correct']:
            fejl.append(f'hånd {i} ({k}, {vis_haand(h["hand"])}): puljen siger {h["correct"]}, reglerne siger {regel}')
        res = m.CLASSIFIERS[k](h['hand'], hp) if k in m.CLASSIFIERS else None
        if not res or res[0] != h['correct']:
            fejl.append(f'hånd {i} ({k}): puljen siger {h["correct"]}, modulet siger {res[0] if res else None}')
        if h['correct'] not in v['calls']:
            fejl.append(f'hånd {i} ({k}): {h["correct"]} er ikke en af situationens meldinger')
        if not h.get('why') or not (h.get('en') or {}).get('why'):
            fejl.append(f'hånd {i} ({k}): forklaringen mangler på dansk eller engelsk')
    return fejl


def nords_haand(h):
    """Nords hånd, når puljen har hele spil: feltet nord eller deal/spil med N eller Nord."""
    if isinstance(h.get('nord'), dict):
        return h['nord']
    for felt in ('deal', 'spil'):
        d = h.get(felt)
        if isinstance(d, dict):
            for n in ('N', 'Nord', 'nord'):
                if isinstance(d.get(n), dict):
                    return d[n]
    return None


def punkt5():
    fejl = []
    p = pulje()
    for i, h in enumerate(p['hands'], 1):
        v = p['situations'].get(h.get('situation')) or {}
        forl = forloeb(v.get('auction', []))
        aabner = forl and forl[0] == ('Dig', '2♦')
        if (aabner or (forl == () and h.get('correct') == '2♦')) and not gyldig_2ru(h['hand']):
            fejl.append(f'hånd {i} ({h["situation"]}, {vis_haand(h["hand"])}): ikke en gyldig 2♦-åbning efter J')
        nord = nords_haand(h)
        if forl and forl[0] == ('Makker', '2♦') and nord is not None and not gyldig_2ru(nord):
            fejl.append(f'hånd {i} ({h["situation"]}): Nords hånd {vis_haand(nord)} er ikke en gyldig 2♦-åbning efter J')
    return fejl


def punkt6():
    fejl = []
    r = subprocess.run(['git', 'show', f'{TAG}:data/konventioner.json'], cwd=ROD, capture_output=True)
    if r.returncode:
        return fejl  # tagget findes ikke (fx i en kopi uden tags); punktet springes over
    if subprocess.run(['git', 'cat-file', '-e', f'{FLETTET}^{{commit}}'], cwd=ROD, capture_output=True).returncode:
        return fejl  # flettecommitten findes ikke; punktet springes over
    fl = subprocess.run(['git', 'show', f'{FLETTET}:data/konventioner.json'], cwd=ROD, capture_output=True)
    fletnu = json.loads(fl.stdout.decode('utf-8'))
    post = [x for x in fletnu if x['id'] == 'multi-2ru']
    if len(post) != 1:
        fejl.append(f'data/konventioner.json i {FLETTET}: {len(post)} poster med id multi-2ru, skal være 1')
    elif post[0] != POST:
        forskel = sorted(k for k in set(POST) | set(post[0]) if POST.get(k) != post[0].get(k))
        fejl.append(f'data/konventioner.json i {FLETTET}: posten multi-2ru er ikke som i specen (felterne {", ".join(forskel)})')
    if 'ff-multi-2ru' in [x['id'] for x in fletnu]:
        fejl.append(f'data/konventioner.json i {FLETTET}: posten ff-multi-2ru står der stadig')
    foer = [x for x in json.loads(r.stdout.decode('utf-8')) if x['id'] != 'ff-multi-2ru']
    efter = [x for x in fletnu if x['id'] not in ('multi-2ru', 'ff-multi-2ru')]
    if foer != efter:
        aendret = sorted({x['id'] for x in foer if x not in efter} | {x['id'] for x in efter if x not in foer})
        fejl.append(f'data/konventioner.json: de øvrige poster er ændret: {", ".join(aendret) or "rækkefølgen"}')
    r = subprocess.run(['git', 'diff', '--name-only', TAG, FLETTET, '--', *FREDET], cwd=ROD, capture_output=True, text=True)
    for f in r.stdout.split():
        fejl.append(f'{f} er ændret, men specen tillader intet der')
    return fejl


def punkt7():
    fejl = []
    sti = ROD / 'data' / 'kort' / 'multi-2ru.json'
    if not sti.exists():
        return ['data/kort/multi-2ru.json findes ikke']
    k = json.loads(sti.read_text(encoding='utf-8'))
    if k.get('type') != 'melding':
        fejl.append('kortet: type skal være "melding"')
    if k.get('traener') != {'url': 'traener.html?k=multi-2ru', 'pool': 'pools/multi-2ru.json'}:
        fejl.append(f'kortet: traener er {k.get("traener")}, specen siger url traener.html?k=multi-2ru og pool pools/multi-2ru.json')
    for felt in ('meldinger', 'fortsaettelser', 'indmelding', 'eksempler', 'faldgruber', 'aabne'):
        if not k.get(felt):
            fejl.append(f'kortet: afsnittet {felt} er tomt')
    eks = [(forloeb(e['auction'][:-1]), e.get('svar')) for e in k.get('eksempler', [])]
    for navn, forl, s in KORT_EKSEMPLER:
        if (forl, s) not in eks:
            fejl.append(f'kortet: intet eksempel med samme meldeforløb og svar som {navn} ({vis(forl)} {s})')
    rc, ud = koer('tools/tjek_konventionskort.py')
    if rc or 'i orden' not in ud:
        fejl.append('tools/tjek_konventionskort.py: ' + ud.strip().replace('\n', ' | ')[:600])
    rc, ud = koer('tools/tjek_kort_eksempler.py', 'multi-2ru')
    if rc or 'Advarsel' in ud or '(0 advarsler)' not in ud:
        sidste = ud.strip().splitlines()[-1] if ud.strip() else 'intet output'
        fejl.append(f'tools/tjek_kort_eksempler.py multi-2ru: {sidste[:600]}')
    return fejl


def punkt8():
    fejl = []
    for script in ('tools/tjek_fagord.py', 'tools/tjek_bydeform.py'):
        rc, ud = koer(script)
        if rc or 'i orden' not in ud:
            fejl.append(f'{script}: ' + ud.strip().replace('\n', ' | ')[:600])
    rc, ud = koer('tools/tjek_sprog.py')
    if rc:
        fejl.append('tools/tjek_sprog.py: ' + ud.strip().replace('\n', ' | ')[-600:])
    return fejl


PUNKTER = [
    (1, 'Facit-eksemplerne og åbningshænderne', punkt1),
    (2, 'ret, spm og spm2 for alle kombinationer', punkt2),
    (3, 'Puljens situationer, meldinger og antal', punkt3),
    (4, 'Hver hånd i puljen efter reglerne', punkt4),
    (5, 'Åbnerhænderne er gyldige 2♦-åbninger efter J', punkt5),
    (6, 'Posten multi-2ru, ff-multi-2ru væk og resten uændret', punkt6),
    (7, 'Konventionskortet og dets tjek', punkt7),
    (8, 'Fagord, beskrivende form og sprogtesten', punkt8),
]


def main():
    roede = []
    for nr, navn, fn in PUNKTER:
        try:
            fejl = fn()
        except Exception as e:  # noqa: BLE001  et punkt, der ikke kan køres endnu, er rødt
            fejl = [f'{type(e).__name__}: {e}']
        print(f'{nr}. {navn}: {"i orden" if not fejl else "RØD"}')
        for f in fejl[:20]:
            print(f'   - {f}')
        if len(fejl) > 20:
            print(f'   … og {len(fejl) - 20} fejl mere')
        if fejl:
            roede.append(nr)
    if roede:
        print(f'Multi 2♦: rød ({len(roede)} af {len(PUNKTER)} punkter fejler: {", ".join(map(str, roede))}).')
        return 1
    print(f'Multi 2♦: i orden ({len(PUNKTER)} af {len(PUNKTER)} punkter).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
