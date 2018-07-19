import json

import boto3

import import_hyp3_process
import hyp3_process

sqs_resource = boto3.resource('sqs')
sqs_client = boto3.client('sqs')
TESTING_QUEUE = 'UnittestingHyp3Queue.fifo'


def test_hyp3_process():
    queue = get_testing_queue()
    print(queue)
    assert hyp3_process.process('Notify Only')


def get_testing_queue():
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


def add_test_event_to_queue():
    queue = sqs.get_queue_by_name(QueueName=TESTING_QUEUE)

    queue.send_message(MessageBody='blablabla', MessageAttributes={
        'ProcessName': {
            'StringValue': 'Notify Only',
            'DataType': 'String'
        }
    })
