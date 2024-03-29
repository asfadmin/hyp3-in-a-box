import multiprocessing as mp

from agg_matplotlib import matplotlib
from matplotlib import pyplot as plt

from shapely import wkt
import geopandas as gpd

import notify_only_utils as utils
import natural_earth
import bounds

PROJECTION_EPSG = '3857'


def browse(granule_wkt, subscription_wkt):
    countries, oceans, lakes, grid = get_geometries()

    granule, subscription = [
        get_wkt_geom(wkt_str) for wkt_str in [granule_wkt, subscription_wkt]
    ]

    fig, ax = plt.subplots(1, figsize=(20, 10))
    colors = get_colors()

    oceans.plot(
        ax=ax,
        edgecolor=colors['water']['edge'],
        facecolor=colors['water']['main']
    )
    countries.plot(
        ax=ax,
        facecolor=colors['land']['main'],
        edgecolor=colors['land']['edge']
    )
    grid.plot(ax=ax, linestyle=':', edgecolor='#000000', alpha=.1)
    lakes.plot(
        ax=ax,
        edgecolor=colors['water']['edge'],
        facecolor=colors['water']['main']
    )
    subscription['gdf'].plot(
        ax=ax,
        edgecolor=colors['subscription']['edge'],
        facecolor=colors['subscription']['main'],
        alpha=0.25,
        linewidth=5
    )
    granule['gdf'].plot(
        ax=ax,
        edgecolor=colors['granule']['edge'],
        facecolor=colors['granule']['main'],
        linewidth=2
    )

    plt_bounds = bounds.zoom_out_around(granule['poly'])
    set_bounds_to(plt_bounds)

    remove_ticks_from(ax)

    png_path = str(utils.get_base_path() / 'world.png')
    plt.savefig(png_path, bbox_inches='tight')

    return png_path


def set_bounds_to(plt_bounds):
    plt.xlim(plt_bounds['lon'])
    plt.ylim(plt_bounds['lat'])


def get_geometries():
    names = get_geometry_names()
    pool = mp.Pool(len(names))

    return pool.map(
        get_natural_earth_geom,
        names
    )


def get_geometry_names():
    return natural_earth \
        .get_natural_earth_geoms() \
        .keys()


def get_natural_earth_geom(name):
    shapefile = natural_earth.download(name)

    return get_geometry_from(shapefile)


def get_wkt_geom(wkt_str):
    poly = wkt.loads(wkt_str)

    return {
        'poly': poly,
        'gdf': get_geo_data_frame_from(poly)
    }


def get_geometry_from(shapefile):
    geometry = gpd.read_file(str(shapefile))
    geometry.crs = {'init': PROJECTION_EPSG}

    return geometry


def get_geo_data_frame_from(poly):
    gdf = gpd.GeoDataFrame(geometry=[poly])
    gdf.crs = {'init': PROJECTION_EPSG}

    return gdf


def remove_ticks_from(ax):
    ax.set_xticks([])
    ax.set_yticks([])


def get_colors():
    return {
        'water': {
            'main': '#bae4fc',
            'edge': '#66c1ff'

        },
        'land': {
            'main': '#cccccc',
            'edge': '#888888'
        },
        'subscription': {
            'main': '#236192',
            'edge': '#000000'
        },
        'granule': {
            'main': '#e83c3c',
            'edge': '#163f60'
        }
    }
