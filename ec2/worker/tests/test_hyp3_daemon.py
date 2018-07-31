# test_hyp3_daemon.py
# Rohan Weeden
# Created: July 30, 2018

# Tests for hyp3 glue code daemon.

import mock
import pytest

import import_ec2_worker
from hyp3_daemon import HyP3Daemon
from hyp3_worker import WorkerStatus
from services import SQSJob, SQSService, BadMessageException


@mock.patch('hyp3_daemon.SQSService')
@mock.patch('hyp3_daemon.HyP3Daemon._process_job')
@mock.patch('hyp3_daemon.HyP3DaemonConfig')
def test_daemon_main(_, process_job_mock, SQSServiceMock):
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


def test_status_enum():
    assert WorkerStatus.NO_STATUS
    assert WorkerStatus.READY
    assert WorkerStatus.BUSY
    assert WorkerStatus.DONE


class MockMessage(object):
    def __init__(self, body, md5_of_body):
        self.body = body
        self.md5_of_body = md5_of_body


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
