// Accepttest i en rigtig browser: skrifttyperne ligger på sitet selv, og siderne ser ud som før. Udgaven før ændringen
// (tagget v-foer-skrifttyper, som henter fra Google Fonts) og den nye vises fra hver sin lokale webserver. På hver side
// sammenlignes de skrifttyper, Chrome faktisk tegner med (overskriften, brødteksten, et Manrope-element og spillefarverne
// ♠♥♦♣); sider uden tilfældige hænder sammenlignes også pixel for pixel. Den nye udgave må ikke hente noget fra Google.
// Kræver Node 22+, git og Chrome eller Edge.
//
//   node tools/tjek_skrifttyper.mjs
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, rmSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROD = fileURLToPath(new URL('..', import.meta.url));
const FOER = 'v-foer-skrifttyper';
const browser = [
  process.env.CHROME,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
].filter(Boolean).find((p) => existsSync(p));
if (!browser) {
  console.error('Fandt hverken Chrome eller Edge; sæt CHROME til stien.');
  process.exit(2);
}

// [side, pixel for pixel?] – trænerne trækker tilfældige hænder, så dem sammenlignes kun på skrifttyperne
const SIDER = [
  ['index.html', true], ['makkeraftaler.html', true], ['traener.html?k=truscott', false], ['markering.html', false],
  ['multi-svar-traener.html', false], ['viden/index.html', true], ['viden/2-over-1.html', true],
  ['viden/2-over-1-makker2.html', true], ['viden/bridgesystem.html', true], ['viden/forslag-2klor-kontrolsvar.html', true],
  ['viden/kampen-om-kontrakten.html', true], ['viden/konventionskort.html#truscott', true],
];

// Udgaven før ændringen pakkes ud fra tagget med et midlertidigt indeks, så repoets eget indeks ikke røres
const gammel = mkdtempSync(join(tmpdir(), 'tjek-skrift-foer-'));
const indeks = { ...process.env, GIT_INDEX_FILE: join(gammel, '.indeks') };
for (const args of [['read-tree', FOER], ['checkout-index', '-a', `--prefix=${gammel.replaceAll('\\', '/')}/`]]) {
  const r = spawnSync('git', args, { cwd: ROD, env: indeks });
  if (r.status !== 0) { console.error(`git ${args[0]} fejlede: ${r.stderr}`); process.exit(2); }
}

const TYPER = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.json': 'application/json', '.txt': 'text/plain; charset=utf-8', '.md': 'text/plain; charset=utf-8' };
async function webserver(mappe) {
  const s = createServer((req, res) => {
    let sti = normalize(join(mappe, decodeURIComponent(new URL(req.url, 'http://x').pathname)));
    if (!sti.startsWith(normalize(mappe))) { res.writeHead(403).end(); return; }
    if (existsSync(sti) && statSync(sti).isDirectory()) sti = join(sti, 'index.html');
    if (!existsSync(sti)) { res.writeHead(404).end(); return; }
    res.writeHead(200, { 'Content-Type': TYPER[extname(sti)] || 'application/octet-stream' }).end(readFileSync(sti));
  });
  await new Promise((r) => s.listen(0, '127.0.0.1', r));
  return { s, url: `http://127.0.0.1:${s.address().port}/` };
}
const før = await webserver(gammel), nu = await webserver(ROD);

const port = 9600 + Math.floor(Math.random() * 90);
const profil = mkdtempSync(join(tmpdir(), 'tjek-skrift-'));
const proces = spawn(browser, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profil}`, '--no-first-run',
  '--hide-scrollbars', '--font-render-hinting=none', 'about:blank'], { stdio: 'ignore' });
const vent = (ms) => new Promise((r) => setTimeout(r, ms));
async function json(sti, metode = 'GET') {
  for (let i = 0; i < 50; i++) {
    try {
      const svar = await fetch(`http://127.0.0.1:${port}${sti}`, { method: metode });
      if (svar.ok) return await svar.json();
    } catch {}
    await vent(200);
  }
  throw new Error(`Browseren svarer ikke på ${sti}`);
}

let fejl = 0;
const tjek = (ok, navn, detalje = '') => {
  if (!ok) fejl++;
  console.log(`${ok ? 'ok  ' : 'FEJL'} ${navn}${!ok && detalje ? ` – ${detalje}` : ''}`);
};

// Markerer de elementer, hvis skrifttyper sammenlignes: overskriften, første afsnit, første element i Manrope og første
// element med en spillefarve i sin egen tekst. Samme regel på begge udgaver, så det er de samme elementer.
const MARKER = `(() => {
  const ud = [];
  const sæt = (navn, el) => { if (el) { el.setAttribute('data-tjek-skrift', navn); ud.push(navn); } };
  sæt('overskrift', document.querySelector('h1'));
  sæt('brødtekst', [...document.querySelectorAll('p')].find((p) => p.textContent.trim().length > 20 && p.offsetParent));
  sæt('manrope', [...document.querySelectorAll('body *')].find((el) => el.offsetParent && el.childNodes.length
    && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) && getComputedStyle(el).fontFamily.startsWith('Manrope')));
  sæt('spillefarver', [...document.querySelectorAll('body *')].find((el) => el.offsetParent
    && [...el.childNodes].some((n) => n.nodeType === 3 && /[♠♥♦♣]/.test(n.textContent))));
  return ud;
})()`;

async function fane() {
  const f = await json('/json/new?about:blank', 'PUT');
  const ws = new WebSocket(f.webSocketDebuggerUrl);
  await new Promise((r, x) => { ws.onopen = r; ws.onerror = x; });
  let id = 0;
  const ventende = new Map();
  const kald = [];
  let indlæst = 0;
  ws.onmessage = (m) => {
    const d = JSON.parse(m.data);
    if (d.id && ventende.has(d.id)) { ventende.get(d.id)(d); ventende.delete(d.id); }
    else if (d.method === 'Page.loadEventFired') indlæst++;
    else if (d.method === 'Network.requestWillBeSent') kald.push(d.params.request.url);
  };
  const send = (method, params = {}) => new Promise((r) => { const n = ++id; ventende.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
  const kør = async (expression) => (await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true })).result.result?.value;
  await send('Page.enable'); await send('Network.enable'); await send('DOM.enable'); await send('CSS.enable');
  return {
    send, kør, kald,
    async åbn(url, bredde) {
      await send('Emulation.setDeviceMetricsOverride', { width: bredde, height: 900, deviceScaleFactor: 1, mobile: bredde < 600 });
      const n = indlæst; kald.length = 0;
      await send('Page.navigate', { url: 'about:blank' });
      await send('Page.navigate', { url });
      for (let i = 0; i < 150 && indlæst <= n; i++) await vent(100);
      await kør('document.fonts.ready.then(() => new Promise((r) => setTimeout(r, 600)))');
    },
    async skrifter(navn, medAntal) {
      const doc = await send('DOM.getDocument', { depth: -1 });
      const q = await send('DOM.querySelector', { nodeId: doc.result.root.nodeId, selector: `[data-tjek-skrift="${navn}"]` });
      if (!q.result?.nodeId) return null;
      const f = await send('CSS.getPlatformFontsForNode', { nodeId: q.result.nodeId });
      return (f.result?.fonts ?? []).map((x) => `${x.familyName}${x.isCustomFont ? '' : ' (system)'}${medAntal ? ':' + x.glyphCount : ''}`).sort().join(', ');
    },
    async billede() {
      const r = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
      return r.result.data;
    },
    luk: async () => { ws.close(); await json(`/json/close/${f.id}`).catch(() => {}); },
  };
}

// Sammenligner to PNG-billeder pixel for pixel i browseren
async function forskel(t, a, b) {
  return t.kør(`(async () => {
    const læs = (d) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = 'data:image/png;base64,' + d; });
    const [x, y] = await Promise.all([læs(${JSON.stringify(a)}), læs(${JSON.stringify(b)})]);
    if (x.width !== y.width || x.height !== y.height) return { størrelse: [x.width, x.height, y.width, y.height] };
    const px = (i) => { const c = new OffscreenCanvas(i.width, i.height); const g = c.getContext('2d'); g.drawImage(i, 0, 0); return g.getImageData(0, 0, i.width, i.height).data; };
    const p = px(x), q = px(y); let n = 0;
    for (let k = 0; k < p.length; k += 4) if (p[k] !== q[k] || p[k + 1] !== q[k + 1] || p[k + 2] !== q[k + 2]) n++;
    return { n, ialt: p.length / 4 };
  })()`);
}

try {
  await json('/json/version');
  const t = await fane();
  for (const [side, pixel] of SIDER) {
    for (const bredde of [390, 1280]) {
      await t.åbn(før.url + side, bredde);
      const bGammel = pixel ? await t.billede() : null;
      const navne = await t.kør(MARKER);
      const fGammel = {}; for (const n of navne) fGammel[n] = await t.skrifter(n, pixel);
      await t.åbn(nu.url + side, bredde);
      const google = t.kald.filter((u) => /fonts\.(googleapis|gstatic)\.com/.test(u));
      const egne = t.kald.filter((u) => u.includes('/assets/fonts/') && u.endsWith('.woff2'));
      const bNu = pixel ? await t.billede() : null;
      const navneNu = await t.kør(MARKER);
      tjek(google.length === 0 && egne.length > 0, `${side} ${bredde} px: intet hentes fra Google; ${egne.length} skrifttyper fra assets/fonts/`, google.join(' '));
      tjek(navne.join() === navneNu.join(), `${side} ${bredde} px: samme elementer at sammenligne (${navne.join(', ')})`, navneNu.join(', '));
      for (const n of navne) {
        const s = await t.skrifter(n, pixel);
        tjek(fGammel[n] && fGammel[n] === s, `${side} ${bredde} px: ${n} tegnes med ${s}`, `før: ${fGammel[n]}`);
      }
      if (pixel) {
        const d = await forskel(t, bGammel, bNu);
        tjek(d.n === 0, `${side} ${bredde} px: siden er pixel for pixel som før`, JSON.stringify(d));
      }
    }
  }
  await t.luk();
} finally {
  proces.kill();
  før.s.close(); nu.s.close();
  await vent(300);
  for (const m of [profil, gammel]) { try { rmSync(m, { recursive: true, force: true }); } catch {} }
}
process.exit(fejl ? 1 : 0);
