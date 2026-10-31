// Accepttest (SPEC-bred-layout.md i Fordelingstræneren; SPEC-bred-layout.md her): multi-svar-træneren har to spalter
// fra 1000 px og er uændret under. Siden vises fra en lokal webserver i Chrome uden vindue, og siden før ændringen vises
// fra tagget v-foer-bred-layout (filerne læses med git show). Ved 1280 px står hånden til venstre og meldingerne,
// meldekassen og forklaringen til højre med toppene ud for hinanden; indholdet er højst 1120 px bredt i midten, og hånden
// står fast, når der rulles. Ved 1000 px er højre spalte mindst 400 px. Ved 999 og 390 px er siden pixel for pixel som
// før, både ved første hånd og efter et svar. Kræver Node 22+, git og Chrome eller Edge.
//
//   node tools/tjek_bred_multi.mjs
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, rmSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROD = fileURLToPath(new URL('..', import.meta.url));
const TAG = 'v-foer-bred-layout';
const SIDE = 'multi-svar-traener.html';
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

const TYPER = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.json': 'application/json', '.txt': 'text/plain; charset=utf-8', '.md': 'text/plain; charset=utf-8' };
/** Webserver for arbejdsmappen eller, med tag, for filerne i tagget. */
async function webserver(tag) {
  const s = createServer((req, res) => {
    let sti = decodeURIComponent(new URL(req.url, 'http://x').pathname).replace(/^\/+/, '');
    if (sti === '' || sti.endsWith('/')) sti += 'index.html';
    if (sti.split('/').includes('..')) { res.writeHead(403).end(); return; }
    let indhold;
    if (tag) {
      const r = spawnSync('git', ['show', `${tag}:${sti}`], { cwd: ROD, maxBuffer: 64 * 1024 * 1024 });
      if (r.status === 0) indhold = r.stdout;
    } else {
      const fil = normalize(join(ROD, sti));
      if (fil.startsWith(normalize(ROD)) && existsSync(fil) && statSync(fil).isFile()) indhold = readFileSync(fil);
    }
    if (!indhold) { res.writeHead(404).end(); return; }
    res.writeHead(200, { 'Content-Type': TYPER[extname(sti)] || 'application/octet-stream' }).end(indhold);
  });
  await new Promise((r) => s.listen(0, '127.0.0.1', r));
  return { s, url: `http://127.0.0.1:${s.address().port}/` };
}
const nu = await webserver();
const før = await webserver(TAG);

const port = 9600 + Math.floor(Math.random() * 90);
const profil = mkdtempSync(join(tmpdir(), 'tjek-bred-'));
const proces = spawn(browser, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profil}`, '--no-first-run',
  '--hide-scrollbars', '--force-color-profile=srgb', '--font-render-hinting=none', 'about:blank'], { stdio: 'ignore' });
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
const ca = (a, b, tol = 1) => Math.abs(a - b) <= tol;

async function fane(bredde, højde = 900) {
  const f = await json('/json/new?about:blank', 'PUT');
  const ws = new WebSocket(f.webSocketDebuggerUrl);
  await new Promise((r, x) => { ws.onopen = r; ws.onerror = x; });
  let id = 0;
  const ventende = new Map();
  ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && ventende.has(d.id)) { ventende.get(d.id)(d); ventende.delete(d.id); } };
  const send = (method, params = {}) => new Promise((r) => { const n = ++id; ventende.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
  const kør = async (expression) => {
    const d = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (d.result?.exceptionDetails) throw new Error(`${expression.slice(0, 80)}: ${d.result.exceptionDetails.exception?.description}`);
    return d.result?.result?.value;
  };
  await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: bredde, height: højde, deviceScaleFactor: 1, mobile: bredde < 600 });
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }, { name: 'prefers-reduced-motion', value: 'reduce' }] });
  return {
    kør,
    async gå(url) {
      await send('Page.navigate', { url });
      for (let i = 0; i < 100; i++) { await vent(100); if ((await kør('document.readyState')) === 'complete') break; }
      await kør('document.fonts.ready');
      await vent(400);
    },
    kasse: (sel) => kør(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e || !e.getClientRects().length) return null;
      const r = e.getBoundingClientRect(); return { top: r.top, left: r.left, right: r.right, bottom: r.bottom, width: r.width }; })()`),
    // Et svar (den sidste mulige melding i meldekassen) viser forklaringen og Næste hånd.
    svar: () => kør(`(() => { const c = [...document.querySelectorAll('#box .cell:not(:disabled)')]; c[c.length - 1]?.click(); return c.length; })()`),
    async billede() {
      await kør('window.scrollTo(0, 0)');
      await vent(200);
      const h = await kør('Math.max(document.documentElement.scrollHeight, innerHeight)');
      const r = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: bredde, height: h, scale: 1 } });
      return r.result.data;
    },
    luk: async () => { ws.close(); await json(`/json/close/${f.id}`).catch(() => {}); },
  };
}

async function forskel(a, b, side) {
  return side.kør(`(async () => {
    const læs = (d) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = 'data:image/png;base64,' + d; });
    const [x, y] = await Promise.all([læs(${JSON.stringify(a)}), læs(${JSON.stringify(b)})]);
    if (x.width !== y.width || x.height !== y.height) return 'størrelsen er ' + y.width + '×' + y.height + ', før ' + x.width + '×' + x.height;
    const px = (i) => { const c = new OffscreenCanvas(i.width, i.height); const g = c.getContext('2d'); g.drawImage(i, 0, 0); return g.getImageData(0, 0, i.width, i.height).data; };
    const p = px(x), q = px(y);
    let n = 0;
    for (let k = 0; k < p.length; k += 4) if (p[k] !== q[k] || p[k + 1] !== q[k + 1] || p[k + 2] !== q[k + 2]) n++;
    return n ? n + ' pixels er forskellige' : '';
  })()`);
}

try {
  // Ved 1280 px: to spalter med toppene ud for hinanden, højst 1120 px i midten.
  let s = await fane(1280);
  await s.gå(nu.url + SIDE);
  const hånd = await s.kasse('.hand');
  const meldinger = await s.kasse('.auction');
  const kasse = await s.kasse('#box');
  const bord = await s.kasse('.table');
  tjek(hånd && meldinger && hånd.right <= meldinger.left && ca(hånd.top, meldinger.top), 'ved 1280 px: hånden til venstre og meldingerne til højre, toppene flugter',
    `${JSON.stringify(hånd)} / ${JSON.stringify(meldinger)}`);
  tjek(kasse && kasse.left >= hånd.right && ca(hånd.width, 420), 'ved 1280 px: meldekassen i højre spalte, hånden 420 px', `${JSON.stringify(kasse)}`);
  tjek(bord.width <= 1120.5 && ca(bord.left, 1280 - bord.right), 'ved 1280 px: højst 1120 px i midten', `${bord.left}–${bord.right}`);
  await s.svar();
  await vent(300);
  const forklaring = await s.kasse('#feedback');
  tjek(forklaring && forklaring.left >= hånd.right, 'ved 1280 px: forklaringen i højre spalte', JSON.stringify(forklaring));
  await s.luk();

  // Hånden står fast, når der rulles.
  s = await fane(1280, 500);
  await s.gå(nu.url + SIDE);
  await s.svar();
  await vent(300);
  const start = await s.kasse('.hand');
  await s.kør('window.scrollTo(0, document.querySelector(".table").getBoundingClientRect().top + scrollY + 60)');
  await vent(200);
  const rullet = await s.kasse('.hand');
  tjek(ca(rullet.top, 16), 'ved 1280 px: hånden står fast, når der rulles', `top ${start.top} → ${rullet.top}`);
  await s.luk();

  // Ved 1000 px er højre spalte mindst 400 px.
  s = await fane(1000);
  await s.gå(nu.url + SIDE);
  const højre = await s.kasse('#box');
  tjek(højre && højre.width >= 400, 'ved 1000 px: højre spalte mindst 400 px', `${højre?.width} px`);
  await s.luk();

  // Ved 999 og 390 px som før, ved første hånd og efter et svar.
  for (const bredde of [999, 390]) {
    for (const svar of [false, true]) {
      const a = await fane(bredde);
      const b = await fane(bredde);
      await a.gå(nu.url + SIDE);
      await b.gå(før.url + SIDE);
      if (svar) { await a.svar(); await b.svar(); await vent(300); }
      const d = await forskel(await b.billede(), await a.billede(), a);
      tjek(!d, `ved ${bredde} px${svar ? ' efter et svar' : ''}: som før`, d);
      await a.luk();
      await b.luk();
    }
  }
} catch (e) {
  tjek(false, 'testen kørte færdig', e.message);
} finally {
  proces.kill();
  nu.s.close();
  før.s.close();
  try { rmSync(profil, { recursive: true, force: true }); } catch {}
}

console.log(fejl ? `\n${fejl} fejl` : '\nMulti-svar-træneren: bred fra 1000 px og uændret under');
process.exit(fejl ? 1 : 0);
