import pytest
import json
import pathlib as pl

import import_path
import schedule
from schedule.environment import environment


path = pl.Path(__file__).parent / 'creds.json'
print(path)
if path.exists():
    with path.open('r') as f:
        creds = json.load(f)
    environment.set_db_creds(creds)

skip_if_creds_not_availbable = pytest.mark.skipif(
    not path.exists(),
    reason="Currently can't run test without creds"
)



@skip_if_creds_not_availbable
def test_scheduler():
    granules = load_testing_granules()

    schedule.hyp3_jobs(granules)


def load_testing_granules():
    path = pl.Path(__file__).parent / 'data' / 'new_granules.json'
    with path.open('r') as f:
        return json.load(f)
