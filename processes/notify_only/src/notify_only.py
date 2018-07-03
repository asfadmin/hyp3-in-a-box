import pathlib as pl

import matplotlib.pyplot as plt

from shapely import wkt

import geopandas as gpd
import pandas as pd

DATA_PATH = pl.Path(__file__).parent / 'data'


def browse(granule_wkt):
    countries = get_countries()

    gran_poly = wkt.loads(granule_wkt)
    granule = get_granule(gran_poly)

    ax = granule.plot(
        ax=countries.plot(cmap='Pastel1', figsize=(20, 10)),
        facecolor='#e83c3c', edgecolor='#163f60', linewidth=2
    )

    set_bounds(gran_poly)

    ax.set_xticks([])
    ax.set_yticks([])

    png_path = str(get_base_path() / 'world.png')
    plt.savefig(png_path, bbox_inches='tight')

    return png_path


def get_countries():
    countries_path = DATA_PATH / \
        '10m' / 'countries' / 'ne_10m_admin_0_countries.shp'

    countries = gpd.read_file(str(countries_path))

    countries.crs = {'init': 'epsg:4326'}

    return countries


def get_granule(granule_poly):
    granule = gpd.GeoDataFrame(pd.DataFrame({
        'Granule': [(
            'S1B_IW_GRDH_1SDV_20180628T052743'
            '_20180628T052808_011569_01543E_B22A')]
    }),
        geometry=[granule_poly]
    )

    granule.crs = {'init': 'epsg:4326'}

    return granule


def set_bounds(poly):
    bounds, area = poly.bounds, poly.area * 4.5

    xmin, xmax = bounds[::2]
    ymin, ymax = bounds[1::2]

    plt.xlim([xmin - 2*area, xmax + 2*area])
    plt.ylim([ymin - area, ymax + area])


def get_base_path():
    return pl.Path('/tmp') if False else pl.Path(__file__).parent
