from hypothesis import given, strategies as st

import hyp3_events

import import_scheduler

import events
import testing_utils as utils


@given(st.lists(st.fixed_dictionaries({
    'name': st.text(),
    'polygon': st.lists(st.floats(), min_size=2),
    'download_url': st.text(),
    'browse_url': st.text()
})))
def test_make_new_granule_events(granule_events):
    new_granule_events = events.make_new_granule_events_with(granule_events)

    assert isinstance(new_granule_events, list)
    assert all([
        isinstance(e, hyp3_events.NewGranuleEvent) for e in new_granule_events
    ])


def test_events():
    packages = utils.load_email_packages()

    new_events = events.make_from(packages)

    assert isinstance(new_events, list)
    for event in new_events:
        assert isinstance(event, hyp3_events.Hyp3Event)
