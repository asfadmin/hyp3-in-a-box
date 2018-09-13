import uuid
import json

import pytest

import hyp3_events
from tempaws import TemporaryQueue, TemporaryTopic

import import_hyp3_process
from hyp3_process.daemon import HyP3Daemon, HyP3DaemonConfig
from hyp3_process.daemon.worker import WorkerStatus


NUM_MESSAGES = 2


def test_daemon_shuts_down_when_no_jobs(daemon, config, handler):
    daemon.run()


def test_daemon_pulls_messages_from_queue(daemon, queue, messages):
    add_messages_to(queue, messages)
    daemon.run()

    assert not queue.receive_messages()


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
def daemon(config, handler):
    return HyP3Daemon(config, handler)


@pytest.fixture()
def config(queue, topic_arn):
    queue_name = queue.attributes['QueueArn'].split(':')[-1]

    daemon_config = HyP3DaemonConfig(
        queue_name=queue_name,
        sns_arn=topic_arn,
        earthdata_creds=json.dumps(
            {"username": "fake-user", "password": "fake-pass"}
        ),
        products_bucket='products-bucket',
        are_ssm_param_names=False
    )

    daemon_config.MAX_IDLE_TIME_SECONDS = 1

    return daemon_config


@pytest.fixture(scope="module")
def queue():
    with TemporaryQueue.create_fifo() as queue:
        yield queue


@pytest.fixture(scope="module")
def topic_arn():
    with TemporaryTopic.create() as topic_arn:
        yield topic_arn


@pytest.fixture
def handler():
    def handler_func(start_event, earthdata_creds, products_bucket):
        return {'browse_url': 'some-url', 'product_url': 'some-url'}

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
