import requests
import datetime as dt
import json
import pathlib as pl
import contextlib as cl
import time

from . import previous_time


API_URL = 'https://api.daac.asf.alaska.edu/services/search/param'


def lambda_handler(event, context):
    get_new()


def get_new():
    request_time = dt.datetime.now()

    prev_time = get_formatted_previous_time()
    check_for_new_granules_after(prev_time)

    previous_time.set(request_time)


def check_for_new_granules_after(prev_time):
    print('making asf api request with: {}'.format(prev_time))
    api = SearchAPI(API_URL)

    resp = api.query({
        'output': 'JSON',
        'processingDate': prev_time,
        'platform': 'Sentinel-1A,Sentinel-1B',
        'maxResults': 5
    })

    data = resp.json()
    save_output(data)


def get_formatted_previous_time():
    prev_time = previous_time.get()

    return prev_time.strftime('%Y-%m-%dT%H:%M:%SZ')


class SearchAPI:
    def __init__(self, api_url):
        self.api_url = api_url

    def query(self, params):
        with timing('request took {} secs to complete'):
            return requests.get(self.api_url, params=params)


@cl.contextmanager
def timing(print_str):
    """print a string formatted with timing information"""
    start = time.time()
    yield
    print(print_str.format(time.time() - start))


def save_output(data):
    """Save output from query for debugging"""
    output_path = pl.Path('cached')
    output_path.mkdir(parents=True, exist_ok=True)

    with (output_path / 'output.json').open('w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    new_time = get_new()
