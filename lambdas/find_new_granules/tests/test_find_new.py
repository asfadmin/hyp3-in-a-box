import unittest
from unittest import mock
import datetime as dt

from . import mocks

from src.find_new import environment as env
from src import find_new


class TestFindNewGranules(unittest.TestCase):
    def setUp(self):
        env.set_is_production(False)

    @mock.patch(
        'src.find_new.find_new.requests.get',
        side_effect=mocks.asf_api_requests_get
    )
    def test_get_new(self, mock_get):
        prev_time = dt.datetime.now()

        granules = find_new.get_new_granules_after(prev_time)

        self.assertIsInstance(granules, list)
        self.assertIsInstance(granules.pop(), dict)

    @mock.patch(
        'src.find_new.find_new.get_new_granules_after',
        side_effect=mocks.asf_api_requests_get
    )
    def test_s3_upload(self, mock_find_new):
        find_new.granules()


if __name__ == "__main__":
    unittest.main()
