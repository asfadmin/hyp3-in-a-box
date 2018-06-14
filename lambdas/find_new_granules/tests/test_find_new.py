import datetime as dt
import unittest
from unittest import mock

import import_find_new

import find_new
import mocks
from find_new import environment as env


class TestFindNewGranules(unittest.TestCase):
    def setUp(self):
        env.maturity = 'test'

    @mock.patch(
        'find_new.find_new.requests.get',
        side_effect=mocks.asf_api_requests_get
    )
    def test_get_new(self, mock_get):
        prev_time = dt.datetime.now()

        granules = find_new.get_new_granules_after(prev_time)

        self.assertIsInstance(granules, list)
        self.assertIsInstance(granules.pop(), dict)

        mock_get.assert_called()

    @mock.patch(
        'find_new.find_new.get_new_granules_after',
        side_effect=mocks.asf_api_requests_get
    )
    @mock.patch(
        'find_new.s3.upload',
        side_effect=mocks.s3_upload
    )
    def test_s3_upload(self, mock_s3_upload, mock_find_new):
        find_new.granules()

        mock_s3_upload.assert_called_once()
        mock_find_new.assert_called_once()


if __name__ == "__main__":
    unittest.main()
