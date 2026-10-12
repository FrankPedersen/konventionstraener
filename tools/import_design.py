"""
Importerer systemet for Makker 2 & mig fra en Claude Design-eksport til viden/2-over-1-makker2.html.

    python tools/import_design.py "C:/Users/frank/Downloads/2 over 1 - Moderne majorstotte.html"

Eksporten er en »bundled page«: indholdet ligger gzip'et i manifestet (doc-content.js med nav og html).
Scriptet pakker det ud og skriver en almindelig statisk side med sitets topmenu, indholdsfortegnelse og søgning.
Ankrene (afsnit-1, bilag-b, afsnit-c4 …) skal bevares – trænerens »Læs aftalen«-links peger på dem.
Layoutet er designsystemet Subtle Gradient: assets/doc-sg.css, og tools/sg_restyle.py oversætter eksportens farver.
Rettelser lavet direkte i den færdige side (fx tilføjelserne i C4 · Lebensohl) skal også ind i Claude Design-
dokumentet – ellers forsvinder de ved næste import.
"""
import base64, gzip, json, os, re, sys, html as H

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sg_restyle import restyle

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '..', 'viden', '2-over-1-makker2.html')
bundle = open(src, encoding='utf-8').read()
manifest = json.loads(re.search(r'<script type="__bundler/manifest">\s*(\{.*?\})\s*</script>', bundle, re.S).group(1))
ext = json.loads(re.search(r'<script type="__bundler/ext_resources">\s*(\[.*?\])\s*</script>', bundle, re.S).group(1))
uuid = next(e['uuid'] for e in ext if e['id'] == 'docContent')
entry = manifest[uuid]
raw = base64.b64decode(entry['data'])
js = (gzip.decompress(raw) if entry.get('compressed') else raw).decode('utf-8')
i = js.index('export const html')
nav = json.loads(js[js.index('=') + 1:i].strip().rstrip(';'))
body = json.loads(js[js.index('=', i) + 1:].strip().rstrip(';'))

toc = []
red = lambda t: re.sub(r'([♥♦])', r'<span style="color:#c62828">\1</span>', H.escape(t))
for p in nav:
    toc.append('<div class="tp"><a class="lp" href="#%s">%s</a>' % (p['id'], red(p['title'])))
    for it in p['items']:
        toc.append('<a class="li" href="#%s">%s</a>' % (it['id'], red(it['title'])))
    toc.append('</div>')
total = sum(1 + len(p['items']) for p in nav)


JS = """
(function(){
  var links=[].slice.call(document.querySelectorAll('#toc a'));
  var ids=links.map(function(a){return a.getAttribute('href').slice(1);});
  function spy(){ var cur=ids[0];
    ids.forEach(function(id){ var el=document.getElementById(id); if(el && el.getBoundingClientRect().top<=130) cur=id; });
    links.forEach(function(a){ a.classList.toggle('on', a.getAttribute('href')==='#'+cur); }); }
  window.addEventListener('scroll',spy,{passive:true}); spy();
  var q=document.getElementById('q'), cnt=document.getElementById('cnt'), base=cnt.textContent;
  q.addEventListener('input',function(){ var v=q.value.trim().toLowerCase(), n=0;
    [].slice.call(document.querySelectorAll('#toc .tp')).forEach(function(g){
      var as=[].slice.call(g.querySelectorAll('a')), self=as[0].textContent.toLowerCase().indexOf(v)>=0, any=false;
      as.slice(1).forEach(function(a){ var ok=!v||self||a.textContent.toLowerCase().indexOf(v)>=0; a.classList.toggle('hide',!ok); if(ok){any=true;n++;} });
      var show=!v||self||any; as[0].classList.toggle('hide',!show); if(show) n++; });
    cnt.textContent = v ? n+' af TOTAL overskrifter' : base; });
})();
""".replace('TOTAL', str(total))

page = """<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>2 over 1 · Moderne majorstøtte — Makker 2 &amp; mig</title>
<!-- Genereret fra Claude Design-eksporten »2 over 1 - Moderne majorstotte.html« (udgave 3).
     Opdatering: eksportér igen fra Claude Design og kør tools/import_design.py. -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Manrope:wght@800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/doc-sg.css?v=2026-10-14">
</head>
<body>
<header class="top"><div class="in">
  <a class="brand" href="../">Konventionstræner</a>
  <nav><a href="../#traen">Træn</a><a href="./" aria-current="page">Viden</a></nav>
</div></header>
<div class="wrap">
  <aside>
    <div class="k">Bridge · Parsystem</div>
    <div class="t1">2 over 1</div>
    <div class="t2">Moderne majorstøtte</div>
    <input id="q" type="search" placeholder="Søg i indholdet…" aria-label="Søg i indholdet">
    <div id="cnt">""" + "%d overskrifter · %d dele" % (total, len(nav)) + """</div>
    <nav class="toc" id="toc">
""" + "\n".join(toc) + """
    </nav>
  </aside>
  <main class="export">
    <header class="hero">
      <div class="k">Bridge · Parsystem · Makker 2 &amp; mig</div>
      <h1>2 over 1</h1>
      <div class="sub">Moderne majorstøtte</div>
      <div class="d"><div>Trumfkontrakter · Sanskontrakter · Spærremeldinger · Indmeldinger · Modspil</div>
      <div>Femkorts major · Two over One udgangskrav · Bekkasin · omvendt minor · RKC 1430</div></div>
      <div class="m"><div>Bygger på Femfarve i major (Røn / Reinholdt)</div><div>Udgave 3.1</div></div>
    </header>
""" + restyle(body) + """
  </main>
</div>
<script>""" + JS + """</script>
<script src="../assets/doc-export.js?v=2026-10-14" defer></script>
</body>
</html>
"""
open(out, 'w', encoding='utf-8').write(page)
print(len(page), total)
