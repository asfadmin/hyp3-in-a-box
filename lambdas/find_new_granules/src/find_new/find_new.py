import requests
import datetime as dt
import json
import pathlib as pl
import contextlib as cl
import time

from . import previous_time


API_URL = 'https://api.daac.asf.alaska.edu/services/search/param'


def get_new():
    """Get new granules using the asf api and return query results
    also save/load the previous runtimes to s3.

        :returns: dict
    """
    prev_time = get_formatted_previous_time()

    request_time = dt.datetime.now()
    results = get_new_granules_after(prev_time)

    previous_time.set(request_time)

    return results


def get_new_granules_after(prev_time):
    """Make the asf api request and return.

        :param prev_time: datetime.datetime

        :returns: dict
    """

    print('making asf api request with: {}'.format(prev_time))
    api = SearchAPI(API_URL)

    resp = api.query({
        'output': 'JSON',
        'processingDate': prev_time,
        'platform': 'Sentinel-1A,Sentinel-1B',
        'maxResults': 5
    })

    data = resp.json()

    cache_output(data)

    return data[0]


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
        with timing('request took {} secs to complete'):
            return requests.get(self.api_url, params=params)


@cl.contextmanager
def timing(print_str):
    """print a string formatted with timing information"""
    start = time.time()
    yield
    print(print_str.format(time.time() - start))


def cache_output(data):
    """Save output from query for debugging"""
    output_path = pl.Path('cached')
    output_path.mkdir(parents=True, exist_ok=True)

    with (output_path / 'output.json').open('w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    new_time = get_new()
