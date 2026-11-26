"""Accepttest for SPEC-modspilsaftaler.md: modspilsaftalerne som konventionskort uden makker, med alle Modspils
varianter, en indstilling fælles med Modspil og en quiz om aftalernes indhold.

Kør fra repoets rod:  python3 tools/tjek_modspilsaftaler.py

Testen tjekker specens ni punkter og skriver for hvert, om det er i orden eller rødt:
1. data/modspilsaftaler.json er indholdsmæssigt lig ../Fordelingstræneren/src/modspil/content/metoder.json.
2. Der er 7 kort ms-<kategori>, ét pr. kategori, og hvert kort har en gruppe pr. metode med metodens navn og en
   række "Aftalen", hvis tekst er metodens aftale ordret (kortene er på dansk som de andre kort; den engelske aftale
   bruges i indstillingen og quizzen).
3. Kortsiden har linket "Træn i Modspil" til /fordelingstraeneren/#modspil for ms-kortene, og hvert kort henviser til
   de eksisterende kort Markeringer, Udspil eller Lavinthal, hvor det passer.
4. data/modspilsaftaler-quiz.json har 2 spørgsmål pr. metode med ét rigtigt og to forkerte svar og en forklaring på
   begge sprog, og intet spørgsmål har en hånd.
5. Hver metode har mindst ét eksempel. Udspilseksemplerne (udspil mod sans og farve og honnørudspil) giver det kort,
   modellen i ../Fordelingstræneren giver (tools/kontrol_modspilsaftaler.mjs).
6. Indstillingen (assets/modspilsaftaler.js, node --test tools/modspilsaftaler.test.mjs): uden gemt tilstand Standard;
   et valg skriver kun profil og metoder i modspil:v1 og bevarer resten; ugyldige data overskrives ikke.
7. Kortsiden viser den valgte metode som "Din aftale", og quizzen tager kun de valgte metoders spørgsmål (alle ved
   "Alle varianter") – testet i samme node-test.
8. tjek_konventionskort.py, tjek_kort_eksempler.py, tjek_fagord.py, tjek_bydeform.py og tjek_sprog.py melder i orden.
9. Tabellen "Tekster til gennemgang" findes under Afklaret i specen og har en kilde i hver række.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

ROD = pathlib.Path(__file__).resolve().parent.parent
METODER = ROD.parent / 'Fordelingstræneren' / 'src' / 'modspil' / 'content' / 'metoder.json'
KOPI = ROD / 'data' / 'modspilsaftaler.json'
QUIZ = ROD / 'data' / 'modspilsaftaler-quiz.json'
KORT = ROD / 'data' / 'kort'
SRC = ROD / 'tools' / 'konventionskort.src.html'
SPEC = next((p for p in [ROD / 'SPEC-modspilsaftaler.md', ROD / 'docs' / 'specs' / 'SPEC-modspilsaftaler.md'] if p.exists()), None)

RELATEREDE = {
    'udspil-sans': ['Udspil'], 'udspil-farve': ['Udspil'], 'honnoerudspil': ['Udspil'],
    'kald': ['Markeringer'], 'laengde': ['Markeringer'], 'afkast': ['Markeringer', 'Lavinthal'], 'forsinket': ['Markeringer'],
}
UDSPIL_ART = {'udspil-sans': 'sans', 'udspil-farve': 'farve'}
VAERDI = {'E': 14, 'K': 13, 'D': 12, 'B': 11}


def laes(p):
    return json.loads(p.read_text(encoding='utf-8'))


def metoder():
    return laes(METODER)


def kort(kid):
    p = KORT / f'{kid}.json'
    if not p.exists():
        raise RuntimeError(f'{p.relative_to(ROD)} findes ikke (ikke bygget)')
    return laes(p)


def grupper(k):
    """Kortets rækker i meldinger delt op efter mellemoverskrift: {gruppe: [rækker]}."""
    ud, cur = {}, None
    for r in k.get('meldinger', []):
        if set(r) == {'gruppe'}:
            cur = r['gruppe']
            ud[cur] = []
        elif cur is not None:
            ud[cur].append(r)
    return ud


def eksempler(k, kat):
    """(metode, holding-tekst, art, kort) for hver eksempelrække (alle rækker undtagen "Aftalen")."""
    m = {x['tekst']: x for x in kat['metoder']}
    for navn, rk in grupper(k).items():
        for r in rk:
            if r.get('kort') == 'Aftalen':
                continue
            yield m.get(navn), r


def valoer(t):
    return VAERDI.get(t) or int(t)


def punkt1():
    if not KOPI.exists():
        return ['data/modspilsaftaler.json findes ikke (ikke bygget)']
    a, b = laes(KOPI), metoder()
    fejl = []
    for felt in ('kategorier', 'profiler'):
        if a.get(felt) != b.get(felt):
            fejl.append(f'{felt} er forskellig fra Fordelingstrænerens metoder.json')
    return fejl


def punkt2():
    fejl = []
    index = laes(KORT / 'index.json')
    for kat in metoder()['kategorier']:
        kid = f"ms-{kat['id']}"
        try:
            k = kort(kid)
        except RuntimeError as e:
            fejl.append(str(e))
            continue
        if f'{kid}.json' not in index:
            fejl.append(f'{kid}: mangler i index.json')
        if k.get('type') != 'modspil' or k.get('kategori') != 'modspil':
            fejl.append(f'{kid}: type og kategori skal være modspil')
        g = grupper(k)
        for x in kat['metoder']:
            if x['tekst'] not in g:
                fejl.append(f"{kid}: ingen gruppe for metoden {x['tekst']}")
                continue
            regel = [r for r in g[x['tekst']] if r.get('kort') == 'Aftalen']
            if len(regel) != 1 or regel[0].get('viser') != x['aftale']:
                fejl.append(f"{kid}: rækken Aftalen for {x['tekst']} er ikke metodens aftale ordret")
    ekstra = sorted(p.stem for p in KORT.glob('ms-*.json')) 
    if len(ekstra) != 7:
        fejl.append(f'{len(ekstra)} kort ms-*, ikke 7')
    return fejl


def punkt3():
    fejl = []
    src = SRC.read_text(encoding='utf-8')
    if '/fordelingstraeneren/#modspil' not in src or 'Træn i Modspil' not in src:
        fejl.append('kortsiden har ikke linket "Træn i Modspil" til /fordelingstraeneren/#modspil (ikke bygget)')
    for kat in metoder()['kategorier']:
        try:
            k = kort(f"ms-{kat['id']}")
        except RuntimeError as e:
            fejl.append(str(e))
            continue
        for navn in RELATEREDE[kat['id']]:
            if navn not in k.get('relaterede', []):
                fejl.append(f"ms-{kat['id']}: relaterede mangler {navn}")
    return fejl


def punkt4():
    if not QUIZ.exists():
        return ['data/modspilsaftaler-quiz.json findes ikke (ikke bygget)']
    q = laes(QUIZ)
    fejl = []
    for kat in metoder()['kategorier']:
        for x in kat['metoder']:
            sp = [s for s in q.get('spoergsmaal', []) if s.get('kategori') == kat['id'] and s.get('metode') == x['id']]
            if len(sp) != 2:
                fejl.append(f"{kat['id']}/{x['id']}: {len(sp)} spørgsmål, ikke 2")
            for s in sp:
                for felt in ('q', 'qEn', 'correct', 'correctEn', 'why', 'whyEn'):
                    if not s.get(felt):
                        fejl.append(f"{kat['id']}/{x['id']}: feltet {felt} mangler")
                for felt in ('wrong', 'wrongEn'):
                    if len(s.get(felt, [])) != 2:
                        fejl.append(f"{kat['id']}/{x['id']}: {felt} skal have 2 svar")
                if any(h in s for h in ('hand', 'haand', 'bordet')):
                    fejl.append(f"{kat['id']}/{x['id']}: spørgsmålet har en hånd")
    return fejl


def punkt5():
    fejl, opgaver, steder = [], [], []
    for kat in metoder()['kategorier']:
        try:
            k = kort(f"ms-{kat['id']}")
        except RuntimeError as e:
            fejl.append(str(e))
            continue
        set_ = {}
        for x, r in eksempler(k, kat):
            if x is None:
                continue
            set_[x['id']] = set_.get(x['id'], 0) + 1
            if kat['id'] in UDSPIL_ART or kat['id'] == 'honnoerudspil':
                tekst = r['kort']
                art = UDSPIL_ART.get(kat['id'])
                mm = re.match(r'Mod (sans|farve): (.*)$', tekst)
                if mm:
                    art, tekst = mm.group(1), mm.group(2)
                if art is None:
                    fejl.append(f"ms-{kat['id']}: eksemplet '{r['kort']}' siger ikke mod sans eller farve")
                    continue
                holding = [valoer(t) for t in tekst.split()]
                svar = r['viser'].split()[0]
                opgaver.append({'kategori': kat['id'], 'metode': x['id'], 'art': art, 'holding': holding})
                steder.append((kat['id'], x['tekst'], r['kort'], svar))
        for x in kat['metoder']:
            if not set_.get(x['id']):
                fejl.append(f"ms-{kat['id']}: metoden {x['tekst']} har intet eksempel")
    if opgaver:
        r = subprocess.run(['node', 'tools/kontrol_modspilsaftaler.mjs'], cwd=ROD, input=json.dumps(opgaver),
                           capture_output=True, text=True, encoding='utf-8')
        if r.returncode:
            return fejl + ['kontrol_modspilsaftaler.mjs fejlede: ' + r.stderr.strip()[-400:]]
        for (kat, metode, tekst, svar), model in zip(steder, json.loads(r.stdout)):
            if model is None:
                if svar not in ('Table', 'table'):
                    fejl.append(f'ms-{kat} {metode} {tekst}: modellen siger "table feeling", kortet {svar}')
            elif valoer(svar) != model:
                fejl.append(f'ms-{kat} {metode} {tekst}: kortet siger {svar}, modellen {model}')
    return fejl


def punkt6og7():
    if not (ROD / 'assets' / 'modspilsaftaler.js').exists() or not (ROD / 'tools' / 'modspilsaftaler.test.mjs').exists():
        return ['assets/modspilsaftaler.js eller tools/modspilsaftaler.test.mjs findes ikke (ikke bygget)']
    r = subprocess.run(['node', '--test', 'tools/modspilsaftaler.test.mjs'], cwd=ROD, capture_output=True, text=True, encoding='utf-8')
    fejl = [] if r.returncode == 0 else ['node --test tools/modspilsaftaler.test.mjs fejlede:\n' + (r.stdout + r.stderr)[-1500:]]
    if 'Din aftale' not in SRC.read_text(encoding='utf-8'):
        fejl.append('kortsiden viser ikke "Din aftale" (ikke bygget)')
    return fejl


def punkt8():
    fejl = []
    env = {**os.environ, 'PYTHONIOENCODING': 'utf-8'}
    for args in (['tools/tjek_konventionskort.py'], ['tools/tjek_kort_eksempler.py'], ['tools/tjek_fagord.py'],
                 ['tools/tjek_bydeform.py'], ['tools/tjek_sprog.py']):
        r = subprocess.run([sys.executable, *args], cwd=ROD, capture_output=True, text=True, encoding='utf-8', env=env)
        if r.returncode:
            fejl.append(f"{args[0]} fejlede:\n" + (r.stdout + r.stderr).strip()[-800:])
    return fejl


def punkt9():
    if SPEC is None:
        return ['specen findes ikke']
    tekst = SPEC.read_text(encoding='utf-8')
    a = tekst.find('\n## Afklaret')
    m = re.search(r'\n#{3,4} Tekster til gennemgang[^\n]*\n', tekst[a:]) if a >= 0 else None
    if not m:
        return ['tabellen "Tekster til gennemgang" findes ikke under Afklaret']
    rest = tekst[a + m.end():]
    raekker = [l for l in rest.split('\n#')[0].splitlines() if l.startswith('|') and not set(l) <= set('|- :')]
    fejl = [] if len(raekker) > 1 else ['tabellen "Tekster til gennemgang" har ingen rækker']
    for l in raekker[1:]:
        celler = [c.strip() for c in l.strip('|').split('|')]
        if not celler[-1]:
            fejl.append(f'rækken uden kilde: {l[:80]}')
    return fejl


def main():
    alle = 0
    for nr, f in [('1', punkt1), ('2', punkt2), ('3', punkt3), ('4', punkt4), ('5', punkt5), ('6–7', punkt6og7),
                  ('8', punkt8), ('9', punkt9)]:
        try:
            fejl = f()
        except Exception as e:  # noqa: BLE001
            fejl = [f'{type(e).__name__}: {e}']
        print(f'Punkt {nr}: ' + ('i orden' if not fejl else 'RØDT'))
        for x in fejl[:15]:
            print('  -', x)
        if len(fejl) > 15:
            print(f'  ... og {len(fejl) - 15} til')
        alle += len(fejl)
    print('Alle punkter er i orden.' if not alle else f'{alle} fejl.')
    sys.exit(1 if alle else 0)


if __name__ == '__main__':
    main()
