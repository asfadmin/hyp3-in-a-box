import random
import uuid

import mock
import pytest

from hyp3_events import EmailEvent, StartEvent
from tempaws import TemporaryQueue, TemporaryTopic

import import_hyp3_process
from hyp3_process.daemon import HyP3Daemon, HyP3DaemonConfig, log
from hyp3_process.daemon.worker import WorkerStatus
from hyp3_process.daemon.services import BadMessageException, SQSJob, SQSService


def test_hyp3_daemon(config, handler, messages):
    config.MAX_IDLE_TIME_SECONDS = 1

    with TemporaryQueue.create_fifo() as queue:
        queue_name = queue.attributes['QueueArn'].split(':')[-1]
        config.queue_name = queue_name

        with TemporaryTopic.create() as topic_arn:
            config.sns_arn = topic_arn

            daemon = HyP3Daemon(config, handler)
            daemon.run()

            add_messages_to(queue, messages)

            daemon = HyP3Daemon(config, handler)
            daemon.run()


def add_messages_to(queue, messages):
    for message in messages:
        queue.send_message(
            MessageBody=message,
            MessageAttributes={
                'EventType': {
                    'StringValue': "StartEvent",
                    'DataType': 'String'
                }
            },
            MessageGroupId=str(uuid.uuid4())
        )


def test_status_enum():
    assert WorkerStatus.NO_STATUS
    assert WorkerStatus.READY
    assert WorkerStatus.BUSY
    assert WorkerStatus.DONE
    assert WorkerStatus.FAILED


class MockMessage(object):
    def __init__(self, body, md5_of_body):
        self.body = body
        self.md5_of_body = md5_of_body
        self.times_delete_called = 0

    def delete(self):
        self.times_delete_called += 1


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
def config():
    return HyP3DaemonConfig(
        queue_name='queue-name',
        sns_arn='sns-arn',
        earthdata_creds='{"username": "fake-user", "password": "fake-pass"}',
        products_bucket='products-bucket',
        are_ssm_param_names=False
    )


@pytest.fixture
def handler():
    def handler_func(start_event, earthdata_creds, products_bucket):
        return {'browse_url': 'some-url', 'product_url': 'some-url'}

    return handler_func


@pytest.fixture
def messages():
    return [
        StartEvent(
            granule="SomeGranule",
            user_id=1,
            sub_id=random.randint(1, 100),
            output_patterns={},
            script_path='/some/script',
            additional_info=[]
        ).to_json() for _ in range(5)
    ]
