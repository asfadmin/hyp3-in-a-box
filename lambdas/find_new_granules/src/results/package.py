import json

import asf_granule_util as gu

from . import granule_package as gp


def package(search_results):
    """Filters out irrelevant granules and packages only relevant metadata.

       :param list[dict] search_results: package results from cmr

       :returns: List of new granule packages
       :rtype: list[GranulePackage]
    """
    hyp3_granules = [
        get_relevant_metadata_from(result) for result in search_results
        if is_relevant(result)
    ]

    return hyp3_granules


def get_relevant_metadata_from(result):
    polygons, name, links = [
        result[k] for k in ('polygons', 'producer_granule_id', 'links')
    ]

    polygon_str = get_polygon_str(polygons)
    polygon = parse_points(polygon_str)

    download_url = get_download_url(links)

    return gp.GranulePackage(name, polygon, download_url)


def get_polygon_str(polygons):
    return polygons.pop().pop()


def parse_points(points_str):
    points = points_str.strip().split(' ')

    return [float(p) for p in points]


def get_download_url(links):
    for link in links:
        url = link['href']

        if not url.endswith('.zip'):
            continue

        return url


def is_relevant(result):
    title = result['title']

    if not is_correct_format(title):
        return False

    granule = make_granule_from(result)

    return is_relevant_type(granule.prod_type)


def is_correct_format(title):
    return is_granule_in(title) and '-' in title


def is_granule_in(title):
    result = gu.SentinelGranule.pattern.search(title) \
        and 'METADATA' not in title

    return result


def make_granule_from(result):
    name = result['producer_granule_id']

    return gu.SentinelGranule(name)


def is_relevant_type(granule_type):
    return granule_type in ('SLC', 'GRD')
