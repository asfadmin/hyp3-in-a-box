import json
import pathlib as pl

import import_find_new
from find_new.previous_time import get_time_file_path


def find_new(*args, **kwargs):
    pass


def asf_api_requests_get(*args, **kwargs):
    """This method will be used by the mock to replace requests.get"""

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        @property
        def text(self):
            return json.dumps(self.json_data)

    if is_api_url(args[0]):
        test_file_path = pl.Path(__file__).parent
        fake_response_path = test_file_path / 'data' / 'api-response.json'

        with fake_response_path.open() as f:
            data = json.load(f)

        return MockResponse(data, 200)


def is_api_url(url):
    return url in (
        "https://api.daac.asf.alaska.edu/services/search/param",
        "https://cmr.earthdata.nasa.gov/search/granules.json"
    )


def s3_upload(*args, **kwargs):
    """used to mock s3.upload"""
    return True


def get_s3_download_func(time):
    def s3_download(*args, **kwargs):
        time_dict = json.dumps({'previous': time.timestamp()})

        with open(get_time_file_path(), 'w') as f:
            f.write(time_dict)

    return s3_download
