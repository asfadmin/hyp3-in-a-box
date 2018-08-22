import json

import hyp3_events
from hyp3_events import HyP3Event


def get_hyp3_event_from(aws_event) -> HyP3Event:
    sns_record = aws_event['Records'][0]['Sns']
    event_json = sns_record['Message']
    event_type = sns_record['Subject']

    EventType = getattr(hyp3_events, event_type)

    return EventType.from_json(event_json)


def get_message_from(aws_event):
    sns_record = aws_event['Records'][0]['Sns']
    event_json = sns_record['Message']

    json.loads(event_json)
