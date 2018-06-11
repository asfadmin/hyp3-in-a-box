import pytest
import pathlib as pl

import import_path
from hyp3_db import Hyp3DB


def test_get_enabled_subs():
    if not creds_file_exists():
        pytest.skip("no creds file fond")

    db = Hyp3DB()
    enabled_subs = db.get_enabled_subs()

    for sub in enabled_subs:
        assert sub.enabled is True


def creds_file_exists():
    creds_path = pl.Path(__file__).parent / '..' / 'hyp3_db' / 'creds.json'
    print(creds_path)

    return creds_path.is_file()
