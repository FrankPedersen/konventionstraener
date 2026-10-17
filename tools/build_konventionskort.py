"""Bygger viden/konventionskort.html og assets/konventionskort-hint.js fra tools/konventionskort.src.html og skalfilerne
tools/konventionskort-shell.html og tools/konventionskort-hint-shell.js.

Kør fra repoets rod:  python3 tools/build_konventionskort.py
Ret aldrig i viden/konventionskort.html eller assets/konventionskort-hint.js direkte. Kortenes indhold ligger i data/kort/ og læses af siden, når den åbnes.
"""
import re, pathlib

HER = pathlib.Path(__file__).resolve().parent
ROD = HER.parent
src = (HER / 'konventionskort.src.html').read_text(encoding='utf-8')

# Siden lægges i shadow DOM, så site.css og kortets klasser ikke støder sammen
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
css = re.sub(r'@media \(prefers-color-scheme: dark\)\{ :root:not\(\[data-theme="light"\]\)\{.*?\}\}\n', '', css, flags=re.S)
css = re.sub(r':root\[data-theme="dark"\]\{.*?\}\n', '', css, flags=re.S)
assert 'prefers-color-scheme: dark' not in css and 'data-theme' not in css
css = css.replace(':root{', ':host{display:block;', 1).replace('--canvas:#f4f4f3', '--canvas:var(--sg-canvas-soft,#f2f3f4)', 1)
css = re.sub(r'\nbody\{.*?\}\n', '\n.kk-body{color:var(--ink);font:16px/1.6 var(--sans);padding:24px 0 64px}\n', css, count=1, flags=re.S)
markup = re.search(r'(<div class="wrap">.*?\n</div>)\n', src, re.S).group(1)
script = re.search(r'<script>\n(.*?)</script>', src, re.S).group(1)
# ⓘ i trænerne bruger de samme visningsfunktioner: fra KATEGORI til vaelg(), uden sidens egen opstart
visning = re.search(r'\n(const KATEGORI = .*?)\nfunction vaelg\(', script, re.S).group(1)
assert 'document.' not in visning and 'function kompakt(' in visning
script = script.replace("JSON.parse(document.getElementById('data').textContent)", 'null')
script = script.replace('document.getElementById(', 'R.getElementById(')
script = script.replace('document.querySelectorAll(', 'R.querySelectorAll(')
script = script.replace("document.addEventListener('click'", "R.addEventListener('click'")
assert 'document.' not in script.replace('document.title', '')
shell = (HER / 'konventionskort-shell.html').read_text(encoding='utf-8')
side = (shell.replace('/*CSS*/', css.replace('`', '\\`').replace('${', '\\${'))
            .replace('<!--MARKUP-->', markup.replace('`', '\\`'))
            .replace('/*SCRIPT*/', script))
out = ROD / 'viden' / 'konventionskort.html'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(side, encoding='utf-8', newline='\n')
print('Bygget', out.relative_to(ROD))

hint_shell = (HER / 'konventionskort-hint-shell.js').read_text(encoding='utf-8')
hint = (hint_shell.replace('/*CSS*/', css.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${'))
                  .replace('/*SCRIPT*/', visning))
out = ROD / 'assets' / 'konventionskort-hint.js'
out.write_text(hint, encoding='utf-8', newline='\n')
print('Bygget', out.relative_to(ROD))
