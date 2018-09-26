import contextlib
import pathlib as pl
from typing import Dict

import mock
import pytest

import import_hyp3_process
import rtc_snap_strategies as strats
from hyp3_process import process


def mock_rtc_script_path():
    return pl.Path(__file__).parent / 'fake-rtc-script.py'


def mock_download(*args, **kwargs):
    granule = args[0]
    dl_dir = pl.Path(kwargs['directory'])

    for suffix in ['.zip', '.SAFE']:
        fname = str(granule) + suffix

        (dl_dir / fname).mkdir(parents=True)


@mock.patch('hyp3_process.handler.products.products.get_bucket')
@mock.patch('hyp3_process.handler.working_directory.create')
@mock.patch('hyp3_process.handler.products.products.get_object_url')
def test_hyp3_process(
        s3_client_mock,
        wrk_dir_mock,
        bucket_mock,
        rtc_snap_job,
        make_working_dir,
        dummy_handler
):
    working_dir = make_working_dir(strats.rtc_example_files())
    wrk_dir_mock.side_effect = mock_working_dir_with(working_dir)

    process = Process(handler_function=dummy_handler)

    resp = process.start(
        job=rtc_snap_job,
        earthdata_creds={},
        product_bucket=''
    )

    assert all([
        'product_url' in resp,
        'browse_url' in resp
    ])


@pytest.fixture
def dummy_handler():
    def handler(
        granule_name: str,
        working_dir: str,
        earthdata_creds: Dict[str, str]
    ) -> None:
        output_files = ['test.txt', 'browse.png']
        wrk_dir = pl.Path(working_dir)

        for ofile in output_files:
            with (wrk_dir / ofile).open('w') as f:
                f.write('test')

        print('hyp3 processing code goes here!')

    return handler


def mock_working_dir_with(mock_directory):
    @contextlib.contextmanager
    def mock_create(*args, **kwargs):
        yield mock_directory

    return mock_create
