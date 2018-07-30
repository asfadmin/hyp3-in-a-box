# test_hyp3_daemon.py
# Rohan Weeden
# Created: July 30, 2018

# Tests for hyp3 glue code daemon.

import import_ec2_worker
import mock
from hyp3_daemon import HyP3Daemon
from hyp3_worker import WorkerStatus


@mock.patch('hyp3_daemon.SQSService')
@mock.patch('hyp3_daemon.HyP3Daemon._process_job')
def test_daemon_main(process_job_mock, SQSServiceMock):
    daemon = HyP3Daemon()
    daemon.main()

    sqsservice_mock = SQSServiceMock.return_value
    message_mock = sqsservice_mock.get_next_message.return_value

    SQSServiceMock.assert_called_once()
    sqsservice_mock.get_next_message.assert_called_once()
    message_mock.delete.assert_called_once()
    process_job_mock.assert_called_once_with(
        message_mock
    )


def test_status_enum():
    WorkerStatus.NO_STATUS
    WorkerStatus.READY
    WorkerStatus.BUSY
    WorkerStatus.DONE
