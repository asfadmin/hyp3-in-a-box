import pathlib as pl

import mock

import import_notify_only
import notify_only
import natural_earth


def get_data_path():
    return pl.Path(__file__).parent / 'data'


@mock.patch(
    'notify_only.utils.get_base_path',
    side_effect=lambda: pl.Path(__file__).parent
)
def test_countries_download(path_mock):
    for geom in ('countries', 'oceans'):
        path = get_data_path() / geom
        print(path)

        if path.exists():
            return

        natural_earth.download(geom)


def get_shapefile_path(dl_path):
    print(dl_path)
    path = get_data_path() / dl_path

    return natural_earth.get_shapefile_in(path)


@mock.patch(
    'notify_only.natural_earth.download',
    side_effect=get_shapefile_path)
def test_notify_only_browse(download_mock):
    gran_poly = (
        'POLYGON((30.455441 18.597095,30.770906 20.107595,28.401737 '
        '20.530865,28.10887 19.023712,30.455441 18.597095))'
    )

    png_path = notify_only.browse(gran_poly)

    assert isinstance(png_path, str)
    assert png_path.endswith('.png')
