import contextlib

import boto3

from . import random_str


class TemporaryQueue:
    @staticmethod
    @contextlib.contextmanager
    def create_fifo():
        sqs_resource = boto3.resource('sqs')
        sqs_client = boto3.client('sqs')

        queue = sqs_resource.create_queue(
            QueueName=f'test{random_str.make(4)}.fifo',
            Attributes={
                'FifoQueue': 'true',
                'ContentBasedDeduplication': 'true'
            }
        )

        try:
            yield queue
        except Exception as e:
            raise e
        finally:
            sqs_client.delete_queue(QueueUrl=queue.url)
