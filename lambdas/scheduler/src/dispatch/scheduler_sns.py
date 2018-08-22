import boto3
from hyp3_events import HyP3Event

from scheduler_env import environment

sns = boto3.client('sns')


def push_event(event: HyP3Event) -> None:
    """ Send sns messages for an event

        :param HyP3Event event: HyP3 event to dispatch
    """
    subject, json_payload = event.event_type, event.to_json()

    resp = push(
        subject=subject,
        payload=json_payload
    )

    print(resp)


def push(subject: str, payload: str):
    return sns.publish(
        TopicArn=environment.sns_arn,
        Subject=subject,
        Message=payload
    )
