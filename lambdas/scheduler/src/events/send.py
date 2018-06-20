from . import sns


def send(events):
    """ Send sns messages for a list of events

        :param list[Hyp3Event] events: Hyp3 events to send off
    """
    for event in events:
        subject, json_payload = event.event_type, event.to_json()

        resp = sns.push(
            subject=subject,
            payload=json_payload
        )

        print(resp)
