import json
import pathlib as pl
import unittest

import asf_granule_util as gu
import hyp3_events

import import_granule_search_api
from granule_search.cmr import results


class TestFindNewGranules(unittest.TestCase):
    def setUp(self):
        path = pl.Path(__file__).parent / 'data/cmr-response.json'

        with path.open('r') as f:
            sample_results = json.load(f)

        self.search_results = sample_results['feed']['entry']

    def test_package(self):
        new_grans = results.package(self.search_results)

        self.assertIsInstance(new_grans, list)
        for result in new_grans:
            self.package_test(result)

    def package_test(self, result):
        self.assertIsInstance(result, hyp3_events.NewGranuleEvent)

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
