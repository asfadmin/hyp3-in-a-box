import collections
import zipfile

import requests

import notify_only_utils as utils


def download(geom_name):
    natural_earth_download_url = get_url_for(geom_name)
    download_path_str = 'data/{geom_name}/{geom_name}.zip'.format(
        geom_name=geom_name
    )

    return get_shapefile(
        download_path_str,
        natural_earth_download_url
    )


def get_natural_earth_geoms():
    return collections.OrderedDict({
        "countries": (
            "https://www.naturalearthdata.com/http/"
            "/www.naturalearthdata.com/download/10m/cultural/"
            "ne_10m_admin_0_countries.zip"
        ),
        "oceans": (
            "https://www.naturalearthdata.com/http/"
            "/www.naturalearthdata.com/download/10m/physical/"
            "ne_10m_ocean.zip"
        ),
        "lakes":  (
            "https://www.naturalearthdata.com/http/"
            "/www.naturalearthdata.com/download/10m/physical/"
            "ne_10m_lakes.zip"
        ),
        "grid": (
            "https://www.naturalearthdata.com/http/"
            "/www.naturalearthdata.com/download/10m/physical"
            "/ne_10m_graticules_15.zip"
        )
    })


def get_url_for(geom):
    return get_natural_earth_geoms()[geom]


def get_shapefile(path_str, natural_earth_download_url):
    path = utils.get_base_path() / path_str
    path.parent.mkdir(parents=True, exist_ok=True)

    dl_path = download_file(natural_earth_download_url, path)
    unzip(dl_path)

    return get_shapefile_in(dl_path.parent)


def download_file(url, path):
    r = requests.get(url, stream=True)

    with path.open('wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if not chunk:
                continue

            f.write(chunk)

    return path


def unzip(path):
    with zipfile.ZipFile(str(path), "r") as zip_ref:
        zip_ref.extractall(str(path.parent))


def get_shapefile_in(dl_path):
    shapefiles = [
        f for f in dl_path.iterdir() if str(f).endswith('.shp')
    ]

    return shapefiles[0]
