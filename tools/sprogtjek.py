"""Stavekontrol (SPEC-sprog-og-ordbog.md, Den varige kontrol): ukendte ord i al dansk synlig tekst.

Kør fra repoets rod:
    python3 tools/sprogtjek.py                 # ukendte ord med antal og første fil
    python3 tools/sprogtjek.py --ord           # kun ordene, ét pr. linje
    python3 tools/sprogtjek.py --ordbog STI    # ordbogens opslagsord, som hunspell ikke kender (til ordliste.txt)

Teksten er den samme som fagordstestens (tools/tjek_fagord.py): siderne, assets, data, puljerne, teksterne i dealer/
og docs/kampen-om-kontrakten.md, uden engelsk. Ordene slås op med hunspell-reglerne for dansk (Python-pakken spylls,
`pip install spylls`, med da_DK fra npm-pakken dictionary-da, som hentes første gang og gemmes i brugerens cache).
Rigtige bridgeord, navne og forkortelser står i tools/ordliste.txt. Værktøjet køres med hånden før hver udgivelse og er
ikke en del af testene. Det slutter med kode 1, når der er ukendte ord.
"""
import html
import importlib.util
import io
import json
import os
import pathlib
import re
import sys
import tarfile
import urllib.request

ROD = pathlib.Path(__file__).resolve().parent.parent
ORDLISTE = ROD / 'tools' / 'ordliste.txt'
ORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")


def fagord():
    spec = importlib.util.spec_from_file_location('tjek_fagord', ROD / 'tools' / 'tjek_fagord.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ordbog_da():
    """hunspell da_DK fra dictionary-da, hentet én gang til brugerens cache."""
    from spylls.hunspell import Dictionary
    cache = pathlib.Path(os.environ.get('LOCALAPPDATA') or pathlib.Path.home() / '.cache') / 'sprogtjek' / 'dictionary-da'
    if not (cache / 'index.dic').exists():
        print('Henter den danske ordbog (dictionary-da) …', file=sys.stderr)
        with urllib.request.urlopen('https://registry.npmjs.org/dictionary-da/latest') as svar:
            tarball = json.load(svar)['dist']['tarball']
        with urllib.request.urlopen(tarball) as svar:
            data = svar.read()
        cache.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as tar:
            for navn in ('index.aff', 'index.dic', 'license'):
                medlem = tar.getmember(f'package/{navn}')
                (cache / navn).write_bytes(tar.extractfile(medlem).read())
    return Dictionary.from_files(str(cache / 'index'))


KODE = re.compile(r'[{};=]|\b[\w-]+:\S|^\s*[#.]')


def strenge(js):
    """Strengene i et script, der ligner tekst: mindst ét mellemrum og ingen CSS, HTML-attributter eller kode."""
    ud = []
    for m in re.finditer(r'''`([^`]*)`|'((?:[^'\\\n]|\\.)*)'|"((?:[^"\\\n]|\\.)*)"''', js):
        s = next(g for g in m.groups() if g is not None)
        s = re.sub(r'<[^>]*>', ' ', re.sub(r'\$\{[^}]*\}', ' ', s))
        if ' ' in s.strip() and not KODE.search(s):
            ud.append(s)
    return ud


def uden_ordlister(js):
    """{'Makker': 'Partner', …} i lang.js: kun den danske nøgle."""
    return re.sub(r"'([^'\n]*)'\s*:\s*'[^'\n]*'", r"'\1'", js)


def tekst_til_kontrol(fil, dansk):
    """Den danske tekst renset for kode, tags og entiteter."""
    if fil.endswith('.html'):
        scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', dansk, flags=re.S)
        uden = re.sub(r'<script\b.*?</script>', ' ', dansk, flags=re.S)
        uden = re.sub(r'<!--.*?-->', ' ', uden, flags=re.S)
        attrs = re.findall(r'\s(?:title|alt|aria-label|placeholder)="([^"]*)"', uden)
        attrs += re.findall(r'<meta name="description" content="([^"]*)"', uden)
        uden = re.sub(r'<[^>]+>', ' ', uden)
        return html.unescape(' '.join([uden, *attrs, *(s for js in scripts for s in strenge(uden_ordlister(js)))]))
    if fil.endswith('.js'):
        return ' '.join(strenge(uden_ordlister(dansk)))
    if fil.endswith('.json'):
        return ' '.join(linje for linje in dansk.splitlines() if ' ' in linje.strip())
    return dansk


def ord_i(tekst):
    tekst = re.sub(r'https?://\S+|\b[\w./-]+\.(?:json|html|js|css|py|md|docx)\b', ' ', tekst)
    for m in ORD.finditer(tekst):
        w = m.group(0)
        if len(w) < 3 or w.isupper():
            continue
        yield w


def læs_ordliste():
    if not ORDLISTE.exists():
        return set()
    return {linje.strip().lower() for linje in ORDLISTE.read_text(encoding='utf-8').splitlines()
            if linje.strip() and not linje.startswith('#')}


def ukendte(ordbog, kendte):
    """{ord: (antal, første fil)} for ord, som hverken hunspell eller ordlisten kender."""
    svar, ud = {}, {}
    for fil, dansk in fagord().dansk_tekst():
        for w in ord_i(tekst_til_kontrol(fil, dansk)):
            if w.lower() in kendte:
                continue
            if w not in svar:
                svar[w] = ordbog.lookup(w)
            if not svar[w]:
                antal, først = ud.get(w, (0, fil))
                ud[w] = (antal + 1, først)
    return ud


def main(argv):
    ordbog = ordbog_da()
    if argv[:1] == ['--ordbog']:
        kilde = pathlib.Path(argv[1]).read_text(encoding='utf-8')
        ord_ = sorted({w.lower() for linje in kilde.splitlines() if linje.startswith('### ')
                       for w in ord_i(linje[4:]) if not ordbog.lookup(w)})
        print('\n'.join(ord_))
        return 0
    fund = ukendte(ordbog, læs_ordliste())
    if argv[:1] == ['--ord']:
        print('\n'.join(sorted(fund, key=str.lower)))
    else:
        for w, (antal, først) in sorted(fund.items(), key=lambda x: (-x[1][0], x[0].lower())):
            print(f'{w:28} {antal:4}  {først}')
        print(f'{len(fund)} ukendte ord.' if fund else 'Stavekontrol: ingen ukendte ord.')
    return 1 if fund else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
