import json

import pytest

import hyp3_events

import import_hyp3_process
from hyp3_process.daemon.services import BadMessageException, SQSJob, SQSService


def test_sqs_job(message, correct_job_output_dict):
    job = SQSJob(message)

    assert isinstance(job.data, hyp3_events.StartEvent)
    assert job.data.to_dict() == json.loads(message.body)

    with pytest.raises(AssertionError):
        job.set_output({"bad": "dict"})

    job.set_output(correct_job_output_dict)
    assert job.output == correct_job_output_dict

    job.delete()
    assert job.message.deleted


def test_sqsservice_get_next_message_bad_checksum(dummy_boto3_queue):
    sqs_service = SQSService(dummy_boto3_queue)

    message = sqs_service.get_next_message()
    assert message is None

    assert sqs_service.sqs_queue.receive_messages_called


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
        hyp3_events.EmailEvent.from_type("A string!")

    hyp3_events.EmailEvent.from_type(
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
def dummy_boto3_queue():
    class DummyQueue:
        def __init__(self):
            self.receive_messages_called = False

        def receive_messages(self, **kwargs):
            self.receive_messages_called = True
            assert 'MaxNumberOfMessages' in kwargs
            assert len(kwargs.keys()) == 1

    return DummyQueue()


@pytest.fixture
def message():
    g = 'S1B_IW_GRDH_1SDV_20180905T092807_20180905T092826_012578_017352_D7D2'
    start_event_json = {
        'granule': g,
        'user_id': 1,
        'sub_id': 1,
        'output_patterns': {},
        'script_path': '/some/path',
        'additional_info': []
    }

    class DummyMessage:
        def __init__(self):
            self.body = json.dumps(start_event_json)
            self.deleted = False

        def delete(self):
            self.deleted = True

    return DummyMessage()


@pytest.fixture
def correct_job_output_dict():
    return {
        "browse_url": "some-url",
        "product_url": "other-url"
    }


class MockMessage(object):
    def __init__(self, body, md5_of_body):
        self.body = body
        self.md5_of_body = md5_of_body
        self.times_delete_called = 0

    def delete(self):
        self.times_delete_called += 1
