"""Fagordstest (SPEC-sprog-og-ordbog.md, Den varige kontrol): husets fagord i al dansk synlig tekst.

Kør fra repoets rod:  python3 tools/tjek_fagord.py

Læser siderne (*.html uden design/ og tools/), assets/*.js, data/**.json, puljerne, teksterne i dealer/ (det
danske argument til tx) og docs/kampen-om-kontrakten.md (kilden til Viden-siden). Engelsk springes over:
data-en-attributter, det engelske argument til T(…), og "en"-felterne i JSON.
Fejler, hvis et af husets "Ikke"-ord står i dansk tekst. "i snit" (gennemsnit) er tilladt.
Husets ord: bordet, kipning, forbindelser og slutspil; og efter Franks svar på T1–T3: hp (ikke HCP), doubleton
(ikke dobbeltton) og fittet (ikke fitten) i dansk tekst, og derfor et fit (ikke en fit).
"""
import ast
import json
import pathlib
import re
import subprocess
import sys

ROD = pathlib.Path(__file__).resolve().parent.parent

IKKE_ORD = [
    (re.compile(r'\bdobbeltknib\w*', re.I), 'dobbelt kipning'),
    (re.compile(r'\bknib\w*', re.I), 'kipning, kippe'),
    (re.compile(r'\bsnit(?:tet|ter|tene)?\b', re.I), 'kipning'),
    (re.compile(r'\bblindemand\w*', re.I), 'bordet'),
    (re.compile(r'\bden blinde\b', re.I), 'bordet'),
    (re.compile(r'\bbroer(?:ne)?\b', re.I), 'forbindelser, indgang'),
    # T1–T3 (Franks svar)
    (re.compile(r'\bHCP\b'), 'hp'),
    (re.compile(r'\bdobbeltton\w*', re.I), 'doubleton'),
    (re.compile(r'\bfitten(?:s)?\b', re.I), 'fittet'),
    # Et fit, som passer med fittet (Franks valg 22. oktober 2026): en fit, en major-fit, en 8+ major-fit …
    (re.compile(r'\ben\s+(?:\S+\s+)?(?:[0-9a-zæøå+]+-)*fit\b', re.I), 'et fit'),
]
I_SNIT = re.compile(r'\bi\s+$', re.I)


def fund(tekst):
    """Alle "Ikke"-ord i en dansk tekst som (ordet, husets ord)."""
    ud = []
    for mønster, husets in IKKE_ORD:
        for m in mønster.finditer(tekst):
            if m.group(0).lower() == 'snit' and I_SNIT.search(tekst[max(0, m.start() - 3):m.start()]):
                continue
            ud.append((m.group(0), husets))
    return ud


# --- Dansk tekst ---

STRENG = r'''(`[^`]*`|'(?:[^'\\\n]|\\.)*'|"(?:[^"\\\n]|\\.)*")'''
# T('dansk', 'English') i lang.js og t(…) i footer.js; link(href, 'dansk', 'English') og kolonne(id, 'dansk', 'English', …)
T_KALD = re.compile(r'\b[Tt]\(\s*' + STRENG + r'\s*,\s*' + STRENG + r'\s*\)')
PAR_KALD = re.compile(r'\b(link|kolonne)\(\s*' + STRENG + r'\s*,\s*' + STRENG + r'\s*,\s*' + STRENG)


def uden_en_objekter(tekst):
    """Fjerner "en": {…} (de engelske udgaver i JSON, også inde i sidernes scripts)."""
    ud, i = [], 0
    for m in re.finditer(r'"en"\s*:\s*\{', tekst):
        if m.start() < i:
            continue
        ud.append(tekst[i:m.start()])
        j, dybde, streng = m.end(), 1, None
        while j < len(tekst) and dybde:
            c = tekst[j]
            if streng:
                if c == '\\':
                    j += 1
                elif c == streng:
                    streng = None
            elif c in '"\'':
                streng = c
            elif c == '{':
                dybde += 1
            elif c == '}':
                dybde -= 1
            j += 1
        i = j
    ud.append(tekst[i:])
    return ''.join(ud)


def dansk_side(tekst):
    """En sides eller et scripts danske tekst: uden stilark, data-en-attributter, engelske T-argumenter og "en"."""
    tekst = re.sub(r'<style\b.*?</style>', ' ', tekst, flags=re.S)
    tekst = re.sub(r'\sdata-en(?:-[a-z]+)?\s*=\s*"[^"]*"', ' ', tekst)
    tekst = re.sub(r"\sdata-en(?:-[a-z]+)?\s*=\s*'[^']*'", ' ', tekst)
    tekst = T_KALD.sub(lambda m: m.group(1), tekst)
    tekst = PAR_KALD.sub(lambda m: f'{m.group(1)}({m.group(2)}, {m.group(3)}', tekst)
    return uden_en_objekter(tekst)


def dansk_json(o):
    """Alle strenge i en JSON-struktur uden "en"-felterne."""
    if isinstance(o, dict):
        return '\n'.join(dansk_json(v) for k, v in o.items() if k != 'en')
    if isinstance(o, list):
        return '\n'.join(dansk_json(v) for v in o)
    return o if isinstance(o, str) else ''


def _streng(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return ''.join(_streng(v) if not isinstance(v, ast.FormattedValue) else ' ' for v in node.values)
    if isinstance(node, ast.BinOp):
        return _streng(node.left) + ' ' + _streng(node.right)
    return ''


def dansk_python(kilde):
    """Det danske argument til tx(…) i et modul under dealer/."""
    træ = ast.parse(kilde)
    return '\n'.join(_streng(n.args[0]) for n in ast.walk(træ)
                     if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'tx' and n.args)


def filer():
    ud = subprocess.run(['git', 'ls-files', '-z'], cwd=ROD, capture_output=True, check=True).stdout.decode('utf-8')
    return [f for f in ud.split('\0') if f]


def dansk_tekst():
    """(fil, dansk tekst) for al dansk synlig tekst i repoet."""
    ud = []
    for f in filer():
        sti = ROD / f
        if f.startswith(('design/', 'tools/')) or not sti.exists():
            continue
        if f.endswith('.html') or (f.startswith('assets/') and f.endswith('.js')):
            ud.append((f, dansk_side(sti.read_text(encoding='utf-8'))))
        elif f.endswith('.json') and f.startswith(('data/', 'pools/')):
            ud.append((f, dansk_json(json.loads(sti.read_text(encoding='utf-8')))))
        elif f.startswith('dealer/') and f.endswith('.py'):
            ud.append((f, dansk_python(sti.read_text(encoding='utf-8'))))
        elif f == 'docs/kampen-om-kontrakten.md':
            ud.append((f, sti.read_text(encoding='utf-8')))
    return ud


def main():
    fejl = []
    for f, tekst in dansk_tekst():
        for linje_nr, linje in enumerate(tekst.splitlines(), 1):
            for ord_, husets in fund(linje):
                fejl.append(f'{f}: "{ord_}" – husets ord er {husets}: {linje.strip()[:100]}')
    if fejl:
        print('\n'.join(fejl))
        print(f'{len(fejl)} steder bruger ikke husets fagord.')
        return 1
    print('Husets fagord: i orden.')
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
