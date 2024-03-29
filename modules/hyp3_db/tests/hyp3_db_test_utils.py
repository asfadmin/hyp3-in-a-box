import json
import os
import pathlib as pl

import hyp3_db

DB_CONNECTION = {}


def creds_file_exists():
    creds_path = get_creds_path()

    return creds_path.is_file() or all(load_creds_from_env())


def get_creds_path():
    return pl.Path(__file__).parent / 'data' / 'creds.json'


def load_creds_from_env():
    return [
        os.environ.get(k, False) for k in ['DB_HOST', 'DB_USER', 'DB_PASS']
    ]


def load_creds():
    path = get_creds_path()

    if path.exists():
        return load_creds_from_path(path)

    return load_creds_from_env()


def load_creds_from_path(path):
    with path.open('r') as f:
        return json.load(f)
