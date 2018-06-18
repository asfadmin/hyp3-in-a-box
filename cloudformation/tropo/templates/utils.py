import json
import pathlib as pl

from troposphere.awslambda import Code

from environment import environment


def get_map(name):
    return load_json_from('maps', name)


def get_static_policy(name, update_with={}):
    static_policy = load_json_from('policies', name)
    static_policy.update(update_with)

    return static_policy


def load_json_from(directory, name):
    file_path, file_name = pl.Path(__file__).parent, name + '.json'

    path = file_path / directory / file_name

    with path.open('r') as f:
        loaded_json = json.load(f)

    return loaded_json


def make_lambda_code(**kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    return Code(**kwargs)
