import re

from hypothesis import given, strategies as st

import import_granule_search_api
from granule_search import CMR
from test_cmr_limit_param import VALID_LIMITS


def test_cmr_constructor():
    assert CMR()


def test_api_url_is_url():
    api_url = CMR().api_url

    assert re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', api_url)


@given(st.lists(st.datetimes(), max_size=3, min_size=3), VALID_LIMITS)
def test_chained_queries(times, amount):
    start, end, after = times
    api = CMR()

    api.between(start, end) \
        .after(after)       \
        .limit(amount)

    params = api.get_query_params()

    assert len(params['created_at[]']) == 2
    assert params['page_size'] == amount
