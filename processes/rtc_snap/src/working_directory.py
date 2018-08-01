import contextlib
import pathlib as pl
import shutil


@contextlib.contextmanager
def create(granule):
    working_dir = _setup(granule)
    yield working_dir
    _teardown(working_dir)


def _setup(granule):
    path = _working_dir_path(granule.unique_id)

    _make(path)

    return str(path)


def _make(path):
    path.mkdir(parents=True)


def _teardown(directory):
    shutil.rmtree(directory)


def _working_dir_path(granule_id):
    name = 'GRAN-{}'.format(granule_id)

    return pl.Path.home() / 'jobs' / name
