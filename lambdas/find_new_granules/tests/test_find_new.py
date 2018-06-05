import unittest
from unittest import mock

from src.find_new import get_new
from . import mocks


class TestFindNewGranules(unittest.TestCase):
    @mock.patch(
        'src.find_new.find_new.requests.get',
        side_effect=mocks.asf_api_requests_get
    )
    def test_get_new(self, mock_get):
        get_new()


if __name__ == "__main__":
    unittest.main()
