import pathlib as pl
import subprocess
from typing import Dict


def handler(
    granule_name: str,
    working_dir: str,
    earthdata_creds: Dict[str, str],
    script_path: str
) -> None:
    base = pl.Path(working_dir)
    preprocessed_products: pl.Path = list(
        (pl.Path.home() / 'data').glob('*rtc-s1tbx')
    ).pop()

    subprocess.check_call(['cp', '-r', str(preprocessed_products), str(base)])
