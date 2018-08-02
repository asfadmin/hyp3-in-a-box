# test_hyp3_daemon.py
# Rohan Weeden
# Created: July 30, 2018

# Tests for hyp3 glue code daemon.

import logging

import mock
import pytest

import import_ec2_worker
from hyp3_daemon import HyP3Daemon, log
from hyp3_worker import WorkerStatus
from services import BadMessageException, SQSJob, SQSService


@mock.patch('hyp3_daemon.SQSService')
@mock.patch('hyp3_daemon.HyP3Daemon._process_job')
@mock.patch('hyp3_daemon.HyP3DaemonConfig')
def test_daemon_main(_, process_job_mock, SQSServiceMock):
    log.setLevel(logging.DEBUG)
    daemon = HyP3Daemon()
    daemon.main()

    sqsservice_mock = SQSServiceMock.return_value
    message_mock = sqsservice_mock.get_next_message.return_value

    SQSServiceMock.assert_called_once()
    sqsservice_mock.get_next_message.assert_called_once()
    message_mock.delete.assert_not_called()
    process_job_mock.assert_called_once_with(
        message_mock
    )


@mock.patch('hyp3_daemon.SNSService')
@mock.patch('hyp3_daemon.SQSService')
@mock.patch('hyp3_daemon.HyP3DaemonConfig')
def test_daemon_main_job_finished(_1, _2, sns_mock):
    log.setLevel(logging.DEBUG)
    daemon = HyP3Daemon()

    worker_mock = mock.Mock()
    daemon.worker = worker_mock
    worker_mock.job = SQSJob(MockMessage('''{
        "user_id": 0,
        "sub_id": 0,
        "additional_info": [],
        "granule_name": "DUMMY_GRANULE"
    }''', ''))
    worker_conn_mock = mock.Mock()
    daemon.worker_conn = worker_conn_mock
    worker_conn_mock.poll.return_value = True
    worker_conn_mock.asdf.return_value = False
    worker_conn_mock.recv.return_value = WorkerStatus.DONE

    daemon.main()

    assert worker_mock.job.message.times_delete_called == 1
    sns_mock.return_value.push.assert_called_once()


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
@mock.patch('services.SQSService.validate_message')
@mock.patch('services.SQSJob')
def test_sqsservice_get_next_message(_, validate_mock, sqs_mock):
    sqs_service = SQSService('')

    sqs_obj = sqs_mock.return_value.get_queue_by_name.return_value
    message_mock = MockMessage('', '')
    sqs_obj.receive_messages.return_value = [message_mock]

    sqs_service.get_next_message()

    sqs_obj.receive_messages.assert_called_once()
    validate_mock.assert_called_once_with(message_mock)


@mock.patch('boto3.resource')
@mock.patch('services.SQSJob')
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
    job = SQSJob(MockMessage('{"some": "json"}', ''))

    assert job["some"] == "json"


def test_sqsjob_bad_input_raises():
    with pytest.raises(BadMessageException):
        SQSJob(MockMessage('Not valid json', ''))


def test_event_creation():
    from hyp3_events import EmailEvent
    with pytest.raises(NotImplementedError):
        EmailEvent.from_type("A string!")
    EmailEvent.from_type(
        SQSJob(MockMessage('''{
            "user_id": 0,
            "sub_id": 0,
            "additional_info": [],
            "granule_name": "DUMMY_GRANULE"
        }''', ''))
    )
