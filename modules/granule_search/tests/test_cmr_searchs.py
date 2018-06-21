import datetime as dt

from granule_search import CMR


def test_cmr_search():
    cmr = CMR()

    query_time = dt.datetime.now() - dt.timedelta(minutes=5)

    resp = cmr             \
        .after(query_time) \
        .limit(5)          \
        .search()

    assert isinstance(resp, dict)
