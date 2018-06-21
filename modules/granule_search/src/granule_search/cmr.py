import requests

from .search_api import GranuleSearchAPI, QueryLimitError


class CMR(GranuleSearchAPI):
    MAX_RESULTS = 2000

    def __init__(self):
        self.output_format = 'json'
        self.query_params = {}

    def search(self):
        total_query_params = {
            **self._get_base_params(),
            **self.query_params
        }

        api_url_with_format = self.api_url.format(
            output=self.output_format
        )

        resp = requests.get(
            api_url_with_format,
            total_query_params
        )

        return resp.json()

    @property
    def api_url(self):
        return "https://cmr.earthdata.nasa.gov/search/granules.{output}"

    def before(self, before_time):
        return self.single_date_param(
            before_time, format_str=",{}"
        )

    def after(self, after_time):
        return self.single_date_param(
            after_time, format_str="{},"
        )

    def between(self, before_time, after_time):
        create_at_params = self.query_params.get('created_at[]', [])

        before_str, after_str = [
            self._cmr_date_format(d) for d in (before_time, before_time)
        ]

        create_at_params.append("{},{}".format(before_str, after_str))
        self.query_params['created_at[]'] = create_at_params

        return self

    def limit(self, amount):
        assert isinstance(amount, int)

        if amount > self.MAX_RESULTS:
            raise QueryLimitError(
                f"limit {amount} is higher then the max"
                f" query limit of {self.MAX_RESULTS}"
            )
        if amount <= 0:
            raise QueryLimitError(
                f"limit {amount} is <= 0"
            )

        self.query_params['page_size'] = amount

        return self

    def single_date_param(self, query_date, format_str):
        create_params = self.query_params.get('created_at[]', [])

        date_str = self._cmr_date_format(query_date)
        create_params.append("{},".format(date_str))

        self.query_params['created_at[]'] = create_params

        return self

    def get_query_params(self):
        return self.query_params

    def _get_base_params(self):
        return {
            'provider': 'ASF',
            'platform[]': ['Sentinel-1A', 'Sentinel-1B'],
            'page_size': self.MAX_RESULTS,
        }

    @staticmethod
    def _cmr_date_format(date):
        return date.strftime('%Y-%m-%dT%H:%M:%SZ')
