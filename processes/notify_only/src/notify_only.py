
import matplotlib.pyplot as plt
from shapely import wkt
import geopandas as gpd

import utils
import natural_earth


def browse(granule_wkt, subscription_wkt):
    countrie_shapefile = natural_earth.download('countries')
    countries = get_geometry_from(countrie_shapefile)

    oceans_shapefile = natural_earth.download('oceans')
    oceans = get_geometry_from(oceans_shapefile)

    lakes_shp = natural_earth.download('lakes')
    lakes = get_geometry_from(lakes_shp)

    gran_poly = wkt.loads(granule_wkt)
    granule = get_geo_data_frame_from(gran_poly)

    sub_poly = wkt.loads(subscription_wkt)
    subscription = get_geo_data_frame_from(sub_poly)

    fig, ax = plt.subplots(1, figsize=(20, 10))

    colors = {
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
    subscription.plot(
        ax=ax,
        edgecolor=colors['subscription']['edge'],
        facecolor=colors['subscription']['main'],
        alpha=0.3,
        linewidth=5
    )
    granule.plot(
        ax=ax,
        edgecolor=colors['granule']['edge'],
        facecolor=colors['granule']['main'],
        linewidth=2
    )

    set_bounds(gran_poly)

    ax.set_xticks([])
    ax.set_yticks([])

    png_path = str(utils.get_base_path() / 'world.png')
    plt.savefig(png_path, bbox_inches='tight')

    return png_path


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
