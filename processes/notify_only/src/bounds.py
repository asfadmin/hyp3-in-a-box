import collections

import numpy as np

LAT_LIMIT, LON_LIMIT = 90, 180


def zoom_out_around(poly):
    poly_bounds = np.array(poly.bounds)

    zoomed_bounds = zoom_bounds_out_around(poly_bounds)

    axis_bounds = shift_back_into_map(zoomed_bounds)

    return labeled_dict_of(axis_bounds)


def zoom_bounds_out_around(poly_bounds):
    zoom_out_amount = 20
    aspect_ratio = np.array([-2, -1, 2, 1])

    return poly_bounds + (aspect_ratio * zoom_out_amount)


def shift_back_into_map(bounds):
    lons, lats = get_lat_lon_ranges_from(bounds)
    axes = [(lats, LAT_LIMIT), (lons, LON_LIMIT)]

    try:
        bounds = [
            shift_to_fit_within_limits(lower_bound, upper_bound, limit) for
            (lower_bound, upper_bound), limit in axes
        ]
    except PolygonWrapError:
        bounds = [
            [-LAT_LIMIT, LAT_LIMIT], [-LON_LIMIT, LON_LIMIT]
        ]

    return bounds


def get_lat_lon_ranges_from(bounds):
    return bounds[::2], bounds[1::2]


def labeled_dict_of(axis_bounds):
    lat_bounds, lon_bounds = axis_bounds

    return {
        'lat': lat_bounds,
        'lon': lon_bounds
    }


Bound = collections.namedtuple('Bound', ['lower', 'upper'])


def shift_to_fit_within_limits(lower, upper, limit):
    bounds = Bound(lower, upper)

    if bounds_are_off_both_sides(bounds, limit):
        raise PolygonWrapError()

    elif bounds_are_off_to_the_left(bounds, limit):
        return bounds_shifted_to_the_right(bounds, limit)

    elif bounds_are_off_to_the_right(bounds, limit):
        return bounds_shifted_to_the_left(bounds, limit)

    else:
        return bounds.lower, bounds.upper


class PolygonWrapError(Exception):
    pass


def bounds_are_off_both_sides(bound, limit):
    return bound.lower < -limit and bound.upper > limit


def bounds_are_off_to_the_left(bound, limit):
    return bound.lower < -limit


def bounds_are_off_to_the_right(bound, limit):
    return bound.upper > limit


def bounds_shifted_to_the_right(bound, limit):
    return -limit, bound.upper + abs(bound.lower + limit)


def bounds_shifted_to_the_left(bound, limit):
    return bound.lower - abs(bound.upper - limit), limit
