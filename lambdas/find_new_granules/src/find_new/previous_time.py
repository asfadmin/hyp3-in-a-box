import json
import datetime as dt
import pathlib as pl

from . import s3
from .environment import environment


def get():
    """Get the last time the find_new lambda was executed.

        :returns: previous lambda runtime
        :rtype: datetime.datetime
    """
    download_path = get_time_file_path()
    s3.download(download_path)

    with open(download_path, 'r') as f:
        prev_state = json.load(f)

    prev_timestamp = prev_state['previous']

    return dt.datetime.fromtimestamp(prev_timestamp)


def set(new_time):
    """Sets a timestamp representing the last time the find_new lambda was run.

        :param datetime.datetime new_time: runtime to set
    """
    update_runtime = {
        "previous": new_time.timestamp()
    }

    time_file_path = get_time_file_path()
    with open(time_file_path, 'w') as f:
        json.dump(update_runtime, f)

    s3.upload(time_file_path)


def get_time_file_path():
    key_name = get_s3_key_name()

    path = pl.Path('/tmp/') if environment.is_production \
        else pl.Path(__file__).parent

    return str(path / key_name)


def get_s3_key_name():
    materity = 'prod' if environment.is_production else 'test'

    return f'previous-time.{materity}.json'
