import json
import pathlib as pl


def get_testing_base_path():
    return pl.Path(__file__).parent


def get_data_path():
    return get_testing_base_path() / 'data'


def load_testing_polys():
    path = pl.Path(__file__).parent / 'data/granule-polys.json'

    with path.open('r') as f:
        return json.load(f)
