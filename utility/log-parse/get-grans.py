import pathlib as pl
import re

import asf_granule_util as gu


def main():
    paths = pl.Path('./data').glob('*.txt')
    log_txt = ""

    for f in paths:
        with f.open('r') as f:
            log_txt += str(f.read())

    grans = set()
    pattern = re.compile("""
            ((S1[AB])_              # Mission ID
            (IW|EW|WV|S[1-6])_     # Mode/Beam
            (GRD|SLC|OCN|RAW)      # Product Type
            ([FHM_])_              # Resolution
            ([12])                 # Processing Level
            ([SA])                 # Product Class
            (SH|SV|DH|DV)_         # Polarization
            ([0-9]{8})T([0-9]{6})_ # Start (Date)T(Time)
            ([0-9]{8})T([0-9]{6})_ # End (Date)T(Time)
            ([0-9]{6})_            # Absolut Orbit Number
            ([0-9A-F]{6})_         # Missin Data Take ID
            ([0-9A-F]{4}))          # Product Unique ID
    """, re.VERBOSE)

    for g in re.findall(pattern, log_txt):
        grans.add(g[0])

    gran_csv = ""
    for g in list(grans)[::3]:
        gran_csv += g + ","
    print(gran_csv)


if __name__ == "__main__":
    main()
