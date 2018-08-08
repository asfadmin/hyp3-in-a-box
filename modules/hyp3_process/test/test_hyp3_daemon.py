# test_hyp3_daemon.py
# Rohan Weeden
# Created: July 30, 2018

# Tests for hyp3 glue code daemon.

import logging

import mock
import pytest

from hyp3_events import EmailEvent

import import_hyp3_process
from hyp3_process.hyp3_daemon import HyP3Daemon, HyP3DaemonConfig, log
from hyp3_process.hyp3_daemon.worker import WorkerStatus
from hyp3_process.hyp3_daemon.services import BadMessageException, SQSJob, SQSService


@mock.patch('hyp3_process.hyp3_daemon.hyp3_daemon.SQSService')
@mock.patch('hyp3_process.hyp3_daemon.hyp3_daemon.HyP3Daemon._process_job')
def test_daemon_main(process_job_mock, SQSServiceMock, config, handler):
    log.setLevel(logging.DEBUG)
    daemon = HyP3Daemon(config, handler)
    daemon.main()

    sqsservice_mock = SQSServiceMock.return_value
    message_mock = sqsservice_mock.get_next_message.return_value

    SQSServiceMock.assert_called_once()
    sqsservice_mock.get_next_message.assert_called_once()
    message_mock.delete.assert_not_called()
    process_job_mock.assert_called_once_with(
        message_mock
    )


@mock.patch('hyp3_process.hyp3_daemon.hyp3_daemon.SNSService')
@mock.patch('hyp3_process.hyp3_daemon.hyp3_daemon.SQSService')
def test_daemon_main_job_finished(_1, sns_mock, config, handler):
    log.setLevel(logging.DEBUG)
    daemon = HyP3Daemon(config, handler)

    worker_mock = mock.Mock()
    daemon.worker = worker_mock
    worker_mock.job = SQSJob(MockMessage('''{
        "user_id": 0,
        "sub_id": 0,
        "additional_info": [],
        "granule": "DUMMY_GRANULE",
        "output_patterns": [],
        "script_path": ""
    }''', ''))
    worker_conn_mock = mock.Mock()
    daemon.worker_conn = worker_conn_mock
    worker_conn_mock.poll.return_value = True
    worker_conn_mock.recv.return_value = WorkerStatus.DONE

    daemon.main()

    assert worker_mock.job.message.times_delete_called == 1
    sns_mock.return_value.push.assert_called_once()


@pytest.mark.timeout(5)
@mock.patch('hyp3_process.hyp3_daemon.hyp3_daemon.EmailEvent')
@mock.patch('hyp3_process.hyp3_daemon.hyp3_daemon.sys')
@mock.patch('hyp3_process.hyp3_daemon.hyp3_daemon.HyP3Daemon._terminate')
@mock.patch('hyp3_process.hyp3_daemon.hyp3_daemon.SNSService')
@mock.patch('hyp3_process.hyp3_daemon.hyp3_daemon.SQSService')
def test_shutdown_if_idle(_1, _2, terminate_mock, sys_mock, event_mock, config, handler):
    daemon = HyP3Daemon(config, handler)
    daemon.config.MAX_IDLE_TIME_SECONDS = 1
    daemon.run()

    terminate_mock.assert_called_once()
    sys_mock.exit.assert_called_once()


def test_status_enum():
    assert WorkerStatus.NO_STATUS
    assert WorkerStatus.READY
    assert WorkerStatus.BUSY
    assert WorkerStatus.DONE


class MockMessage(object):
    def __init__(self, body, md5_of_body):
        self.body = body
        self.md5_of_body = md5_of_body
        self.times_delete_called = 0

    def delete(self):
        self.times_delete_called += 1


@mock.patch('boto3.resource')
@mock.patch('hyp3_process.hyp3_daemon.services.SQSService.validate_message')
@mock.patch('hyp3_process.hyp3_daemon.services.SQSJob')
def test_sqsservice_get_next_message(_, validate_mock, sqs_mock):
    sqs_service = SQSService('')

    sqs_obj = sqs_mock.return_value.get_queue_by_name.return_value
    message_mock = MockMessage('', '')
    sqs_obj.receive_messages.return_value = [message_mock]

    sqs_service.get_next_message()

    sqs_obj.receive_messages.assert_called_once()
    validate_mock.assert_called_once_with(message_mock)


@mock.patch('boto3.resource')
@mock.patch('hyp3_process.hyp3_daemon.services.SQSJob')
def test_sqsservice_get_next_message_bad_checksum(_, sqs_mock):
    sqs_service = SQSService('')

    sqs_obj = sqs_mock.return_value.get_queue_by_name.return_value
    message_mock = MockMessage('', '')
    sqs_obj.receive_messages.return_value = [message_mock]

    message = sqs_service.get_next_message()

    sqs_obj.receive_messages.assert_called_once()
    assert message is None


def test_validate_message_successfull():
    SQSService.validate_message(
        MockMessage(
            "This is a valid message",
            "b9df57e64d6ad2ac628f117fb7b7f9d9"
        )
    )


def test_validate_bad_message_raises():
    with pytest.raises(BadMessageException):
        SQSService.validate_message(
            MockMessage(
                "This is a valid message",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            )
        )


def test_sqsjob_parse_successful():
    job = SQSJob(MockMessage('''{
        "user_id": 0,
        "sub_id": 0,
        "additional_info": [],
        "granule": "DUMMY_GRANULE",
        "output_patterns": [],
        "script_path": ""
    }''', ''))

    assert job.data.user_id == 0


def test_sqsjob_bad_input_raises():
    with pytest.raises(BadMessageException):
        SQSJob(MockMessage('Not valid json', ''))


def test_event_creation():
    with pytest.raises(NotImplementedError):
        EmailEvent.from_type("A string!")

    EmailEvent.from_type(
        SQSJob(MockMessage('''{
            "user_id": 0,
            "sub_id": 0,
            "additional_info": [],
            "granule": "DUMMY_GRANULE",
            "output_patterns": [],
            "script_path": ""
        }''', ''))
    )


@pytest.fixture
def handler():
    return lambda *args, **kwargs: print('processing')


@pytest.fixture
def config():
    return HyP3DaemonConfig(
        queue_name='queue-name',
        sns_arn='sns-arn',
        earthdata_creds='{"username": "hello", "password": "world"}',
        products_bucket='prodcuts',
        are_ssm_param_names=False
    )
