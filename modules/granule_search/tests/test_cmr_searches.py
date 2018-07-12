import datetime as dt

import hyp3_events

from granule_search import CMR


def test_cmr_search():
    cmr = CMR()
    query_time = dt.datetime.now() - dt.timedelta(minutes=5)

    resp = cmr             \
        .after(query_time) \
        .search()

    print(len(resp['feed']['entry']))
    assert isinstance(resp, dict)


def test_cmr_get_new_granule_events():
    cmr = CMR()

    now = dt.datetime.now()
    query_time = now - dt.timedelta(minutes=5)

    resp = cmr             \
        .between(query_time, now) \
        .get_new_granule_events()

    print(len(resp))
    assert all(
        isinstance(e, hyp3_events.NewGranuleEvent) for e in resp
    )
