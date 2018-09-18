import json
import pathlib as pl

import boto3
import pytest

import hyp3_events

import import_hyp3_process
from hyp3_process.daemon import HyP3Worker


@pytest.fixture
def worker(creds, bucket, handler):
    return HyP3Worker(
        handler=handler,
        creds=creds,
        bucket=bucket
    )


@pytest.fixture
def creds():
    return json.dumps({
        "username": "fake-user",
        "password": "fake-pass"
    })


@pytest.fixture
def bucket():
    return 'products-bucket'


@pytest.fixture
def handler():
    def handler_func(start_event, earthdata_creds, products_bucket):
        return {'browse_url': 'some-url', 'product_url': 'some-url'}

    return handler_func


@pytest.fixture
def rtc_snap_job():
    return hyp3_events.StartEvent(
        granule=('S1A_WV_OCN__2SSV_20180805T042601'
                 '_20180805T043210_023106_028262_4799'),
        user_id=80,
        sub_id=80,
        additional_info=[],
        output_patterns={
            'archive': ["*.txt"],
            'browse': '*.png'
        },
        script_path='/users/script/path/here'
    )


@pytest.fixture()
def make_working_dir(tmpdir):
    working_dir = tmpdir

    def make_working_dir(file_paths):
        create_output_files(
            file_paths,
            working_dir
        )

        return str(working_dir)

    return make_working_dir


def create_output_files(output_paths, working_dir):
    for p in output_paths:
        full_path = pl.Path(working_dir) / p

        write_sample_file(full_path)


def write_sample_file(path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open('w') as f:
        f.write('test')
