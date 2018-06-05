import json
import datetime as dt
import pathlib as pl

from . import s3

IS_PRODUCTION = True


def get():
    """Get the last time the find_new lambda was executed.

        :returns: datetime.datetime
    """
    key_name, download_path = get_s3_key_name(), get_time_file_path()
    s3.download(key_name)

    with open(download_path, 'r') as f:
        prev_state = json.load(f)

    prev_timestamp = prev_state['previous']

    return dt.datetime.fromtimestamp(prev_timestamp)


def set(new_time):
    """Sets a timestamp representing the last time the find_new lambda
    was run.

        :param new_time: datetime.datetime

        :returns: s3.Object
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

    return str(pl.Path(__file__).parent / key_name)


def get_s3_key_name():
    materity = 'prod' if IS_PRODUCTION else 'test'

    return 'previous-time.{}.json'.format(materity)
