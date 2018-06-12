from . import sns


def send(subs, package):
    notifications_dicts = get_notifications(subs, package)

    for notification in notifications_dicts:
        resp = sns.push(
            subject="Hyp3 Notify Only",
            payload=notification
        )

        print(resp)


def get_notifications(subs, package):
    events = []

    for sub in subs:
        event_json = make_event_json(sub, package)
        events.append(event_json)

    return events


def make_event_json(sub, package):
    package.update({
        "sub_id": sub.id
    })

    return package
