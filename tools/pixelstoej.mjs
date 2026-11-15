// Grænserne for støj i pixelsammenligningen (SPEC-pixeltolerance.md, Franks valg (b) 15. november 2026), fælles for
// tools/tjek_viden_320.mjs og tools/tjek_crowhurst_390.mjs.
//
// Chrome tegner en gang imellem nogle pixels en anelse anderledes, også når filerne er de samme. Målingen før mod før
// (10 runder i begge scripts) gav op til 25 pixels i ét skærmbillede, næsten alle med en forskel på 1–5 farvetrin, mens
// en ægte ændring af tekst afviger med over 200 trin. Derfor tæller en pixel kun, når den afviger mere end TRIN trin i
// mindst én kanal (R, G eller B), og højst LOFT sådanne pixels i ét skærmbillede er støj: scripts skriver en NB-linje,
// og testen består. Over loftet skal forskellen være der i tre forsøg i træk, før testen fejler. En forskel i højden
// er aldrig støj.
export const TRIN = 5;
export const LOFT = 5;

/** Tæller pixlen med? [r, g, b] før og nu. */
export function tæller(før, nu) {
  return Math.max(Math.abs(før[0] - nu[0]), Math.abs(før[1] - nu[1]), Math.abs(før[2] - nu[2])) > TRIN;
}

/** Er så mange tællende pixels støj? Infinity (forskel i højden) er det ikke. */
export function erStøj(pixels) {
  return Number.isFinite(pixels) && pixels >= 0 && pixels <= LOFT;
}

/** Afgørelsen for en liste af forskellige pixels, hver som [før, nu]. */
export function afgør(forskelle) {
  const pixels = forskelle.filter(([før, nu]) => tæller(før, nu)).length;
  return { pixels, støj: erStøj(pixels) };
}
