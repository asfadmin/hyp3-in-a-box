import pathlib as pl
import json

import pytest

import hyp3_events
from hyp3_db import hyp3_models
import import_scheduler
from schedule import Job

data_path = pl.Path(__file__).parent / 'data'


@pytest.fixture
def granule_events(testing_granules):
    return [
        hyp3_events.NewGranuleEvent(**e) for e in
        testing_granules['new_granules']
    ]


@pytest.fixture
def testing_granules():
    new_grans_path = data_path / 'new_granules.json'

    with new_grans_path.open('r') as f:
        return json.load(f)


def format_packages(packages):
    return [format_package(package) for package in packages]


def format_package(pack):
    sub, user, granule = pack

    return Job(
        hyp3_models.Subscription(**sub),
        hyp3_models.User(**user),
        hyp3_events.NewGranuleEvent(**granule)
    )
