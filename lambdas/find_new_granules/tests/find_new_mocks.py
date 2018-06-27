import json
import pathlib as pl

import import_find_new
from find_new.previous_time import get_time_file_path


def asf_api_requests_get(*args, **kwargs):
    """This method will be used by the mock to replace requests.get"""

    test_file_path = pl.Path(__file__).parent
    fake_response_path = test_file_path / 'data' / 'api-response.json'

    with fake_response_path.open() as f:
        data = json.load(f)

    return data


def is_api_url(url):
    return url in (
        "https://api.daac.asf.alaska.edu/services/search/param",
        "https://cmr.earthdata.nasa.gov/search/granules.json"
    )


def get_s3_download_func(time):
    def s3_download(*args, **kwargs):
        time_dict = json.dumps({'previous': time.timestamp()})

        with open(get_time_file_path(), 'w') as f:
            f.write(time_dict)

    return s3_download
