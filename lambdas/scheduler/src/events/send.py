from . import sns


def send(events):
    for event in events:
        subject, payload = event.event_type, event.to_json()

        resp = sns.push(
            subject=subject,
            payload=payload
        )

        print(resp)
