import pathlib as pl
import random
import string


def setup(granule):
    path = working_dir_path(granule.unique_id)

    path.mkdir(parents=True)

    return path


def working_dir_path(granule_id):
    name = '{}-GRAN-{}'.format(random_str(4), granule_id)

    return pl.Path.home() / 'jobs' / name


def random_str(N):
    choices = string.ascii_uppercase + string.digits

    return ''.join(
        random.SystemRandom().choice(choices) for _ in range(N)
    )
