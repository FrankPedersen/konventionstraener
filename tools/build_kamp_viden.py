"""
Bygger viden/kampen-om-kontrakten.html fra docs/kampen-om-kontrakten.md (referencedokumentet 01-principper.md
plus vores tillæg om forsvar mod 1NT). Samme ramme og stil som systemsiderne.

    python tools/build_kamp_viden.py
"""
import os, re, html as H

ROOT = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(ROOT, 'docs', 'kampen-om-kontrakten.md')
OUT = os.path.join(ROOT, 'viden', 'kampen-om-kontrakten.html')

def slug(t):
    t = t.lower()
    for a, b in (('æ', 'ae'), ('ø', 'oe'), ('å', 'aa'), ('♣', ''), ('♦', ''), ('♥', ''), ('♠', '')):
        t = t.replace(a, b)
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return t

def inline(t):
    t = H.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'([♥♦])', r'<span class="su su-h">\1</span>', t)
    return t

def convert(md):
    out, nav, i = [], [], 0
    lines = md.split('\n')
    open_section = False
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            j = i + 1
            while j < len(lines) and not lines[j].startswith('```'):
                j += 1
            out.append('<pre>' + H.escape('\n'.join(lines[i + 1:j])) + '</pre>')
            i = j + 1
            continue
        m = re.match(r'(#{1,3}) (.*)', ln)
        if m:
            lvl, title = len(m.group(1)), m.group(2).strip()
            if lvl == 1:
                i += 1
                continue                      # dokumenttitlen står i forsiden
            sid = slug(title)
            if lvl == 2:
                if open_section:
                    out.append('</section>')
                out.append(f'<section class="part"><h1 id="{sid}">{inline(title)}</h1>')
                open_section = True
                nav.append({'id': sid, 'title': title, 'items': []})
            else:
                out.append(f'<h2 id="{sid}">{inline(title)}</h2>')
                if nav:
                    nav[-1]['items'].append({'id': sid, 'title': title})
            i += 1
            continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r':?-+:?', c) for c in r)]
            out.append('<table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>'
                       + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body) + '</tbody></table>')
            continue
        if ln.startswith('> '):
            q = []
            while i < len(lines) and lines[i].startswith('>'):
                q.append(lines[i][1:].strip())
                i += 1
            out.append('<blockquote>' + inline(' '.join(q)) + '</blockquote>')
            continue
        if re.match(r'(-|\d+\.) ', ln):
            tag = 'ol' if ln[0].isdigit() else 'ul'
            items = []
            while i < len(lines) and re.match(r'(-|\d+\.) ', lines[i]):
                items.append(re.sub(r'^(-|\d+\.) ', '', lines[i]))
                i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
            continue
        if ln.strip() == '---':
            i += 1
            continue
        if ln.strip():
            p = []
            while i < len(lines) and lines[i].strip() and not re.match(r'(#|\||>|-|\d+\.|```)', lines[i]):
                p.append(lines[i].strip())
                i += 1
            out.append('<p>' + inline(' '.join(p)) + '</p>')
            continue
        i += 1
    if open_section:
        out.append('</section>')
    return '\n'.join(out), nav

def main():
    # JS (indholdsfortegnelsens markering og søgning) deles med tools/import_design.py. Stilen ligger i
    # assets/doc-sg.css (Subtle Gradient), fælles for dokumentsiderne, ligesom topbjælken og sidefoden.
    src = open(os.path.join(os.path.dirname(__file__), 'import_design.py'), encoding='utf-8').read()
    JS = re.search(r'JS = """(.*?)"""', src, re.S).group(1)
    body, nav = convert(open(SRC, encoding='utf-8').read())
    total = sum(1 + len(p['items']) for p in nav)
    JS = JS.replace('TOTAL', str(total))
    toc = []
    plain = lambda t: re.sub(r'[*`]', '', t).strip()
    for p in nav:
        p['title'] = plain(p['title'])
        for it in p['items']:
            it['title'] = plain(it['title'])
        toc.append('<div class="tp"><a class="lp" href="#%s">%s</a>' % (p['id'], re.sub(r'([♥♦])', r'<span class="su su-h">\1</span>', H.escape(p['title']))))
        toc += ['<a class="li" href="#%s">%s</a>' % (it['id'], re.sub(r'([♥♦])', r'<span class="su su-h">\1</span>', H.escape(it['title']))) for it in p['items']]
        toc.append('</div>')
    page = """<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kampen om kontrakten — Konventionstræner</title>
<link rel="canonical" href="https://www.kontraktbridge.dk/konventionstraener/viden/kampen-om-kontrakten.html">
<!-- Genereret af tools/build_kamp_viden.py fra docs/kampen-om-kontrakten.md – ret i markdown-filen. -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Manrope:wght@800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Symbols+2&text=%E2%99%A0%E2%99%A5%E2%99%A6%E2%99%A3&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/doc-sg.css?v=2026-10-18">
</head>
<body>
<header id="topbjaelke" data-aktiv="viden"></header>
<script src="../assets/topbar.js"></script>
<div class="wrap">
  <aside>
    <div class="k">Referencelag · Forsvar og indmelding</div>
    <div class="t1">Kampen om kontrakten</div>
    <div class="t2">20-20 · konkurrerende meldeforløb</div>
    <input id="q" type="search" placeholder="Søg i indholdet…" aria-label="Søg i indholdet">
    <div id="cnt">""" + "%d overskrifter · %d dele" % (total, len(nav)) + """</div>
    <nav class="toc" id="toc">
""" + "\n".join(toc) + """
    </nav>
  </aside>
  <main class="doc">
    <header class="hero">
      <div class="k">Referencelag · konkurrerende meldeforløb</div>
      <h1>Kampen om kontrakten</h1>
      <div class="sub">Forsvar og indmelding</div>
      <div class="d"><div>Kilde: <em>20-20 – kampen om kontrakten</em> (opfølger til <em>Kampen ved bridgebordet</em>, 2017), omskrevet til regelform.</div>
      <div>Profiler: Grund = bogens regler · Klub = + faste aftaler · Turnering = + Stenberg og Lebensohl</div>
      <div><strong>(aftale)</strong> = vores beslutning, hvor bogen ikke tager stilling · ⚠ = kendt fælde</div></div>
      <div class="m"><div><a href="../#traen">Træn emnerne →</a></div></div>
    </header>
""" + body + """
  </main>
</div>
<script>""" + JS + """</script>
<script src="../assets/doc-export.js?v=2026-10-14" defer></script>
<footer id="sidefod"></footer>
<script src="../assets/footer.js"></script>
</body>
</html>
"""
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)
    print(OUT, total)

if __name__ == '__main__':
    main()
