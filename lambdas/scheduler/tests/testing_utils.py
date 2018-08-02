import json
import pathlib as pl

import hyp3_events
from hyp3_db import hyp3_models

from schedule import Job

data_path = pl.Path(__file__).parent / 'data'


def cache_results(email_packages):
    packages = [
        (serializeable(sub), serializeable(user), gran) for
        sub, user, gran in email_packages
    ]

    with (data_path / 'email-packages.json').open('w') as f:
        json.dump(packages, f, indent=2)


def serializeable(sub):
    sub_dict = {}
    for k, v in sub.__dict__.items():
        try:
            json.dumps(v)
        except TypeError:
            continue

        sub_dict[k] = v

    return sub_dict


def load_testing_granules():
    new_grans_path = data_path / 'new_granules.json'

    with new_grans_path.open('r') as f:
        return json.load(f)


def load_email_packages():
    email_packages_path = data_path / 'email-packages.json'

    with email_packages_path.open('r') as f:
        unformatted_packages = json.load(f)

    return format_packages(unformatted_packages)


def format_packages(packages):
    return [format_package(package) for package in packages]


def format_package(pack):
    sub, user, granule = pack

    return Job(
        hyp3_models.Subscription(**sub),
        hyp3_models.User(**user),
        hyp3_events.NewGranuleEvent(**granule)
    )
