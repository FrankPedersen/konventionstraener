"""
Importerer Flemming & Franks system fra en Claude Design-eksport til viden/2-over-1-flemming.html.

    python tools/import_design.py "C:/Users/frank/Downloads/2 over 1 - Moderne majorstotte.html"

Eksporten er en »bundled page«: indholdet ligger gzip'et i manifestet (doc-content.js med nav og html).
Scriptet pakker det ud og skriver en almindelig statisk side med sitets topmenu, indholdsfortegnelse og søgning.
Ankrene (afsnit-1, bilag-b, afsnit-c4 …) skal bevares – trænerens »Læs aftalen«-links peger på dem.
"""
import base64, gzip, json, os, re, sys, html as H

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '..', 'viden', '2-over-1-flemming.html')
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
for p in nav:
    toc.append('<div class="tp"><a class="lp" href="#%s">%s</a>' % (p['id'], H.escape(p['title'])))
    for it in p['items']:
        toc.append('<a class="li" href="#%s">%s</a>' % (it['id'], H.escape(it['title'])))
    toc.append('</div>')
total = sum(1 + len(p['items']) for p in nav)

CSS = """
:root{ --font-heading:"Cormorant Garamond"; --font-body:"Lora"; --color-bg:#f3f2f2; --color-text:#201f1d; }
*{ box-sizing:border-box; }
body{ margin:0; background:var(--color-bg); color:var(--color-text); font-family:var(--font-body),Lora,Georgia,serif; font-size:15px; line-height:1.55; }
a{ color:#2C5446; } a:hover{ color:#b68235; }
::selection{ background:rgba(182,130,53,0.22); }
.top{ border-bottom:1px solid rgba(32,31,29,0.16); }
.top .in{ display:flex; align-items:center; justify-content:space-between; gap:20px; max-width:1560px; margin:0 auto; padding:14px clamp(14px,3vw,44px); }
.top .brand{ font-family:var(--font-heading),Georgia,serif; font-size:21px; font-weight:600; color:#2C5446; text-decoration:none; }
.top nav{ display:flex; gap:6px; font-size:14px; }
.top nav a{ padding:6px 12px; border:1px solid transparent; border-radius:4px; color:#201f1d; text-decoration:none; }
.top nav a[aria-current]{ border-color:#b68235; color:#2C5446; }
.top nav a:hover{ background:rgba(182,130,53,0.09); color:#2C5446; }
.wrap{ display:flex; flex-wrap:wrap; align-items:flex-start; max-width:1560px; margin:0 auto; padding:0 clamp(14px,3vw,44px) 90px; }
aside{ flex:0 0 292px; min-width:0; padding:26px 24px 48px 0; }
main{ flex:1 1 620px; min-width:0; padding:0 0 0 clamp(0px,3vw,44px); border-left:1px solid rgba(32,31,29,0.16); }
@media (min-width:960px){ aside{ position:sticky; top:0; max-height:100vh; overflow:auto; } }
@media (max-width:959px){ aside{ flex:1 1 100%; padding-right:0; } .toc{ max-height:40vh; overflow:auto; } main{ border-left:0; padding-left:0; } }
.k{ font-family:var(--font-heading),Georgia,serif; font-size:10px; letter-spacing:0.28em; color:#9A7B3F; text-transform:uppercase; margin-bottom:10px; }
.t1{ font-family:var(--font-heading),Georgia,serif; font-size:26px; line-height:1.05; color:#122E42; }
.t2{ font-family:var(--font-heading),Georgia,serif; font-size:16px; line-height:1.2; color:#0E3A52; margin-bottom:16px; }
#q{ width:100%; padding:8px 10px; font:13.5px var(--font-body),Georgia,serif; color:#201f1d; background:transparent; border:1px solid rgba(32,31,29,0.2); border-radius:4px; margin-bottom:6px; }
#q:focus{ outline:2px solid #b68235; outline-offset:2px; }
#cnt{ font-size:11.5px; letter-spacing:0.06em; color:rgba(32,31,29,0.5); padding:4px 0 14px; border-bottom:1px solid rgba(32,31,29,0.16); }
.toc{ display:flex; flex-direction:column; gap:2px; padding-top:12px; }
.tp{ display:flex; flex-direction:column; gap:1px; padding-bottom:10px; }
.toc a{ display:block; text-decoration:none; padding:4px 10px 4px 11px; border-left:2px solid transparent; border-radius:2px; }
.toc a.lp{ font-family:var(--font-heading),Georgia,serif; font-size:16.5px; font-weight:600; line-height:1.25; color:#201f1d; }
.toc a.li{ font-size:13.5px; line-height:1.45; color:rgba(32,31,29,0.7); }
.toc a:hover{ color:#2C5446; background:rgba(182,130,53,0.09); }
.toc a.on{ color:#2C5446; border-left-color:#b68235; background:rgba(182,130,53,0.11); }
.toc .hide{ display:none; }
.hero{ padding:52px 0 34px; border-bottom:1px solid rgba(32,31,29,0.18); }
.hero .k{ font-size:11px; letter-spacing:0.34em; }
.hero h1{ font-family:var(--font-heading),Georgia,serif; font-size:clamp(46px,7vw,82px); font-weight:400; line-height:0.98; letter-spacing:-0.02em; color:#122E42; margin:18px 0 6px; }
.hero .sub{ font-family:var(--font-heading),Georgia,serif; font-size:clamp(24px,3.4vw,36px); line-height:1.1; color:#0E3A52; margin-bottom:24px; }
.hero .d{ display:flex; flex-direction:column; gap:6px; font-size:14.5px; line-height:1.6; color:#5A6B76; max-width:70ch; }
.hero .m{ display:flex; flex-wrap:wrap; gap:22px; margin-top:26px; padding-top:16px; border-top:1px solid rgba(32,31,29,0.14); font-size:13px; letter-spacing:0.04em; color:#5A6B76; }
@media print{ .top, aside{ display:none; } main{ border:0; padding:0; } }
"""

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
<title>2 over 1 · Moderne majorstøtte — Flemming &amp; Frank</title>
<!-- Genereret fra Claude Design-eksporten »2 over 1 - Moderne majorstotte.html« (udgave 3).
     Opdatering: eksportér igen fra Claude Design og kør build_ff_page.py. -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Lora:wght@400;600&display=swap" rel="stylesheet">
<style>""" + CSS + """</style>
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
  <main>
    <header class="hero">
      <div class="k">Bridge · Parsystem · Flemming &amp; Frank</div>
      <h1>2 over 1</h1>
      <div class="sub">Moderne majorstøtte</div>
      <div class="d"><div>Trumfkontrakter · Sanskontrakter · Spærremeldinger · Indmeldinger · Modspil</div>
      <div>Femkorts major · Two over One udgangskrav · Bekkasin · omvendt minor · RKC 1430</div></div>
      <div class="m"><div>Bygger på Femfarve i major (Røn / Reinholdt)</div><div>Udgave 3</div></div>
    </header>
""" + body + """
  </main>
</div>
<script>""" + JS + """</script>
</body>
</html>
"""
open(out, 'w', encoding='utf-8').write(page)
print(len(page), total)
