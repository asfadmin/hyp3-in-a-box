import import_scheduler

import mock
import json

import custom_mocks
import schedule
from schedule.environment import environment
from db_cred_setup import skip_if_creds_not_availbable, data_path


@skip_if_creds_not_availbable
@mock.patch(
    'schedule.sns.push',
    side_effect=custom_mocks.sns_mock
)
def test_scheduler(sns_mock):
    granules = load_testing_granules()

    email_packages = schedule.hyp3_jobs(granules)

    assert isinstance(email_packages, list)

    for sub, granule_package in email_packages:
        assert hasattr(sub, 'id')
        assert all(
            k in granule_package for k in ['name', 'download_url', 'polygon']
        )

    if 'test' in environment.maturity:
        cache_results(email_packages)


def cache_results(email_packages):
    packages = [
        (serializeable(sub), gran) for sub, gran in email_packages
    ]

    with (data_path / 'email-packages.json').open('w') as f:
        json.dump(packages, f, indent=2)


def serializeable(sub):
    sub_dict = {}
    for k, v in sub.__dict__.items():
        try:
            json.dumps(v)
        except Exception:
            continue

        sub_dict[k] = v

    return sub_dict


def load_testing_granules():
    new_grans_path = data_path / 'new_granules.json'

    with new_grans_path.open('r') as f:
        return json.load(f)['new_granules']
