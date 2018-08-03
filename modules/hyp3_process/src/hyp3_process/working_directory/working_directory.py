
import asf_granule_util as gu

import contextlib
import pathlib as pl
import shutil


@contextlib.contextmanager
def create(granule: gu.SentinelGranule):
    working_dir = _setup(granule)

    try:
        yield working_dir
    except Exception as e:
        _save_failed(working_dir)

        raise e from None
    else:
        _teardown(working_dir)


def _setup(granule: gu.SentinelGranule) -> str:
    path = _working_dir_path(granule.unique_id)

    _make(path)

    return str(path)


def _make(path: pl.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _teardown(directory: str) -> None:
    shutil.rmtree(directory)


def _save_failed(directory: str) -> None:
    failed_dir = pl.Path.home() / 'failed-jobs' / pl.Path(directory).name

    _move(directory, str(failed_dir))


def _move(src, dst):
    shutil.move(src, dst)


def _working_dir_path(granule_id: str) -> pl.Path:
    name = _working_dir_name(granule_id)

    return pl.Path.home() / 'jobs' / name


def _working_dir_name(granule_id: str) -> str:
    return 'GRAN-{}'.format(granule_id)
