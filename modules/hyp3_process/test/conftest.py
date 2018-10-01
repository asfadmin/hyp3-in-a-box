import json
import pathlib as pl

import boto3
import pytest
import asf_granule_util as gu

import hyp3_events
from tempaws import TemporaryBucket

import import_hyp3_process
from hyp3_process.daemon import HyP3Worker


@pytest.fixture
def worker(creds, bucket, processing_func):
    return HyP3Worker(
        processing_func=processing_func,
        creds=creds,
        bucket=bucket
    )


@pytest.fixture
def creds():
    return {
        "username": "fake-user",
        "password": "fake-pass"
    }


@pytest.fixture(scope='session')
def bucket():
    with TemporaryBucket.create() as bucket:
        yield bucket.name


@pytest.fixture
def handler_func():
    def h(granule, creds):
        assert gu.SentinelGranule(granule), creds
        assert set(creds.keys()) == set(['username', 'password'])

        browse_path = pl.Path.cwd() / 'test.png'
        browse_path.touch()
        print('path', browse_path)

    return h


@pytest.fixture
def processing_func():
    def processing_func(*args, **kwargs):
        print('fake processing function')

        return {"browse_url": "", "product_url": ""}

    return processing_func


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
            'browse': ['*.png']
        }
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
