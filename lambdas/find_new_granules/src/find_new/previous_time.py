import datetime as dt
import json
import pathlib as pl

from . import s3
from . import ssm
from .find_new_env import environment


def get_time():
    """ Get the last time the find_new lambda was executed.

        :returns: previous lambda runtime
        :rtype: datetime.datetime
    """
    prev_state = json.loads(ssm.download(param_name()))

    prev_timestamp = prev_state['previous']

    return dt.datetime.fromtimestamp(prev_timestamp)


def set_time(new_time):
    """ Sets a timestamp representing the last time the find_new lambda was run.

        :param datetime.datetime new_time: runtime to set
    """
    update_runtime = {
        "previous": new_time.timestamp()
    }

    ssm.upload(
        param_name(),
        json.dumps(update_runtime)
    )


def get_time_file_path():
    key_name = get_s3_key_name()

    path = pl.Path('/tmp/') if environment.maturity == 'prod' \
        else pl.Path(__file__).parent

    return str(path / key_name)


def get_s3_key_name():
    return 'previous-time.{}.json'.format(environment.maturity)


def param_name():
    return '/stack_name/previous-time.json'
