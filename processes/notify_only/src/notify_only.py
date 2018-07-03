
import matplotlib.pyplot as plt
from shapely import wkt
import geopandas as gpd

import countries


def browse(granule_wkt):
    shapefile = countries.download('data/countries/countries.zip')
    countries_gdf = get_countries_from(shapefile)

    gran_poly = wkt.loads(granule_wkt)
    granule = get_granule(gran_poly)

    fig, ax = plt.subplots(1, figsize=(20, 10))

    countries_gdf.plot(ax=ax, cmap='Pastel1', edgecolor='#dddddd')
    granule.plot(ax=ax, facecolor='#e83c3c', edgecolor='#163f60', linewidth=2)

    set_bounds(gran_poly)

    ax.set_xticks([]), ax.set_yticks([])

    png_path = str(countries.get_base_path() / 'world.png')
    plt.savefig(png_path, bbox_inches='tight')

    return png_path


def get_countries_from(shapefile):
    countries = gpd.read_file(str(shapefile))
    countries.crs = {'init': 'epsg:4326'}

    return countries


def get_granule(granule_poly):
    granule = gpd.GeoDataFrame(
        geometry=[granule_poly]
    )

    granule.crs = {'init': 'epsg:4326'}

    return granule


def set_bounds(poly):
    bounds, scaled_area = poly.bounds, poly.area * 4.5

    xmin, xmax = bounds[::2]
    ymin, ymax = bounds[1::2]

    plt.xlim([xmin - 2*scaled_area, xmax + 2*scaled_area])
    plt.ylim([ymin - scaled_area, ymax + scaled_area])
