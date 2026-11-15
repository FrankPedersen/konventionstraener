"""Accepttest for SPEC-makker2-markeringer.md (Franks afgørelse 15. november 2026).

Kør fra repoets rod:  python3 tools/tjek_makker2_markeringer.py

Makker 2 spiller markeringerne som Bridgesystem og Kompendium over modspilsaftaler: lavt kort = kald, højt kort =
afvisning, og lavt kort = lige antal, højt kort = ulige (lavt-højt = lige, højt-lavt = ulige). Lavinthal er uændret.
Testen læser Makker 2-dokumentet og Mine makkeraftaler og sammenligner resten af dokumentet med tagget før ændringen.
"""
import html
import pathlib
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROD = pathlib.Path(__file__).resolve().parent.parent
TAG = 'v-foer-makker2-markeringer'
STI = 'viden/2-over-1-makker2.html'
DOK = (ROD / STI).read_text(encoding='utf-8')
FOER = subprocess.run(['git', 'show', f'{TAG}:{STI}'], cwd=ROD, capture_output=True, encoding='utf-8', check=True).stdout
AFTALER = (ROD / 'makkeraftaler.html').read_text(encoding='utf-8')
AFTALER_FOER = subprocess.run(['git', 'show', f'{TAG}:makkeraftaler.html'], cwd=ROD, capture_output=True, encoding='utf-8',
                              check=True).stdout


def tekst(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).replace(' ,', ',').replace(' .', '.').strip()


def afsnit(dok, a, b):
    start = dok.index(f'id="{a}"')
    return dok[start:dok.index(f'id="{b}"', start)]


fejl = []


def tjek(betingelse, besked):
    if not betingelse:
        fejl.append(besked)


a19 = tekst(afsnit(DOK, 'afsnit-19', 'afsnit-20'))
attitude = a19[a19.index('Attitude — kald og afvisning'):a19.index('Rangorden')]
rangorden = a19[a19.index('Rangorden'):a19.index('Reglen om 11')]

# 1. Attitude: reglen, tabellen og noten
tjek('Lavt kort = kald (»fortsæt«), højt kort = afvisning (»skift«)' in attitude, 'reglen i Attitude')
tjek('Lavt kort (fx 2 fra 8-3-2) Kald.' in attitude, 'tabellen: 2 fra 8-3-2 er kald')
tjek('Højt kort (fx 8 fra 8-3-2) Afvisning.' in attitude, 'tabellen: 8 fra 8-3-2 er afvisning')
tjek(attitude.index('Lavt kort (fx 2') < attitude.index('Højt kort (fx 8'), 'tabellen: kald står først')
rækker = re.findall(r'<tr>\s*<td style="background:(#[0-9A-F]+);[^>]*><strong>(Lavt|Højt) kort \(fx', afsnit(DOK, 'afsnit-19', 'afsnit-20'))
tjek(rækker == [('#EDF3E9', 'Lavt'), ('#F4E3E3', 'Højt')], f'rækkernes farver følger betydningen (grøn kald, rød afvisning): {rækker}')
tjek('En 6’er kan være en afvisning fra 6-4-3 og et kald fra 9-8-6.' in attitude, 'noten om 6’eren')

# 2. Rangorden: count-linjen
tjek('lavt kort = lige antal (lavt-højt), højt kort = ulige antal (højt-lavt)' in rangorden, 'count-linjen i Rangorden')

# 3. Den gamle retning står ingen steder i dokumentet
hele = tekst(DOK).lower()
for gammel in ('højt kort = kald', 'lavt kort = afvisning', 'højt-lavt = lige', 'lavt-højt = ulige', 'kald fra 6-4-3',
               'afvisning fra 9-8-6', 'højt kort (fx 8 fra 8-3-2) kald', 'lavt kort (fx 2 fra 8-3-2) afvisning'):
    tjek(gammel not in hele, f'den gamle retning står stadig: {gammel}')

# 4. Uændret uden for afsnit 19, og Lavinthal tegn for tegn som i tagget
start, slut = DOK.index('id="afsnit-19"'), DOK.index('id="afsnit-20"')
start_f, slut_f = FOER.index('id="afsnit-19"'), FOER.index('id="afsnit-20"')
tjek(DOK[:start] == FOER[:start_f], 'dokumentet før afsnit 19 er ændret')
tjek(DOK[slut:] == FOER[slut_f:], 'dokumentet efter afsnit 19 (fra Lavinthal) er ændret')
tjek(afsnit(DOK, 'afsnit-20', 'bilag-a') == afsnit(FOER, 'afsnit-20', 'bilag-a'), 'Lavinthal (afsnit 20) er ændret')
uden_attitude = lambda d: re.sub(r'Attitude — kald og afvisning.*?Reglen om 11', '', tekst(afsnit(d, 'afsnit-19', 'afsnit-20')))
tjek(uden_attitude(DOK) == uden_attitude(FOER), 'afsnit 19 er ændret uden for Attitude og Rangorden')

# 5. Mine makkeraftaler: rækken Markering
række = re.search(r'<tr><td data-en="Signals">Markering</td>.*?</tr>', AFTALER, re.S)
tjek(række is not None, 'rækken Markering findes ikke på Mine makkeraftaler')
if række:
    celler = re.findall(r'<td data-l="([^"]+)" data-en="([^"]+)">([^<]+)</td>', række.group(0))
    tjek(len(celler) == 2, f'rækken Markering har to celler: {celler}')
    for navn, en, da in celler:
        tjek(da.startswith('Lavt kort = kald'), f'{html.unescape(navn)}: {da}')
        tjek(en.startswith('Low card = encouraging'), f'{html.unescape(navn)} (engelsk): {en}')
        tjek('Højt kort = kald' not in da and 'High card = encouraging' not in en, f'{html.unescape(navn)}: den gamle retning')
    if len(celler) == 2:
        tjek(celler[0][2] == 'Lavt kort = kald; antal efter konge-udspil og ved ny farve', f'Makker 1: {celler[0][2]}')
        tjek(celler[1][2] == 'Lavt kort = kald; antal, når attitude er kendt, eller spilfører angriber farven', f'Makker 2: {celler[1][2]}')
uden_række = lambda s: re.sub(r'<tr><td data-en="Signals">Markering</td>.*?</tr>', '', s, flags=re.S)
tjek(uden_række(AFTALER) == uden_række(AFTALER_FOER), 'Mine makkeraftaler er ændret uden for rækken Markering')

if fejl:
    print(f'{len(fejl)} fejl:')
    for f in fejl:
        print(' -', f)
    sys.exit(1)
print('Makker 2-markeringerne: i orden')
