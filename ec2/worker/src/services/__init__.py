# services/__init__.py
# Rohan Weeden
# Created: June 22, 2018

# This module contains application wrappers around various apis.

import json
from hashlib import md5

import boto3

from hyp3_logging import getLogger

log = getLogger(__name__)


class BadMessageException(Exception):
    pass


class SQSJob(object):
    def __init__(self, message):
        self.message = message
        try:
            self.data = json.loads(message.body)
        except json.JSONDecodeError:
            raise BadMessageException("Message could not be parsed!")

    def delete(self):
        self.message.delete()

    def __getitem__(self, name):
        return self.data[name]

    def __str__(self):
        return str(self.data)


class SQSService(object):
    def __init__(self, queue_name):
        sqs = boto3.resource('sqs')
        self.sqs_queue = sqs.get_queue_by_name(
            QueueName=queue_name
        )

    def get_next_message(self):
        messages = self.sqs_queue.receive_messages(
            MaxNumberOfMessages=1,
        )
        if len(messages) > 1:
            log.warning(("API call returned more messages that it was supposed to. ",
                         "Some jobs might not be processed"))

        if not messages:
            return None

        message = messages[0]
        job_info = None
        try:
            SQSService.validate_message(message)
            job_info = SQSJob(message)
        except BadMessageException as e:
            log.debug("DEBUG: Failed to recieve message due to the following error:\n\t%s", str(e))
        return job_info

    @staticmethod
    def validate_message(message):
        """ Raises a BadMessageException if the checksum doesn't match """
        if md5(message.body.encode()).hexdigest() != message.md5_of_body:
            raise BadMessageException("Message checksum did not match!")


class SNSService(object):
    def __init__(self, arn):
        sns = boto3.resource('sns')
        self.sns_topic = sns.Topic(arn)

    def push(self, job: SQSJob):
        self.sns_topic.publish(
            Subject="Job Finished",
            Message=json.dumps({
                "address": "",
                "subject": "[hyp3] Processing Completed",
                "browse_url": "",
                "download_url": ""
            })
        )
