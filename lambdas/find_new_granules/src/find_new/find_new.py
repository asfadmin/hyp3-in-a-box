import requests
import datetime as dt
import json
import pathlib as pl
import contextlib as cl
import time

from . import previous_time
from .environment import environment
from . import s3

MAX_RESULTS = 2000


def granules():
    """
        :returns: new granules before previous runtime
        :rtype: list[dict]
    """
    prev_time = get_previous_time_formatted()

    request_time = dt.datetime.utcnow()
    print('time-range: {} -> {}'.format(prev_time, cmr_date_format(request_time)))
    results = get_new_granules_after(prev_time)

    previous_time.set(request_time)

    return results


def get_previous_time_formatted():
    try:
        prev_time = previous_time.get()
    except s3.ObjectDoesntExist:
        prev_time = get_init_prev_time()

    return cmr_date_format(prev_time)


def get_init_prev_time():
    return dt.datetime.now() - dt.timedelta(minutes=5)


def cmr_date_format(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


def get_new_granules_after(prev_time):
    """
        :param datetime.datetime prev_time: previous lambda runtime

        :returns: response from cmr
        :rtype: dict
    """
    print('making api request with: {}'.format(prev_time))
    cmr_data = make_cmr_query(prev_time)
    print("cmr returned {} results".format(len(cmr_data)))

    return cmr_data['feed']['entry']


def make_cmr_query(prev_time):
    api = CMRSearchAPI()

    resp = api.query({
        'provider': 'ASF',
        'created_at[]': ["{},".format(prev_time)],
        'platform[]': ['Sentinel-1A', 'Sentinel-1B'],
        'page_size': MAX_RESULTS
    })

    data = resp.json()

    if not environment.is_production:
        cache_output(data)

    return data


class SearchAPI:
    """ Class to wrap searching an generic api"""
    def __init__(self, api_url):
        self.api_url = api_url

    def query(self, params):
        """
            :param params: dict

            :returns: response from cmr
            :rtype: requests.Response

        """
        with timing('request took {runtime} secs to complete'):
            return requests.get(self.api_url, params=params)


class CMRSearchAPI(SearchAPI):
    def __init__(self):
        super().__init__("https://cmr.earthdata.nasa.gov/search/granules.json")


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
