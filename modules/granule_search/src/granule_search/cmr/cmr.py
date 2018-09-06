import json
import requests

from ..search_api import GranuleSearchAPI, QueryLimitError
from . import results


class CMR(GranuleSearchAPI):
    MAX_RESULTS = 2000

    def __init__(self):
        self.output_format = 'json'
        self.package = json.dump
        self.query_params = {}

    def get_new_granule_events(self):
        raw_data = self.search()
        data = raw_data['feed']['entry']

        return results.package(data)

    def search(self):
        total_query_params = {
            **self._get_base_params(),
            **self.query_params
        }
        print(json.dumps(total_query_params))

        resp = requests.get(
            self.api_url,
            params=total_query_params
        )
        print(resp.url)

        return resp.json()

    @property
    def api_url(self):
        return "https://cmr.earthdata.nasa.gov/search/granules.json"

    def before(self, before_time):
        return self._single_date_param(
            before_time, format_str=",{}"
        )

    def after(self, after_time):
        return self._single_date_param(
            after_time, format_str="{},"
        )

    def _single_date_param(self, query_date, format_str):
        create_params = self.query_params.get('created_at[]', [])

        date_str = self._cmr_date_format(query_date)
        print(date_str)
        create_params.append(format_str.format(date_str))

        self.query_params['created_at[]'] = create_params

        return self

    def between(self, before_time, after_time):
        create_at_params = self.query_params.get('created_at[]', [])

        before_str, after_str = [
            self._cmr_date_format(d) for d in (before_time, after_time)
        ]

        cmr_date_range = f"{before_str},{after_str}"
        create_at_params.append(cmr_date_range)
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
