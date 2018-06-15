import datetime as dt
import mock

import import_find_new

import custom_mocks
from find_new import previous_time, environment as env

TESTING_TIME = dt.datetime(2017, 12, 6, 15, 29, 43, 79060)

env.maturity = 'test'


@mock.patch('find_new.previous_time.s3.upload')
def test_set_time(mock_upload):
    previous_time.set_time(TESTING_TIME)

    mock_upload.assert_called()


@mock.patch(
    'find_new.previous_time.s3.download',
    side_effect=custom_mocks.get_s3_download_func(time=TESTING_TIME)
)
def test_get_time(mock_download):
    t = previous_time.get_time()

    assert t == TESTING_TIME

    mock_download.assert_called()


def test_prod_file_name():
    env.maturity = 'prod'
    prod_file_path = previous_time.get_time_file_path()

    # only tmp directory is writable in aws lambdas
    assert prod_file_path == '/tmp/previous-time.prod.json'
