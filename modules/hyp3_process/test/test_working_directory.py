import pathlib as pl

import asf_granule_util as gu
import pytest

import import_hyp3_process
from hyp3_process.handler import working_directory


LINK_DIR_TREE = {
    'files': [
        'handler.py',
        'test2.txt'
    ],
    'dirs': [
        'hyp3-lib',
        'hyp3-rtc-snap/src'
    ]
}


def test_working_directory(new_path, link_dir):
    with working_directory.create(new_path, link_dir) as wd:
        wd_path = pl.Path(wd)
        assert wd_path.exists()

        wd_files = list(wd_path.iterdir())
        assert len(wd_files) != 0

        assert all([
            (wd_path / f).is_file() for f in LINK_DIR_TREE['files']
        ])
        assert all([
            (wd_path / d).exists() for d in LINK_DIR_TREE['dirs']
        ])


def test_failed(new_path, link_dir):
    with pytest.raises(Exception):
        with working_directory.create(new_path, link_dir):
            raise Exception('Job Failed!')


@pytest.fixture
def new_path():
    cwd = pl.Path.home()

    return cwd / 'test-temp-working-dir'


@pytest.fixture
def link_dir(tmpdir):
    tmppath = pl.Path(tmpdir)
    for f in LINK_DIR_TREE['files']:
        (tmppath / f).touch()

    for d in LINK_DIR_TREE['dirs']:
        (tmppath / d).mkdir(parents=True)

    yield pl.Path(tmpdir)
