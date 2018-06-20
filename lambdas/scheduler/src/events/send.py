from . import sns


def send(events):
    """ Send sns messages for a list of events

        :param list[Hyp3Event] events: Hyp3 events to send off
    """
    print(f'Sending {len(events)} events')
    for event in events:
        print(f'sending {event.event_type}')
        subject, json_payload = event.event_type, event.to_json()

        resp = sns.push(
            subject=subject,
            payload=json_payload
        )

        print(resp)
