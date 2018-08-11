import datetime as dt
import json

from . import find_new_ssm as ssm
from .find_new_env import environment


def get_time():
    """ Get the last time the find_new lambda was executed.

        :returns: previous lambda runtime
        :rtype: datetime.datetime
    """
    try:
        prev_state = json.loads(ssm.download(param_name()))
    except (ssm.ParamDoesntExist, json.decoder.JSONDecodeError):
        raise NotSet('need to set previous time before downloading')

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


def param_name():
    return environment.ssm_previous_time_name


class NotSet(Exception):
    pass
