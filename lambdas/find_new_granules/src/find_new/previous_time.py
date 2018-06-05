from . import s3
import json
import datetime as dt
import pathlib as pl


TIME_FILE_PATH = str(pl.Path(__file__).parent / 'previous-time.find-new.json')


def get():
    """Get the last time the find_new lambda was executed.

        :returns: datetime.datetime
    """
    s3.download(TIME_FILE_PATH)

    with open(TIME_FILE_PATH, 'r') as f:
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

    with open(TIME_FILE_PATH, 'w') as f:
        json.dump(update_runtime, f)

    s3.upload(TIME_FILE_PATH)
