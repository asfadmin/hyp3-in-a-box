
import matplotlib.pyplot as plt
from shapely import wkt
import geopandas as gpd

import utils
import natural_earth


def browse(granule_wkt, subscription_wkt):
    countries, oceans, lakes = [
        get_natural_earth_geom(g) for g in ['countries', 'oceans', 'lakes']
    ]

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
    lakes.plot(
        ax=ax,
        edgecolor=colors['water']['edge'],
        facecolor=colors['water']['main']
    )
    subscription['gdf'].plot(
        ax=ax,
        edgecolor=colors['subscription']['edge'],
        facecolor=colors['subscription']['main'],
        alpha=0.3,
        linewidth=5
    )
    granule['gdf'].plot(
        ax=ax,
        edgecolor=colors['granule']['edge'],
        facecolor=colors['granule']['main'],
        linewidth=2
    )

    set_bounds(granule['poly'])

    ax.set_xticks([])
    ax.set_yticks([])

    png_path = str(utils.get_base_path() / 'world.png')
    plt.savefig(png_path, bbox_inches='tight')

    return png_path


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
    geometry.crs = {'init': 'epsg:4326'}

    return geometry


def get_geo_data_frame_from(poly):
    gdf = gpd.GeoDataFrame(geometry=[poly])
    gdf.crs = {'init': 'epsg:4326'}

    return gdf


def set_bounds(poly):
    bounds, scaled_area = poly.bounds, poly.area * 4.5

    xmin, ymin, xmax, ymax = bounds

    plt.xlim([xmin - 2*scaled_area, xmax + 2*scaled_area])
    plt.ylim([ymin - scaled_area, ymax + scaled_area])


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
