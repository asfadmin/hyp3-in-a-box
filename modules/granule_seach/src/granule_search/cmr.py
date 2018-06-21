from .search_api import GranuleSearchAPI


class CMR(GranuleSearchAPI):
    """
        Hoping to build a cleaner interface that will make interchanging
        API's simple

        Old:
            api = CMRSearchAPI()

            resp = api.query({
                'provider': 'ASF',
                'created_at[]': ["{},".format(prev_time)],
                'platform[]': ['Sentinel-1A', 'Sentinel-1B'],
                'page_size': MAX_RESULTS
            })

        New:
            api = CMR()

            resp = api \
                .before(prev_time)
                .limit(MAX_RESULTS)
                .search()
    """
    @property
    def api_url(self):
        return "https://cmr.earthdata.nasa.gov/search/granules.json"

    @staticmethod
    def cmr_date_format(date):
        return date.strftime('%Y-%m-%dT%H:%M:%SZ')

    def search(self):
        return NotImplemented
