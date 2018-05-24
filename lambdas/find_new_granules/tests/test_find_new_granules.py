import unittest
from unittest import mock

from .fake_api import cmr_requests_get
from find_new_granules.find_new_granules import get_new


class TestFindNewGranules(unittest.TestCase):
    @mock.patch(
        'find_new_granules.find_new_granules.requests.get',
        side_effect=cmr_requests_get
    )
    def test_cmr_get(self, mock_get):
        get_new()


if __name__ == "__main__":
    unittest.main()
