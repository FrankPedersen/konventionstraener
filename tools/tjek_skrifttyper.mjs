// Fast test i en rigtig browser (SPEC-skrifttyper-fast.md): skrifttyperne ligger på sitet selv. Siderne vises fra en
// lokal webserver ved 390 og 1280 px, og intet må hentes fra Google. Chrome skal tegne overskriften og et Manrope-element
// med Manrope, brødteksten med Inter og spillefarverne ♠♥♦♣ med Noto Sans Symbols 2, hvor siden beder om den, alle fra
// assets/fonts/ og ikke fra systemet. (Accepttesten for skrifttypeændringen sammenlignede også pixel for pixel med tagget v-foer-skrifttyper;
// den er bestået.) Kræver Node 22+ og Chrome eller Edge.
//
//   node tools/tjek_skrifttyper.mjs
import { spawn } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, rmSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROD = fileURLToPath(new URL('..', import.meta.url));
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

const SIDER = [
  'index.html', 'makkeraftaler.html', 'traener.html?k=truscott', 'markering.html', 'multi-svar-traener.html',
  'viden/index.html', 'viden/2-over-1.html', 'viden/2-over-1-makker2.html', 'viden/bridgesystem.html',
  'viden/forslag-2klor-kontrolsvar.html', 'viden/kampen-om-kontrakten.html', 'viden/konventionskort.html#truscott',
];
// Den skrifttype, hvert element skal tegnes med
const SKRIFT = { overskrift: 'Manrope', brødtekst: 'Inter', manrope: 'Manrope', spillefarver: 'Noto Sans Symbols 2' };

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
const nu = await webserver(ROD);

const port = 9600 + Math.floor(Math.random() * 90);
const profil = mkdtempSync(join(tmpdir(), 'tjek-skrift-'));
const proces = spawn(browser, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profil}`, '--no-first-run',
  'about:blank'], { stdio: 'ignore' });
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

// Markerer de elementer, hvis skrifttyper tjekkes: overskriften, første afsnit, første element i Manrope og første
// element med en spillefarve i sin egen tekst, der beder om Noto Sans Symbols 2. Spillefarver i sidens almindelige
// skrift (fx i Multi-træneren og Makker 2, der ikke henter symbolskriften) tegnes med systemets tegn, som før
// skrifttyperne kom på sitet, og tjekkes ikke.
const MARKER = `(() => {
  const ud = [];
  const sæt = (navn, el) => { if (el) { el.setAttribute('data-tjek-skrift', navn); ud.push(navn); } };
  sæt('overskrift', document.querySelector('h1'));
  sæt('brødtekst', [...document.querySelectorAll('p')].find((p) => p.textContent.trim().length > 20 && p.offsetParent));
  sæt('manrope', [...document.querySelectorAll('body *')].find((el) => el.offsetParent && el.childNodes.length
    && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) && getComputedStyle(el).fontFamily.startsWith('Manrope')));
  sæt('spillefarver', [...document.querySelectorAll('body *')].find((el) => el.offsetParent
    && [...el.childNodes].some((n) => n.nodeType === 3 && /[♠♥♦♣]/.test(n.textContent))
    && getComputedStyle(el).fontFamily.includes('Noto Sans Symbols 2')));
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
    kør, kald,
    async åbn(url, bredde) {
      await send('Emulation.setDeviceMetricsOverride', { width: bredde, height: 900, deviceScaleFactor: 1, mobile: bredde < 600 });
      const n = indlæst; kald.length = 0;
      await send('Page.navigate', { url: 'about:blank' });
      await send('Page.navigate', { url });
      for (let i = 0; i < 150 && indlæst <= n; i++) await vent(100);
      await kør('document.fonts.ready.then(() => new Promise((r) => setTimeout(r, 600)))');
    },
    // Skrifttyperne, Chrome tegner elementet med, som { familie, egen } (egen: fra sitet, ikke fra systemet)
    async skrifter(navn) {
      const doc = await send('DOM.getDocument', { depth: -1 });
      const q = await send('DOM.querySelector', { nodeId: doc.result.root.nodeId, selector: `[data-tjek-skrift="${navn}"]` });
      if (!q.result?.nodeId) return [];
      const f = await send('CSS.getPlatformFontsForNode', { nodeId: q.result.nodeId });
      return (f.result?.fonts ?? []).map((x) => ({ familie: x.familyName, egen: x.isCustomFont }));
    },
    luk: async () => { ws.close(); await json(`/json/close/${f.id}`).catch(() => {}); },
  };
}

try {
  await json('/json/version');
  const t = await fane();
  for (const side of SIDER) {
    for (const bredde of [390, 1280]) {
      await t.åbn(nu.url + side, bredde);
      const google = t.kald.filter((u) => /fonts\.(googleapis|gstatic)\.com/.test(u));
      const egne = t.kald.filter((u) => u.includes('/assets/fonts/') && u.endsWith('.woff2'));
      tjek(google.length === 0 && egne.length > 0, `${side} ${bredde} px: intet hentes fra Google; ${egne.length} skrifttyper fra assets/fonts/`, google.join(' '));
      const navne = await t.kør(MARKER);
      tjek(navne.includes('brødtekst'), `${side} ${bredde} px: der er brødtekst at tjekke (${navne.join(', ')})`);
      for (const n of navne) {
        const skrifter = await t.skrifter(n);
        const vist = skrifter.map((s) => `${s.familie}${s.egen ? '' : ' (system)'}`).sort().join(', ');
        tjek(skrifter.some((s) => s.egen && s.familie.startsWith(SKRIFT[n])), `${side} ${bredde} px: ${n} tegnes med ${SKRIFT[n]} fra sitet`, vist);
      }
    }
  }
  await t.luk();
} finally {
  proces.kill();
  nu.s.close();
  await vent(300);
  try { rmSync(profil, { recursive: true, force: true }); } catch {}
}
process.exit(fejl ? 1 : 0);
