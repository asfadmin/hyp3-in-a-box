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
    path = working_dir_path(granule.unique_id)

    path.mkdir(parents=True)

    return str(path)


def _teardown(directory):
    shutil.rmtree(directory)


def working_dir_path(granule_id):
    name = '{}-GRAN-{}'.format(random_str(4), granule_id)

    return pl.Path.home() / 'jobs' / name


def random_str(N):
    choices = string.ascii_uppercase + string.digits

    return ''.join(
        random.SystemRandom().choice(choices) for _ in range(N)
    )
