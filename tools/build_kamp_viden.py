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
    import importlib.util
    spec = importlib.util.spec_from_file_location('imp', os.path.join(os.path.dirname(__file__), 'import_design.py'))
    src = open(spec.origin, encoding='utf-8').read()
    CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)
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
        toc.append('<div class="tp"><a class="lp" href="#%s">%s</a>' % (p['id'], re.sub(r'([♥♦])', r'<span class="su su-h"></span>', H.escape(p['title']))))
        toc += ['<a class="li" href="#%s">%s</a>' % (it['id'], re.sub(r'([♥♦])', r'<span class="su su-h"></span>', H.escape(it['title']))) for it in p['items']]
        toc.append('</div>')
    CSS += """
.doc h1{ font-family:var(--font-heading),Georgia,serif; font-size:36px; font-weight:400; line-height:1.1; color:#2C5446; margin:0 0 18px; }
.doc section.part{ padding:40px 0 8px; border-top:1px solid rgba(32,31,29,0.18); margin-top:36px; }
.doc header.hero + section.part{ border-top:0; margin-top:0; }
.doc h2{ font-family:var(--font-heading),Georgia,serif; font-size:26px; font-weight:400; line-height:1.15; color:#3D6E58; margin:30px 0 12px; }
.doc h1, .doc h2{ scroll-margin-top:20px; }
.doc p, .doc li{ line-height:1.75; max-width:78ch; }
.doc p{ margin:0 0 14px; }
.doc table{ display:block; overflow-x:auto; border-collapse:collapse; font-size:15px; line-height:1.55; margin:18px 0 24px; }
.doc th{ text-align:left; padding:0 14px 9px; border-bottom:1.5px solid #2C5446; font-family:var(--font-heading),Georgia,serif; font-size:17px; font-weight:600; color:#2C5446; }
.doc td{ padding:9px 14px; border-bottom:1px solid rgba(32,31,29,0.13); vertical-align:top; }
.doc tbody tr:nth-child(odd) td{ background:rgba(237,243,233,0.55); }
.doc blockquote{ margin:18px 0; padding:12px 18px; border-left:3px solid #b68235; background:rgba(182,130,53,0.08); font-family:var(--font-heading),Georgia,serif; font-size:21px; color:#122E42; }
.doc code{ font-size:13px; background:rgba(32,31,29,0.06); padding:1px 5px; border-radius:3px; }
.doc pre{ font-size:13px; background:rgba(32,31,29,0.05); padding:12px 14px; border-radius:4px; overflow-x:auto; }
.su-h{ color:#C00000; }
"""
    page = """<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kampen om kontrakten — Konventionstræner</title>
<!-- Genereret af tools/build_kamp_viden.py fra docs/kampen-om-kontrakten.md – ret i markdown-filen. -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Lora:wght@400;600&display=swap" rel="stylesheet">
<style>""" + CSS + """</style>
</head>
<body>
<header class="top"><div class="in">
  <a class="brand" href="../">Konventionstræner</a>
  <nav><a href="../?system=kamp#traen">Træn</a><a href="./" aria-current="page">Viden</a></nav>
</div></header>
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
      <h1 style="font-size:clamp(42px,6.5vw,76px);line-height:0.98;letter-spacing:-0.02em;color:#122E42;margin:18px 0 6px">Kampen om kontrakten</h1>
      <div class="sub">Forsvar og indmelding</div>
      <div class="d"><div>Kilde: <em>20-20 – kampen om kontrakten</em> (opfølger til <em>Kampen ved bridgebordet</em>, 2017), omskrevet til regelform.</div>
      <div>Profiler: Grund = bogens regler · Klub = + faste aftaler · Turnering = + Stenberg og Lebensohl</div>
      <div><strong>(aftale)</strong> = vores beslutning, hvor bogen ikke tager stilling · ⚠ = kendt fælde</div></div>
      <div class="m"><div><a href="../?system=kamp#traen">Træn emnerne →</a></div></div>
    </header>
""" + body + """
  </main>
</div>
<script>""" + JS + """</script>
</body>
</html>
"""
    open(OUT, 'w', encoding='utf-8').write(page)
    print(OUT, total)

if __name__ == '__main__':
    main()
