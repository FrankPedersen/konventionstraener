"""Accepttest for SPEC-muiderberg.md: træneren Muiderberg (Bikini) 2♥/2♠ efter Franks tekst (F), med hullerne udfyldt
fra dokumentet "Ruder Multi" (W).

Kør fra repoets rod:  python3 tools/tjek_muiderberg.py

Testen tjekker specens syv punkter og skriver for hvert, om det er i orden eller rødt:
1. Franks eksempel ♠KBT75 ♥73 ♦98 ♣KD65 giver 2♠ med reglerne her og med dealer/muiderberg.py's bedømmelse. Grænserne
   i modulet er de samme som i specens kodeblok og står under overskriften
   "# --- Grænser, som kilderne ikke giver tal for – ret dem her".
2. ret og spm giver tabellens svar for alle kombinationer af major, minor og minimum eller maksimum.
3. Puljen har alle fire situationer med specens meldeforløb, roller og meldinger og et bonusspørgsmål på begge sprog;
   hver melding, der genereres, har mindst 7 hænder, og build_pools.py skriver ingen "Advarsel: kun …".
4. For hver hånd er correct det svar, reglerne her giver (og modulet giver). Hver svarhånd i svar rammer en regel, og
   alle åbnerhænder i svar, ret og spm er gyldige Muiderberg-åbninger (i svar: åbners hånd, når puljen har den).
5. Posten muiderberg står i data/konventioner.json som i specen, ff-muiderberg er væk, og de øvrige poster og de filer,
   specen ikke tillader ændret, er som i tagget v-foer-muiderberg.
6. Kortet data/kort/muiderberg.json har de seks afsnit, traener-feltet og Franks eksempel; på multi-2ru-kortet er kun
   Bikini-linjen under "Åbne spørgsmål" erstattet af en henvisning til Muiderberg. tjek_konventionskort.py,
   tjek_kort_eksempler.py muiderberg (0 advarsler), tjek_fagord.py, tjek_bydeform.py og tjek_sprog.py melder "i orden".
7. Tabellen "Tekster til gennemgang" findes under Afklaret med en række pr. situation og melding i puljen, et
   bonusspørgsmål pr. situation og kortets faldgruber, og hver række har en kilde (F, W eller "(tilføjelse)").

Reglerne er skrevet her igen direkte fra specen, uafhængigt af modulet; tallene kommer fra specens kodeblok under
Grænser. traener.html tager meldeforløbet fra situationen, så svar, ret og spm har én situation pr. åbning (2♥ og 2♠)
i puljen. Testen finder situationerne ud fra meldeforløbet, ikke ud fra navnene.

Fortolkninger (specen, Afklaret, Session 1):
- En Muiderberg-hånd har præcis fem kort i majoren, højst tre i den anden major, 4–5 kort i én minor og højst tre i
  den anden. Med to minorer på 4+ kort er minoren ikke entydig, og hånden genereres ikke.
- 1♥/1♠ (11–15 hp) og pas (0–4 hp) har samme fordeling; 2♦ er en gyldig Multi-åbning efter multi-2ru's regel.
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

TAG = 'v-foer-muiderberg'
ID = 'muiderberg'
HP = {14: 4, 13: 3, 12: 2, 11: 1}
SYM = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
NAVN = {'S': 'spar', 'H': 'hjerter', 'D': 'ruder', 'C': 'klør'}
OVERSKRIFT = '# --- Grænser, som kilderne ikke giver tal for – ret dem her'
PER_CALL_MIN = 7
FREDET = ['viden/2-over-1-makker2.html', 'dealer/multi_2ru.py', 'traener.html', 'dealer/core.py']


# ---------- Specen: grænserne og posten ----------

def spec_tekst():
    for sti in (ROD / 'SPEC-muiderberg.md', ROD / 'docs' / 'specs' / 'SPEC-muiderberg.md'):
        if sti.exists():
            return sti.read_text(encoding='utf-8')
    raise FileNotFoundError('SPEC-muiderberg.md findes hverken i roden eller i docs/specs/')


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
    """'KBT75 73 98 KD65' (♠ ♥ ♦ ♣) → {'S': [13, 11, 10, 7, 5], …}. – er en renonce."""
    vaerdi = {'E': 14, 'K': 13, 'D': 12, 'B': 11, 'T': 10}
    farver = s.split()
    assert len(farver) == 4, s
    return {f: sorted((vaerdi.get(c) or int(c) for c in x if c not in '–-'), reverse=True) for f, x in zip('SHDC', farver)}


def info(h):
    L = {s: len(h[s]) for s in 'SHDC'}
    hp = sum(HP.get(c, 0) for s in 'SHDC' for c in h[s])
    return L, hp


def mellem(x, ab):
    return ab[0] <= x <= ab[1]


def anden(M):
    return 'S' if M == 'H' else 'H'


def vis_haand(h):
    navn = {14: 'E', 13: 'K', 12: 'D', 11: 'B', 10: 'T'}
    return ' '.join(SYM[s] + (''.join(navn.get(c, str(c)) for c in h[s]) or '–') for s in 'SHDC')


# ---------- Reglerne (specen, Regler og Grænser) ----------

def fordeling(h):
    """(major, minor) for en Muiderberg-fordeling, ellers None: præcis fem i majoren, højst tre i den anden major og
    4–5 kort i én minor (den anden højst tre)."""
    L, _ = info(h)
    for M in 'HS':
        if L[M] == 5 and L[anden(M)] <= 3:
            minorer = [m for m in 'CD' if L[m] >= 4]
            if len(minorer) == 1 and L[minorer[0]] <= 5:
                return M, minorer[0]
    return None


def gyldig(h):
    """En gyldig Muiderberg-åbning: fordelingen ovenfor og 5–10 hp."""
    return fordeling(h) is not None and 5 <= info(h)[1] <= 10


def gyldig_multi(h):
    """multi-2ru: præcis seks kort i én major, højst tre i den anden, 5–10 hp og højst ét es."""
    L, hp = info(h)
    esser = sum(1 for s in 'SHDC' if 14 in h[s])
    return any(L[M] == 6 and L[anden(M)] <= 3 for M in 'HS') and 5 <= hp <= 10 and esser <= 1


def aabning(h):
    if gyldig_multi(h):
        return '2♦'
    f = fordeling(h)
    if not f:
        return None
    _, hp = info(h)
    if hp <= 4:
        return 'Pas'
    if hp <= 10:
        return '2' + SYM[f[0]]
    if hp <= 15:
        return '1' + SYM[f[0]]
    return None


def svar(h, M):
    """2M – Pas – ?  Første regel, der passer (specen, Grænser). None: hånden rammer ingen regel."""
    L, hp = info(h)
    st = L[M]
    u = g('UDGANG')
    if st >= u['stoette'] and mellem(hp, u['hp']):
        return '4' + SYM[M]
    u = g('SPAER_UDGANG')
    if st >= u['stoette'] and mellem(hp, u['hp']):
        return '4' + SYM[M]
    if hp >= g('SPOERG', 'hp'):
        return '2NT'
    u = g('SPOERG_INVIT')
    if st >= u['stoette'] and mellem(hp, u['hp']):
        return '2NT'
    u = g('ENKELTLOEFT')
    if st == u['stoette'] and mellem(hp, u['hp']):
        return '3' + SYM[M]
    u = g('MINOR_RET')
    if st <= u['major_max'] and L['C'] >= u['minor'] and L['D'] >= u['minor'] and hp <= u['hp_max']:
        return '3♣'
    if st >= 2 and hp <= 10:  # Pas: 2+ i åbners major og højst 10 hp
        return 'Pas'
    return None


def ret(h, M):
    """2M – Pas – 3♣ – Pas – ?  Pas med klør, 3♦ med ruder."""
    if not gyldig(h) or fordeling(h)[0] != M:
        return None
    return 'Pas' if fordeling(h)[1] == 'C' else '3♦'


def spm(h, M):
    """2M – Pas – 2NT – Pas – ?  3♣ min/klør, 3♦ min/ruder, 3♥ maks/klør, 3♠ maks/ruder."""
    if not gyldig(h) or fordeling(h)[0] != M:
        return None
    _, hp = info(h)
    minor = fordeling(h)[1]
    if mellem(hp, g('MAX_HP')):
        return '3♥' if minor == 'C' else '3♠'
    return '3♣' if minor == 'C' else '3♦'


TABEL = {  # specens tabeller: (situation, minor, maksimum) → svar
    ('ret', 'C', False): 'Pas', ('ret', 'C', True): 'Pas', ('ret', 'D', False): '3♦', ('ret', 'D', True): '3♦',
    ('spm', 'C', False): '3♣', ('spm', 'D', False): '3♦', ('spm', 'C', True): '3♥', ('spm', 'D', True): '3♠',
}


# ---------- Meldeforløbene (specen, Situationer) ----------

PAS = ('Modstander', 'Pas')
SVAR_CALLS = ['Pas', '2♠', '2NT', '3♣', '3♦', '3♥', '3♠', '4♥', '4♠']

SITUATIONER = {}  # meldeforløb (tuple) → (familie, rolle, meldinger, svar reglerne kan give, regel, åbners major)
SITUATIONER[()] = ('aabning', 'Åbner', ['Pas', '1♥', '1♠', '2♦', '2♥', '2♠'], {'Pas', '1♥', '1♠', '2♦', '2♥', '2♠'},
                   aabning, None)
for _M in 'HS':
    _aab = '2' + SYM[_M]
    SITUATIONER[(('Makker', _aab), PAS)] = (
        'svar', 'Svarer', [c for c in SVAR_CALLS if not (_M == 'S' and c == '2♠')],
        {'Pas', '2NT', '3♣', '3' + SYM[_M], '4' + SYM[_M]}, (lambda M: lambda h: svar(h, M))(_M), _M)
    SITUATIONER[(('Dig', _aab), PAS, ('Makker', '3♣'), PAS)] = (
        'ret', 'Åbner', ['Pas', '3♦', '3' + SYM[_M]], {'Pas', '3♦'}, (lambda M: lambda h: ret(h, M))(_M), _M)
    SITUATIONER[(('Dig', _aab), PAS, ('Makker', '2NT'), PAS)] = (
        'spm', 'Åbner', ['3♣', '3♦', '3♥', '3♠', '3NT'], {'3♣', '3♦', '3♥', '3♠'},
        (lambda M: lambda h: spm(h, M))(_M), _M)
FAMILIER = ['aabning', 'svar', 'ret', 'spm']


def forloeb(auction):
    return tuple(tuple(x) for x in auction)


def vis(forl):
    return ' – '.join(c for _, c in forl) + (' – ?' if forl else '?')


FRANK = ('Franks eksempel', (), 'KBT75 73 98 KD65', '2♠')


# ---------- Modulet og puljen ----------

_modul = None


def modul():
    global _modul
    if _modul is None:
        if not (ROD / 'dealer' / 'muiderberg.py').exists():
            raise RuntimeError('dealer/muiderberg.py findes ikke endnu')
        from dealer import muiderberg
        _modul = muiderberg
    return _modul


def noegle(forl):
    """Modulets situation med dette meldeforløb."""
    ns = [k for k, v in modul().SITUATIONS.items() if forloeb(v['auction']) == forl]
    if len(ns) != 1:
        raise RuntimeError(f'modulet har {len(ns)} situationer med meldeforløbet {vis(forl)}')
    return ns[0]


def bedoem(forl, h):
    res = modul().CLASSIFIERS[noegle(forl)](h, info(h)[1])
    return res[0] if res else None


def pulje():
    sti = ROD / 'pools' / f'{ID}.json'
    if not sti.exists():
        raise RuntimeError(f'pools/{ID}.json findes ikke endnu')
    return json.loads(sti.read_text(encoding='utf-8'))


def koer(*args):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    r = subprocess.run([sys.executable, *args], cwd=ROD, capture_output=True, text=True, encoding='utf-8', env=env)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def git_show(sti):
    r = subprocess.run(['git', 'show', f'{TAG}:{sti}'], cwd=ROD, capture_output=True)
    if r.returncode:
        raise RuntimeError(f'git show {TAG}:{sti} fejlede (findes tagget?)')
    return r.stdout.decode('utf-8')


# ---------- De syv punkter ----------

def punkt1():
    fejl = []
    navn, forl, kort, facit = FRANK
    h = haand(kort)
    if aabning(h) != facit:
        fejl.append(f'{navn}: reglerne i testen giver {aabning(h)}, facit er {facit} (testen er forkert)')
    m = modul()
    kilde = (ROD / 'dealer' / 'muiderberg.py').read_text(encoding='utf-8')
    if OVERSKRIFT not in kilde:
        fejl.append(f'dealer/muiderberg.py: overskriften "{OVERSKRIFT}" mangler')
    for n in NAVNE:
        if not hasattr(m, n):
            fejl.append(f'dealer/muiderberg.py: konstanten {n} mangler')
        elif getattr(m, n) != G[n]:
            fejl.append(f'dealer/muiderberg.py: {n} = {getattr(m, n)!r}, specen siger {G[n]!r}')
    s = bedoem(forl, h)
    if s != facit:
        fejl.append(f'{navn} ({kort}): modulet giver {s}, facit er {facit}')
    return fejl


def aabnerhaender():
    """To gyldige Muiderberg-åbninger for hver major, minor og hvert hp fra 5 til 10 (samme frø hver gang)."""
    rnd = random.Random(2611)
    ud = []
    for M in 'HS':
        for minor in 'CD':
            for maal in range(5, 11):
                fundet = 0
                while fundet < 2:
                    lm = rnd.randint(4, 5)
                    la = rnd.randint(max(0, 8 - lm - 3), min(3, 8 - lm))
                    lo = 8 - lm - la
                    if lo > 3:
                        continue
                    L = {M: 5, anden(M): la, minor: lm, ('D' if minor == 'C' else 'C'): lo}
                    h = {s: sorted(rnd.sample(range(2, 15), L[s]), reverse=True) for s in 'SHDC'}
                    if info(h)[1] == maal and gyldig(h) and fordeling(h) == (M, minor):
                        ud.append(h)
                        fundet += 1
    return ud


def punkt2():
    fejl = []
    haender = aabnerhaender()
    sete = set()
    for forl, (familie, _, _, _, regel, M) in SITUATIONER.items():
        if familie not in ('ret', 'spm'):
            continue
        for h in haender:
            if fordeling(h)[0] != M:
                continue
            minor, hp = fordeling(h)[1], info(h)[1]
            mx = mellem(hp, g('MAX_HP'))
            tabel = TABEL[(familie, minor, mx)]
            if regel(h) != tabel:
                fejl.append(f'{familie} ({vis(forl)}): reglerne i testen giver {regel(h)}, tabellen siger {tabel}')
            faktisk = bedoem(forl, h)
            if faktisk != tabel and (forl, minor, mx) not in sete:
                sete.add((forl, minor, mx))
                fejl.append(f'{familie} ({vis(forl)}), {NAVN[minor]} og {"maksimum" if mx else "minimum"} '
                            f'({vis_haand(h)}, {hp} hp): modulet giver {faktisk}, tabellen siger {tabel}')
    return fejl


def punkt3():
    fejl = []
    m, p = modul(), pulje()
    import build_pools
    if build_pools.CONVENTIONS.get(ID) is not m:
        fejl.append(f'build_pools.py: "{ID}": muiderberg mangler i CONVENTIONS')
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
    for forl, (familie, rolle, calls, svarene, _, _) in SITUATIONER.items():
        if forl not in sit:
            fejl.append(f'{familie}: puljen mangler meldeforløbet {vis(forl)}')
            continue
        familier.add(familie)
        k, v = sit[forl]
        if v.get('rolle') != rolle:
            fejl.append(f'{k}: rollen er {v.get("rolle")}, specen siger {rolle}')
        if set(v.get('calls', [])) != set(calls) or len(v.get('calls', [])) != len(calls):
            fejl.append(f'{k} ({vis(forl)}): meldingerne er {v.get("calls")}, specen siger {calls}')
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
    with tempfile.TemporaryDirectory() as mappe:
        ud = io.StringIO()
        with contextlib.redirect_stdout(ud):
            build_pools.CONVENTIONS[ID].export_pool(os.path.join(mappe, f'{ID}.json'))
        for linje in ud.getvalue().splitlines():
            if 'Advarsel: kun' in linje:
                fejl.append(f'build_pools.py: {linje.strip()}')
    return fejl


def aabners_haand(h):
    """Åbners hånd i svar, når puljen har den: feltet nord eller deal/spil med N eller Nord."""
    if isinstance(h.get('nord'), dict):
        return h['nord']
    for felt in ('deal', 'spil'):
        d = h.get(felt)
        if isinstance(d, dict):
            for n in ('N', 'Nord', 'nord'):
                if isinstance(d.get(n), dict):
                    return d[n]
    return None


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
        familie, _, _, _, regel_fn, M = SITUATIONER[forl]
        L, hp = info(h['hand'])
        if sum(L.values()) != 13 or hp != h.get('hp'):
            fejl.append(f'hånd {i} ({k}): {sum(L.values())} kort og {hp} hp (puljen siger {h.get("hp")} hp)')
        regel = regel_fn(h['hand'])
        if regel is None:
            fejl.append(f'hånd {i} ({k}, {vis_haand(h["hand"])}): rammer ingen regel (puljen siger {h["correct"]})')
        elif regel != h['correct']:
            fejl.append(f'hånd {i} ({k}, {vis_haand(h["hand"])}): puljen siger {h["correct"]}, reglerne siger {regel}')
        res = m.CLASSIFIERS[k](h['hand'], hp) if k in m.CLASSIFIERS else None
        if not res or res[0] != h['correct']:
            fejl.append(f'hånd {i} ({k}): puljen siger {h["correct"]}, modulet siger {res[0] if res else None}')
        if h['correct'] not in v['calls']:
            fejl.append(f'hånd {i} ({k}): {h["correct"]} er ikke en af situationens meldinger')
        if not h.get('why') or not (h.get('en') or {}).get('why'):
            fejl.append(f'hånd {i} ({k}): forklaringen mangler på dansk eller engelsk')
        if familie in ('ret', 'spm') and not (gyldig(h['hand']) and fordeling(h['hand'])[0] == M):
            fejl.append(f'hånd {i} ({k}, {vis_haand(h["hand"])}): ikke en gyldig Muiderberg-åbning på 2{SYM[M]}')
        if familie == 'svar':
            aab = aabners_haand(h)
            if aab is not None and not (gyldig(aab) and fordeling(aab)[0] == M):
                fejl.append(f'hånd {i} ({k}): åbners hånd {vis_haand(aab)} er ikke en gyldig Muiderberg-åbning')
        if familie == 'aabning' and h['correct'] in ('2♥', '2♠') and not gyldig(h['hand']):
            fejl.append(f'hånd {i} ({k}, {vis_haand(h["hand"])}): {h["correct"]} er ikke en gyldig Muiderberg-åbning')
    return fejl


def punkt5():
    fejl = []
    nu = json.loads((ROD / 'data' / 'konventioner.json').read_text(encoding='utf-8'))
    ids = [x['id'] for x in nu]
    post = [x for x in nu if x['id'] == ID]
    if len(post) != 1:
        fejl.append(f'data/konventioner.json: {len(post)} poster med id {ID}, skal være 1')
    elif post[0] != POST:
        forskel = sorted(k for k in set(POST) | set(post[0]) if POST.get(k) != post[0].get(k))
        fejl.append(f'data/konventioner.json: posten {ID} er ikke som i specen (felterne {", ".join(forskel)})')
    if 'ff-muiderberg' in ids:
        fejl.append('data/konventioner.json: posten ff-muiderberg står der stadig')
    foer = [x for x in json.loads(git_show('data/konventioner.json')) if x['id'] != 'ff-muiderberg']
    efter = [x for x in nu if x['id'] not in (ID, 'ff-muiderberg')]
    if foer != efter:
        aendret = sorted({x['id'] for x in foer if x not in efter} | {x['id'] for x in efter if x not in foer})
        fejl.append(f'data/konventioner.json: de øvrige poster er ændret: {", ".join(aendret) or "rækkefølgen"}')
    r = subprocess.run(['git', 'diff', '--name-only', TAG, '--', *FREDET], cwd=ROD, capture_output=True, text=True)
    for f in r.stdout.split():
        fejl.append(f'{f} er ændret, men specen tillader intet der')
    return fejl


def punkt6():
    fejl = []
    sti = ROD / 'data' / 'kort' / f'{ID}.json'
    if not sti.exists():
        return [f'data/kort/{ID}.json findes ikke']
    k = json.loads(sti.read_text(encoding='utf-8'))
    if k.get('type') != 'melding':
        fejl.append('kortet: type skal være "melding"')
    if k.get('traener') != {'url': f'traener.html?k={ID}', 'pool': f'pools/{ID}.json'}:
        fejl.append(f'kortet: traener er {k.get("traener")}, specen siger url traener.html?k={ID} og pool pools/{ID}.json')
    for felt in ('meldinger', 'fortsaettelser', 'indmelding', 'eksempler', 'faldgruber', 'aabne'):
        if not k.get(felt):
            fejl.append(f'kortet: afsnittet {felt} er tomt')
    frank = haand(FRANK[2])
    if not any(e.get('haand') == frank and e.get('svar') == FRANK[3] and forloeb(e['auction'][:-1]) == FRANK[1]
               for e in k.get('eksempler', [])):
        fejl.append('kortet: Franks eksempel (♠KBT75 ♥73 ♦98 ♣KD65 → 2♠) står ikke under Eksempler')
    tekst = json.dumps(k, ensure_ascii=False)
    if 'multi-2ru' not in tekst and 'Multi 2♦' not in tekst:
        fejl.append('kortet: nævner ikke, at Muiderberg forudsætter Multi 2♦ (multi-2ru)')
    # multi-2ru-kortet: kun Bikini-linjen under Åbne spørgsmål er erstattet af en henvisning til Muiderberg
    mnu = json.loads((ROD / 'data' / 'kort' / 'multi-2ru.json').read_text(encoding='utf-8'))
    mfoer = json.loads(git_show('data/kort/multi-2ru.json'))
    for felt in sorted(set(mnu) | set(mfoer)):
        if felt != 'aabne' and mnu.get(felt) != mfoer.get(felt):
            fejl.append(f'multi-2ru-kortet: feltet {felt} er ændret, specen tillader kun Bikini-linjen')
    a_nu, a_foer = mnu.get('aabne', []), mfoer.get('aabne', [])
    bikini = [i for i, x in enumerate(a_foer) if 'Bikini' in x]
    if len(a_nu) != len(a_foer) or len(bikini) != 1:
        fejl.append('multi-2ru-kortet: Åbne spørgsmål skal have lige så mange linjer som før, og én med Bikini')
    else:
        for i, (x, y) in enumerate(zip(a_foer, a_nu)):
            if i != bikini[0] and x != y:
                fejl.append(f'multi-2ru-kortet: Åbne spørgsmål, linje {i + 1} er ændret')
        ny = a_nu[bikini[0]]
        if ny == a_foer[bikini[0]] or 'Muiderberg' not in ny or 'Bikini (2♥/2♠' in ny:
            fejl.append('multi-2ru-kortet: Bikini-linjen er ikke erstattet af en henvisning til Muiderberg-kortet')
    rc, ud = koer('tools/tjek_konventionskort.py')
    if rc or 'i orden' not in ud:
        fejl.append('tools/tjek_konventionskort.py: ' + ud.strip().replace('\n', ' | ')[:600])
    rc, ud = koer('tools/tjek_kort_eksempler.py', ID)
    if rc or 'Advarsel' in ud or '(0 advarsler)' not in ud:
        sidste = ud.strip().splitlines()[-1] if ud.strip() else 'intet output'
        fejl.append(f'tools/tjek_kort_eksempler.py {ID}: {sidste[:600]}')
    for script in ('tools/tjek_fagord.py', 'tools/tjek_bydeform.py'):
        rc, ud = koer(script)
        if rc or 'i orden' not in ud:
            fejl.append(f'{script}: ' + ud.strip().replace('\n', ' | ')[:600])
    rc, ud = koer('tools/tjek_sprog.py')
    if rc:
        fejl.append('tools/tjek_sprog.py: ' + ud.strip().replace('\n', ' | ')[-600:])
    return fejl


def tabel_raekker():
    """Rækkerne i tabellen under en overskrift "Tekster til gennemgang" efter "## Afklaret" som lister af celler."""
    afklaret = SPEC.find('\n## Afklaret')
    if afklaret < 0:
        raise RuntimeError('specen har intet afsnit "## Afklaret"')
    m = re.search(r'\n#{3,4} Tekster til gennemgang[^\n]*\n', SPEC[afklaret:])
    if not m:
        raise RuntimeError('tabellen "Tekster til gennemgang" findes ikke under Afklaret')
    linjer = SPEC[afklaret + m.end():].split('\n')
    start = next((i for i, x in enumerate(linjer) if x.startswith('|')), None)
    if start is None:
        raise RuntimeError('afsnittet "Tekster til gennemgang" har ingen tabel')
    raekker = []
    for x in linjer[start:]:
        if not x.startswith('|'):
            break
        raekker.append([c.strip() for c in x.strip().strip('|').split('|')])
    return raekker[0], [r for r in raekker[2:]]


def punkt7():
    fejl = []
    hoved, raekker = tabel_raekker()
    if [h.lower() for h in hoved] != ['situation', 'melding', 'dansk', 'engelsk', 'kilde']:
        fejl.append(f'tabellen: kolonnerne er {hoved}, skal være Situation, Melding, Dansk, Engelsk og Kilde')
        return fejl
    for i, r in enumerate(raekker, 1):
        if len(r) != 5:
            fejl.append(f'tabellen, række {i}: {len(r)} celler, skal være 5')
        elif not re.search(r'\bF\b|\bW\b|tilføjelse', r[4]):
            fejl.append(f'tabellen, række {i} ({r[0]} {r[1]}): kilden mangler (F, W eller "(tilføjelse)")')
    p = pulje()
    for k, v in p['situations'].items():
        svarene = sorted({h['correct'] for h in p['hands'] if h['situation'] == k})
        for c in svarene:
            if not any(f'`{k}`' in r[0] and r[1] == c for r in raekker if len(r) == 5):
                fejl.append(f'tabellen: ingen række for {k} og {c}')
        q = (v.get('bonus') or {}).get('q', '')
        if not any(f'`{k}`' in r[0] and r[1] == 'Bonusspørgsmål' and q in r[2] for r in raekker if len(r) == 5):
            fejl.append(f'tabellen: bonusspørgsmålet for {k} mangler ("{q}")')
    sti = ROD / 'data' / 'kort' / f'{ID}.json'
    if sti.exists():
        for fg in json.loads(sti.read_text(encoding='utf-8')).get('faldgruber', []):
            if not any(r[1] == 'Faldgrube' and fg in r[2] for r in raekker if len(r) == 5):
                fejl.append(f'tabellen: faldgruben "{fg}" mangler')
    return fejl


PUNKTER = [
    (1, 'Franks eksempel giver 2♠', punkt1),
    (2, 'ret og spm for alle kombinationer', punkt2),
    (3, 'Puljens situationer, meldinger og antal', punkt3),
    (4, 'Hver hånd i puljen efter reglerne', punkt4),
    (5, 'Posten muiderberg, ff-muiderberg væk og resten uændret', punkt5),
    (6, 'Kortet, multi-2ru-kortet og tjekkene', punkt6),
    (7, 'Tabellen "Tekster til gennemgang"', punkt7),
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
        print(f'Muiderberg: rød ({len(roede)} af {len(PUNKTER)} punkter fejler: {", ".join(map(str, roede))}).')
        return 1
    print(f'Muiderberg: i orden ({len(PUNKTER)} af {len(PUNKTER)} punkter).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
