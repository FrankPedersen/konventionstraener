"""Accepttest for SPEC-sprog-og-ordbog.md i konventionstræneren.

Kør fra repoets rod:  python3 tools/tjek_sprog.py

Sidefodens kolonne Opslag, de fem rettelser, puljen ff-trial-bids i takt med dealer/ff_trial.py, fagordstesten og
ordlisten til sprogtjek. Selve stavekontrollen køres med hånden: python3 tools/sprogtjek.py.
"""
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys
import unittest

ROD = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROD))


def modul(navn, sti):
    spec = importlib.util.spec_from_file_location(navn, ROD / sti)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


fagord = modul('tjek_fagord', 'tools/tjek_fagord.py')

# (forkert, rigtigt, filer med det rigtige) fra specens rettelsesliste
RETTELSER = [
    (r'\btrumffarv\b', 'Støtte til en ny trumffarve', ['dealer/ff_trial.py', 'pools/ff-trial-bids.json']),
    (r'\btrumfene\b', 'hvor gode trumferne er', ['data/kort/ff-ogust.json']),
    (r'\bespecielt\b', 'bekræft især', ['viden/2-over-1-makker2.html']),
    (r'\bhændertyper\b', 'håndtyper', ['viden/2-over-1-makker2.html']),
    (r'\binvitter\b', 'stopmeldinger fra invitationer', ['docs/kampen-om-kontrakten.md', 'viden/kampen-om-kontrakten.html']),
]

FODHARNESK = r'''
const src = require('fs').readFileSync('assets/footer.js', 'utf8');
const ud = {};
for (const lang of ['da', 'en']) {
  const el = { innerHTML: '' };
  const document = { getElementById: () => el, currentScript: { getAttribute: () => 'assets/footer.js' },
                     head: { appendChild() {} }, createElement: () => ({}) };
  new Function('window', 'document', src)({ LANG: lang }, document);
  ud[lang] = el.innerHTML;
}
process.stdout.write(JSON.stringify(ud));
'''


class Sidefoden(unittest.TestCase):
    def test_kolonnen_opslag_efter_traenere_i_footer_js(self):
        js = (ROD / 'assets/footer.js').read_text(encoding='utf-8')
        self.assertIn("kolonne('opslag', 'Opslag', 'Reference',", js)
        self.assertIn("link('/ordbog/', 'Bridgeordbog', 'Bridge dictionary')", js)

    @unittest.skipUnless(shutil.which('node'), 'kræver Node')
    def test_sidefoden_paa_dansk_og_engelsk(self):
        ud = json.loads(subprocess.run(['node', '-e', FODHARNESK], cwd=ROD, capture_output=True, check=True, text=True,
                                       encoding='utf-8').stdout)
        for lang, titel, link in (('da', 'Opslag', 'Bridgeordbog'), ('en', 'Reference', 'Bridge dictionary')):
            html = ud[lang]
            self.assertIn(f'id="sf-opslag">{titel}</h2>', html, lang)
            self.assertIn(f'<a href="/ordbog/">{link}</a>', html, lang)
            self.assertLess(html.index('sf-traenere'), html.index('sf-opslag'), lang)
            self.assertLess(html.index('sf-opslag'), html.index('sf-aftaler'), lang)


class Rettelserne(unittest.TestCase):
    def test_de_fem_ord_er_rettet(self):
        filer = [f for f in fagord.filer()
                 if not f.startswith(('_design/', 'SPEC-')) and (ROD / f).exists()]
        for forkert, rigtigt, steder in RETTELSER:
            for f in filer:
                tekst = (ROD / f).read_text(encoding='utf-8', errors='ignore')
                self.assertIsNone(re.search(forkert, tekst), f'{f}: {forkert}')
            for f in steder:
                tekst = re.sub(r'\s+', ' ', (ROD / f).read_text(encoding='utf-8'))
                self.assertIn(rigtigt, tekst, f)


class Fagord(unittest.TestCase):
    def test_fagordstesten_bestaar(self):
        for f, tekst in fagord.dansk_tekst():
            self.assertEqual(fagord.fund(tekst), [], f)

    def test_fejler_hvis_man_skriver_knibning(self):
        self.assertEqual(fagord.fund('Spil en knibning mod damen.'), [('knibning', 'kipning, kippe')])
        self.assertTrue(fagord.fund(fagord.dansk_side("T('Tag en knibning', 'Take a finesse')")))
        self.assertEqual(fagord.fund('I snit giver det 9 stik.'), [])

    def test_husets_ord_t1_til_t3(self):
        self.assertEqual(fagord.fund('12 HCP'), [('HCP', 'hp')])
        self.assertEqual(fagord.fund('Tre trumf og dobbeltton klør'), [('dobbeltton', 'doubleton')])
        self.assertEqual(fagord.fund('når fitten er fundet'), [('fitten', 'fittet')])
        self.assertEqual(fagord.fund('en fit i spar'), [('en fit', 'et fit')])
        self.assertEqual(fagord.fund('med en 8+ major-fit'), [('en 8+ major-fit', 'et fit')])
        self.assertEqual(fagord.fund('fittens farve'), [('fittens', 'fittet')])
        self.assertEqual(fagord.fund('12 hp, doubleton i klør, og fittet er fundet; et 4-3-fit'), [])

    def test_engelsk_tekst_taeller_ikke(self):
        side = '<td data-en="10+ HCP">10+ hp</td> T(`Din hånd: ${q.hp} hp`, `Your hand: ${q.hp} HCP`)'
        self.assertEqual(fagord.fund(fagord.dansk_side(side)), [])
        self.assertEqual(fagord.fund(fagord.dansk_json({'tekst': '10 hp', 'en': {'tekst': '10 HCP'}})), [])
        self.assertEqual(fagord.fund(fagord.dansk_python('tx("12 hp", "12 HCP")')), [])


class Ordlisten(unittest.TestCase):
    def test_ordlisten_har_bridgeordene(self):
        linjer = (ROD / 'tools/ordliste.txt').read_text(encoding='utf-8').splitlines()
        ord_ = {l.strip().lower() for l in linjer if l.strip() and not l.startswith('#')}
        for w in ('cuebid', 'sleminvit', 'Stayman', 'kipning'):
            self.assertIn(w.lower(), ord_)


if __name__ == '__main__':
    unittest.main()
