import os

import import_notify_only
import notify_only


def test_notify_only_browse():
    gran_poly = (
        'POLYGON((30.455441 18.597095,30.770906 20.107595,28.401737 '
        '20.530865,28.10887 19.023712,30.455441 18.597095))'
    )

    png_path = notify_only.browse(gran_poly)

    assert isinstance(png_path, str)
    assert png_path.endswith('.png')


