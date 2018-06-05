import json
import pathlib as pl

from src.find_new.previous_time import get_time_file_path


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

    if 'https://api.daac.asf.alaska.edu/services/search/param' in args[0]:
        test_file_path = pl.Path(__file__).parent
        fake_response_path = test_file_path / 'data' / 'api-response.json'

        with fake_response_path.open() as f:
            data = json.load(f)

        return MockResponse(data, 200)


def s3_upload(*args, **kwargs):
    """used to mock s3.upload"""
    return True


def get_s3_download_func(time):
    def s3_download(*args, **kwargs):
        time_dict = json.dumps({'previous': time.timestamp()})

        with open(get_time_file_path(), 'w') as f:
            f.write(time_dict)

    return s3_download
