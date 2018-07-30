# services/__init__.py
# Rohan Weeden
# Created: June 22, 2018

# This module contains application wrappers around various apis.

import boto3
from hashlib import md5
import json

from hyp3_logging import getLogger

log = getLogger(__name__)


class BadMessageException(Exception):
    pass


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
            log.warn("API call returned more messages that it was supposed to. Some jobs might not be processed")

        if not messages:
            return None

        message = messages[0]
        job_info = {}
        try:
            SQSService.validate_message(message)
            job_info = SQSService.parse_message(message)
        except BadMessageException as e:
            log.debug("DEBUG: Failed to recieve message due to the following error:\n\t", str(e))
        return job_info

    @staticmethod
    def validate_message(message):
        """ Raises a BadMessageException if the checksum doesn't match """
        if md5(message.body.encode()).hexdigest() != message.md5_of_body:
            raise BadMessageException("Message checksum did not match!")

    @staticmethod
    def parse_message(message):
        try:
            return json.loads(message.body)
        except json.JSONDecodeError:
            raise BadMessageException("Message could not be parsed!")
