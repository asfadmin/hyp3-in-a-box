from . import sns


def send(events):
    for event in events:
        subject, json_payload = event.event_type, event.to_json()

        resp = sns.push(
            subject=subject,
            payload=json_payload
        )

        print(resp)
