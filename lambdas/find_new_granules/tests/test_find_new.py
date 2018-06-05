import unittest
from unittest import mock
import datetime as dt

from src.find_new import get_new_granules_after
from . import mocks


class TestFindNewGranules(unittest.TestCase):
    @mock.patch(
        'src.find_new.find_new.requests.get',
        side_effect=mocks.asf_api_requests_get
    )
    def test_get_new(self, mock_get):
        prev_time = dt.datetime.now()

        granules = get_new_granules_after(prev_time)

        self.assertIsInstance(granules, list)
        self.assertIsInstance(granules.pop(), dict)


if __name__ == "__main__":
    unittest.main()
