import boto3

import pytest

from tempaws import TemporaryTopic


def test_tempqueue(sns):
    with TemporaryTopic.create() as topic_arn:
        topic = sns.Topic(topic_arn)
        topic.load()

        assert topic.arn


@pytest.fixture
def sns():
    return boto3.resource('sns')
