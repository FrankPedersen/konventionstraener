"""Tjekker konventionskortene i data/kort/ mod skabelonen.

Kør fra repoets rod:  python3 tools/tjek_konventionskort.py
Kræver pakken jsonschema (pip install jsonschema).
"""
import json
import pathlib
import sys

from jsonschema import Draft202012Validator

ROD = pathlib.Path(__file__).resolve().parent.parent / "data" / "kort"
skema = json.loads((ROD / "konvention.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(skema)
index = json.loads((ROD / "index.json").read_text(encoding="utf-8"))

fejl = []
filer = sorted(p for p in ROD.glob("*.json") if p.name not in ("index.json", "konvention.schema.json"))
ids = {}

for p in filer:
    k = json.loads(p.read_text(encoding="utf-8"))
    for e in validator.iter_errors(k):
        sti = "/".join(str(x) for x in e.absolute_path) or "(rod)"
        fejl.append(f"{p.name}: {sti}: {e.message}")
    if k.get("id") != p.stem:
        fejl.append(f"{p.name}: id '{k.get('id')}' skal være det samme som filnavnet")
    if k.get("id") in ids:
        fejl.append(f"{p.name}: id '{k['id']}' findes også i {ids[k['id']]}")
    ids[k.get("id")] = p.name
    if p.name not in index:
        fejl.append(f"{p.name}: mangler i index.json")
    modspil = k.get("type") == "modspil"
    tilladt = {"gron", "bla", "gul", "brun", "rosa", "gra"} if not modspil else {"kald", "afvis", "antal", "farvevalg", "udspil", "gra"}
    raekker = list(k.get("meldinger", [])) + [r for f in k.get("fortsaettelser", []) for r in f["meldinger"]] + list(k.get("indmelding", []))
    for r in raekker:
        if "noegle" in r and r["noegle"] not in tilladt:
            fejl.append(f"{p.name}: farvenøglen '{r['noegle']}' hører ikke til typen {k.get('type')}")
    for i, ex in enumerate(k.get("eksempler", []), 1):
        for navn in ("haand", "bordet"):
            if navn not in ex:
                continue
            antal = sum(len(ex[navn].get(f, [])) for f in "SHDC")
            # Modspilshænder kan være midt i spillet og have færre end 13 kort.
            if antal != 13 and not (modspil and 0 < antal <= 13):
                fejl.append(f"{p.name}: eksempel {i} har {antal} kort i {navn}, ikke 13")
        if modspil and ex.get("svar"):
            f, v = ex["svar"][0], int(ex["svar"][1:])
            if v not in ex["haand"].get(f, []):
                fejl.append(f"{p.name}: eksempel {i}: svaret {ex['svar']} er ikke på hånden")

for navn in index:
    if not (ROD / navn).exists():
        fejl.append(f"index.json: {navn} findes ikke")

if fejl:
    print("\n".join(fejl))
    sys.exit(1)
print(f"{len(filer)} konventionskort er i orden.")
