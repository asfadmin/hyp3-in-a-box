import json
import pathlib as pl

import import_hyp3_events
import hyp3_events

"""

        * subject - Email subject
        * additional_info - list of dict with more meta data about the event
            * name - Metadata title
            * value - Metadata content
        * browse_url - URL of a browse image to display
        * download_url - URL where the processed data can be downloaded from
        * unsubscribe_url - URL to disable email notifications of this type
"""


def test_notify_only():
    test_json = load_sample_event('notify-only')

    event = hyp3_events.NotifyOnlyEvent.from_json(test_json)

    for k, v in json.loads(test_json).items():
        assert getattr(event, k) == v
        assert hasattr(event, k)


def load_sample_event(event_name):
    file_path = pl.Path(__file__).parent
    events_path = file_path / 'data' / 'sample-events.json'

    with events_path.open('r') as f:
        sample_events = json.load(f)

    selected_event = sample_events[event_name]

    return json.dumps(selected_event)
