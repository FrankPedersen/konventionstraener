"""
Laver hånd-puljerne til konventionstræneren: pools/<konvention>.json.

    python build_pools.py              # alle konventioner
    python build_pools.py multiforsvar # kun én

En ny konvention får sit eget modul i dealer/ med en export_pool(path) og
tilføjes i CONVENTIONS herunder og i data/konventioner.json.
"""
import os
import sys

from types import SimpleNamespace

from dealer import (ass, bekkasin, cuebids, dont, fjerde_farve, kontrolsvar, lebensohl, multiforsvar,
                    omvendt_bergen, rkc1430, stayman, tofarvet, transfer, xysans,
                    ff_bergen, ff_trial, ff_fast, ff_2over1, ff_genmeld, ff_minor,
                    ff_transfer, ff_gerber, ff_2kl, ff_ogust, ff_rkc,
                    ff_michaels, ff_genaabning, ff_doblinger, ff_kravpas, ff_lebensohl,
                    landy, kamp_stoette, kamp_konk)

CONVENTIONS = {
    "multiforsvar": multiforsvar,
    "bekkasin": bekkasin,
    "xy-sans": xysans,
    "ff-dont": dont,
    "stayman": stayman,
    "ff-ass": ass,
    "forslag-2kl-kontrolsvar": kontrolsvar,
    "michaels": SimpleNamespace(export_pool=tofarvet.export_michaels),
    "usaedvanlig-2nt": SimpleNamespace(export_pool=tofarvet.export_unusual),
    "lebensohl": lebensohl,
    "omvendt-bergen": omvendt_bergen,
    "transfer": transfer,
    "1430": rkc1430,
    "cuebids": cuebids,
    "fjerde-farve": fjerde_farve,
    "ff-revideret-omvendt-bergen": ff_bergen,
    "ff-trial-bids": ff_trial,
    "ff-fast-arrival": ff_fast,
    "ff-two-over-one": ff_2over1,
    "ff-staerke-genmeldinger": ff_genmeld,
    "ff-omvendt-minor": ff_minor,
    "ff-overfoeringer": ff_transfer,
    "ff-gerber": ff_gerber,
    "ff-2kl": ff_2kl,
    "ff-ogust": ff_ogust,
    "ff-1430": ff_rkc,
    "ff-michaels": ff_michaels,
    "ff-genaabning": ff_genaabning,
    "ff-doblinger": ff_doblinger,
    "ff-kravpas": ff_kravpas,
    "ff-lebensohl": ff_lebensohl,
    "kamp-landy": landy,
    "kamp-stoette-def": SimpleNamespace(export_pool=kamp_stoette.exporter("def")),
    "kamp-stoette-off": SimpleNamespace(export_pool=kamp_stoette.exporter("off")),
    "kamp-stoette-minor": SimpleNamespace(export_pool=kamp_stoette.exporter("minor")),
    "kamp-efter-od": SimpleNamespace(export_pool=kamp_stoette.exporter("od")),
    "kamp-gif": SimpleNamespace(export_pool=kamp_konk.exporter("gif")),
    "kamp-2020": SimpleNamespace(export_pool=kamp_konk.exporter("2020")),
    "kamp-doblinger": SimpleNamespace(export_pool=kamp_konk.exporter("dobl")),
    "kamp-1ut-indmeldt": SimpleNamespace(export_pool=kamp_konk.exporter("ut8")),
    "kamp-1ut-forsvar": SimpleNamespace(export_pool=kamp_konk.exporter("ut9")),
}

def main(names):
    here = os.path.dirname(os.path.abspath(__file__))
    for name in names or CONVENTIONS:
        path = os.path.join(here, 'pools', f'{name}.json')
        counts = CONVENTIONS[name].export_pool(path)
        print(f"{name}: {sum(counts.values())} hænder {counts}")

if __name__ == '__main__':
    main(sys.argv[1:])
