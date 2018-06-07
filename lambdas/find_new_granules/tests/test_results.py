
import unittest
import pathlib as pl
import json

from src import results


class TestFindNewGranules(unittest.TestCase):
    def setUp(self):
        path = pl.Path(__file__).parent / 'data/api-response.json'

        with path.open('r') as f:
            results = json.load(f)

        self.search_results = results['feed']['entry']

    def test_package(self):
        packaged_results = results.package(self.search_results)

        self.assertIsInstance(packaged_results, list)
        for result in packaged_results:
            self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main()
