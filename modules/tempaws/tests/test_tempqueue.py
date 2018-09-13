import boto3

import pytest

from tempaws import TemporaryQueue


def test_tempqueue(sqs):
    with TemporaryQueue.create_fifo() as queue:
        new_queue_name = queue.attributes['QueueArn'].split(':')[-1]
        new_queue = sqs.get_queue_by_name(QueueName=new_queue_name)

        assert new_queue.url == queue.url
        assert new_queue_name.endswith('fifo')


@pytest.fixture
def sqs():
    return boto3.resource('sqs')
