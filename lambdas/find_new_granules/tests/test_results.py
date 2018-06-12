import import_path

import json
import pathlib as pl
import unittest

import asf_granule_util as gu
import results
from results import granule_package as gp


class TestFindNewGranules(unittest.TestCase):
    def setUp(self):
        path = pl.Path(__file__).parent / 'data/api-response.json'

        with path.open('r') as f:
            results = json.load(f)

        self.search_results = results['feed']['entry']

    def test_package(self):
        new_grans = results.package(self.search_results)

        self.assertIsInstance(new_grans, list)
        for result in new_grans:
            self.package_test(result)

    def test_format_as_json(self):
        new_grans = results.package(self.search_results)
        new_grans_json = results.format_into_json(new_grans)

        formatted_new_grans = json.loads(new_grans_json)

        self.assertIn('new_granules', formatted_new_grans)
        self.assertIsInstance(
            formatted_new_grans['new_granules'],
            list
        )

        path = pl.Path(__file__).parent / 'new_granules.package.json'
        with path.open('w') as f:
            f.write(new_grans_json)

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
