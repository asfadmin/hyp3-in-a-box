from . import sns


def notify_only(event):
    """ Send sns messages for a list of events

        :param Hyp3Event event: Hyp3 event to dispatch
    """
    print(f'sending {event.event_type}')
    subject, json_payload = event.event_type, event.to_json()

    resp = sns.push(
        subject=subject,
        payload=json_payload
    )

    print(resp)


def start_event(event):
    pass
