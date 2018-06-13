import import_scheduler

import pytest
import mock
import json
import pathlib as pl

import custom_mocks
import schedule
from schedule.environment import environment

data_path = pl.Path(__file__).parent / 'data'
if data_path.exists():
    with (data_path / 'creds.json').open('r') as f:
        creds = json.load(f)
    environment.set_db_creds(creds)

skip_if_creds_not_availbable = pytest.mark.skipif(
    not data_path.exists(),
    reason="Currently can't run test without creds"
)


@skip_if_creds_not_availbable
@mock.patch(
    'schedule.sns.push',
    side_effect=custom_mocks.sns_mock
)
def test_scheduler(sns_mock):
    granules = load_testing_granules()

    schedule.hyp3_jobs(granules)


def load_testing_granules():
    new_grans_path = data_path / 'new_granules.json'
    with new_grans_path.open('r') as f:
        return json.load(f)['new_granules']
