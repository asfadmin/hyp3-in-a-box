from hypothesis import given, strategies as st
import pytest

import import_granule_search_api
from granule_search import CMR, QueryLimitError

VALID_LIMITS = st.integers(min_value=1, max_value=CMR.MAX_RESULTS)


@given(VALID_LIMITS)
def test_limit(amount):
    api = CMR()

    api.limit(amount)
    params = api.get_query_params()

    assert 'page_size' in params
    assert params['page_size'] == amount


@given(st.integers(min_value=CMR.MAX_RESULTS+1))
def test_large_limits_raise(too_large_amount):
    api = CMR()

    with pytest.raises(QueryLimitError):
        api.limit(too_large_amount)


@given(st.integers(max_value=0))
def test_negative_limits_raise(too_small_amount):
    api = CMR()

    with pytest.raises(QueryLimitError):
        api.limit(too_small_amount)
