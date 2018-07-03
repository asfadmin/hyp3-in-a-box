import zipfile
import pathlib as pl

import requests


DOWNLOAD_URL = (
    'https://www.naturalearthdata.com/http//www.naturalearthdata.com'
    '/download/10m/cultural/ne_10m_admin_0_countries.zip'
)


def download(path_str):
    return get_countries_shapefile(path_str)


def get_countries_shapefile(path_str):
    print('starting download')
    path = get_base_path() / path_str

    path.parent.mkdir(parents=True, exist_ok=True)

    dl_path = download_file(DOWNLOAD_URL, path)

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
