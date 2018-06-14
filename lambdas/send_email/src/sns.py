import hyp3_events


def get_hyp3_event_from(aws_event):
    sns_record = aws_event['Records'].pop()['Sns']
    event_json = sns_record['Message']

    return hyp3_events.NotifyOnlyEvent \
        .from_json(event_json)