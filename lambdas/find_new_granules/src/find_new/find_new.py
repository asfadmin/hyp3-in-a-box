import contextlib as cl
import datetime as dt
import json
import pathlib as pl
import time

import granule_search

from . import previous_time, s3
from .environment import environment


def granule_events():
    """
        :returns: new granules before the previous runtime of the lambda
        :rtype: list[dict]
    """
    prev_time = get_previous_time_formatted()

    request_time = dt.datetime.utcnow()
    print('time-range: {} -> {}'.format(
        prev_time,
        request_time
    ))

    results = get_new_granules_after(prev_time)
    previous_time.set_time(request_time)

    return results


def get_previous_time_formatted():
    try:
        prev_time = previous_time.get_time()
    except s3.ObjectDoesntExist:
        prev_time = get_init_prev_time()

    return prev_time


def get_init_prev_time():
    return dt.datetime.now() - dt.timedelta(minutes=5)


def get_new_granules_after(prev_time):
    """
        :param datetime.datetime prev_time: previous lambda runtime

        :returns: response from cmr
        :rtype: hyp3_events.NewGranuleEvent
    """
    print('making api request with: {}'.format(prev_time))
    new_granule_events = make_cmr_query(prev_time)
    print("cmr returned {} results".format(len(new_granule_events)))

    return new_granule_events


def make_cmr_query(prev_time):
    api = granule_search.CMR()

    new_granule_events = api        \
        .after(prev_time) \
        .get_new_granule_events()

    if 'test' in environment.maturity:
        cache_output(new_granule_events)

    return new_granule_events


@cl.contextmanager
def timing(print_str):
    """ Print a string formatted with timing information"""
    start = time.time()
    yield
    runtime = time.time() - start
    timing_msg = print_str.format(runtime=runtime)

    print(timing_msg)


def cache_output(data):
    """ Save output from query for debugging"""
    output_path = pl.Path('cached')
    output_path.mkdir(parents=True, exist_ok=True)

    with (output_path / 'output.json').open('w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    new_time = granules()
