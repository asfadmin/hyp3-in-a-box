from hypothesis import given, strategies as st

import import_granule_search_api
from granule_search import CMR


@given(st.datetimes())
def test_before(query_time):
    api = CMR()

    api.before(query_time)
    params = api.get_query_params()

    time_query_tests(params)
    assert all(d.startswith(',') for d in params['created_at[]'])


@given(st.datetimes())
def test_after(query_time):
    api = CMR()

    api.after(query_time)
    params = api.get_query_params()

    time_query_tests(params)
    assert all(d.endswith(',') for d in params['created_at[]'])


@given(st.datetimes(), st.datetimes())
def test_between(start_time, end_time):
    api = CMR()

    api.between(start_time, end_time)
    params = api.get_query_params()

    time_query_tests(params)


def time_query_tests(params):
    assert 'created_at[]' in params
    assert isinstance(params['created_at[]'], list)
