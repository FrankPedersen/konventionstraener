"""
Laver hånd-puljerne til konventionstræneren: pools/<konvention>.json.

    python build_pools.py              # alle konventioner
    python build_pools.py multiforsvar # kun én

En ny konvention får sit eget modul i dealer/ med en export_pool(path) og
tilføjes i CONVENTIONS herunder og i data/konventioner.json.
"""
import os
import sys

from dealer import ass, bekkasin, dont, kontrolsvar, multiforsvar, stayman, xysans

CONVENTIONS = {
    "multiforsvar": multiforsvar,
    "bekkasin": bekkasin,
    "xy-sans": xysans,
    "ff-dont": dont,
    "stayman": stayman,
    "ff-ass": ass,
    "forslag-2kl-kontrolsvar": kontrolsvar,
}

def main(names):
    here = os.path.dirname(os.path.abspath(__file__))
    for name in names or CONVENTIONS:
        path = os.path.join(here, 'pools', f'{name}.json')
        counts = CONVENTIONS[name].export_pool(path)
        print(f"{name}: {sum(counts.values())} hænder {counts}")

if __name__ == '__main__':
    main(sys.argv[1:])
