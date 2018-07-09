import numpy as np


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
    lons, lats = bounds[::2], bounds[1::2]

    return [
        shift_to_fit_within_limits(min_val, max_val, limit) for
        (min_val, max_val), limit in [(lats, 90), (lons, 180)]
    ]


def labeled_dict_of(axis_bounds):
    lat_bounds, lon_bounds = axis_bounds

    return {
        'lat': lat_bounds,
        'lon': lon_bounds
    }


def shift_to_fit_within_limits(min_val, max_val, limit):
    if bounds_are_off_both_sides(min_val, max_val, limit):
        return bounds_zoomed_out_to(limit)

    elif bounds_are_off_to_the_left(min_val, max_val, limit):
        return bounds_shifted_to_the_right(min_val, max_val, limit)

    elif bounds_are_off_to_the_right(min_val, max_val, limit):
        return bounds_shifted_to_the_left(min_val, max_val, limit)

    else:
        return min_val, max_val


def bounds_are_off_both_sides(min_val, max_val, limit):
    min_val < -limit and max_val > limit


def bounds_zoomed_out_to(limit):
    return -limit, limit


def bounds_are_off_to_the_left(min_val, max_val, limit):
    return min_val < -limit


def bounds_shifted_to_the_right(min_val, max_val, limit):
    return -limit, max_val + abs(min_val + limit)


def bounds_are_off_to_the_right(min_val, max_val, limit):
    return max_val > limit


def bounds_shifted_to_the_left(min_val, max_val, limit):
    return min_val - abs(max_val - limit), limit
