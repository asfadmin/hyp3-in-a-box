import requests
import datetime as dt
import json

API_URL = 'https://cmr.earthdata.nasa.gov/search/granules.json'


def get_new():
    time_to_check = get_time_to_check()

    # https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html#g-created-at
    ret = requests.get(API_URL, params={
        'provider': 'ASF',
        'page_size': '5',
        'created_at[]': [time_to_check]
    })
    print(ret.url)

    data = ret.json()
    results = data['feed']['entry']

    print(len(results))

    with open('cached/output.json', 'w') as f:
        json.dump(data, f, indent=2)


def get_time_to_check():
    lookback_amount = dt.timedelta(minutes=5)
    to_check = dt.datetime.now() - lookback_amount

    return to_check.strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == "__main__":
    get_new()
