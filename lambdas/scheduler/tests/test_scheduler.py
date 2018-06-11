import json
import pathlib as pl

import import_path
import schedule


def test_scheduler():
    granules = load_testing_granules()

    schedule.hyp3_jobs(granules)


def load_testing_granules():
    path = pl.Path(__file__).parent / 'data' / 'new_granules.json'
    with path.open('r') as f:
        return json.load(f)
