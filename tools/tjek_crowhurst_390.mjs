// Accepttest (SPEC-crowhurst-390.md): crowhurst-kortet giver ingen vandret scroll ved 390–398 px, og alt andet er pixel for
// pixel som før. Crowhurst-kortet tjekkes ved 390, 393, 395 og 398 px på dansk og engelsk i alle visninger med alt foldet ud
// og i hint-vinduet i traener.html?k=crowhurst. Ved 390 px er de andre 48 kort, crowhurst i kompakt visning og alle sider i
// viden/ som tagget; ved 399 og 1280 px er alle sider og alle 49 kort som tagget. Kortet multi-2ru (SPEC-multi-2ru.md) er
// kommet til efter tagget, så der er 50 kort; det tjekkes kun for vandret scroll ved 390–399 og 1280 px (se NYE_KORT), og
// de 49 kort fra tagget sammenlignes med tagget som før. Siden før vises fra tagget (filerne læses
// med git show). Hver side åbnes i sin egen browserkontekst med tom localStorage og uden faneskift, som i tjek_viden_320.mjs.
// "Stikker ud" måles mod clientWidth, også inde i kortets shadow root. Med --live åbnes siderne, kortene og træneren på
// www.kontraktbridge.dk/konventionstraener/, og pixelsammenligningen med tagget, der kun giver mening lokalt, springes
// over (SPEC-tjek-live.md). Kræver Node 22+, git og Chrome eller Edge.
//
//   node tools/tjek_crowhurst_390.mjs                    før fletning: tjekker siderne fra arbejdsmappen
//   node tools/tjek_crowhurst_390.mjs --live             efter en udgivelse: tjekker vandret scroll på sitet
//   node tools/tjek_crowhurst_390.mjs ingen              springer pixelsammenligningen over
//   node tools/tjek_crowhurst_390.mjs --billeder=mappe   gemmer også crowhurst-kortet ved 390 px før og efter
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

import { LOFT, TRIN, erStøj } from './pixelstoej.mjs';

const ROD = fileURLToPath(new URL('..', import.meta.url));
const TAG = 'v-foer-crowhurst-390';
// Filer, der bevidst er ændret efter tagget, sammenlignes med deres godkendte udgave i stedet, som i tjek_viden_320.mjs:
// Makker 2-dokumentet fik markeringerne rettet og tre rettelser mere (SPEC-makker2-markeringer.md), og udgaven i commit
// bca7e0c er den godkendte (Franks valg 15. november 2026, SPEC-pixeltolerance.md). Alt andet kommer fra tagget.
const NYERE = { 'viden/2-over-1-makker2.html': 'bca7e0c446f14ebf86724675b336c9e7306f8303' };
const INGEN_PIXEL = process.argv.includes('ingen');
const LIVE = process.argv.includes('--live');
const SITE = 'https://www.kontraktbridge.dk/konventionstraener/';
const BILLEDER = process.argv.find((a) => a.startsWith('--billeder='))?.slice('--billeder='.length);
const SIDER = readdirSync(join(ROD, 'viden')).filter((f) => f.endsWith('.html')).map((f) => `viden/${f}`);
const KORT = 'viden/konventionskort.html';
const ID = 'crowhurst';
const BREDDER = [390, 393, 395, 398];
const VISNINGER = ['fuld', 'kompakt', 'skabelon'];
// Kort, der er kommet til efter tagget, findes ikke dér og tjekkes kun for vandret scroll, ved de bredder, hvor de andre kort
// sammenlignes med tagget (SPEC-multi-2ru.md, Franks svar 21. november 2026).
const NYE_KORT = ['multi-2ru'];
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
        const r = spawnSync('git', ['show', `${NYERE[sti] ?? tag}:${sti}`], { cwd: ROD, maxBuffer: 64 * 1024 * 1024 });
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
// Siden nu: arbejdsmappen eller, med --live, sitet. Siden før kommer altid fra tagget.
const nu = LIVE ? { s: { close() {} }, url: SITE } : await webserver();
const før = await webserver(TAG);
if (LIVE) console.log(`Siden nu: ${SITE} (GitHub Pages kan være op til 10 minutter om at vise den nye udgave)`);

const port = 9600 + Math.floor(Math.random() * 90);
const profil = mkdtempSync(join(tmpdir(), 'tjek-crowhurst-'));
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
// Pixeltjek, der springes over med --live
let sprunget = 0;
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

/** En forskel skal være der i tre forsøg i træk, hvert med nye kontekster; Chrome tegner en sjælden gang én pixel anderledes. */
async function somFør(bredde, urlFør, urlNu, forbered, navn) {
  const forsøgene = [];
  for (let forsøg = 1; forsøg <= 3; forsøg++) {
    const d = await sammenlign(bredde, urlFør, urlNu, forbered);
    if (erStøj(d.n)) {
      const slut = d.alle ? `støj i forsøg ${forsøg}` : `ens i forsøg ${forsøg}`;
      for (const f of forsøgene) console.log(`NB ${navn} ved ${bredde} px: ${f}, ${slut}`);
      if (d.alle) console.log(`NB ${navn} ved ${bredde} px: forsøg ${forsøg}: ${d.tekst} – støj (højst ${LOFT} pixels over ${TRIN} trin)`);
      return '';
    }
    forsøgene.push(`forsøg ${forsøg}: ${d.tekst}`);
  }
  return `forskellig i tre forsøg i træk; ${forsøgene.join('; ')}`;
}

async function forskel(a, b, side) {
  if (a.h !== b.h) return { n: Infinity, alle: Infinity, tekst: `højden er ${b.h} px, før ${a.h} px` };
  let n = 0, alle = 0;
  const områder = [];
  let første = '';
  for (let i = 0; i < a.bidder.length; i++) {
    if (a.bidder[i] === b.bidder[i]) continue;
    // En pixel tæller, når den afviger mere end TRIN farvetrin i én kanal (tools/pixelstoej.mjs); området og det første
    // element gælder de tællende pixels, eller alle forskellige, når ingen tæller.
    const d = await side.kør(`(async () => {${FÆLLES}
      const læs = (d) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = 'data:image/png;base64,' + d; });
      const [x, y] = await Promise.all([læs(${JSON.stringify(a.bidder[i])}), læs(${JSON.stringify(b.bidder[i])})]);
      const px = (i) => { const c = new OffscreenCanvas(i.width, i.height); const g = c.getContext('2d'); g.drawImage(i, 0, 0); return g.getImageData(0, 0, i.width, i.height).data; };
      const p = px(x), q = px(y);
      const fund = { n: 0, alle: 0 };
      const felt = () => ({ x0: 1e9, y0: 1e9, x1: -1, y1: -1, først: '' });
      const tællende = felt(), forskellige = felt();
      const med = (f, k, u, v) => {
        if (!f.først) f.først = [p[k], p[k + 1], p[k + 2]].join('.') + ' før, ' + [q[k], q[k + 1], q[k + 2]].join('.') + ' nu';
        f.x0 = Math.min(f.x0, u); f.y0 = Math.min(f.y0, v); f.x1 = Math.max(f.x1, u); f.y1 = Math.max(f.y1, v);
      };
      for (let k = 0; k < p.length; k += 4) {
        const afvigelse = Math.max(Math.abs(p[k] - q[k]), Math.abs(p[k + 1] - q[k + 1]), Math.abs(p[k + 2] - q[k + 2]));
        if (!afvigelse) continue;
        const u = (k / 4) % x.width, v = Math.floor(k / 4 / x.width) + ${i * 6000};
        fund.alle++; med(forskellige, k, u, v);
        if (afvigelse > ${TRIN}) { fund.n++; med(tællende, k, u, v); }
      }
      if (!fund.alle) return null;
      const f = fund.n ? tællende : forskellige;
      // Elementet ved den første forskel, også inde i en shadow root.
      scrollTo(0, Math.max(0, f.y0 - 200));
      let e = document.elementFromPoint(f.x0, f.y0 - scrollY);
      while (e?.shadowRoot) { const g = e.shadowRoot.elementFromPoint(f.x0, f.y0 - scrollY); if (!g || g === e) break; e = g; }
      const om = e ? navn(e) + ' "' + (e.textContent || '').trim().slice(0, 30) + '"' : '?';
      return { n: fund.n, alle: fund.alle, område: f.x0 + ',' + f.y0 + '–' + f.x1 + ',' + f.y1, først: f.først + '; ' + om };
    })()`);
    if (!d) continue;
    n += d.n;
    alle += d.alle;
    områder.push(d.område);
    if (!første) første = d.først;
  }
  // Tallene gælder hele skærmbilledet (alle bidder), så loftet gælder billedet, ikke én bid.
  return alle
    ? { n, alle, tekst: `${n} pixels over ${TRIN} trin, ${alle} forskellige i alt, i ${områder.join(' og ')} (${første})` }
    : { n: 0, alle: 0, tekst: '' };
}

/**
 * Crowhurst-kortet i fuld visning ved 390 px, med en rød streg, hvor skærmen slutter, når kortet stikker ud: hele kortet
 * (`<navn>-fuld-…`) og udsnittet omkring chippen (`<navn>-chip-…`).
 */
async function gemKort(url, navn) {
  const s = await fane(390);
  try {
    await s.gå(url);
    await s.kortKlar();
    await s.visKort(ID, 'fuld');
    await s.kør(ÅBN);
    await vent(200);
    const r = await s.kør(`(() => {
      const e = document.getElementById('kk-app'); const k = e.getBoundingClientRect();
      const chip = [...${R}.querySelectorAll('.chip')].find((c) => c.textContent.includes('checkback efter'));
      const c = chip.getBoundingClientRect();
      return { y: Math.max(0, k.top + scrollY - 12), h: k.height + 24, cy: Math.max(0, c.top + scrollY - 160), sw: Math.max(390, document.documentElement.scrollWidth) };
    })()`);
    if (r.sw > 390) await s.kør(`document.body.insertAdjacentHTML('beforeend', '<div style="position:absolute;top:0;left:390px;width:2px;height:' + document.documentElement.scrollHeight + 'px;background:#e00;z-index:9999"></div>')`);
    for (const [del, y, h] of [['fuld', r.y, r.h], ['chip', r.cy, 340]]) {
      const b = await s.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y, width: r.sw, height: h, scale: 1 } });
      writeFileSync(join(BILLEDER, navn.replace('DEL', del)), Buffer.from(b.data, 'base64'));
    }
  } finally {
    await s.luk();
  }
}

try {
  // 1. Crowhurst-kortet ved 390–398 px: ingen vandret scroll i nogen visning.
  for (const bredde of BREDDER) {
    for (const lang of ['da', 'en']) {
      const s = await fane(bredde);
      await s.gå(`${nu.url}${KORT}?lang=${lang}`);
      const ider = await s.kortKlar();
      tjek(ider.includes(ID), `Konventionskortet ved ${bredde} px på ${lang}: crowhurst er med`);
      for (const visning of VISNINGER) {
        await s.visKort(ID, visning);
        await s.kør(ÅBN);
        await vent(40);
        const m = await s.kør(MÅL);
        tjek(m.ud <= 0 && !m.fund.length, `Crowhurst, ${visning}, ved ${bredde} px på ${lang}: ingen vandret scroll`, `${m.ud} px, ${m.fund.join(', ')}`);
        tjek(!m.skjult.length, `Crowhurst, ${visning}, ved ${bredde} px på ${lang}: siden skjuler ikke noget med overflow`, m.skjult.join(', '));
      }
      await s.luk();
    }
  }

  // 1b. De nye kort ved 390–399 og 1280 px: kun vandret scroll, for de findes ikke i tagget.
  for (const bredde of [...BREDDER, 399, 1280]) {
    for (const lang of ['da', 'en']) {
      const s = await fane(bredde);
      await s.gå(`${nu.url}${KORT}?lang=${lang}`);
      const ider = await s.kortKlar();
      for (const id of NYE_KORT) {
        tjek(ider.includes(id), `Konventionskortet ved ${bredde} px på ${lang}: ${id} er med`);
        if (!ider.includes(id)) continue;
        for (const visning of ['fuld', 'kompakt']) {
          await s.visKort(id, visning);
          await s.kør(ÅBN);
          await vent(40);
          const m = await s.kør(MÅL);
          tjek(m.ud <= 0 && !m.fund.length, `Kortet ${id}, ${visning}, ved ${bredde} px på ${lang}: ingen vandret scroll`, `${m.ud} px, ${m.fund.join(', ')}`);
        }
      }
      await s.luk();
    }
  }

  // 2. Hint-vinduet i træneren (kompaktvisningen bag ⓘ ved titlen).
  for (const bredde of BREDDER) {
    for (const lang of ['da', 'en']) {
      const s = await fane(bredde);
      await s.gå(`${nu.url}traener.html?k=${ID}&lang=${lang}`);
      let knap = false;
      for (let i = 0; i < 100 && !knap; i++) { knap = await s.kør(`!!document.querySelector('.kk-i')`); if (!knap) await vent(50); }
      tjek(knap, `Træneren for crowhurst ved ${bredde} px på ${lang}: ⓘ findes`);
      if (knap) {
        await s.kør(`document.querySelector('.kk-i').click()`);
        await vent(150);
        await s.kør(ÅBN);
        await vent(40);
        const åben = await s.kør(`!document.getElementById('kk-hint-${ID}')?.hidden`);
        tjek(åben, `Hint-vinduet for crowhurst ved ${bredde} px på ${lang}: er åbent`);
        const m = await s.kør(MÅL);
        tjek(m.ud <= 0 && !m.fund.length, `Hint-vinduet for crowhurst ved ${bredde} px på ${lang}: ingen vandret scroll`, `${m.ud} px, ${m.fund.join(', ')}`);
      }
      await s.luk();
    }
  }

  // 3. Pixel for pixel som tagget: ved 390 px alt undtagen crowhurst i fuld visning, ved 399 og 1280 px alt. Med --live
  // tælles sammenligningerne kun, for sitet sammenlignes ikke med tagget.
  if (!INGEN_PIXEL) {
    for (const bredde of [390, 399, 1280]) {
      for (const side of SIDER) {
        for (const lang of ['da', 'en']) {
          if (LIVE) { sprunget++; continue; }
          const klar = async (s) => { if (side === KORT) { await s.kortKlar(); await vent(200); } };
          const d = await somFør(bredde, `${før.url}${side}?lang=${lang}`, `${nu.url}${side}?lang=${lang}`, klar, `${side} på ${lang}`);
          tjek(!d, `${side} ved ${bredde} px på ${lang}: som før`, d);
        }
      }
      const s = await fane(bredde);
      await s.gå(`${før.url}${KORT}`);
      const ider = await s.kortKlar();
      await s.luk();
      const t = await fane(bredde);
      await t.gå(`${nu.url}${KORT}`);
      const iderNu = await t.kortKlar();
      await t.luk();
      tjek(iderNu.length === 50 && ider.length === 49 && ider.every((id) => iderNu.includes(id)),
        `Konventionskortet ved ${bredde} px: alle 50 kort er med, og de 49 fra tagget sammenlignes`, `${iderNu.length} nu, ${ider.length} i tagget`);
      for (const id of ider) {  // kortene fra tagget; de nye kort er ikke med dér
        if (NYE_KORT.includes(id)) continue;
        for (const visning of ['fuld', 'kompakt']) {
          if (bredde === 390 && id === ID && visning === 'fuld') continue;
          if (LIVE) { sprunget++; continue; }
          const vis = async (t) => { await t.kortKlar(); await t.visKort(id, visning); };
          const d = await somFør(bredde, `${før.url}${KORT}`, `${nu.url}${KORT}`, vis, `Kortet ${id}, ${visning}`);
          tjek(!d, `Kortet ${id}, ${visning}, ved ${bredde} px: som før`, d);
        }
      }
    }
    if (LIVE) console.log(`SPRUNGET OVER med --live: pixelsammenligningen med ${TAG} (${sprunget} tjek ved 390, 399 og 1280 px), for den giver kun mening lokalt.`);
  }

  if (BILLEDER) {
    mkdirSync(BILLEDER, { recursive: true });
    for (const lang of ['da', 'en']) {
      await gemKort(`${før.url}${KORT}?lang=${lang}`, `390-${lang}-crowhurst-DEL-foer.png`);
      await gemKort(`${nu.url}${KORT}?lang=${lang}`, `390-${lang}-crowhurst-DEL-efter.png`);
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
const live = LIVE ? ` på ${SITE}; ${sprunget} pixeltjek sprunget over` : '';
console.log(fejl ? `${fejl} FEJL ud af ${antal} tjek${live}` : `Alt i orden: ${antal} tjek${live}`);
process.exit(fejl ? 1 : 0);
