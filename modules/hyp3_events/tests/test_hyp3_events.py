import json
import pathlib as pl

import import_hyp3_events

import pytest
from hypothesis import given

import hyp3_events
import event_strategies


PARAM_NAMES = 'EventType, sample_name'
EVENTS_TO_TEST = [
    (hyp3_events.NotifyOnlyEvent, 'notify-only')
]


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_to_dict(EventType, sample_name):

    @given(event_strategies.strategies[EventType])
    def to_dict(event):
        e_dict = event.to_dict()

        assert isinstance(e_dict, dict)
        assert e_dict.keys()

    to_dict()


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_notify_only_json_round_trip(EventType, sample_name):

    @given(event_strategies.strategies[EventType])
    def round_trip_property_test(event):
        event_json = event.to_json()
        new_event = EventType.from_json(event_json)

        assert new_event == event

    round_trip_property_test()

