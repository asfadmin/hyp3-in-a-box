import import_rtc_snap

import contextlib
import pathlib as pl

import asf_granule_util as gu
import hyp3_events
import hyp3_process
import mock
import pytest
import rtc_snap_strategies as strats


def mock_rtc_script_path():
    return pl.Path(__file__).parent / 'fake-rtc-script.py'


def mock_download(*args, **kwargs):
    granule = args[0]
    dl_dir = pl.Path(kwargs['directory'])

    for suffix in ['.zip', '.SAFE']:
        fname = str(granule) + suffix

        (dl_dir / fname).mkdir(parents=True)


@mock.patch('hyp3_process.products.products.get_bucket')
@mock.patch('asf_granule_util.download', side_effect=mock_download)
@mock.patch('hyp3_process.working_directory.create')
def test_rtc_snap_mocked(
        wrk_dir_mock,
        download_mock,
        bucket_mock,
        rtc_snap_job,
        make_working_dir
):
    working_dir = make_working_dir(strats.rtc_example_files())
    wrk_dir_mock.side_effect = mock_working_dir_with(working_dir)

    @hyp3_process.hyp3_handler
    def process(granule_name: str, working_dir: str, script_path: str) -> None:
        print('hyp3 processing code goes here!')

    resp = process(rtc_snap_job, {'fake': 'creds'}, 'some-s3-bucket')

    dl_call = download_mock.mock_calls[0]
    assert download_has_valid_params(dl_call, rtc_snap_job)

    assert all([
        'product_url' in resp,
        'browse_url' in resp
    ])


def download_has_valid_params(dl_call, job):
    (dl_granule, creds), kwargs = dl_call[1:3]
    expected_granule = gu.SentinelGranule(job.granule)

    return all([
        expected_granule == dl_granule,
        creds == {'fake': 'creds'},
        'directory' in kwargs
    ])


@pytest.fixture
def rtc_snap_job():
    return hyp3_events.RTCSnapJob(
        granule='S1A_WV_OCN__2SSV_20180805T042601_20180805T043210_023106_028262_4799',
        address='test@email.com',
        username='test',
        subscription='test',
        output_patterns={
            'archive': ["output.*.files"],
            'browse': '*.for.finding.png.*'
        },
        script_path='/users/script/path/here'
    )


def mock_working_dir_with(mock_directory):
    @contextlib.contextmanager
    def mock_create(*args, **kwargs):
        yield mock_directory

    return mock_create
