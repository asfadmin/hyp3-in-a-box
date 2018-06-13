from . import sns
import hyp3_events


def send(subs, user, package):
    notify_events = make_notify_events(subs, user, package)

    for event in notify_events:
        subject, payload = event.event_type, event.to_json()

        resp = sns.push(
            subject=subject,
            payload=payload
        )

        print(resp)


def make_notify_events(subs, user, package):
    events = []

    for sub in subs:
        event_json = make_notify_event(sub, user, package)
        events.append(event_json)

    return events


def make_notify_event(sub, user, package):
    return hyp3_events.NotifyOnlyEvent(
        address=user.email,
        subject='[hyp3] New Subscription Data',
        additional_info=[{
            'Name': 'Subscripton',
            'Value': sub.name
        }, {
            'Name': 'Granule',
            'Value': package['name']
        }],
        browse_url='',
        download_url=package['download_url']
    )

