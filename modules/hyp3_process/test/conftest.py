import pathlib as pl

import boto3
import pytest

import hyp3_events


@pytest.fixture
def event_in_queue(rtc_snap_job):
    pass


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
