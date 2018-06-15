import json
import pathlib as pl

import import_hyp3_events

import hyp3_events
import pytest


PARAM_NAMES = 'EventType, sample_name'
EVENTS_TO_TEST = [
    (hyp3_events.NotifyOnlyEvent, 'notify-only')
]


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_notify_only_construction(EventType, sample_name):
    test_event_data = load_sample_event_data(sample_name, output='dict')
    event = EventType(**test_event_data)

    assert event


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_notify_only_dict(EventType, sample_name):
    test_event_data = load_sample_event_data(sample_name, output='dict')
    event = EventType(**test_event_data)

    e_dict = event.to_dict()

    assert isinstance(e_dict, dict)
    assert e_dict.keys()


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_notify_only_from_json(EventType, sample_name):
    test_json = load_sample_event_data(sample_name)
    event = EventType.from_json(test_json)

    check_json_attrs_against_event(test_json, event)


@pytest.mark.parametrize(PARAM_NAMES, EVENTS_TO_TEST)
def test_notify_only_to_json(EventType, sample_name):
    test_json = load_sample_event_data(sample_name)
    event = EventType.from_json(test_json)

    event_json = event.to_json()

    assert isinstance(event_json, str)
    check_json_attrs_against_event(event_json, event)


def check_json_attrs_against_event(test_json, event):
    test_dict = json.loads(test_json)
    assert test_dict.keys()

    for k, v in test_dict.items():
        assert getattr(event, k) == v
        assert hasattr(event, k)


def load_sample_event_data(event_name, output='json'):
    file_path = pl.Path(__file__).parent
    events_path = file_path / 'data' / 'sample-events.json'

    with events_path.open('r') as f:
        sample_events = json.load(f)

    selected_event = sample_events[event_name]

    return json.dumps(selected_event) if 'json' in output \
        else selected_event
