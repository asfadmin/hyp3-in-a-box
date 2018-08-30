import mock
import schedule

import hyp3_events
import hyp3_db

import import_scheduler
import testing_utils as utils
from db_cred_setup import skip_if_creds_not_available
from scheduler_env import environment
import scheduler_main


@skip_if_creds_not_available
@mock.patch('dispatch.scheduler_sns.push')
@mock.patch('dispatch.scheduler_sqs.add_event')
def test_scheduler_main(sns_mock, sqs_mock, testing_granules):
    scheduler_main.scheduler(testing_granules)


@skip_if_creds_not_available
def test_scheduler(granule_events):
    jobs = schedule.hyp3_jobs(granule_events)

    assert isinstance(jobs, list)
    assert len(jobs) == 5

    for job in jobs:
        assert hasattr(job.sub, 'id')
        assert isinstance(job.granule, hyp3_events.NewGranuleEvent)
        assert job.sub.user_id == job.user.id
        assert job.process

    if 'local' in environment.maturity:
        utils.cache_results(jobs)
