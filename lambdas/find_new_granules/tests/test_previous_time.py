import unittest
from unittest import mock
import datetime as dt

from . import mocks
from src.find_new import previous_time


class TestPreviousTime(unittest.TestCase):
    @mock.patch(
        'src.find_new.s3.upload',
        sid_effect=mocks.s3_upload
    )
    def test_set_time(self, mock_upload):
        time_to_set = dt.datetime.now()

        previous_time.set(time_to_set)


if __name__ == "__main__":
    unittest.main()

