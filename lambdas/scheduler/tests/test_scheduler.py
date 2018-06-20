import import_scheduler

import mock
import schedule
import testing_utils as utils

import hyp3_events

from db_cred_setup import skip_if_creds_not_available
from environment import environment
import scheduler_main


@skip_if_creds_not_available
@mock.patch('dispatch.sns.push')
def test_scheduler_main(sns_mock):
    event = utils.load_testing_granules()

    scheduler_main.scheduler(event)

    sns_mock.assert_called()


@skip_if_creds_not_available
def test_scheduler():
    granules = utils.load_testing_granules()['new_granules']
    granule_events = [
        hyp3_events.NewGranuleEvent(**e) for e in granules
    ]
    email_packages = schedule.hyp3_jobs(granule_events)

    assert isinstance(email_packages, list)

    for sub, user, granule_event in email_packages:
        assert hasattr(sub, 'id')
        assert isinstance(granule_event, hyp3_events.NewGranuleEvent)
        assert sub.user_id == user.id

    if 'local' in environment.maturity:
        utils.cache_results(email_packages)
