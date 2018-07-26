import pytest
import mock

import hyp3_events

import import_rtc_snap
import hyp3_process


@mock.patch('asf_granule_util.download')
@mock.patch('working_directory.setup', side_effect=lambda g: 'tmpdir')
def test_rtc_snap(download_mock, wrk_dir_mock, rtc_snap_job):
    resp = hyp3_process.hyp3_handler(rtc_snap_job)

    download_mock.assert_called_once()
    assert 'product_link' in resp


@pytest.fixture()
def rtc_snap_job():
    return hyp3_events.RTCSnapJob(
        granule=('S1B_IW_GRDH_1SDV_20170813T033816'
                 '_20170813T033849_006916_00C2DD_1FC1'),
        address='test@email.com',
        username='test-user',
        subscription='test-subscription',
        output_file_patterns=[
            "*_TC_G??.tif", "*.png", "*.txt"
        ]
    )
