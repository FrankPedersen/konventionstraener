"""Accepttest for SPEC-makker2-aftaler.md (Franks valg 31. oktober 2026).

Kør fra repoets rod:  python3 tools/tjek_makker2_aftaler.py

1. Åbners nye højere farve på 2-trinnet er naturlig, 5-4, 12–15 hp og ikke krav; spring i ny højere farve er 16+ og
   krav i én runde, og med 19+ viser åbner udgangskraft i næste melding. Ny lavere farve er uændret: 12–18 og ikke
   krav, spring 19+ og udgangskrav. Efter 1♥ – 1NT er 2♠ 12–15, og 3♠ viser 5-4 eller 5-5 med 16+, krav i én runde;
   3♣/3♦ er fortsat 5-5 med 15–18. Revers spilles ikke: træneren ff-revers er taget af Træn, men filerne og kortet
   bliver. Testen tjekker dealeren, puljen, Makker 2-dokumentet, beskrivelserne, tegnefladen, kortet og Træn, og at
   "foreløbig – bekræftes" er væk alle steder.
2. Svar på makkers konkurrencedobling: 0–7 hp laveste farve, 8–11 hp spring i farven (invit) og 12+ hp cuebid af
   modpartens farve (krav). Testen tjekker afsnit 17 i Makker 2-dokumentet og kortet ff-doblinger.
"""
import html
import json
import pathlib
import re
import sys

ROD = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROD))
from dealer import ff_genmeld  # noqa: E402

DOK = ROD / 'viden' / '2-over-1-makker2.html'
FORELØBIG = ('foreløbig – bekræftes', 'foreløbig, bekræftes', 'provisional – to be confirmed')
# Afsnit 4: den nye højere farve og springet i den har de nye grænser; den nye lavere farve er uændret
NYE = ('Ny farve på 2-trinnet, højere end åbningsfarven (fx 1♦ – 1♠ – 2♥) Naturlig, 5-4, 12–15 hp, ikke krav',
       'Spring i ny højere farve (fx 1♦ – 1♠ – 3♥) 16+ hp, ubalanceret, 5-4 eller bedre. Krav i én runde',
       'Ny farve på 2-trinnet, lavere end åbningsfarven (fx 1♦ – 1♠ – 2♣) Naturlig, 12–18 hp, ikke krav',
       'Spring i ny lavere farve (fx 1♦ – 1♠ – 3♣) 19–21 hp, ubalanceret, 5-4 eller bedre. Udgangskrav')
# Afsnit 1, åbners genmelding efter 1NT-svaret
EFTER_1NT = ('2 i ny højere farve · naturlig, 5-4, 12–15 hp, ikke krav',
             '3♠ efter 1♥ · 5-4 eller 5-5, 16+ hp, krav i én runde',
             '3♣ / 3♦ · 5-5, 15–18 hp, rundekrav')


def tekst(s):
    """Synlig tekst uden tags og med enkelte mellemrum."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def afsnit(dok, navn, næste):
    """Teksten i afsnittet med id="afsnit-<navn>" frem til id="afsnit-<næste>" (eller sidens slutning)."""
    start = dok.index(f'id="afsnit-{navn}"')
    slut = dok.index(f'id="afsnit-{næste}"', start) if næste else len(dok)
    return tekst(dok[start:slut])


def hånd(**længder):
    """En hånd med de givne længder; kortene betyder intet for genmeldingen ud over farvelængderne."""
    return {f: list(range(14, 14 - længder[f], -1)) for f in 'SHDC'}


def tjek_dealeren():
    fejl = []
    # Ny højere farve (1♦ – 1♠ – 2♥): 12–15 uden spring, 16+ med spring (krav i én runde; med 19+ udgangskraft i næste
    # melding).
    L = hånd(S=2, H=4, D=5, C=2)
    for hp in range(12, 22):
        melding, why = ff_genmeld.rebid(L, hp) or (None, '')
        if hp <= 15 and melding != '2♥':
            fejl.append(f'dealeren: 5-4 med hjerter og {hp} hp giver {melding}, ventede 2♥')
        if hp >= 16 and melding != '3♥':
            fejl.append(f'dealeren: 5-4 med hjerter og {hp} hp giver {melding}, ventede spring til 3♥')
        if hp >= 16 and ('krav i én runde' not in why or 'forcing for one round' not in why.en):
            fejl.append(f'dealeren: springet med {hp} hp siger ikke "krav i én runde": {why}')
        if hp >= 19 and 'udgangskraft i næste melding' not in why:
            fejl.append(f'dealeren: springet med {hp} hp siger ikke, at åbner viser udgangskraft i næste melding: {why}')
    # Ny lavere farve (1♦ – 1♠ – 2♣) er uændret: 12–18 uden spring, også med 16–18, og spring med 19+ er udgangskrav
    # (Franks rettelse 31. oktober 2026).
    L = hånd(S=2, H=2, D=5, C=4)
    for hp in range(12, 22):
        melding, why = ff_genmeld.rebid(L, hp) or (None, '')
        if hp <= 18 and melding != '2♣':
            fejl.append(f'dealeren: 5-4 med klør og {hp} hp giver {melding}, ventede 2♣')
        if hp >= 19 and (melding != '3♣' or 'udgangskrav' not in why):
            fejl.append(f'dealeren: 5-4 med klør og {hp} hp giver {melding} ({why}), ventede spring til 3♣ som udgangskrav')
    bonus = ff_genmeld.BONUS['aab']
    if '12–15' not in bonus['correct'] or '16+' not in bonus['correct'] or '12–15' not in bonus['correct'].en:
        fejl.append(f'bonusspørgsmålet har ikke de nye grænser: {bonus["correct"]}')
    return fejl


def tjek_puljen():
    fejl = []
    pulje = json.loads((ROD / 'pools' / 'ff-staerke-genmeldinger.json').read_text(encoding='utf-8'))
    spring = set()
    for i, h in enumerate(pulje['hands'], 1):
        if h['situation'] != 'aab_1ru':
            continue
        grænser = {'2♥': (12, 15), '3♥': (16, 21), '2♣': (12, 18), '3♣': (19, 21)}
        if h['correct'] in grænser and not grænser[h['correct']][0] <= h['hp'] <= grænser[h['correct']][1]:
            fejl.append(f'puljen, hånd {i}: {h["correct"]} med {h["hp"]} hp (grænserne er {grænser[h["correct"]]})')
        if h['correct'] == '3♥':
            spring.add('19+' if h['hp'] >= 19 else '16–18')
    if spring != {'16–18', '19+'}:
        fejl.append(f'puljen har ikke spring til 3♥ med både 16–18 og 19+ hp: {sorted(spring)}')
    return fejl


def tjek_foreløbig():
    filer = [DOK, ROD / 'data' / 'konventioner.json', ROD / '_design' / 'tegneflade' / 'Main.dc.html',
             *sorted((ROD / 'data' / 'kort').glob('*.json')), *sorted((ROD / 'dealer').glob('*.py')),
             *sorted((ROD / 'pools').glob('*.json'))]
    return [f'{f.relative_to(ROD).as_posix()}: "{m}" står der stadig' for f in filer
            for m in FORELØBIG if m in f.read_text(encoding='utf-8')]


def tjek_dokumentet():
    fejl = []
    dok = DOK.read_text(encoding='utf-8')
    a4 = afsnit(dok, '4', '5')
    for s in NYE:
        if s not in a4:
            fejl.append(f'afsnit 4: mangler "{s}"')
    if 'udgangskraft i næste melding' not in a4:
        fejl.append('afsnit 4: siger ikke, at åbner med 19+ viser udgangskraft i næste melding')
    a1 = afsnit(dok, '1', '2')
    for s in EFTER_1NT:
        if s not in a1:
            fejl.append(f'afsnit 1, genmeldingen efter 1NT-svaret: mangler "{s}"')
    if '3 i ny farve · 5-5' in a1:
        fejl.append('afsnit 1: "3 i ny farve" gælder nu kun 3♣ og 3♦')
    alt = tekst(dok)
    if 'ny højere farve på 2-trinnet er naturlig, 5-4, 12–18' in alt or '5-4, 12–18 hp' in alt:
        fejl.append('Makker 2-dokumentet: 12–18 for ny højere farve står der stadig')
    c1 = afsnit(dok, 'c1', 'c2')
    if 'Revers' in c1 or 'revers' in c1:
        fejl.append('C1: spørgsmålet om revers står der stadig')
    g = afsnit(dok, 'g', None)
    if 'overvejet og fravalgt' not in g:
        fejl.append('Bilag G: siger ikke, at revers er overvejet og fravalgt')
    a17 = afsnit(dok, '17', '18')
    if 'bekræft gerne intervallerne' in a17:
        fejl.append('afsnit 17: konkurrencedoblingens intervaller står stadig som forslag')
    for s in ('0–7 hp', '8–11 hp', '12+ hp', 'Cuebid i modpartens farve'):
        if s not in a17[a17.index('Konkurrencedobling — makkers svar'):]:
            fejl.append(f'afsnit 17, konkurrencedoblingen: mangler "{s}"')
    return fejl


def tjek_beskrivelser_og_kort():
    fejl = []
    konv = json.loads((ROD / 'data' / 'konventioner.json').read_text(encoding='utf-8'))
    konv = konv if isinstance(konv, list) else konv['konventioner']
    k = next(x for x in konv if x['id'] == 'ff-staerke-genmeldinger')
    if '12–15' not in k['beskrivelse'] or '16+' not in k['beskrivelse'] or '12–15' not in k['en']['beskrivelse']:
        fejl.append(f'data/konventioner.json: beskrivelsen har ikke de nye grænser: {k["beskrivelse"]}')
    if '12–18' not in k['beskrivelse'] or '12–18' not in k['en']['beskrivelse']:
        fejl.append('data/konventioner.json: beskrivelsen nævner ikke, at ny lavere farve fortsat er 12–18')
    tegneflade = (ROD / '_design' / 'tegneflade' / 'Main.dc.html').read_text(encoding='utf-8')
    if k['beskrivelse'] not in tegneflade:
        fejl.append('tegnefladen: beskrivelsen af ff-staerke-genmeldinger er ikke den samme som i data/konventioner.json')
    # Revers er fravalgt: træneren er taget af Træn, men filerne og kortet bliver (Franks valg 31. oktober 2026)
    r = next(x for x in konv if x['id'] == 'ff-revers')
    if r.get('fravalgt') != 'ff' or 'Fravalgt i Makker 2-systemet' not in r['beskrivelse'] or 'Partner 2' not in r['en']['beskrivelse']:
        fejl.append('data/konventioner.json: ff-revers er ikke markeret som fravalgt i Makker 2-systemet')
    if '!k.fravalgt' not in (ROD / 'index.html').read_text(encoding='utf-8'):
        fejl.append('index.html: Træn viser stadig fravalgte trænere')
    for f in ('pools/ff-revers.json', 'dealer/ff_revers.py', 'data/kort/ff-revers.json'):
        if not (ROD / f).is_file():
            fejl.append(f'{f} skal blive')

    kort = json.loads((ROD / 'data' / 'kort' / 'ff-staerke-genmeldinger.json').read_text(encoding='utf-8'))
    styrke = {r.get('bud'): r.get('styrke') for r in kort['meldinger']}
    for bud, ventet in (('Ny højere farve på 2-trinnet', '12–15 hp'), ('Spring i ny højere farve', '16+ hp'),
                        ('Ny lavere farve på 2-trinnet', '12–18 hp'), ('Spring i ny lavere farve', '19–21 hp')):
        if styrke.get(bud) != ventet:
            fejl.append(f'kortet ff-staerke-genmeldinger: "{bud}" har {styrke.get(bud)}, ventede {ventet}')
    efter_1nt = [f for f in kort.get('fortsaettelser', []) if f['auction'][:3] == [['Dig', '1♥'], ['Modstander', 'Pas'], ['Makker', '1NT']]]
    styrke = {r.get('bud'): r.get('styrke') for f in efter_1nt for r in f['meldinger']}
    if (styrke.get('2♠'), styrke.get('3♠'), styrke.get('3♣ / 3♦')) != ('12–15 hp', '16+ hp', '15–18 hp'):
        fejl.append(f'kortet ff-staerke-genmeldinger: genmeldingerne efter 1♥ – 1NT mangler eller er forkerte: {styrke}')
    if any('revers' in s.lower() for s in kort.get('aabne', [])):
        fejl.append('kortet ff-staerke-genmeldinger: spørgsmålet om revers står stadig under Åbne spørgsmål')

    kort = json.loads((ROD / 'data' / 'kort' / 'ff-doblinger.json').read_text(encoding='utf-8'))
    if any('Konkurrencedoblingens intervaller' in s for s in kort.get('aabne', [])):
        fejl.append('kortet ff-doblinger: konkurrencedoblingens intervaller står stadig under Åbne spørgsmål')
    rækker = kort['meldinger']
    try:
        start = rækker.index({'gruppe': 'Svar på makkers konkurrencedobling'})
    except ValueError:
        return fejl + ['kortet ff-doblinger: gruppen "Svar på makkers konkurrencedobling" mangler']
    slut = next((i for i in range(start + 1, len(rækker)) if 'gruppe' in rækker[i]), len(rækker))
    gruppe = {r.get('styrke'): r for r in rækker[start + 1:slut]}
    for styrke_, bud in (('0–7 hp', 'Farve billigst muligt'), ('8–11 hp', 'Spring i farven'),
                         ('12+ hp', 'Cuebid i modpartens farve')):
        if (gruppe.get(styrke_) or {}).get('bud') != bud:
            fejl.append(f'kortet ff-doblinger: mangler "{bud}" med {styrke_}')
    return fejl


def main():
    fejl = tjek_dealeren() + tjek_puljen() + tjek_foreløbig() + tjek_dokumentet() + tjek_beskrivelser_og_kort()
    if fejl:
        print('\n'.join(fejl))
        print(f'{len(fejl)} fejl.')
        return 1
    print('Makker 2-aftalerne: i orden.')
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
