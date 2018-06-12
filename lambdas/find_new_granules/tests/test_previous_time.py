import import_path

import unittest
from unittest import mock
import datetime as dt

import mocks
from find_new import previous_time
from find_new import environment as env

TESTING_TIME = dt.datetime(2017, 12, 6, 15, 29, 43, 79060)


class TestPreviousTime(unittest.TestCase):
    def setUp(self):
        env.maturity = 'test'

    @mock.patch(
        'find_new.previous_time.s3.upload',
        side_effect=mocks.s3_upload
    )
    def test_set_time(self, mock_upload):
        previous_time.set(TESTING_TIME)

    @mock.patch(
        'find_new.previous_time.s3.download',
        side_effect=mocks.get_s3_download_func(time=TESTING_TIME)
    )
    def test_get_time(self, mock_download):
        t = previous_time.get()

        self.assertEqual(t, TESTING_TIME)

    def test_prod_file_name(self):
        env.maturity = 'prod'
        prod_file_path = previous_time.get_time_file_path()

        # only tmp directory is writable in aws lambdas
        self.assertEqual(prod_file_path, '/tmp/previous-time.prod.json')


if __name__ == "__main__":
    unittest.main()
