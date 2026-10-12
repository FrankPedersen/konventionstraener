/* Knapper på aftalesiderne: udskriv eller gem som PDF, hent som Word (.doc) og som Markdown (.md).
   Indholdet er sidens <main> uden knapperne. Word-filen er HTML, som Word åbner direkte. */
(function () {
  const main = document.querySelector('main');
  if (!main) return;
  // Udskrift: hver tabel ligger i sin egen blok, så printreglerne i doc-sg.css kan holde den samlet på én side –
  // Chrome deler ellers en tabel, der står direkte i teksten. Tabeller, der allerede har deres egen blok, røres ikke.
  main.querySelectorAll('table').forEach(t => {
    const p = t.parentElement;
    if (p && p.tagName === 'DIV' && p.children.length === 1) return;
    const box = document.createElement('div');
    box.className = 'tabel';
    t.before(box);
    box.appendChild(t);
  });
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
  // Sideskift i Word: ingen række deles over to sider, og hver række holdes sammen med den næste (Words »hold sammen
  // med næste«), så tabellen står samlet på én side, når den kan være der.
  // Word kender kun de gamle navne (page-break-…); browserens style-objekt skriver dem om til break-…, så de skrives
  // direkte i style-attributten.
  const KEEP = 'page-break-after:avoid';
  const addStyle = (el, decl) => {
    const cur = (el.getAttribute('style') || '').trim().replace(/;+$/, '');
    el.setAttribute('style', cur ? cur + ';' + decl : decl);   // Word afviser en style, der starter med »;«
  };
  // En sammenflettet celle (rowspan) foldes ud til en celle pr. række med samme baggrund og uden streg imellem, så den
  // stadig ser sammenhængende ud: Words egne fortsættelsesceller er tomme og bryder »hold sammen med næste«.
  // Teksten flyttes til den midterste række, så den står centreret som på siden.
  function unspan(t) {
    const hold = [];
    [...t.querySelectorAll('tr')].forEach(tr => {
      const cells = [...tr.children].filter(c => c.tagName === 'TH' || c.tagName === 'TD');
      const out = [];
      let i = 0, ci = 0;
      const pending = () => hold.some((h, k) => k >= i && h && h.left > 0);
      while (ci < cells.length || pending()) {
        const h = hold[i];
        if (h && h.left > 0) {
          const c = document.createElement(h.src.tagName);
          c.className = h.src.className;
          const bg = h.src.style.background;
          c.setAttribute('style', (bg ? 'background:' + bg + ';' : '') + 'border-top:none;' + (h.left > 1 ? 'border-bottom:none;' : ''));
          if (++h.row === h.mid) { c.innerHTML = h.src.innerHTML; h.src.innerHTML = ''; }
          out.push(c);
          h.left--; i++;
        } else if (ci < cells.length) {
          const c = cells[ci++];
          const span = +c.getAttribute('rowspan') || 1;
          if (span > 1) {
            hold[i] = { left: span - 1, src: c, row: 0, mid: Math.floor((span - 1) / 2) };
            c.removeAttribute('rowspan');
            addStyle(c, 'border-bottom:none');
          }
          out.push(c);
          i += +c.getAttribute('colspan') || 1;
        } else i++;
      }
      tr.replaceChildren(...out);
    });
  }
  function keepTables(c) {
    c.querySelectorAll('table').forEach(t => {
      unspan(t);
      const rows = [...t.querySelectorAll('tr')];
      rows.forEach((tr, i) => {
        addStyle(tr, 'page-break-inside:avoid');
        const last = i === rows.length - 1;
        [...tr.children].forEach(cell => {
          // cellernes egne marginer og skriftstørrelse (fra designeksporten) erstattes af Word-filens, så tabellen fylder mindre
          cell.style.removeProperty('padding');
          cell.style.removeProperty('font-size');
          // en tom celle får et hårdt mellemrum – ellers mister Word »hold sammen med næste« på cellens afsnit
          if (!cell.textContent.trim()) cell.innerHTML = '&nbsp;';
          const ps = [...cell.children].filter(x => x.tagName === 'P');
          if (!ps.length) cell.innerHTML = `<p style="margin:0">${cell.innerHTML}</p>`;
          // »hold linjer sammen« på hvert afsnit, så heller ikke sidste række deles; i sidste række holdes en celles
          // afsnit også sammen indbyrdes (Word overholder ikke page-break-inside på selve rækken)
          const cps = [...cell.querySelectorAll('p')];
          cps.forEach((p, k) => {
            addStyle(p, 'page-break-inside:avoid');
            if (!last || k < cps.length - 1) addStyle(p, KEEP);
          });
        });
      });
    });
    return c;
  }

  function word() {
    const css = 'body{font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#1a1a1a}'
      + 'h1{font-size:22pt;margin:12pt 0 6pt}h2{font-size:15pt;margin:14pt 0 6pt}h3,h4{font-size:12pt;margin:10pt 0 4pt}'
      + 'h1,h2,h3,h4{' + KEEP + '}tr{page-break-inside:avoid}'
      + 'table{border-collapse:collapse;width:100%;margin:6pt 0 10pt}'
      + 'th,td{border:1px solid #c8c8c8;padding:4pt 6pt;vertical-align:top;text-align:left}th{background:#f2f3f4}'
      + '.su-h,.su-d{color:#c62828}'
      + '.k-gron{background:#edf3e9}.k-bla{background:#e9eef6}.k-gul{background:#faf3e0}'
      + '.k-brun{background:#f7ebe0}.k-rosa{background:#f4e3e3}.k-gra{background:#f2f2f2}';
    return '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">'
      + '<head><meta charset="utf-8"><title>' + esc(name) + '</title>'
      + '<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom></w:WordDocument></xml><![endif]-->'
      + '<style>' + css + '</style></head><body>' + keepTables(content()).innerHTML + '</body></html>';
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
    // Celler med rowspan (fx åbnercellen i systemkortets skemaer) fylder også rækkerne under; dér står en tom celle.
    // Celler med colspan (fx en regel, der gælder både mod farve og sans) gentages i hver kolonne, de dækker.
    const hold = [];
    const rows = [...n.querySelectorAll('tr')].map(tr => {
      const line = [];
      let i = 0;
      const skip = () => { while (hold[i] > 0) { hold[i]--; line[i++] = null; } };
      [...tr.children].filter(c => c.tagName === 'TH' || c.tagName === 'TD').forEach(c => {
        skip();
        const span = +c.getAttribute('rowspan') || 1, cols = +c.getAttribute('colspan') || 1;
        for (let k = 0; k < cols; k++) {
          line[i] = c;
          if (span > 1) hold[i] = span - 1;
          i++;
        }
      });
      for (; i < hold.length; i++) if (hold[i] > 0) { hold[i]--; line[i] = null; }
      return line;
    });
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
