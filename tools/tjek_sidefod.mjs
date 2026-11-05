// Accepttest (SPEC-sidefod.md): sidefoden er ens med forsidens efter målene under Afklaret i
// ../Forside/docs/specs/SPEC-ny-forside.md. Siderne vises fra en lokal webserver i Chrome uden vindue.
//
//   node tools/tjek_sidefod.mjs                    tjekker
//   node tools/tjek_sidefod.mjs --billeder=mappe   gemmer også sidefoden ved 1280 og 390 px
//
// Kræver Node 22+ og Chrome eller Edge.
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROD = fileURLToPath(new URL('..', import.meta.url));
const BILLEDER = process.argv.find((a) => a.startsWith('--billeder='))?.slice('--billeder='.length);
const SIDER = ['index.html', 'traener.html', 'multi-svar-traener.html', 'viden/index.html', 'makkeraftaler.html', 'viden/2-over-1.html'];
const CHROME = [
  process.env.CHROME,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
].filter(Boolean).find((p) => existsSync(p));
if (!CHROME) {
  console.error('Fandt hverken Chrome eller Edge; sæt CHROME til stien.');
  process.exit(2);
}

const TYPER = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.json': 'application/json', '.txt': 'text/plain; charset=utf-8', '.md': 'text/plain; charset=utf-8' };
const server = createServer((req, res) => {
  let sti = normalize(join(ROD, decodeURIComponent(new URL(req.url, 'http://x').pathname)));
  if (existsSync(sti) && statSync(sti).isDirectory()) sti = join(sti, 'index.html');
  if (!sti.startsWith(normalize(ROD)) || !existsSync(sti)) return res.writeHead(404).end();
  res.writeHead(200, { 'Content-Type': TYPER[extname(sti)] || 'application/octet-stream' }).end(readFileSync(sti));
});
await new Promise((ok) => server.listen(0, '127.0.0.1', ok));
const UD = `http://127.0.0.1:${server.address().port}/`;

const vent = (ms) => new Promise((r) => setTimeout(r, ms));
let fejl = 0;
const tjek = (ok, navn, detalje = '') => {
  if (!ok) fejl++;
  console.log(`${ok ? 'ok  ' : 'FEJL'} ${navn}${!ok && detalje ? ` – ${detalje}` : ''}`);
};

const profil = mkdtempSync(join(tmpdir(), 'sidefod-'));
const port = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profil}`, '--no-first-run', '--hide-scrollbars', '--force-color-profile=srgb', '--lang=da-DK', 'about:blank'], { stdio: 'ignore' });
let targets;
for (let i = 0; i < 100 && !targets; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); } catch { await vent(200); }
}
const ws = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
await new Promise((ok, nej) => { ws.onopen = ok; ws.onerror = nej; });
let id = 0;
const venter = new Map();
ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && venter.has(d.id)) { venter.get(d.id)(d); venter.delete(d.id); } };
const send = (method, params = {}) => new Promise((ok) => { const n = ++id; venter.set(n, ok); ws.send(JSON.stringify({ id: n, method, params })); });
const kør = async (expression) => {
  const d = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (d.result?.exceptionDetails) throw new Error(`${expression.slice(0, 80)}: ${d.result.exceptionDetails.exception?.description}`);
  return d.result?.result?.value;
};
await send('Page.enable');
const åbn = async (side, bredde, højde = 900) => {
  await send('Emulation.setDeviceMetricsOverride', { width: bredde, height: højde, deviceScaleFactor: 1, mobile: bredde < 600 });
  await send('Page.navigate', { url: UD + side });
  await vent(900);
  await kør('document.fonts.ready.then(() => true)');
};
const MÅL = `(() => {
  const f = document.querySelector('#sidefod .sf');
  const t = (e) => e.textContent.replace(/\\s+/g, ' ').trim();
  const k = (e) => e.getBoundingClientRect();
  const cs = getComputedStyle(f);
  const logo = f.querySelector('.sf-logo');
  const links = [...f.querySelectorAll('nav a')];
  const li = [...f.querySelectorAll('nav li')];
  const knap = f.querySelector('a.sf-knap');
  const navn = f.querySelector('a.sf-navn');
  const titel = f.querySelector('h2');
  return {
    højde: Math.round(k(f).height),
    kolonner: [...f.querySelectorAll('nav')].map((n) => ({ titel: t(n.querySelector('h2')), links: [...n.querySelectorAll('a')].map((a) => [t(a), a.getAttribute('href')]) })),
    polstring: [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].join(' '),
    skrift: cs.fontSize + '/' + getComputedStyle(links[0]).lineHeight,
    hjørne: cs.borderTopLeftRadius,
    logo: [Math.round(k(logo).width), Math.round(k(logo).height)],
    rækker: links.map((a) => Math.round(k(a).height)),
    afstand: Math.round(k(li[1]).top - k(li[0]).bottom),
    titel: getComputedStyle(titel).fontSize + '/' + getComputedStyle(titel).lineHeight,
    samme: Math.abs((k(knap).top + k(knap).height / 2) - (k(navn).top + k(navn).height / 2)) < 2,
    knapHøjde: Math.round(k(knap).height),
    knap: t(knap),
    linje: f.querySelector('.sf-om p')?.getClientRects().length > 0,
    legal: f.querySelector('.sf-legal').innerText.replace(/\\s+/g, ' ').trim(),
    ud: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    tekst: t(f),
  };
})()`;
const KOLONNER_DA = (rod) => JSON.stringify([
  { titel: 'Trænere', links: [['Konventionstræner', rod], ['Fordeling', '/fordelingstraeneren/#fordeling'], ['Pointregnskab', '/fordelingstraeneren/#pointregnskab'], ['Farvebehandling', '/fordelingstraeneren/#farvebehandling'], ['Håndevaluering', '/fordelingstraeneren/#haandevaluering']] },
  { titel: 'Opslag', links: [['Analyse', '/fordelingstraeneren/#analyse'], ['Bridgeordbog', '/ordbog/'], ['Scoring i bridge', '/scoring/']] },
]);

try {
  for (const side of SIDER) {
    const rod = side.startsWith('viden/') ? '../' : './';
    for (const bredde of [1280, 390]) {
      await åbn(side, bredde);
      const f = await kør(MÅL);
      const hvor = `${side} ved ${bredde} px`;
      tjek(JSON.stringify(f.kolonner) === KOLONNER_DA(rod), `${hvor}: Trænere og Opslag i rigtig rækkefølge`, JSON.stringify(f.kolonner));
      tjek(f.skrift === '14px/20px' && f.titel === '11px/16px' && f.hjørne === '20px', `${hvor}: 14/20 px, titler 11/16 px og hjørner 20 px`, JSON.stringify([f.skrift, f.titel, f.hjørne]));
      tjek(!/Aftaler og notater|Om mig\b(?! og kontakt)|Skriv til mig/.test(f.tekst), `${hvor}: Om mig, Kontakt og Aftaler og notater er væk`, f.tekst.slice(0, 120));
      if (bredde === 1280) {
        tjek(f.polstring === '24px 28px 18px 28px' && f.logo[0] === 32 && f.afstand === 4 && f.knapHøjde === 36 && f.linje, `${hvor}: polstring 24/28 px, logo 32 px, 4 px mellem links, knappen 36 px og linjen`, JSON.stringify([f.polstring, f.logo, f.afstand, f.knapHøjde, f.linje]));
        tjek(f.legal === '© 2026 Frank Pedersen', `${hvor}: ©-linjen`, f.legal);
        tjek(f.knap === 'Om mig og kontakt →', `${hvor}: knappen med pil`, f.knap);
      } else {
        tjek(f.polstring === '18px 18px 14px 18px' && f.logo[0] === 30 && f.afstand === 2 && !f.linje, `${hvor}: polstring 18 px, logo 30 px, 2 px mellem links og uden linjen`, JSON.stringify([f.polstring, f.logo, f.afstand, f.linje]));
        tjek(f.samme && f.knapHøjde >= 44, `${hvor}: logo og knappen på én række, med en trykflade på 44 px`, JSON.stringify([f.samme, f.knapHøjde]));
        tjek(f.rækker.every((h) => h >= 24), `${hvor}: alle links har mindst 24 px rækkehøjde`, f.rækker.join());
        tjek(f.legal === '© 2026 Frank Pedersen · Gratis bridgetræning i browseren', `${hvor}: ©-linjen`, f.legal);
      }
      tjek(f.ud <= 0, `${hvor}: intet stikker ud`, `${f.ud} px`);
    }
    await åbn(side, 320, 700);
    // Sidefoden selv: opgaverne i viden/2-over-1.html stikker 20 px ud ved 320 px, også på main, og hører ikke til her.
    const ud = await kør(`Math.round(Math.max(...[...document.querySelectorAll('#sidefod *')].map((e) => e.getBoundingClientRect().right)) - document.documentElement.clientWidth)`);
    tjek(ud <= 0, `${side} ved 320 px: sidefoden stikker ikke ud`, `${ud} px`);
  }

  // Knappen står inden for sidefodens polstring ved de smalle bredder og på begge sprog; teksten må brække.
  // "Stikker ud" måles mod clientWidth: i mobilvisning vokser innerWidth med det, der stikker ud, så tjekket aldrig ville fejle.
  for (const [lang, sprog] of [['da', 'dansk'], ['en', 'engelsk']]) {
    for (const bredde of [390, 360, 320]) {
      await åbn(`index.html?lang=${lang}`, bredde);
      const ud = await kør(`(() => { const f = document.querySelector('#sidefod .sf'); const r = f.getBoundingClientRect().right - parseFloat(getComputedStyle(f).paddingRight); return Math.round(f.querySelector('a.sf-knap').getBoundingClientRect().right - r); })()`);
      tjek(ud <= 0, `Knappen ved ${bredde} px på ${sprog}: inden for polstringen`, `${ud} px`);
    }
  }

  // Engelsk.
  await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: `${UD}index.html?lang=en` });
  await vent(900);
  const en = await kør(MÅL);
  tjek(JSON.stringify(en.kolonner.map((k) => [k.titel, k.links.map((l) => l[0])])) === JSON.stringify([['Trainers', ['Convention trainer', 'Distribution', 'Point count', 'Suit combinations', 'Hand evaluation']], ['Reference', ['Analysis', 'Bridge dictionary', 'Scoring in bridge']]]), 'Engelsk: kolonnerne', JSON.stringify(en.kolonner));
  tjek(/Free bridge training in the browser\. Made by Frank Pedersen\./.test(en.tekst) && en.knap === 'About me and contact →', 'Engelsk: linjen og knappen', en.tekst.slice(0, 120));

  // Skærmbillederne: kun sidefoden.
  if (BILLEDER) {
    mkdirSync(BILLEDER, { recursive: true });
    for (const [lang, navn] of [['da', ''], ['en', '-en']]) for (const bredde of [1280, 390]) {
      await åbn(`index.html?lang=${lang}`, bredde);
      const r = await kør(`(() => { const e = document.querySelector('#sidefod'); const k = e.getBoundingClientRect(); return { x: 0, y: k.top + scrollY - 16, width: innerWidth, height: k.height + 32, scale: 1 }; })()`);
      const b = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: r });
      writeFileSync(join(BILLEDER, `${bredde}-konventionstraener-sidefod${navn}.png`), Buffer.from(b.result.data, 'base64'));
    }
  }
} catch (e) {
  tjek(false, 'testen kørte færdig', e.message);
} finally {
  proc.kill();
  server.close();
  try { rmSync(profil, { recursive: true, force: true }); } catch {}
}
console.log(fejl ? `\n${fejl} FEJL` : '\nAlt i orden');
process.exit(fejl ? 1 : 0);
