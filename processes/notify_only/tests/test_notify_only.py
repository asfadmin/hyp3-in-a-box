import pathlib as pl

import mock

import import_notify_only
import notify_only
import countries


def get_data_path():
    return pl.Path(__file__).parent / 'data'


@mock.patch(
    'notify_only.countries.get_base_path',
    side_effect=lambda: pl.Path(__file__).parent
)
def test_countries_download(path_mock):
    path = get_data_path() / 'countries'

    if path.exists():
        return

    countries.download('data/countries/countries.zip')


def get_shapefile_path(dl_path):
    path = get_data_path() / 'countries'

    return countries.get_shapefile_in(path)


@mock.patch(
    'notify_only.countries.download',
    side_effect=get_shapefile_path)
def test_notify_only_browse(download_mock):
    gran_poly = (
        'POLYGON((30.455441 18.597095,30.770906 20.107595,28.401737 '
        '20.530865,28.10887 19.023712,30.455441 18.597095))'
    )

    png_path = notify_only.browse(gran_poly)

    assert isinstance(png_path, str)
    assert png_path.endswith('.png')
