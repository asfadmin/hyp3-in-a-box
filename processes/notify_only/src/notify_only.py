
import matplotlib.pyplot as plt
from shapely import wkt
import geopandas as gpd

import utils
import natural_earth


def browse(granule_wkt):
    countrie_shapefile = natural_earth.download('countries')
    countries = get_geometry_from(countrie_shapefile)

    oceans_shapefile = natural_earth.download('oceans')
    oceans = get_geometry_from(oceans_shapefile)

    gran_poly = wkt.loads(granule_wkt)
    granule = get_granule(gran_poly)

    fig, ax = plt.subplots(1, figsize=(20, 10))

    oceans.plot(ax=ax, edgecolor='#222222', facecolor='#bae4fc')
    countries.plot(ax=ax, facecolor='#cccccc', edgecolor='#222222')
    granule.plot(ax=ax, facecolor='#e83c3c', edgecolor='#163f60', linewidth=2)

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


def get_granule(granule_poly):
    granule = gpd.GeoDataFrame(geometry=[granule_poly])
    granule.crs = {'init': 'epsg:4326'}

    return granule


def set_bounds(poly):
    bounds, scaled_area = poly.bounds, poly.area * 4.5

    xmin, ymin, xmax, ymax = bounds

    plt.xlim([xmin - 2*scaled_area, xmax + 2*scaled_area])
    plt.ylim([ymin - scaled_area, ymax + scaled_area])
