import json
import pathlib as pl


def asf_api_requests_get(*args, **kwargs):
    """This method will be used by the mock to replace requests.get"""

    if 'https://api.daac.asf.alaska.edu/services/search/param' in args[0]:
        test_file_path = pl.Path(__file__).parent
        fake_response_path = test_file_path / 'data' / 'api-response.json'

        with fake_response_path.open() as f:
            data = json.load(f)

        return MockResponse(data, 200)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    @property
    def text(self):
        return json.dumps(self.json_data)
