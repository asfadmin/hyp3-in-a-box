import pathlib as pl

import boto3
import pytest


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


def pytest_addoption(parser):
    parser.addoption(
        "--full-rtc-snap", action="store_true",
        default=False, help="Full rtc-snap-runthrough"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--full-rtc-snap"):
        return

    skip_rtc_runthrough = pytest.mark.skip(
        reason="need --full-rtc-snap option to run"
    )
    for item in items:
        if "rtc_snap_run" in item.keywords:
            item.add_marker(skip_rtc_runthrough)
