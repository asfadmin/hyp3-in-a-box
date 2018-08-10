import pathlib as pl
from typing import Dict


def handler(
    granule_name: str,
    working_dir: str,
    earthdata_creds: Dict[str, str],
    script_path: str
) -> None:
    files = ['hello.txt', 'browse.png']
    
    for f in files:
        with (pl.Path(working_dir) / f).open('w') as f:
            f.write('test file')
