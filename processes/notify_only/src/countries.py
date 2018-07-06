import zipfile
import pathlib as pl

import requests


DOWNLOAD_URL_BASE = (
    'https://www.naturalearthdata.com/http//www.naturalearthdata.com'
    '/download/10m/cultural/'
)


def download(geom_name):
    zip_file = get_zip_file_from(geom_name)
    download_path_str = f'data/{geom_name}/{geom_name}.zip'

    return get_shapefile(download_path_str, geom=zip_file)


def get_zip_file_from(geom):
    return {
        'oceans': 'ne_10m_ocean.zip',
        'countries': 'ne_10m_admin_0_countries.zip'
    }[geom]


def get_shapefile(path_str, zip_file):
    print('starting download')
    path = get_base_path() / path_str

    path.parent.mkdir(parents=True, exist_ok=True)

    url = DOWNLOAD_URL_BASE + zip_file
    dl_path = download_file(url, path)

    unzip(dl_path)

    return get_shapefile_in(dl_path.parent)


def get_base_path():
    return pl.Path(__file__).parent


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

    return shapefiles.pop()
