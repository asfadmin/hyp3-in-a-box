import multiprocessing as mp
import os

import pytest
import mock

import import_notify_only
import notify_only_test_utils as utils
import notify_only
import natural_earth


skip_if_running_in_codebuild = pytest.mark.skipif(
    'CODEBUILD_BUILD_ARN' in os.environ,
    reason="Don't run test if running in codebuild"
)


@skip_if_running_in_codebuild
@mock.patch(
    'notify_only_utils.get_base_path',
    side_effect=utils.get_testing_base_path
)
def test_countries_download(path_mock):
    names = notify_only.get_geometry_names()

    pool = mp.Pool(len(names))
    pool.map(download_geom, names)


def download_geom(geom_name):
    path = utils.get_data_path() / geom_name

    if path.exists():
        return

    natural_earth.download(geom_name)


def get_shapefile_path(dl_path):
    path = utils.get_data_path() / dl_path

    return natural_earth.get_shapefile_in(path)


@skip_if_running_in_codebuild
@mock.patch(
    'natural_earth.download',
    side_effect=get_shapefile_path)
def test_notify_only_browse(download_mock):
    polys = utils.load_testing_polys()

    gran_poly = polys['gran-polys'][0]
    png_path = notify_only.browse(gran_poly, polys['sub-poly'])

    assert isinstance(png_path, str)
    assert png_path.endswith('.png')
