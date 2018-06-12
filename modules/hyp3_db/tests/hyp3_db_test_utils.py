import pytest
import json
import os
import pathlib as pl

from hyp3_db import Hyp3DB

DB_CONNECTION = {}


def creds_file_exists():
    creds_path = get_creds_path()

    return creds_path.is_file() or all(load_creds_from_env())


def get_creds_path():
    return pl.Path(__file__).parent / '..' / 'hyp3_db' / 'creds.json'


run_if_creds = pytest.mark.skipif(
    not creds_file_exists(),
    reason='Test requires database creds'
)


def with_db(func):
    def wrapper(*args, **kwargs):
        if 'connection' not in DB_CONNECTION:
            creds = load_creds()
            db = Hyp3DB(*creds)
            DB_CONNECTION['connection'] = db
        else:
            db = DB_CONNECTION['connection']
        func(db)

    return wrapper


def load_creds():
    path = get_creds_path()

    if path.exists():
        return load_creds_from_path(path)
    else:
        return load_creds_from_env


def load_creds_from_path(path):
    with path.open('r') as f:
        return json.load(f)


def load_creds_from_env():
    return [
        os.environ.get(k, False) for k in ['DB_HOST', 'DB_USER', 'DB_PASS']
    ]
