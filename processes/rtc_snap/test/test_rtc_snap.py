import contextlib
import pathlib as pl

import pytest
import mock

import hyp3_events

import rtc_snap_strategies as strats
import import_rtc_snap
import hyp3_process


def mock_rtc_script_path():
    return pl.Path(__file__).parent / 'fake-rtc-script.py'


def mock_download(*args, **kwargs):
    granule = args[0]
    dl_dir = pl.Path(kwargs['directory'])

    for suffix in ['.zip', '.SAFE']:
        fname = str(granule) + suffix

        (dl_dir / fname).mkdir(parents=True)


@mock.patch('hyp3_process.get_bucket_name')
@mock.patch('rtc_snap.script_path', side_effect=mock_rtc_script_path)
@mock.patch('asf_granule_util.download', side_effect=mock_download)
@mock.patch('working_directory.create')
def test_rtc_snap_mocked(
        wrk_dir_mock,
        download_mock,
        rtc_script_mock,
        bucket_name_mock,
        testing_bucket,
        rtc_snap_job,
        make_working_dir
):
    working_dir = make_working_dir(strats.rtc_example_files())

    bucket_name_mock.side_effect = lambda: testing_bucket
    wrk_dir_mock.side_effect = mock_working_dir_with(working_dir)

    resp = hyp3_process.hyp3_handler(rtc_snap_job)

    download_mock.assert_called_once()
    assert 'product_url' in resp


@pytest.mark.rtc_snap_run
def test_full_rtc_snap(rtc_snap_job):
    print('running rtc_snap with processing')
    resp = hyp3_process.hyp3_handler(rtc_snap_job)

    assert 'product_url' in resp


@pytest.fixture()
def rtc_snap_job():
    return hyp3_events.RTCSnapJob(
        granule=('S1B_IW_GRDH_1SDV_20170813T033816'
                 '_20170813T033849_006916_00C2DD_1FC1'),
        address='test@email.com',
        username='test-user',
        subscription='test-subscription',
        output_patterns={
            'archive': ["*/*_TC_G??.tif", "*/*.png", "*/*.txt"],
            'browse': '*/*GVV.png'
        }
    )


def mock_working_dir_with(mock_directory):
    @contextlib.contextmanager
    def mock_create(*args, **kwargs):
        yield mock_directory

    return mock_create
