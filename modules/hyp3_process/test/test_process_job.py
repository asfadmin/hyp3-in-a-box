import pytest

import import_hyp3_process

from hyp3_process.daemon.process_job import process_job


def test_process_job(rtc_snap_job, worker):
    email_event = process_job(rtc_snap_job, worker)

    assert email_event


@pytest.fixture
def bad_handler():
    def handler_func(start_event, earthdata_creds, products_bucket):
        raise Exception("error in handler function!")

    return handler_func
