import unittest
from unittest import mock
import os
import pathlib as pl
import json

from src.find_new import get_new


def cmr_requests_get(*args, **kwargs):
    """This method will be used by the mock to replace requests.get"""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        @property
        def url(self):
            return args[0]

        @property
        def text(self):
            return json.dumps(self.json_data)

    if 'https://api.daac.asf.alaska.edu/services/search/param' in args[0]:
        test_file_path = pl.Path(os.path.dirname(os.path.abspath(__file__)))
        fake_response_path = test_file_path / 'data' / 'api-response.json'

        with fake_response_path.open() as f:
            data = json.load(f)

        return MockResponse(data, 200)


class TestFindNewGranules(unittest.TestCase):
    @mock.patch(
        'src.find_new.find_new.requests.get',
        side_effect=cmr_requests_get
    )
    def test_cmr_get(self, mock_get):
        get_new()


if __name__ == "__main__":
    unittest.main()
