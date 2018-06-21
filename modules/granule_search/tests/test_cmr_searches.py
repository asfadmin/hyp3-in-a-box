import datetime as dt

import hyp3_events

from granule_search import CMR


def test_cmr_search():
    cmr = CMR()

    query_time = dt.datetime.now() - dt.timedelta(minutes=5)

    resp = cmr             \
        .after(query_time) \
        .limit(1)          \
        .search()

    assert isinstance(resp, dict)


def test_cmr_get_new_granule_events():
    cmr = CMR()

    query_time = dt.datetime.now() - dt.timedelta(minutes=5)

    resp = cmr             \
        .after(query_time) \
        .limit(1)          \
        .get_new_granule_events()

    assert all(
        isinstance(e, hyp3_events.NewGranuleEvent) for e in resp
    )
