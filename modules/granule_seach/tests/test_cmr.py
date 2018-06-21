import import_granule_search_api

from granule_search import CMR


def test_cmr():
    search_api = CMR()
    assert search_api
