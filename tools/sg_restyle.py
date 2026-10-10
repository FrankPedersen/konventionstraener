"""
Oversætter Claude Design-eksportens inline-farver til designsystemet Subtle Gradient.

Bruges af import_design.py og kan køres alene på den færdige side:

    python tools/sg_restyle.py viden/2-over-1-makker2.html

Farvenøglens seks kategorifarver (grøn, blå, gul, brun, rosa, grå), zonefarverne i bilag D
og de røde kulører bevares – de betyder noget i teksten. Kun tekstfarver, accenter og rammer skiftes.
Skrifterne skiftes via --font-heading og --font-body i assets/doc-sg.css.
"""
import re, sys

INK, BODY, MUTE, SOFT = '#1a1a1a', '#4a4a4a', '#8a8a8a', '#f2f3f4'
COLORS = {
    '#2c5446': INK, '#3d6e58': INK, '#122e42': INK, '#0e3a52': INK, '#201f1d': INK,   # overskrifter og tekst
    '#555555': BODY, '#5a6b76': BODY, '#9a7b3f': BODY, '#7a5520': BODY,              # sekundær tekst
    '#b68235': MUTE,                                                                    # rammen om »alertér«
    '#f3f2f2': SOFT,
}

def restyle(html):
    html = re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: COLORS.get(m.group(0).lower(), m.group(0)), html)
    html = html.replace('rgba(182,130,53,0.38)', 'rgba(26,26,26,0.12)')
    # »alertér«-mærker og farvenøglens felter som piller
    html = html.replace(f'border:1px solid {MUTE};border-radius:3px', f'border:1px solid {MUTE};border-radius:9999px')
    html = html.replace('padding:7px 11px;border-radius:4px', 'padding:7px 11px;border-radius:9999px')
    return html

if __name__ == '__main__':
    p = sys.argv[1]
    raw = open(p, encoding='utf-8', newline='').read()
    out = restyle(raw)
    open(p, 'w', encoding='utf-8', newline='').write(out)
    print(p, 'ændret' if out != raw else 'uændret')
