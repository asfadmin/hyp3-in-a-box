import boto3
import json


def poll(queue, event_type):
    resp = queue.receive_messages(
        MaxNumberOfMessages=1,
        MessageAttributeNames=[event_type]
    )

    return resp.pop()
