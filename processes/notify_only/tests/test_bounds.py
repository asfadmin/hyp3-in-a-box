import math

from shapely import wkt

import import_notify_only
import notify_only_test_utils as utils
import bounds


def test_bounds_check():
    testing_polys = utils.load_testing_polys()

    polys = [wkt.loads(p) for p in testing_polys['gran-polys']]

    gran_bounds = [bounds.zoom_out_around(poly) for poly in polys]

    for b, correct in zip(gran_bounds, testing_polys['correct-bounds']):
        assert bounds_are_equal(b, correct)

    assert gran_bounds


def bounds_are_equal(test, correct):
    return \
        math.isclose(test['lat'][0], correct['lat'][0]) and \
        math.isclose(test['lat'][1], correct['lat'][1]) and \
        math.isclose(test['lon'][0], correct['lon'][0]) and \
        math.isclose(test['lon'][1], correct['lon'][1])
