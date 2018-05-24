import requests


def get_new():
    return requests.get('http://someurl.com/test.json').json()
