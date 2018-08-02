import hyp3_events
import json


def get_hyp3_event_from(aws_event):
    sns_record = aws_event['Records'][0]['Sns']
    event_json = sns_record['Message']

    return hyp3_events.NotifyOnlyEvent \
        .from_json(event_json)


def get_message_from(aws_event):
    sns_record = aws_event['Records'][0]['Sns']
    event_json = sns_record['Message']

    json.loads(event_json)
