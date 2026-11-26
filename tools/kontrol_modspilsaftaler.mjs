// Kontrollerer udspilseksemplerne på kortene ms-udspil-sans, ms-udspil-farve og ms-honnoerudspil mod modellen i
// ../Fordelingstræneren/src/modspil/model (SPEC-modspilsaftaler.md, accepttest 5). Læser en JSON-liste på stdin:
// [{kategori, metode, art: "sans"|"farve", holding: [valører]}] og skriver en liste med modellens kort (valør) eller
// null ("table feeling", ikke entydigt). Fordelingstræneren læses kun.
import { register } from 'node:module';
import { fileURLToPath } from 'node:url';
register('./ts-hooks.mjs', import.meta.url);

const MODEL = new URL('../../Fordelingstræneren/src/modspil/model/', import.meta.url);
const u = await import(new URL('udspil.ts', MODEL).href);
const m = await import(new URL('metoder.ts', MODEL).href);

let ind = '';
for await (const bid of process.stdin) ind += bid;
const ud = JSON.parse(ind).map(({ kategori, metode, art, holding }) => {
  const p = m.medMetode(m.profil('standard'), kategori, metode);
  return u.udspil(holding, art, p);
});
process.stdout.write(JSON.stringify(ud));
void fileURLToPath;
