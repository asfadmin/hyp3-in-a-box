import json
import pathlib as pl

import import_hyp3_events
import hyp3_events


def test_notify_only_construction():
    test_event_data = load_sample_event_data('notify-only', output='dict')
    event = hyp3_events.NotifyOnlyEvent(**test_event_data)

    assert event


def test_notify_only_dict():
    test_event_data = load_sample_event_data('notify-only', output='dict')

    event = hyp3_events.NotifyOnlyEvent(**test_event_data)
    e_dict = event.to_dict()

    assert isinstance(e_dict, dict)
    assert 'address' in e_dict


def test_notify_only_from_json():
    test_json = load_sample_event_data('notify-only')
    event = hyp3_events.NotifyOnlyEvent.from_json(test_json)

    check_json_attrs_against_event(test_json, event)


def test_notify_only_to_json():
    test_json = load_sample_event_data('notify-only')
    event = hyp3_events.NotifyOnlyEvent.from_json(test_json)

    event_json = event.to_json()

    assert isinstance(event_json, str)
    check_json_attrs_against_event(event_json, event)


def check_json_attrs_against_event(test_json, event):
    test_dict = json.loads(test_json)
    assert 'address' in test_dict

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
