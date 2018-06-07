import asf_granule_util as gu

types = set()


def package(search_results):
    """Filters out irrelevant granules and packages only relevant
    metadata for the HyP3 scheduler lambda

       :param search_results: list[dict]

       :returns: list[dict]
    """
    hyp3_granules = [
        get_relevant_metadata_from(result) for result in search_results
        if is_relevant(result)
    ]
    print(types)

    return hyp3_granules


def get_relevant_metadata_from(result):
    return result


def is_relevant(result):
    title = result['title']

    if not is_correct_format(title):
        return False

    granule = make_granule_from(title)

    types.add(granule.prod_type)
    return is_relevant_type(granule.prod_type)


def is_correct_format(title):
    return is_granule_in(title) and '-' in title


def is_granule_in(title):
    result = gu.SentinelGranule.is_valid(title) \
        and 'METADATA' not in title

    return result


def make_granule_from(title):
    name, granule_type = title.split('-')

    return gu.SentinelGranule(name)


def is_relevant_type(granule_type):
    return granule_type in ('SLC', 'GRD')
