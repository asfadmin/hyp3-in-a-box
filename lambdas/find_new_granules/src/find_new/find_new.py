import requests
import datetime as dt
import json
import pathlib as pl
import contextlib as cl
import time

from . import previous_time
from . import environment as env


def granules():
    """Get new granules using the asf api and return query results
    also save/load the previous runtimes to s3.

        :returns: dict
    """
    prev_time = get_formatted_previous_time()

    request_time = dt.datetime.utcnow()
    print(f'time-range: {prev_time} -> {request_time}')
    results = get_new_granules_after(prev_time)

    previous_time.set(request_time)

    return results


def get_new_granules_after(prev_time):
    """Make the asf api request and return.

        :param prev_time: datetime.datetime

        :returns: dict
    """
    print('making api request with: {prev_time}')
    cmr_data = make_cmr_query(prev_time)

    print(f"cmr returned {len(cmr_data)} results")

    return cmr_data


def make_asf_api_query(prev_time):
    api = ASFSearchAPI()

    resp = api.query({
        'output': 'JSON',
        'processingDate': prev_time,
        'platform': 'Sentinel-1A,Sentinel-1B',
        'maxResults': 500
    })

    data = resp.json()

    if not env.IS_PRODUCTION:
        cache_output(data)

    return data[0]


def make_cmr_query(prev_time):
    api = CMRSearchAPI()

    resp = api.query({
        'provider': 'ASF',
        'created_at[]': ["{},".format(prev_time)],
        'platform[]': ['Sentinel-1A', 'Sentinel-1B'],
        'page_size': 50
    })

    data = resp.json()

    if not env.IS_PRODUCTION:
        cache_output(data)

    return data['feed']['entry']


def get_formatted_previous_time():
    """Get previous lambda runtime from s3 and format it as asf api compatible
    string.

        :returns: str
    """
    prev_time = previous_time.get()

    return prev_time.strftime('%Y-%m-%dT%H:%M:%SZ')


class SearchAPI:
    """Class to wrap searching an generic api"""

    def __init__(self, api_url):
        self.api_url = api_url

    def query(self, params):
        """Make a search query to an api

            :param params: dict

            :returns: requests.Response
        """
        with timing('request took {runtime} secs to complete'):
            return requests.get(self.api_url, params=params)


class ASFSearchAPI(SearchAPI):
    def __init__(self):
        self.api_url = "https://api.daac.asf.alaska.edu/services/search/param"


class CMRSearchAPI(SearchAPI):
    def __init__(self):
        self.api_url = "https://cmr.earthdata.nasa.gov/search/granules.json"


@cl.contextmanager
def timing(print_str):
    """print a string formatted with timing information"""
    start = time.time()
    yield
    runtime = time.time() - start
    timing_msg = print_str.format(runtime=runtime)

    print(timing_msg)


def cache_output(data):
    """Save output from query for debugging"""
    output_path = pl.Path('cached')
    output_path.mkdir(parents=True, exist_ok=True)

    with (output_path / 'output.json').open('w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    new_time = get_new()
