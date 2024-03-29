import json
import pathlib as pl


class Environment:
    """Environment variables for the troposphere templates"""

    def __init__(self):
        self.source_bucket = "asf-hyp3-in-a-box-source"

        process_cfg = load_process_cfg()
        self.default_processes_key = process_cfg['default_processes_key']

        self.maturity = "test"
        self.release = None

        self.set_lambda_version_variables()

        self.use_name_parameters = True
        self.should_create_db = True

    def get_default_processes_key(self):
        if not self.release:
            return self.default_processes_key

        return "releases/{}/{}".format(self.release, self.default_processes_key)

    def get_variables(self):
        return [
            (k, get_var_type(v))
            for k, v in self.__dict__.items()
        ]

    def set_lambda_version_variables(self):
        for lambda_name in get_lambdas_names():
            setattr(self, '{}_version'.format(lambda_name), None)


def get_lambdas_names():
    path = pl.Path(__file__).parent / '../../lambdas/'

    return [
        d.name for d in path.iterdir()
        if is_lambda_directory(d)
    ]


def is_lambda_directory(d):
    return d.is_dir() and not d.name.startswith('.')


def load_process_cfg():
    path = pl.Path(__file__).parent / '../../processes/.config.json'

    with path.open('r') as f:
        return json.load(f)


def get_var_type(v):
    return type(v) if v is not None else str


environment = Environment()
