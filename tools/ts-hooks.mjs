// Indlæser Fordelingstrænerens TypeScript-model direkte i Node (typerne fjernes af Node selv, Node 22.18+):
// importer uden filendelse får .ts, og JSON-filer indlæses som JSON. Bruges af tools/kontrol_modspilsaftaler.mjs.
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

export async function resolve(spec, ctx, next) {
  if ((spec.startsWith('.') || spec.startsWith('/')) && !/\.[a-z]+$/i.test(spec)) {
    const u = new URL(spec + '.ts', ctx.parentURL);
    if (existsSync(fileURLToPath(u))) return { url: u.href, shortCircuit: true };
  }
  return next(spec, ctx);
}

export async function load(url, ctx, next) {
  if (url.endsWith('.json')) return next(url, { ...ctx, importAttributes: { type: 'json' } });
  return next(url, ctx);
}
