import unittest
from unittest import mock
import datetime as dt

from . import mocks
from src.find_new import previous_time

TESTING_TIME = dt.datetime(2017, 12, 6, 15, 29, 43, 79060)


class TestPreviousTime(unittest.TestCase):
    def setUp(self):
        previous_time.set_is_production(False)

    @mock.patch(
        'src.find_new.previous_time.s3.upload',
        side_effect=mocks.s3_upload
    )
    def test_set_time(self, mock_upload):
        previous_time.set(TESTING_TIME)

    @mock.patch(
        'src.find_new.previous_time.s3.download',
        side_effect=mocks.get_s3_download_func(time=TESTING_TIME)
    )
    def test_get_time(self, mock_download):
        t = previous_time.get()

        self.assertEqual(t, TESTING_TIME)


if __name__ == "__main__":
    unittest.main()
