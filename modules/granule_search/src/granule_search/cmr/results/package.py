import asf_granule_util as gu

import hyp3_events


def package(search_results):
    """ Filters out irrelevant granules and packages only relevant metadata.

        :param list[dict] search_results: package results from CMR

        :returns: List of new granule packages
        :rtype: list[hyp3_events.NewGranuleEvent]
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

    print(f'found granule: {name}')

    polygon_str = get_polygon_str(polygons)
    polygon = parse_points(polygon_str)

    download_url = get_download_url(links)
    browse_url = get_browse_url(links)

    return hyp3_events.NewGranuleEvent(
        name,
        polygon,
        download_url,
        browse_url
    )


def get_polygon_str(polygons):
    return polygons.pop().pop()


def parse_points(points_str):
    points = points_str.strip().split(' ')

    return [float(p) for p in points]


def get_download_url(links):
    url = get_valid_url(links, validator_func=is_zip_url)

    if url == "":
        raise RuntimeError(
            f"No url found in granule links matching "
            f"validator: {is_zip_url.__name__}"
        )

    return url


def get_browse_url(links):
    return get_valid_url(links, validator_func=is_img_url)


def get_valid_url(links, *, validator_func):
    for link in links:
        url = link['href']

        if validator_func(url):
            return url

    return ""


def is_zip_url(url):
    return url.endswith('.zip')


def is_img_url(url):
    img_extensions = ('jpg', 'png', 'jpeg')

    return any(
        has_extension(url, extension) for extension in img_extensions
    )


def has_extension(url, extension):
    return url.lower().endswith(f'.{extension}')


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
