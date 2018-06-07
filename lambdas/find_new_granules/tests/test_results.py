
import unittest
import pathlib as pl
import json

import asf_granule_util as gu
from src import results
from src.results import granule_package as gp


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
            self.package_test(result)

    def package_test(self, result):
        self.assertIsInstance(result, gp.GranulePackage)

        for point in result.polygon:
            self.assertIsInstance(point, float)

        self.assertTrue(
            result.download_url.endswith('.zip')
        )
        self.assertTrue(
            gu.SentinelGranule.is_valid(result.name)
        )

    def test_filtering(self):
        packaged_results = results.package(self.search_results)

        for result in packaged_results:
            g = gu.SentinelGranule(result.name)

            self.assertIn(g.prod_type, ('GRD', 'SLC'))


if __name__ == "__main__":
    unittest.main()
