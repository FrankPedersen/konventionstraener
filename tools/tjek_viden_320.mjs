// Accepttest (SPEC-viden-320.md): siderne i viden/ har ingen vandret scroll ved 320 px, og ved 390 og 1280 px er de pixel
// for pixel som før. Alle sider tjekkes på dansk og engelsk med <details> lukket og åbne, og alle konventionskort i deres
// visninger; kortene står i en shadow root, så målingen går også derind. "Stikker ud" måles mod clientWidth: i mobilvisning
// vokser innerWidth med det, der stikker ud, så en måling mod den aldrig ville fejle. Siden før vises fra tagget (filerne
// læses med git show). Hver side åbnes i sin egen browserkontekst, som et nyt privat vindue: localStorage er tom, fanen er
// den eneste i sit vindue, og der skiftes aldrig fane, så intet afhænger af, hvad testen viste før. Kræver Node 22+, git og
// Chrome eller Edge.
//
//   node tools/tjek_viden_320.mjs                    tjekker
//   node tools/tjek_viden_320.mjs ingen              springer pixelsammenligningen over
//   node tools/tjek_viden_320.mjs --billeder=mappe   gemmer også udsnit ved 320 px før og efter
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROD = fileURLToPath(new URL('..', import.meta.url));
const TAG = 'v-foer-viden-320';
const INGEN_PIXEL = process.argv.includes('ingen');
const BILLEDER = process.argv.find((a) => a.startsWith('--billeder='))?.slice('--billeder='.length);
const SIDER = readdirSync(join(ROD, 'viden')).filter((f) => f.endsWith('.html')).map((f) => `viden/${f}`);
const KORT = 'viden/konventionskort.html';
const SMALLE = [320, 340, 360, 375];
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
const vent = (ms) => new Promise((r) => setTimeout(r, ms));

const TYPER = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.json': 'application/json', '.txt': 'text/plain; charset=utf-8', '.md': 'text/plain; charset=utf-8' };
/** Webserver for arbejdsmappen eller, med tag, for filerne i tagget (gemt, for kortene henter mange filer). */
async function webserver(tag) {
  const gemt = new Map();
  const s = createServer((req, res) => {
    let sti = decodeURIComponent(new URL(req.url, 'http://x').pathname).replace(/^\/+/, '');
    if (sti === '' || sti.endsWith('/')) sti += 'index.html';
    if (sti.split('/').includes('..')) { res.writeHead(403).end(); return; }
    let indhold;
    if (tag) {
      if (!gemt.has(sti)) {
        const r = spawnSync('git', ['show', `${tag}:${sti}`], { cwd: ROD, maxBuffer: 64 * 1024 * 1024 });
        gemt.set(sti, r.status === 0 ? r.stdout : null);
      }
      indhold = gemt.get(sti);
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

const port = 9500 + Math.floor(Math.random() * 90);
const profil = mkdtempSync(join(tmpdir(), 'tjek-viden-'));
const proces = spawn(browser, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profil}`, '--no-first-run',
  '--hide-scrollbars', '--force-color-profile=srgb', '--font-render-hinting=none', 'about:blank'], { stdio: 'ignore' });

async function json(sti) {
  for (let i = 0; i < 50; i++) {
    try {
      const svar = await fetch(`http://127.0.0.1:${port}${sti}`);
      if (svar.ok) return await svar.json();
    } catch {}
    await vent(200);
  }
  throw new Error(`Browseren svarer ikke på ${sti}`);
}

// Én forbindelse til browseren; hver fane har sin egen session på den.
const forbindelse = new WebSocket((await json('/json/version')).webSocketDebuggerUrl);
await new Promise((r, x) => { forbindelse.onopen = r; forbindelse.onerror = x; });
let næste = 0;
const ventende = new Map();
forbindelse.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && ventende.has(d.id)) { ventende.get(d.id)(d); ventende.delete(d.id); } };
// Et svar, der udebliver, bliver en fejl i stedet for en test, der aldrig slutter.
const send = (method, params = {}, sessionId) => new Promise((r, x) => {
  const n = ++næste;
  const ur = setTimeout(() => { ventende.delete(n); x(new Error(`${method} svarede ikke inden for 60 s`)); }, 60000);
  ventende.set(n, (d) => { clearTimeout(ur); if (d.error) x(new Error(`${method}: ${d.error.message}`)); else r(d.result); });
  forbindelse.send(JSON.stringify(sessionId ? { id: n, method, params, sessionId } : { id: n, method, params }));
});

let fejl = 0;
let antal = 0;
const tjek = (ok, navn, detalje = '') => {
  antal++;
  if (!ok) fejl++;
  if (!ok) console.log(`FEJL ${navn}${detalje ? ` – ${detalje}` : ''}`);
};

// Alle elementer, også i shadow roots; det, der står i en beholder med egen scroll, stikker ikke siden ud.
const FÆLLES = `
  const alle = (rod) => [...rod.querySelectorAll('*')].flatMap((e) => e.shadowRoot ? [e, ...alle(e.shadowRoot)] : [e]);
  const forælder = (e) => e.parentElement ?? e.getRootNode().host ?? null;
  const navn = (e) => e.tagName.toLowerCase() + (typeof e.className === 'string' && e.className ? '.' + e.className.trim().split(/\\s+/).join('.') : '');`;
const MÅL = `(() => {${FÆLLES}
  const rod = document.documentElement;
  const cw = rod.clientWidth;
  const iScroll = (e) => { for (let a = forælder(e); a && a !== rod && a !== document.body; a = forælder(a)) if (getComputedStyle(a).overflowX !== 'visible') return true; return false; };
  const fund = [];
  for (const e of alle(document.body)) {
    if (!e.getClientRects().length || iScroll(e)) continue;
    const h = e.getBoundingClientRect().right;
    if (h > cw + 0.5) fund.push(navn(e) + ' +' + Math.round(h - cw));
    for (const n of e.childNodes) {
      if (n.nodeType !== 3 || !n.nodeValue.trim()) continue;
      const r = document.createRange(); r.selectNodeContents(n);
      let t = 0; for (const k of r.getClientRects()) t = Math.max(t, k.right);
      if (t > cw + 0.5) fund.push(navn(e) + ' tekst "' + n.nodeValue.trim().slice(0, 24) + '" +' + Math.round(t - cw));
    }
  }
  return { ud: rod.scrollWidth - cw, skjult: [getComputedStyle(rod).overflowX, getComputedStyle(document.body).overflowX].filter((o) => o !== 'visible'), fund: [...new Set(fund)].slice(0, 4) };
})()`;
const ÅBN = `(() => {${FÆLLES} for (const e of alle(document.body)) if (e.tagName === 'DETAILS') e.open = true; })()`;
const R = `document.getElementById('kk-app').shadowRoot`;

/** En fane i sin egen browserkontekst med tom localStorage; luk() kasserer konteksten. */
async function fane(bredde, højde = 800) {
  const { browserContextId } = await send('Target.createBrowserContext');
  const { targetId } = await send('Target.createTarget', { url: 'about:blank', browserContextId, newWindow: true });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const s = (method, params) => send(method, params, sessionId);
  const kør = async (expression) => {
    const d = await s('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (d.exceptionDetails) throw new Error(`${expression.slice(0, 80)}: ${d.exceptionDetails.exception?.description}`);
    return d.result?.value;
  };
  await s('Page.enable');
  await s('Emulation.setDeviceMetricsOverride', { width: bredde, height: højde, deviceScaleFactor: 1, mobile: bredde < 600 });
  await s('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }, { name: 'prefers-reduced-motion', value: 'reduce' }] });
  return {
    kør,
    send: s,
    async gå(url) {
      await s('Page.navigate', { url });
      for (let i = 0; i < 100; i++) { await vent(50); if ((await kør('document.readyState')) === 'complete') break; }
      await kør('document.fonts.ready.then(() => true)');
      await vent(150);
    },
    async kortKlar() {
      for (let i = 0; i < 200; i++) {
        if (await kør(`${R}.querySelectorAll('#valg [data-k]').length`)) return kør(`[...${R}.querySelectorAll('#valg [data-k]')].map((b) => b.dataset.k)`);
        await vent(50);
      }
      throw new Error('Kortene kom ikke frem');
    },
    async visKort(id, visning) {
      await kør(`(() => { const r = ${R}; r.querySelector(${JSON.stringify(`#valg [data-k="${id}"]`)}).click(); r.querySelector(${JSON.stringify(`.tabs button[data-v="${visning}"]`)}).click(); })()`);
      await vent(40);
    },
    // Hele siden i bidder, så lange sider ikke rammer browserens grænse for et skærmbillede.
    async billeder() {
      await kør('window.scrollTo(0, 0)');
      await vent(60);
      const h = await kør('Math.max(document.documentElement.scrollHeight, innerHeight)');
      const bidder = [];
      for (let y = 0; y < h; y += 6000) {
        const r = await s('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y, width: bredde, height: Math.min(6000, h - y), scale: 1 } });
        bidder.push(r.data);
      }
      return { h, bidder };
    },
    luk: () => send('Target.disposeBrowserContext', { browserContextId }).catch(() => {}),
  };
}

/** Siden før og siden nu, hver i sin egen kontekst; forskellen regnes ud i fanen med siden nu, så den kan sige, hvor den er. */
async function sammenlign(bredde, urlFør, urlNu, forbered = async () => {}) {
  const a = await fane(bredde);
  await a.gå(urlFør);
  await forbered(a);
  const billedeFør = await a.billeder();
  await a.luk();
  const b = await fane(bredde);
  try {
    await b.gå(urlNu);
    await forbered(b);
    return await forskel(billedeFør, await b.billeder(), b);
  } finally {
    await b.luk();
  }
}

/**
 * Chrome tegner en sjælden gang én pixel en anelse anderledes på meget lange sider, også når filerne er de samme (målt 5. nov.
 * 2026: før mod før og nu mod nu på 2-over-1-makker2 ved 1280 px gav én pixel forskel i én af fem runder). En ændring kommer
 * igen hver gang, støj gør ikke, så en forskel skal være der i tre forsøg i træk, hvert med nye kontekster.
 */
async function somFør(bredde, urlFør, urlNu, forbered, navn) {
  const støj = [];
  for (let forsøg = 1; forsøg <= 3; forsøg++) {
    const d = await sammenlign(bredde, urlFør, urlNu, forbered);
    if (!d) {
      for (const s of støj) console.log(`NB ${navn} ved ${bredde} px: ${s}, ens i forsøg ${forsøg}`);
      return '';
    }
    støj.push(`forsøg ${forsøg}: ${d}`);
  }
  return `forskellig i tre forsøg i træk; ${støj.join('; ')}`;
}

async function forskel(a, b, side) {
  if (a.h !== b.h) return `højden er ${b.h} px, før ${a.h} px`;
  for (let i = 0; i < a.bidder.length; i++) {
    if (a.bidder[i] === b.bidder[i]) continue;
    const d = await side.kør(`(async () => {${FÆLLES}
      const læs = (d) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = 'data:image/png;base64,' + d; });
      const [x, y] = await Promise.all([læs(${JSON.stringify(a.bidder[i])}), læs(${JSON.stringify(b.bidder[i])})]);
      const px = (i) => { const c = new OffscreenCanvas(i.width, i.height); const g = c.getContext('2d'); g.drawImage(i, 0, 0); return g.getImageData(0, 0, i.width, i.height).data; };
      const p = px(x), q = px(y);
      let n = 0, x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1, først = '';
      for (let k = 0; k < p.length; k += 4) {
        if (p[k] === q[k] && p[k + 1] === q[k + 1] && p[k + 2] === q[k + 2]) continue;
        const u = (k / 4) % x.width, v = Math.floor(k / 4 / x.width) + ${i * 6000};
        if (!n) først = [p[k], p[k + 1], p[k + 2]].join('.') + ' før, ' + [q[k], q[k + 1], q[k + 2]].join('.') + ' nu';
        n++; x0 = Math.min(x0, u); y0 = Math.min(y0, v); x1 = Math.max(x1, u); y1 = Math.max(y1, v);
      }
      if (!n) return '';
      // Elementet ved den første forskel, også inde i en shadow root.
      scrollTo(0, Math.max(0, y0 - 200));
      let e = document.elementFromPoint(x0, y0 - scrollY);
      while (e?.shadowRoot) { const f = e.shadowRoot.elementFromPoint(x0, y0 - scrollY); if (!f || f === e) break; e = f; }
      const om = e ? navn(e) + ' "' + (e.textContent || '').trim().slice(0, 30) + '"' : '?';
      return n + ' pixels er forskellige i ' + x0 + ',' + y0 + '–' + x1 + ',' + y1 + ' (' + først + '; ' + om + ')';
    })()`);
    if (d) return d;
  }
  return '';
}

// Udsnit til Frank: samme element før og efter ved 320 px, med en rød streg, hvor skærmen slutter, når noget stikker ud.
const UDSNIT = [
  ['viden/2-over-1.html', '2-over-1-opgaver', `document.querySelector('.quiz')`, 420],
  ['viden/2-over-1.html', '2-over-1-spil', `[...document.querySelectorAll('.deal')].sort((a, b) => b.scrollWidth - a.scrollWidth)[0]`, 340],
  ['viden/bridgesystem.html', 'bridgesystem-overskrift', `document.getElementById('6-konkurrencemeldinger')`, 170],
  ['viden/forslag-2klor-kontrolsvar.html', 'forslag-tabel', `document.querySelector('table.abner')`, 420],
  ['viden/konventionskort.html', 'konventionskort-top', `document.getElementById('kk-app')`, 620],
];
async function gemUdsnit(url, navn, vælger, højde) {
  const s = await fane(320);
  try {
    await s.gå(url);
    await vent(500);
    await s.kør(ÅBN);
    const r = await s.kør(`(() => {
      const rod = document.documentElement;
      const e = ${vælger};
      const k = e.getBoundingClientRect();
      return { y: Math.max(0, k.top + scrollY - 20), sw: Math.max(320, rod.scrollWidth) };
    })()`);
    if (r.sw > 320) await s.kør(`document.body.insertAdjacentHTML('beforeend', '<div style="position:absolute;top:0;left:320px;width:2px;height:' + document.documentElement.scrollHeight + 'px;background:#e00;z-index:9999"></div>')`);
    const b = await s.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: r.y, width: r.sw, height: højde, scale: 1 } });
    writeFileSync(join(BILLEDER, `320-${navn}.png`), Buffer.from(b.data, 'base64'));
  } finally {
    await s.luk();
  }
}

try {
  // Ingen vandret scroll.
  for (const bredde of SMALLE) {
    for (const side of SIDER) {
      for (const lang of ['da', 'en']) {
        const s = await fane(bredde);
        await s.gå(`${nu.url}${side}?lang=${lang}`);
        if (side === KORT) await s.kortKlar();
        const lukket = await s.kør(MÅL);
        tjek(lukket.ud <= 0 && !lukket.fund.length, `${side} ved ${bredde} px på ${lang}: ingen vandret scroll`, `${lukket.ud} px, ${lukket.fund.join(', ')}`);
        tjek(!lukket.skjult.length, `${side} ved ${bredde} px på ${lang}: siden skjuler ikke noget med overflow`, lukket.skjult.join(', '));
        await s.kør(ÅBN);
        await vent(60);
        const åben = await s.kør(MÅL);
        tjek(åben.ud <= 0 && !åben.fund.length, `${side} ved ${bredde} px på ${lang} med alt foldet ud: ingen vandret scroll`, `${åben.ud} px, ${åben.fund.join(', ')}`);
        await s.luk();
      }
    }
  }

  // Alle kort i alle visninger.
  for (const bredde of [320, 375]) {
    for (const lang of ['da', 'en']) {
      const s = await fane(bredde);
      await s.gå(`${nu.url}${KORT}?lang=${lang}`);
      const ider = await s.kortKlar();
      tjek(ider.length === 49, `Konventionskortet ved ${bredde} px på ${lang}: alle kort er med`, String(ider.length));
      for (const id of ider) {
        for (const visning of ['fuld', 'kompakt', 'skabelon']) {
          if (visning === 'skabelon' && id !== ider[0]) continue;
          await s.visKort(id, visning);
          await s.kør(ÅBN);
          await vent(30);
          const m = await s.kør(MÅL);
          tjek(m.ud <= 0 && !m.fund.length, `Kortet ${id}, ${visning}, ved ${bredde} px på ${lang}: ingen vandret scroll`, `${m.ud} px, ${m.fund.join(', ')}`);
        }
      }
      await s.luk();
    }
  }

  // Ved 390 og 1280 px er alt pixel for pixel som før; hvert skærmbillede tages i sin egen kontekst.
  if (!INGEN_PIXEL) {
    for (const bredde of [390, 1280]) {
      for (const side of SIDER) {
        for (const lang of ['da', 'en']) {
          const klar = async (s) => { if (side === KORT) { await s.kortKlar(); await vent(200); } };
          const d = await somFør(bredde, `${før.url}${side}?lang=${lang}`, `${nu.url}${side}?lang=${lang}`, klar, `${side} på ${lang}`);
          tjek(!d, `${side} ved ${bredde} px på ${lang}: som før`, d);
        }
      }
      const s = await fane(bredde);
      await s.gå(`${før.url}${KORT}`);
      const ider = await s.kortKlar();
      await s.luk();
      for (const id of ider) {
        for (const visning of ['fuld', 'kompakt']) {
          const vis = async (t) => { await t.kortKlar(); await t.visKort(id, visning); };
          const d = await somFør(bredde, `${før.url}${KORT}`, `${nu.url}${KORT}`, vis, `Kortet ${id}, ${visning}`);
          tjek(!d, `Kortet ${id}, ${visning}, ved ${bredde} px: som før`, d);
        }
      }
    }
  }

  if (BILLEDER) {
    mkdirSync(BILLEDER, { recursive: true });
    for (const [side, navn, vælger, højde] of UDSNIT) {
      await gemUdsnit(`${før.url}${side}`, `${navn}-foer`, vælger, højde);
      await gemUdsnit(`${nu.url}${side}`, `${navn}-efter`, vælger, højde);
    }
  }
} catch (e) {
  tjek(false, 'testen kørte færdig', e.message);
} finally {
  forbindelse.close();
  proces.kill();
  nu.s.close();
  før.s.close();
  await vent(300);
  try { rmSync(profil, { recursive: true, force: true }); } catch {}
}
console.log(fejl ? `${fejl} FEJL ud af ${antal} tjek` : `Alt i orden: ${antal} tjek`);
process.exit(fejl ? 1 : 0);
