import asf_granule_util as gu


def package(search_results):
    hyp3_granules = [
        get_relevant_metadata_from(result) for result in search_results[:5]
        if is_relevant(result)
    ]

    return hyp3_granules


def get_relevant_metadata_from(result):
    return result


def is_relevant(result):
    title = result['title']

    if not is_correct_format(title):
        return False

    granule = make_granule_from(title)

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
