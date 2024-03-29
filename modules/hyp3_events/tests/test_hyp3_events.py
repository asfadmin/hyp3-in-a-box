
import pytest
from hypothesis import given

import import_hyp3_events

import hyp3_events
import event_strategies as es


PARAM_NAMES = 'EventType'
EVENTS_TO_TEST = [
    (hyp3_events.NewGranuleEvent),
    (hyp3_events.StartEvent),
    (hyp3_events.EmailEvent)
]

STRATEGIES = {
    hyp3_events.NewGranuleEvent: es.new_granule_events(),
    hyp3_events.StartEvent: es.start_events(),
    hyp3_events.EmailEvent: es.email_events()
}


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_to_dict(EventType):

    @given(STRATEGIES[EventType])
    def to_dict_test(event):
        assert event.event_type != 'HyP3Event'
        e_dict = event.to_dict()

        assert isinstance(e_dict, dict)
        assert e_dict.keys()

    to_dict_test()  # pylint: disable=E1120


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_json_round_trip(EventType):

    @given(STRATEGIES[EventType])
    def round_trip_property_test(event):
        event_json = event.to_json()
        new_event = EventType.from_json(event_json)

        assert new_event == event

    round_trip_property_test()  # pylint: disable=E1120
