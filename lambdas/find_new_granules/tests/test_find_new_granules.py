import unittest
from unittest import mock

from find_new_granules.find_new_granules import get_new


def cmr_requests_get(*args, **kwargs):
    """This method will be used by the mock to replace requests.get"""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://someurl.com/test.json':
        return MockResponse({"key1": "value1"}, 200)


class TestFindNewGranules(unittest.TestCase):
    @mock.patch(
        'find_new_granules.find_new_granules.requests.get',
        side_effect=cmr_requests_get
    )
    def test_cmr_get(self, mock_get):
        get_new()


if __name__ == "__main__":
    unittest.main()
