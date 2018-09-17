import uuid
import json

import pytest
import boto3

import hyp3_events
from tempaws import TemporaryQueue, TemporaryTopic

import import_hyp3_process
from hyp3_process.daemon import HyP3Daemon, HyP3Worker


sns = boto3.resource('sns')

NUM_MESSAGES = 2


def test_daemon_stops_with_empty_queue(daemon):
    daemon.run()


def test_daemon_pulls_messages_from_queue(daemon, queue, messages):
    add_messages_to(queue, messages)
    daemon.run()

    assert len(queue.receive_messages()) == 0


def add_messages_to(temp_queue, testing_messages):
    for message in testing_messages:
        temp_queue.send_message(
            MessageBody=message,
            MessageAttributes={
                'EventType': {
                    'StringValue': "StartEvent",
                    'DataType': 'String'
                }
            },
            MessageGroupId=str(uuid.uuid4())
        )


@pytest.fixture()
def daemon(queue, sns_topic, worker):
    daemon = HyP3Daemon(
        queue,
        sns_topic,
        worker
    )

    daemon.MAX_IDLE_TIME_SECONDS = 2

    return daemon


@pytest.fixture
def worker(creds, bucket, handler):
    return HyP3Worker(
        handler=handler,
        creds=creds,
        bucket=bucket
    )


@pytest.fixture
def creds():
    return json.dumps({
        "username": "fake-user",
        "password": "fake-pass"
    })


@pytest.fixture
def bucket():
    return 'products-bucket'


@pytest.fixture()
def queue():
    with TemporaryQueue.create_fifo() as queue:
        yield queue


@pytest.fixture()
def sns_topic():
    with TemporaryTopic.create() as topic_arn:
        yield sns.Topic(topic_arn)


@pytest.fixture
def handler():
    def handler_func(start_event, earthdata_creds, products_bucket):
        return {'browse_url': 'some-url', 'product_url': 'some-url'}

    return handler_func


@pytest.fixture
def bad_handler():
    def handler_func(start_event, earthdata_creds, products_bucket):
        raise Exception("error in handler function!")

    return handler_func


@pytest.fixture
def messages():
    return [
        hyp3_events.StartEvent(
            granule="SomeGranule",
            user_id=1,
            sub_id=sub_id,
            output_patterns={},
            script_path='/some/script',
            additional_info=[]
        ).to_json() for sub_id in range(NUM_MESSAGES)
    ]
