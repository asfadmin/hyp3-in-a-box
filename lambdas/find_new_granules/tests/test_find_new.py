import datetime as dt

import mock
import hyp3_events

import import_find_new

import find_new_mocks
import find_new


find_new.environment.maturity = 'test'


@mock.patch(
    'find_new.find_new.granule_search.CMR.search',
    side_effect=find_new_mocks.asf_api_requests_get
)
def test_get_new(mock_get):
    request_time = dt.datetime.now()
    prev_time = request_time - dt.timedelta(minutes=5)

    granules = find_new.get_new_granules_between(prev_time, request_time)

    assert isinstance(granules, list)
    assert all(isinstance(e, hyp3_events.NewGranuleEvent) for e in granules)

    mock_get.assert_called()


@mock.patch(
    'find_new.find_new.get_new_granules_between',
    side_effect=find_new_mocks.asf_api_requests_get
)
@mock.patch(
    'find_new.s3.upload'
)
def test_s3_upload(mock_s3_upload, mock_find_new):
    find_new.granule_events()

    mock_s3_upload.assert_called_once()
    mock_find_new.assert_called_once()
