"""Bydeformtest (SPEC-beskrivende-form.md; husets regel i ../CLAUDE.md, Franks valg 30. oktober 2026): instruktioner og
forklaringer skrives i beskrivende form, ikke i bydeform. Knapper og links og navnene på opgaver og øvelser er undtaget.

Kør fra repoets rod:  python3 tools/tjek_bydeform.py

Læser samme danske tekst som tools/tjek_fagord.py (siderne, assets/*.js, data/**.json og docs/kampen-om-kontrakten.md)
og desuden sidernes danske attributter (meta-beskrivelser, aria-label, placeholder, title). Fejler, hvis en sætning
eller et led efter kolon eller semikolon begynder med et udsagnsord i bydeform.

Springes over efter Franks valg 30. oktober 2026 (docs/beskrivende-form.md, A2–A4): konventionskortene (data/kort/,
viden/konventionskort.html og kortenes hint), puljernes forklaringer og deres skabeloner (pools/, dealer/) og
systemdokumenterne i viden/ og docs/; meldesproget og kilderne har deres egen form.
"""
import html
import pathlib
import re
import sys

ROD = pathlib.Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROD / 'tools'))
from tjek_fagord import dansk_tekst  # noqa: E402

# Udsagnsord i bydeform, der kan stå først i en dansk instruktion. "Pas" og "lav" mangler med vilje: det er meldingen og
# tillægsordet. Som Fordelingstrænerens src/sprog/bydeform.ts og forsidens tools/tjek_bydeform.py.
BYDEFORMER = set('''
afbryd angiv annullér behold bemærk brug byg eksportér erstat find fjern flyt fold følg fortsæt gem gentag giv gruppér
gå gæt hent hold husk importér indsæt kig kip klik kom kopiér kryds lad luk lås læg læs markér navngiv noter notér
nulstil opdatér overskriv prøv regn ret ryd sammenlign se send sikr skift skriv slet slå spil spring start stop svar sæt
tag tast tjek træk tryk tæl tænk udfyld udled undgå vent vis vælg vurdér øv åbn
træn søg filtrér skjul lær spørg indtast bekræft tilføj vend afslut overvej meld byd dobl doble genmeld genåbn kæmp ofr
kontrollér vær bliv gør glem sørg gennemgå lån sælg udskriv
'''.split())

# A2–A4: kortene, puljerne, skabelonerne og systemdokumenterne.
SPRING_OVER = re.compile(r'^(data/kort/|pools/|dealer/|docs/)|^viden/(?!index\.html$)|^assets/konventionskort-hint\.js$')

# Knapper, links og navne, der bliver i bydeform (gruppe 1 og 2 i docs/beskrivende-form.md). Et regulært udtryk
# dækker en tekst med et indsat navn eller tal.
UNDTAGELSER = [
    # Knapper og links
    'Vis alle trænere',
    'Se resultat →',
    'Gå til',
    'Hent som Word',
    'Hent som Markdown',
    'Vis reglen',
    'Vis fire mulige meldinger',
    'Træn',
    'Træn 8',
    'Vælg konvention',
    'Skift forsvar',
    'Forfra',
    'Udskriv eller hent',
    'Udskriv eller gem som PDF',
    # Søgefeltet
    'Søg',
    # Navne på emner og trænere
    'Svar på 1NT',
    'Svar på doblingen — Multitræner',
    'Giv markering',
    'Læs markering',
    re.compile(r'^Svar på 4NT\b'),
]

# Fundet, da testen blev skrevet, og venter på Franks svar. K2's godkendte "Ingen træner passer på ordet." gentager
# overskriften "Ingen trænere passer" (forslag i docs/beskrivende-form.md, Tillæg).
VENTER = [
    'Prøv et andet ord.',
    # Overskriften over metodevalget i traener.html, når konventionen ikke har sit eget spørgsmål (forslag: "Hvilken
    # metode spiller I?" som konventionernes "Hvilket forsvar mod 1NT spiller I?").
    'Vælg metode',
    # Trænernes slutskærm (traener.html, markering.html, multi-svar-traener.html) og tre beskrivelser i
    # data/konventioner.json (ff-genaabning, kamp-gif, kamp-2020).
    'Gennemgå forklaringerne igen, og prøv en gang til.',
    'Lån ca. 3 hp af makker',
    'Lån 3–4 hp på ujævne hænder',
    'Sælg ikke ud under 2♠, når de har fundet tilpasning – og meld efter trumfreglen og zonen, når I selv kæmper videre.',
]

# Sætninger, der begynder med et af ordene, men ikke er bydeform: "spring" og "hold" som navneord.
FALSKE_TRÆF = [
    re.compile(r'^Spring i ny farve er\b', re.I),
    re.compile(r'^Hold i farven\b'),
]

PREFIX = re.compile(r'^[\s"\'“„«(\[▶→←↓↑✓✗·•–—#*>-]*')
# Sætninger (ikke efter forkortelser som "pr." og "fx."; også efter "**Råd.**"), led efter kolon og semikolon (også
# "**Råd:**") og linjer.
SPLIT = re.compile(r'(?<=[.!?])(?<!\b[Pp]r\.)(?<!\b[Cc]a\.)(?<!\b[Ff]x\.)(?<!\b[Kk]l\.)(?<!\b[Nn]r\.)\**\s+|[:;]\**\s+|\n+')
STRENG = r"""'(?:[^'\\\n]|\\.)*'|"(?:[^"\\\n]|\\.)*\""""
# Kommentarer og strenge i et script, fra venstre mod højre, så en apostrof i en kommentar eller // i en adresse ikke
# forveksles.
JS_TOKEN = re.compile(r'/\*.*?\*/|//[^\n]*|`(?:[^`\\]|\\.)*`|' + STRENG, re.S)
WHY = re.compile(r'"why"\s*:\s*"(?:[^"\\]|\\.)*"')
ATTRIBUT = re.compile(r'\s(?:content|aria-label|placeholder|title|alt)="([^"]*)"')


def undtaget(tekst):
    t = tekst.strip()
    return any(u == t if isinstance(u, str) else u.search(t) for u in UNDTAGELSER)


def bydeform(tekst):
    """Sætningerne i en dansk tekst, der begynder med et udsagnsord i bydeform, også efter kolon og semikolon. Knapper,
    links og navne på undtagelseslisten, ventelisten og de falske træf tæller ikke."""
    if undtaget(tekst):
        return []
    ud = []
    for led in SPLIT.split(tekst):
        s = PREFIX.sub('', led).strip()
        # Et enkelt ord med små bogstaver er kode (fx 'hold', 'svar-1nt'), ikke en instruktion.
        if re.fullmatch(r'[a-zæøå0-9-]+', s):
            continue
        første = re.match(r'[A-Za-zÆØÅæøåÉé]+', s)
        # Et ord med store bogstaver er en forkortelse (ØV, NS), ikke et udsagnsord.
        if not første or første.group(0).lower() not in BYDEFORMER or første.group(0).isupper():
            continue
        if undtaget(s) or s in VENTER or any(r.search(led.strip()) or r.search(s) for r in FALSKE_TRÆF):
            continue
        ud.append(s)
    return ud


def script_tekster(kode):
    """Strengene i et script uden kommentarer (det engelske er allerede fjernet af tjek_fagord.dansk_side)."""
    ud = []
    for m in JS_TOKEN.finditer(kode):
        token = m.group(0)
        if token.startswith(('/*', '//')):
            continue
        indhold = token[1:-1]
        if token.startswith('`'):
            # Skabelonstrenge: teksten mellem tags og strengene i ${…}
            ud += [t[1:-1] for t in re.findall(STRENG, indhold)]
            indhold = re.sub(r'\$\{[^}]*\}', ' ', indhold)
        ud += [html.unescape(v) for v in ATTRIBUT.findall(indhold)]
        ud += [html.unescape(t).strip() for t in re.split(r'<[^>]+>', indhold) if t.strip()]
    return ud


def tekster(fil, tekst):
    """Tekststykkerne i en fil, som en læser kan se eller høre."""
    if fil.endswith('.js'):
        return script_tekster(tekst)
    if not fil.endswith('.html'):
        return [tekst]
    ud = []
    for del_ in re.split(r'(<script\b[^>]*>.*?</script>)', tekst, flags=re.S):
        if del_.startswith('<script'):
            ud += script_tekster(re.sub(r'^<script\b[^>]*>|</script>$', '', del_))
            continue
        del_ = re.sub(r'<!--.*?-->', ' ', del_, flags=re.S)
        ud += [html.unescape(v) for v in ATTRIBUT.findall(del_)]
        ud += [html.unescape(t).strip() for t in re.split(r'<[^>]+>', del_) if t.strip()]
    return ud


def al_dansk_tekst():
    """(fil, tekststykker) for al dansk tekst, testen læser."""
    ud = []
    for f, t in dansk_tekst():
        if SPRING_OVER.search(f):
            continue
        # Multitrænerens forklaringer er puljeforklaringer efter kilden (A3).
        t = WHY.sub(' ', t)
        ud.append((f, tekster(f, t)))
    return ud


def selvtest():
    """Testens egne eksempler: den fejler ved bydeform og består ved beskrivende form, knapper og navne."""
    forventet = [
        ('Vælg en konvention og få 8 tilfældige meldeforløb.', ['Vælg en konvention og få 8 tilfældige meldeforløb.']),
        ('Modstanderen åbner 1NT. Meld ind med D (straf).', ['Meld ind med D (straf).']),
        ('Multiforsvar: vælg dit svar i meldekassen; tryk på pæren.', ['vælg dit svar i meldekassen', 'tryk på pæren.']),
        ('Træn konventionerne, til de sidder', ['Træn konventionerne, til de sidder']),
        ('Hver konvention giver 8 tilfældige meldeforløb.', []),
        ('Du vælger dit svar i meldekassen; pæren giver et hint.', []),
        ('Vis alle trænere', []),
        ('Svar på 4NT (1430) og på spørgsmålet efter trumfdamen: …', []),
        ('Spring i ny farve er udgangskrav.', []),
        ('hold', []),
    ]
    return [f'selvtest: bydeform({tekst!r}) gav {bydeform(tekst)}, ventede {ud}' for tekst, ud in forventet
            if bydeform(tekst) != ud]


def main():
    fejl = selvtest()
    alle = al_dansk_tekst()
    for f, stykker in alle:
        for stykke in stykker:
            fejl += [f'{f}: {s[:120]}' for s in bydeform(stykke)]
    # Når Frank har svaret, og en tekst er rettet, skal den af ventelisten.
    står = {PREFIX.sub('', led).strip() for _, stykker in alle for stykke in stykker for led in SPLIT.split(stykke)}
    fejl += [f'ventelisten: "{v}" står ikke længere i teksten' for v in VENTER if v not in står]
    if fejl:
        print('\n'.join(fejl))
        print(f'{len(fejl)} steder er i bydeform.')
        return 1
    print('Beskrivende form: i orden.')
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
