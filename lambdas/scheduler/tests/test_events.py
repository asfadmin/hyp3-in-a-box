import import_scheduler

import events
from hyp3_events import Hyp3Event, NotifyOnlyEvent
import testing_utils as utils


def test_events():
    packages = utils.load_email_packages()

    notify_events = events.make_notify_events(packages)

    assert isinstance(notify_events, list)
    for event in notify_events:
        assert isinstance(event, Hyp3Event)
        assert isinstance(event, NotifyOnlyEvent)
