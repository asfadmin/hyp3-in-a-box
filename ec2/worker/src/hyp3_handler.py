import pathlib as pl
from typing import Dict


def handler(
    granule_name: str,
    working_dir: str,
    earthdata_creds: Dict[str, str],
    script_path: str
) -> None:
    files = ['hello.txt', 'browse.png', 'granule_TC_Gxx.tif']
    base = pl.Path(working_dir) / 'output-files'
    base.mkdir(parents=True, exist_ok=True)

    for ofile in files:
        with (base / ofile).open('w') as f:
            f.write('test file')
