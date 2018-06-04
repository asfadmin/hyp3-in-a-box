import requests
import datetime as dt
import json
import pathlib as pl
import time
import contextlib as cl


@cl.contextmanager
def timing(print_str):
    start = time.time()
    yield
    print(print_str.format(time.time() - start))


API_URL = 'https://api.daac.asf.alaska.edu/services/search/param'
# https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html#g-created-at


def get_new():
    time_to_check = get_time_to_check()

    print('making asf api request')
    with timing('request took {} secs to complete'):
        ret = requests.get(API_URL, params={
            'output': 'JSON',
            'processingDate': time_to_check,
            'maxResults': 5
        })

    print(ret.url)

    data = ret.json()
    print(data[0][0].keys())


def save_output(data):
    output_path = pl.Path('cached')
    output_path.mkdir(parents=True, exist_ok=True)

    with (output_path / 'output.json').open('w') as f:
        json.dump(data, f, indent=2)


def get_time_to_check():
    lookback_amount = dt.timedelta(minutes=900)
    to_check = dt.datetime.now() - lookback_amount

    return to_check.strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == "__main__":
    get_new()
