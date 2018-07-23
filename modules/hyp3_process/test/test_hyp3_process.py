import random
import string

import boto3
import pytest

import import_hyp3_process
import hyp3_process

sqs_resource = boto3.resource('sqs')
sqs_client = boto3.client('sqs')
TESTING_QUEUE = 'UnittestingHyp3Queue.fifo'


@pytest.fixture
def testing_queue():
    resp = sqs_client.list_queues(
        QueueNamePrefix=TESTING_QUEUE
    )

    if "QueueUrls" in resp:
        queue = sqs_resource.get_queue_by_name(QueueName=TESTING_QUEUE)
    else:
        queue = sqs_resource.create_queue(
            QueueName=TESTING_QUEUE,
            Attributes={
                'FifoQueue': 'true',
                "ContentBasedDeduplication": 'true',
            }
        )

    return queue


def test_hyp3_process(testing_queue):
    event_type = 'NotifyOnly'
    add_test_event_to_queue(testing_queue, event_type)
    print(testing_queue)
    assert hyp3_process.process(testing_queue, event_type)


def add_test_event_to_queue(testing_queue, event_type):
    testing_queue.send_message(
        MessageBody='{}'.format(random_string()),
        MessageGroupId='1',
        MessageAttributes={
            event_type: {
                'StringValue': 'Process Type',
                'DataType': 'String'
            }
        })


def random_string():
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )
