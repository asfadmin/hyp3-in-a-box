import pathlib as pl
import multiprocessing as mp

import mock

import import_notify_only
import notify_only
import natural_earth


def get_testing_base_path():
    return pl.Path(__file__).parent


def get_data_path():
    return get_testing_base_path() / 'data'


@mock.patch(
    'notify_only_utils.get_base_path',
    side_effect=get_testing_base_path
)
def test_countries_download(path_mock):
    names = notify_only.get_geometry_names()

    pool = mp.Pool(len(names))
    pool.map(download_geom, names)


def download_geom(geom_name):
    path = get_data_path() / geom_name

    if path.exists():
        return

    natural_earth.download(geom_name)


def get_shapefile_path(dl_path):
    path = get_data_path() / dl_path

    return natural_earth.get_shapefile_in(path)


@mock.patch(
    'natural_earth.download',
    side_effect=get_shapefile_path)
def test_notify_only_browse(download_mock):
    gran_polys = [
        ('POLYGON((30.455441 18.597095,30.770906 20.107595,28.401737 '
        '20.530865,28.10887 19.023712,30.455441 18.597095))'
        ), 'POLYGON((-122.374016 40.047749,-121.967674 38.427338,-119.047066 38.829082,-119.382103 40.448418,-122.374016 40.047749))',
        'POLYGON((-145.369354 67.583824,-144.403641 66.114708,-138.803253 66.584755,-139.426422 68.070457,-145.369354 67.583824))',
        'POLYGON((151.06724688555676 -24.528223362574582,163.02037188555676 -26.432299499496587,164.60240313555676 -37.858451843817015,146.32115313555676 -35.03097612917617,151.06724688555676 -24.528223362574582))',
        # 'POLYGON((163.11227482192282 -32.992958890226774,-178.25491267807718 -35.32001562618694,177.70211857192282 -43.07125968935438,160.12399357192282 -40.583050605123454,163.11227482192282 -32.992958890226774))'
    ]

    subscription_poly = (
        'POLYGON((24.2041015625 26.37285889825242,33.4326171875 '
        '28.633406561208858,41.0791015625 18.917390875830886,'
        '29.411002797539595 12.701507059220022,17.809440297539595 '
        '19.94966746671995,24.2041015625 26.37285889825242))'
    )

    for gran_poly in gran_polys:
        png_path = notify_only.browse(gran_poly, subscription_poly)

        assert isinstance(png_path, str)
        assert png_path.endswith('.png')
