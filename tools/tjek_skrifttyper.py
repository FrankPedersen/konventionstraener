"""Skrifttyperne ligger på sitet selv: ingen udgivet fil henter fra Google Fonts.

Kør fra repoets rod:  python3 tools/tjek_skrifttyper.py

Udgivet er alle filer i git, som GitHub Pages lægger på sitet: alt undtagen stier, hvor en mappe eller fil begynder med
"_" eller "." (Jekyll springer dem over, fx _design/). Testen fejler, hvis en udgivet html-, css- eller js-fil eller en
af sidegeneratorerne i tools/ henviser til fonts.googleapis.com eller fonts.gstatic.com, eller hvis en skrifttype, som
assets/fonts/*.css nævner, mangler. At siderne ser ud som før, tjekkes i Chrome med `node tools/tjek_skrifttyper.mjs`.
"""
import pathlib
import re
import subprocess
import sys

ROD = pathlib.Path(__file__).resolve().parent.parent
GOOGLE = ('fonts.' + 'googleapis.com', 'fonts.' + 'gstatic.com')
GENERATORER = ('tools/import_design.py', 'tools/build_kamp_viden.py', 'tools/build_konventionskort.py')


def filer():
    ud = subprocess.run(['git', 'ls-files', '-z'], cwd=ROD, capture_output=True, check=True).stdout.decode('utf-8')
    return [f for f in ud.split('\0') if f and (ROD / f).is_file()]


def udgivet(f):
    return not any(del_.startswith(('_', '.')) for del_ in f.split('/'))


def main():
    fejl = []
    for f in filer():
        if (udgivet(f) and f.endswith(('.html', '.css', '.js'))) or f in GENERATORER:
            tekst = (ROD / f).read_text(encoding='utf-8', errors='ignore')
            for g in GOOGLE:
                if g in tekst:
                    fejl.append(f'{f}: henviser til {g}')
    for css in sorted((ROD / 'assets' / 'fonts').glob('*.css')):
        for navn in re.findall(r"url\('([^']+)'\)", css.read_text(encoding='utf-8')):
            sti = css.parent / navn
            if not sti.is_file() or sti.read_bytes()[:4] != b'wOF2':
                fejl.append(f'assets/fonts/{css.name}: {navn} mangler eller er ikke woff2')
    for navn in ('Inter', 'Manrope', 'Noto-Sans-Symbols-2'):
        sti = ROD / 'assets' / 'fonts' / f'OFL-{navn}.txt'
        if not sti.is_file() or 'SIL OPEN FONT LICENSE' not in sti.read_text(encoding='utf-8').upper():
            fejl.append(f'assets/fonts/OFL-{navn}.txt mangler')
    if fejl:
        print('\n'.join(fejl))
        return 1
    print('Skrifttyperne: i orden.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
