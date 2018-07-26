
import pytest
from hypothesis import given

import import_hyp3_events

import hyp3_events
import event_strategies


PARAM_NAMES = 'EventType'
EVENTS_TO_TEST = [
    (hyp3_events.StartEvent),
    (hyp3_events.NotifyOnlyEvent),
    (hyp3_events.NewGranuleEvent)
]


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_to_dict(EventType):

    @given(event_strategies.strategies[EventType])
    def to_dict(event):
        e_dict = event.to_dict()

        assert isinstance(e_dict, dict)
        assert e_dict.keys()

    to_dict()  # pylint: disable=E1120


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_notify_only_json_round_trip(EventType):

    @given(event_strategies.strategies[EventType])
    def round_trip_property_test(event):
        event_json = event.to_json()
        new_event = EventType.from_json(event_json)

        assert new_event == event

    round_trip_property_test()  # pylint: disable=E1120
