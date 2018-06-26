import json
import pathlib as pl

from troposphere.awslambda import Code


def get_map(name):
    return load_json_from('maps', name)


def get_static_policy(name):
    static_policy = load_json_from('policies', name)

    return static_policy


def load_json_from(directory, name):
    file_path, file_name = pl.Path(__file__).parent, name + '.json'

    path = file_path / directory / file_name

    with path.open('r') as f:
        loaded_json = json.load(f)

    return loaded_json


def get_lambda_function(name):
    func_path = pl.Path(__file__).parent / 'functions' / '{}.py'.format(name)

    with func_path.open('r') as f:
        return f.read().strip().split('\n')


def make_lambda_code(**kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    return Code(**kwargs)
