import contextlib
import uuid

import pytest
import boto3

import hyp3_events
from tempaws import TemporaryQueue, TemporaryTopic

import import_hyp3_process

from hyp3_process.daemon import HyP3Daemon

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
def daemon(queue, sns_topic, logger, worker):
    daemon = HyP3Daemon(
        queue,
        sns_topic,
        logger,
        worker
    )

    daemon.MAX_IDLE_TIME_SECONDS = 2

    return daemon


@pytest.fixture
def logger():
    class DummyLogger:
        @contextlib.contextmanager
        def stdout_to(self, name):
            yield

    return DummyLogger()


@pytest.fixture()
def queue():
    with TemporaryQueue.create_fifo() as queue:
        yield queue


@pytest.fixture()
def sns_topic():
    sns = boto3.resource('sns')

    with TemporaryTopic.create() as topic_arn:
        yield sns.Topic(topic_arn)


@pytest.fixture
def messages(rtc_snap_job):
    return [rtc_snap_job.to_json()] * NUM_MESSAGES
