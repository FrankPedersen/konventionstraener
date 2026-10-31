# SPEC-sprog-kipning-toppe (konventionstræneren)

31. oktober 2026 · Franks valg, skrevet ud af Claude Code

Husets ord ændres i alle tre repoer (Franks valg 31. oktober 2026; `../CLAUDE.md`, Husets ord, og tabellen i `docs/specs/SPEC-sprog-og-ordbog.md`): **kipning** og **dobbelt kipning** altid som navneord (ikke kip, kippe, kipper, kippes eller kippet), **toppe** farven i stedet for "fald" som navn på teknikken, og **frafald** og "falde fra" kun om hold-up. Engelsk er uændret. Fordelingstræneren og forsiden har hver deres spec med samme navn.

## Afgrænsning

`main` er tagget `v-foer-sprog-kipning-toppe`, og arbejdet sker på grenen `sprog-kipning-toppe`. Der flettes først efter Franks godkendelse.

| Sted | Må ske | Må ikke ske |
| --- | --- | --- |
| `tools/tjek_fagord.py` og `tools/tjek_sprog.py` | fagordstesten fejler på kip, kippe, kipper, kippes, kippet og "fald" som navn på teknikken | andre ord |
| Kortene, puljerne, siderne og `viden/` | de samme ord rettes; "frafalder" om en konvention, der ikke gælder, bliver "bortfalder" som i Makker 2-dokumentet | resten |
| `docs/specs/SPEC-sprog-og-ordbog.md` | tabellen over husets ord | resten |

## Accepttest

- [ ] Fagordstesten fejler på kip, kippe, kipper, kippes og kippet og på "Fald eller", "spil på fald" og "fald ="; kipning, kipningen, kipninger, toppe, toppes og falder går igennem.
- [ ] Ingen af ordene står i konventionstrænerens danske tekst, og "frafald" bruges kun om hold-up.
- [ ] `tjek_fagord.py`, `tjek_sprog.py`, `tjek_bydeform.py`, `tjek_konventionskort.py`, `tjek_kort_eksempler.py`, `tjek_crowhurst.py`, `tjek_makker2_aftaler.py`, `tjek_skrifttyper.py` og `sprogtjek.py` består.

## Afklaret

1. **Valget** er Franks, 31. oktober 2026.
2. **"Frafalder"** stod 9 steder om konventioner, der ikke gælder efter indblanding (Stayman, transfer, omvendt Bergen); det er "bortfalder" nu, som Makker 2-dokumentet og kortene allerede skriver.
