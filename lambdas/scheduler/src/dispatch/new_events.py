import hyp3_events

from . import send


def new_events(new_hyp3_events):
    print(f'Dispatching {len(new_hyp3_events)} events')

    for event in new_hyp3_events:
        dispatch_event(event)


def dispatch_event(event):
    if isinstance(event, hyp3_events.NotifyOnlyEvent):
        send.notify_only(event)
    else:
        send.start_event(event)
