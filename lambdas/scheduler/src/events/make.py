import hyp3_events


def make_notify_events(email_packages):
    events = [
        make_notify_event(sub, user, granule) for
        sub, user, granule in email_packages
    ]

    return events


def make_notify_event(sub, user, granule):
    return hyp3_events.NotifyOnlyEvent(
        address=user.email,
        subject='[hyp3] New Subscription Data',
        additional_info=[{
            'Name': 'User',
            'Value': user.username
        }, {
            'Name': 'Subscripton',
            'Value': sub.name
        }, {
            'Name': 'Granule',
            'Value': granule['name']
        }],
        browse_url='',
        download_url=granule['download_url']
    )
