import hyp3_events


def make_new_granule_events_with(new_granule_dicts):
    events = [
        hyp3_events.NewGranuleEvent(**event)
        for event in new_granule_dicts
    ]

    return events


def make_from(email_packages):
    """ make email packages into notify only events

        :param list(tuple): email packages of the form (sub, user, granule)

        :returns: hyp3 events corresponding to each package
        :rtype: list[hyp3_events.NotifyOnlyEvent]
    """
    events = [
        make_event(sub, user, granule) for
        sub, user, granule in email_packages
    ]

    return events


def make_event(sub, user, granule):
    if sub.process_id == 1:
        make_notify_only_event(sub, user, granule)

    make_start_event(sub, user, granule)


def make_notify_only_event(sub, user, granule):
    return hyp3_events.NotifyOnlyEvent(
        address=user.email,
        subject='New Subscription Data',
        additional_info=[{
            'name': 'User',
            'value': user.username
        }, {
            'name': 'Subscripton',
            'value': sub.name
        }, {
            'name': 'Granule',
            'value': granule.name
        }],
        browse_url='',
        download_url=granule.download_url
    )


def make_start_event(sub, user, granule):
    return hyp3_events.StartEvent()
