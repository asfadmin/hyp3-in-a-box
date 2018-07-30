import contextlib
import pathlib as pl
import random
import string
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
    name = '{}-GRAN-{}'.format(_random_str(4), granule_id)

    return pl.Path.home() / 'jobs' / name


def _random_str(N):
    choices = string.ascii_uppercase + string.digits

    return ''.join(
        random.SystemRandom().choice(choices) for _ in range(N)
    )
