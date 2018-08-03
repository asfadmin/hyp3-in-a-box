import contextlib
import pathlib as pl
import json

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


@mock.patch('products.products.get_bucket')
@mock.patch('asf_granule_util.download', side_effect=mock_download)
@mock.patch('hyp3_process.working_directory.create')
def test_rtc_snap_mocked(
        wrk_dir_mock,
        download_mock,
        bucket_mock,
        rtc_snap_fake_script,
        make_working_dir
):
    working_dir = make_working_dir(strats.rtc_example_files())

    wrk_dir_mock.side_effect = mock_working_dir_with(working_dir)

    resp = hyp3_process.hyp3_handler(rtc_snap_fake_script, {})

    download_mock.assert_called_once()
    assert 'product_url' in resp


@pytest.mark.rtc_snap_run
def test_full_rtc_snap(rtc_snap_full, earthdata_creds):
    print('running rtc_snap with processing')
    resp = hyp3_process.hyp3_handler(rtc_snap_full)

    assert 'product_url' in resp


@pytest.fixture()
def rtc_snap_full():
    return rtc_job_with_script_path(
        str(
            pl.Path(__file__).parent /
            './../build/hyp3-rtc-snap/src/procSentinelRTC-3.py'
        )
    )


@pytest.fixture()
def earthdata_creds():
    path = pl.Path(__file__).parent / 'earthdata-creds.json'

    with path.open('r') as f:
        return json.load(f)


@pytest.fixture()
def rtc_snap_fake_script():
    return rtc_job_with_script_path(
        str(pl.Path(__file__).parent / 'fake-rtc-script.py')
    )


def rtc_job_with_script_path(path):
    return hyp3_events.RTCSnapJob(
        granule=('S1A_IW_GRDH_1SDV_20180801T155817'
                 '_20180801T155842_023055_0280C4_749A'),
        address='test@email.com',
        username='test-user',
        subscription='test-subscription',
        output_patterns={
            'archive': ["*/*_TC_G??.tif", "*/*.png", "*/*.txt"],
            'browse': '*/*GVV.png'
        },
        script_path=path
    )


def mock_working_dir_with(mock_directory):
    @contextlib.contextmanager
    def mock_create(*args, **kwargs):
        yield mock_directory

    return mock_create
