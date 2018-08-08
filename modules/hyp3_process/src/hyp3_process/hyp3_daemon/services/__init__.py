# services/__init__.py
# Rohan Weeden
# Created: June 22, 2018

# This module contains application wrappers around various apis.

import json
from hashlib import md5
from typing import Union

import boto3
from hyp3_events import EmailEvent, StartEvent

from ..hyp3_logging import getLogger

log = getLogger(__name__)


class BadMessageException(Exception):
    pass


class SQSJob(object):
    def __init__(self, message):
        self.message = message
        try:
            self.data = StartEvent.from_json(message.body)
        except json.JSONDecodeError:
            raise BadMessageException("Message could not be parsed!")
        except TypeError as e:
            raise BadMessageException(str(e))

    def delete(self):
        self.message.delete()

    def __str__(self):
        return str(self.data)


class SQSService(object):
    def __init__(self, queue_name):
        sqs = boto3.resource('sqs')
        self.sqs_queue = sqs.get_queue_by_name(
            QueueName=queue_name
        )

    def get_next_message(self):
        log.info('checking queue for message')
        messages = self.sqs_queue.receive_messages(
            MaxNumberOfMessages=1,
        )

        if not messages:
            log.debug('no messages found')
            return

        assert len(messages) == 1
        message = messages[0]

        return self.get_job_info_from(message)

    def get_job_info_from(self, message) -> Union[SQSJob, None]:
        try:
            SQSService.validate_message(message)

            return SQSJob(message)
        except BadMessageException as e:
            log.debug(
                "Failed to recieve message due to the following error:\n\t%s",
                str(e)
            )

            return None

    @staticmethod
    def validate_message(message):
        """ Raises a BadMessageException if the checksum doesn't match """
        if md5(message.body.encode()).hexdigest() != message.md5_of_body:
            raise BadMessageException("Message checksum did not match!")


class SNSService(object):
    def __init__(self, arn):
        sns = boto3.resource('sns')
        self.sns_topic = sns.Topic(arn)

    def push(self, event: EmailEvent) -> None:
        self.sns_topic.publish(
            Subject=event.event_type,
            Message=event.to_json()
        )
