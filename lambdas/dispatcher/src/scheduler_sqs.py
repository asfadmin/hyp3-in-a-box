import uuid

import boto3

from hyp3_events import StartEvent
from scheduler_env import environment

sqs = boto3.client('sqs')


def add_event(event: StartEvent) -> None:
    send(
        event_type=event.event_type,
        body=event.to_json()
    )


def send(event_type: str, body: str) -> None:
    sqs.send_message(
        QueueUrl=environment.queue_url,
        MessageBody=body,
        MessageAttributes={
            'EventType': {
                'StringValue': event_type,
                'DataType': 'String'
            }
        },
        MessageGroupId=str(uuid.uuid4())
    )
