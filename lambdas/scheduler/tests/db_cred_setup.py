import pytest
import json
import pathlib as pl

from schedule.environment import environment

data_path = pl.Path(__file__).parent / 'data'
if data_path.exists():
    with (data_path / 'creds.json').open('r') as f:
        creds = json.load(f)
    environment.db_creds = creds

skip_if_creds_not_availbable = pytest.mark.skipif(
    not data_path.exists(),
    reason="Currently can't run test without creds"
)
