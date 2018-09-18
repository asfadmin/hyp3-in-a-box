import pytest

import hyp3_events

import import_hyp3_process
from hyp3_process.daemon.process_job import process_job


def test_process_job(rtc_snap_job, worker):
    email_event = process_job(rtc_snap_job, worker)

    assert isinstance(email_event, hyp3_events.EmailEvent)
    assert email_event.status == 'Success'


def test_process_job_with_bad_worker(rtc_snap_job, bad_worker):
    email_event = process_job(rtc_snap_job, bad_worker)

    assert email_event.status == 'Failure'



@pytest.fixture
def bad_worker(worker, bad_handler):
    worker.handler = bad_handler

    return worker


@pytest.fixture
def bad_handler():
    def handler_func(start_event, earthdata_creds, products_bucket):
        raise Exception("error in handler function!")

    return handler_func
