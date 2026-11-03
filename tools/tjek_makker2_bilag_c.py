"""Accepttest for SPEC-makker2-bilag-c.md (Franks valg 3. november 2026).

Kør fra repoets rod:  python3 tools/tjek_makker2_bilag_c.py

Aftalerne fra Bilag C står i Makker 2-dokumentet: forsvar mod svag 2 og 3 med Lebensohl (15d), forsvar mod deres
to-farvede (15b), responsiv dobling og maksimal-dobling (17), udspil mod slem (19), 2♣ med kontrolsvar (14 og 8) og
Flannery på 2♦ (12, 1, 5, B1, Bilag A og F). Bilag C er én linje, og alle links i indholdsfortegnelsen virker.
"""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROD = pathlib.Path(__file__).resolve().parent.parent
DOK = (ROD / 'viden' / '2-over-1-makker2.html').read_text(encoding='utf-8')


def tekst(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).replace(' ,', ',').replace(' .', '.').strip()


def ren(s):
    """Som tekst, men uden mellemrum om kort og tegn, der kommer af tags."""
    return re.sub(r'(\d) (♣|♦|♥|♠)', r'\1\2', tekst(s))


def mellem(a, b):
    start = DOK.index(f'id="{a}"')
    return ren(DOK[start:DOK.index(f'id="{b}"', start)]) if b else ren(DOK[start:])


fejl = []


def norm(s):
    """Uden forskel på store og små bogstaver og på mellemrum, som tags giver omkring / og parenteser."""
    return re.sub(r'\s*([/()])\s*', r'', s.lower())


def skal(afsnit, navn, *sætninger):
    for s in sætninger:
        if norm(s) not in norm(afsnit):
            fejl.append(f'{navn}: mangler "{s}"')


def ikke(afsnit, navn, *sætninger):
    for s in sætninger:
        if s.lower() in afsnit.lower():
            fejl.append(f'{navn}: "{s}" står der stadig')


a15d = mellem('afsnit-15d', 'afsnit-16') if 'id="afsnit-15d"' in DOK else ''
skal(a15d, 'afsnit 15d', '15d · Forsvar mod svag 2 og 3', 'oplysning op til og med 4♥', '15–18 hp med hold', 'til spil',
     'Mod svag 3', 'ny farve er naturlig', 'Lebensohl', '2NT · relæ')
if 'id="afsnit-c4"' not in a15d and 'afsnit-c4' not in DOK[DOK.find('id="afsnit-15d"'):DOK.find('id="afsnit-16"')]:
    fejl.append('afsnit 15d: ankeret afsnit-c4 følger ikke Lebensohl-skemaet med')

a15b = mellem('afsnit-15b', 'afsnit-15c')
skal(a15b, 'afsnit 15b', '10+ hp og interesse i straf', 'Cuebid i deres laveste farve', 'støtte til vores farve, invit eller mere',
     'Cuebid i deres højeste farve', 'den anden major og krav', 'konkurrence og svag')

a17 = mellem('afsnit-17', 'afsnit-18')
skal(a17, 'afsnit 17', '17 · Doblingstyper', 'Responsiv dobling', 'oplysning op til og med 3♠ med 6+ hp',
     'begge minorer eller en farve, svarer ikke kan melde', 'Over støtte i minor viser den begge majorer', 'Maksimal-dobling',
     'dobling maksimum og invit', '3 i vores farve er konkurrence')

a19 = mellem('afsnit-19', 'afsnit-20')
skal(a19, 'afsnit 19', 'Udspil mod slem', 'Mod lilleslem spilles der passivt ud', 'Et es spilles kun ud med en plan', 'Lightner',
     'usædvanligt udspil, ofte bordets først meldte farve')

a14 = mellem('afsnit-14', 'del-iv')
skal(a14, 'afsnit 14', '14 · Stærkåbning 2♣ — kontrolsvar', '20+ hp, eller 9 sikre stik i major / 10 i minor', 'es = 2, konge = 1',
     '0–1 kontrol', 'Præcis 2', 'Præcis 3', 'Præcis 4', '5+ kontroller', 'Overføring', 'alertér', '24+ hp', '22–23 hp', '24–25 hp',
     '26–27 hp', '28–29 hp', 'Relæ', 'Splinter', 'afløser 2♦', 'afløser 2♥', 'ikke straf', 'Gerber', 'RKC 1430',
     'E K D x x x(x)', 'Åbners pas er krav')
ikke(ren(DOK), 'dokumentet', 'waiting', 'andet negative')
ikke(a14, 'afsnit 14', 'Positivt svar')

a8 = mellem('afsnit-8', 'afsnit-9')
skal(a8, 'afsnit 8', '22–23 jævn', '24–25 jævn', '24+ jævn')
ikke(a8, 'afsnit 8', '22–24 jævn', '25–27 jævn')

a12 = mellem('afsnit-12', 'afsnit-13')
skal(a12, 'afsnit 12', 'Svag 2 (2♥/2♠)', 'Flannery', 'Præcis 5♥ og 4♠, 11–15 hp')
ikke(a12, 'afsnit 12', '2♦/2♥/2♠')
skal(mellem('afsnit-13', 'afsnit-14'), 'afsnit 13', 'Over Flannery 2♦')

a1 = mellem('afsnit-1', 'afsnit-2')
skal(a1, 'afsnit 1', '2♠ efter 1♥ · 5-5, 12–15 hp, ikke krav', '3♠ efter 1♥ · 5-4 eller 5-5, 16+ hp, krav i én runde',
     'Med 5-5 i majorerne åbnes 1♥')
a5 = mellem('afsnit-5', 'afsnit-5a')
skal(a5, 'afsnit 5', 'bevidst undtagelse', '16+ med 5-4')
ikke(a5, 'afsnit 5', '5+ hjerter, 15+')
a4 = mellem('afsnit-4', 'afsnit-5')
skal(a4, 'afsnit 4', 'Naturlig, 5-4, 12–15 hp, ikke krav', 'Spring i ny højere farve', 'Undtagelserne er')

a = mellem('bilag-a', 'bilag-b')
skal(a, 'Bilag A', 'Flannery', '2NT-spørgsmålet', 'kontrolsvar', 'overføringssvarene')

b = mellem('bilag-b', 'bilag-c')
skal(b, 'Bilag B', 'Flannery er valgt', 'B1 · Flannery 2♦ — aftalt', '11–15 hp', 'Med 5-5 i majorerne åbnes 1♥', 'dobling er oplysning med kort ruder',
     'svar i major er naturligt og svagt', '2NT er stadig krav', 'efter 1♥ – 1NT viser 2♠ derfor 5-5 med 12–15', 'B2 · Multi 2♦', 'B3 · Anbefaling')
ikke(b, 'Bilag B', 'diskussionsoplæg', 'Uden revers kan åbner godt melde', 'normalt 16–18', 'det skal aftales')

c = mellem('bilag-c', 'bilag-d')
skal(c, 'Bilag C', 'Alle emner er aftalt 3. november 2026')
ikke(c, 'Bilag C', 'C1', 'C2', 'C3', 'C4', 'Huller i aftalerne')

f = mellem('bilag-f', 'afsnit-g')
ikke(f, 'Bilag F', 'Åbent spørgsmål', 'alternativ', 'To huller')
skal(f, 'Bilag F', 'Flannery 2♦')

# Alle interne links peger på et anker, der findes.
ankre = set(re.findall(r'\bid="([^"]+)"', DOK))
for mål in sorted(set(re.findall(r'href="#([^"]+)"', DOK))):
    if mål not in ankre:
        fejl.append(f'link til #{mål}, som ikke findes')
indhold = DOK[:DOK.index('id="afsnit-1"')]
for s in ('C1 ·', 'C2 ·', 'C3 ·', 'C4 ·', 'waiting', 'fem doblingstyper'):
    if s in indhold:
        fejl.append(f'indholdsfortegnelsen: "{s}" står der stadig')
if '15d · Forsvar mod svag 2 og 3' not in ren(indhold):
    fejl.append('indholdsfortegnelsen: 15d mangler')

if fejl:
    print('\n'.join(fejl))
    print(f'\n{len(fejl)} fejl')
    sys.exit(1)
print('Makker 2, Bilag C: i orden.')
