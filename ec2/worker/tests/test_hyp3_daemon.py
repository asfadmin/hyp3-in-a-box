# test_hyp3_daemon.py
# Rohan Weeden
# Created: July 30, 2018

# Tests for hyp3 glue code daemon.

import import_ec2_worker
import mock
from hyp3_daemon import HyP3Daemon


@mock.patch('hyp3_daemon.SQSService')
@mock.patch('hyp3_daemon.HyP3Daemon._process_job')
def test_daemon_main(process_job_mock, SQSServiceMock):
    sqsservice_mock = SQSServiceMock.return_value

    daemon = HyP3Daemon()
    daemon.main()

    SQSServiceMock.assert_called_once()
    sqsservice_mock.get_next_message.assert_called_once()
    process_job_mock.assert_called_once_with(
        sqsservice_mock.get_next_message.return_value
    )
