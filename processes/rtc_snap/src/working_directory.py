
import asf_granule_util as gu

import contextlib
import pathlib as pl
import shutil


@contextlib.contextmanager
def create(granule: gu.SentinelGranule):
    working_dir = _setup(granule)
    yield working_dir
    _teardown(working_dir)


def _setup(granule: gu.SentinelGranule) -> str:
    path = _working_dir_path(granule.unique_id)

    _make(path)

    return str(path)


def _make(path: pl.Path) -> None:
    path.mkdir(parents=True)


def _teardown(directory: str) -> None:
    shutil.rmtree(directory)


def _working_dir_path(granule_id: str) -> pl.Path:
    name = 'GRAN-{}'.format(granule_id)

    return pl.Path.home() / 'jobs' / name
