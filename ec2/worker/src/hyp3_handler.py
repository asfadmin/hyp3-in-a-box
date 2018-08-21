from typing import Dict
import subprocess


def handler(
    granule_name: str,
    working_dir: str,
    earthdata_creds: Dict[str, str],
    script_path: str
) -> None:
    # Call your processing script here. Use subprocess.check_call so that errors
    # will raise an Exception
    subprocess.check_call([script_path, "arg1", "arg2"])
