import contextlib

import boto3

from . import random_str


class TemporaryTopic:
    @staticmethod
    @contextlib.contextmanager
    def create():
        sns_client = boto3.client('sns')

        topic = sns_client.create_topic(
            Name=f'test{random_str.make(6)}'
        )['TopicArn']

        try:
            yield topic
        except Exception as e:
            raise e
        finally:
            sns_client.delete_topic(TopicArn=topic)
