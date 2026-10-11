/* Knapper på aftalesiderne: udskriv eller gem som PDF, hent som Word (.doc) og som Markdown (.md).
   Indholdet er sidens <main> uden knapperne. Word-filen er HTML, som Word åbner direkte. */
(function () {
  const main = document.querySelector('main');
  if (!main) return;
  const name = document.title.split(' — ')[0].replace(/\s*·\s*/g, ' – ').replace(/&/g, 'og').replace(/[\\/:*?"<>|]/g, '').trim() || 'Aftaler';

  const bar = document.createElement('div');
  bar.className = 'export-bar';
  bar.setAttribute('role', 'group');
  bar.setAttribute('aria-label', 'Udskriv eller hent');
  bar.innerHTML = '<button type="button" class="primary" data-x="pdf">Udskriv eller gem som PDF</button>'
                + '<button type="button" data-x="doc">Hent som Word</button>'
                + '<button type="button" data-x="md">Hent som Markdown</button>';
  (main.querySelector('header.hero') || main).appendChild(bar);

  bar.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.dataset.x === 'pdf') window.print();
    if (b.dataset.x === 'doc') download(name + '.doc', '﻿' + word(), 'application/msword');
    if (b.dataset.x === 'md') download(name + '.md', markdown(), 'text/markdown');
  });

  function content() {
    const c = main.cloneNode(true);
    c.querySelectorAll('.export-bar, script, style, colgroup').forEach(n => n.remove());
    return c;
  }

  function download(file, text, type) {
    const url = URL.createObjectURL(new Blob([text], { type: type + ';charset=utf-8' }));
    const a = document.createElement('a');
    a.href = url; a.download = file;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  }

  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ---------- Word ---------- */
  function word() {
    const css = 'body{font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#1a1a1a}'
      + 'h1{font-size:22pt;margin:12pt 0 6pt}h2{font-size:15pt;margin:14pt 0 6pt}h3,h4{font-size:12pt;margin:10pt 0 4pt}'
      + 'table{border-collapse:collapse;width:100%;margin:6pt 0 10pt}'
      + 'th,td{border:1px solid #c8c8c8;padding:4pt 6pt;vertical-align:top;text-align:left}th{background:#f2f3f4}'
      + '.su-h,.su-d{color:#c00000}';
    return '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">'
      + '<head><meta charset="utf-8"><title>' + esc(name) + '</title>'
      + '<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom></w:WordDocument></xml><![endif]-->'
      + '<style>' + css + '</style></head><body>' + content().innerHTML + '</body></html>';
  }

  /* ---------- Markdown ---------- */
  const BLOCK = new Set(['P', 'DIV', 'SECTION', 'HEADER', 'FOOTER', 'ARTICLE', 'MAIN', 'NAV', 'ASIDE', 'FIGURE',
    'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'UL', 'OL', 'LI', 'TABLE', 'BLOCKQUOTE', 'PRE', 'HR']);
  const isBlock = n => n.nodeType === 1 && BLOCK.has(n.tagName);

  function inline(n) {
    if (n.nodeType === 3) return n.textContent.replace(/\s+/g, ' ');
    if (n.nodeType !== 1) return '';
    const t = n.tagName, inner = () => [...n.childNodes].map(inline).join('');
    if (t === 'BR') return '<br>';
    if (t === 'STRONG' || t === 'B') { const s = inner().trim(); return s ? '**' + s + '** ' : ''; }
    if (t === 'EM' || t === 'I') { const s = inner().trim(); return s ? '*' + s + '* ' : ''; }
    if (t === 'CODE') return '`' + n.textContent + '`';
    if (t === 'A') {
      const s = inner().trim(), href = n.getAttribute('href') || '';
      return href && !href.startsWith('#') ? '[' + s + '](' + n.href + ')' : s;
    }
    return inner();
  }
  const tidy = s => s.replace(/ +/g, ' ').replace(/ ([,.;:!?)])/g, '$1').replace(/\( /g, '(').trim();

  function cell(n) {
    const parts = [];
    let run = '';
    for (const c of n.childNodes) {
      if (isBlock(c)) { if (tidy(run)) parts.push(tidy(run)); run = ''; const s = tidy(inline(c)); if (s) parts.push(s); }
      else run += inline(c);
    }
    if (tidy(run)) parts.push(tidy(run));
    return parts.join('<br>').replace(/\|/g, '\\|');
  }

  function table(n) {
    const rows = [...n.querySelectorAll('tr')].map(tr => [...tr.children].filter(c => c.tagName === 'TH' || c.tagName === 'TD'));
    if (!rows.length) return '';
    if (rows.length === 1 && rows[0].length === 1) return '> ' + cell(rows[0][0]).replace(/<br>/g, '\n> ') + '\n\n';
    const width = Math.max(...rows.map(r => r.length));
    const line = r => '| ' + Array.from({ length: width }, (_, i) => r[i] ? cell(r[i]) : '').join(' | ') + ' |';
    // Første række bliver overskrift – også når tabellen ikke har <thead>; den er fed i forvejen
    const out = [line(rows[0]).replace(/\*\*/g, ''), '| ' + Array(width).fill('---').join(' | ') + ' |'];
    rows.slice(1).forEach(r => out.push(line(r)));
    return out.join('\n') + '\n\n';
  }

  function block(n, ctx) {
    if (n.nodeType === 3) { const s = tidy(n.textContent); return s ? s + '\n\n' : ''; }
    if (n.nodeType !== 1) return '';
    const t = n.tagName;
    if (/^H[1-6]$/.test(t)) {
      const lvl = ctx.hero ? 1 : Math.min(6, Math.max(2, +t[1] + ctx.shift));
      return '#'.repeat(lvl) + ' ' + tidy(inline(n)) + '\n\n';
    }
    if (t === 'TABLE') return table(n);
    if (t === 'HR') return '---\n\n';
    if (t === 'PRE') return '```\n' + n.textContent.replace(/\n$/, '') + '\n```\n\n';
    if (t === 'UL' || t === 'OL') {
      return [...n.children].filter(li => li.tagName === 'LI')
        .map((li, i) => (t === 'OL' ? (i + 1) + '. ' : '- ') + tidy(inline(li))).join('\n') + '\n\n';
    }
    if (t === 'BLOCKQUOTE') return blocks(n, ctx).trim().split('\n').map(l => '> ' + l).join('\n') + '\n\n';
    if ([...n.childNodes].some(isBlock)) return blocks(n, { ...ctx, hero: ctx.hero || (t === 'HEADER' && n.classList.contains('hero')) });
    const s = tidy(inline(n));
    return s ? s + '\n\n' : '';
  }
  const blocks = (n, ctx) => {
    let out = '', run = '';
    for (const c of n.childNodes) {
      if (isBlock(c)) { if (tidy(run)) out += tidy(run) + '\n\n'; run = ''; out += block(c, ctx); }
      else run += inline(c);
    }
    if (tidy(run)) out += tidy(run) + '\n\n';
    return out;
  };

  function markdown() {
    const c = content();
    // Sidens titel bliver #; den øverste overskrift i indholdet bliver ##, uanset om siden bruger h1 eller h2 til den
    const levels = [...c.querySelectorAll('h1, h2, h3, h4, h5, h6')].filter(h => !h.closest('header.hero')).map(h => +h.tagName[1]);
    const shift = levels.length ? 2 - Math.min(...levels) : 1;
    return blocks(c, { hero: false, shift }).replace(/\n{3,}/g, '\n\n').trim() + '\n';
  }
})();
