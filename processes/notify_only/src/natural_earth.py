import zipfile

import requests

import notify_only_utils as utils


class NaturalEarthUrl:
    def __init__(self, geom_name, zip_name, data_classification, scale):
        self.base_download_url = (
            'https://www.naturalearthdata.com/http/'
            '/www.naturalearthdata.com/download'
        )

        self.geom_name = geom_name
        self.scale = scale
        self.zip_name = zip_name
        self.data_classification = data_classification

    def build_url(self):
        return '{base}/{scale}/{data}/{zip_name}'.format(
            base=self.base_download_url,
            scale=self.scale,
            data=self.data_classification,
            zip_name=self.zip_name
        )


def download(geom_name):
    ne_download = get_download_from(geom_name)
    download_path_str = f'data/{geom_name}/{geom_name}.zip'

    return get_shapefile(download_path_str, ne_download)


def get_download_from(geom):
    return {
        'oceans': NaturalEarthUrl(
            geom_name='oceans',
            scale='10m',
            data_classification='physical',
            zip_name='ne_10m_ocean.zip'
        ),
        'countries': NaturalEarthUrl(
            geom_name='countries',
            scale='10m',
            data_classification='cultural',
            zip_name='ne_10m_admin_0_countries.zip'
        ),
        'lakes': NaturalEarthUrl(
            geom_name='lakes',
            scale='10m',
            data_classification='physical',
            zip_name='ne_10m_lakes.zip'
        )
    }[geom]


def get_shapefile(path_str, ne_download):
    print('starting download')
    path = utils.get_base_path() / path_str

    path.parent.mkdir(parents=True, exist_ok=True)

    url = ne_download.build_url()
    dl_path = download_file(url, path)

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

    return shapefiles.pop()
