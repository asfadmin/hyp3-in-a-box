import json
import pathlib as pl


class Environment:
    """Environment variables for the troposphere templates"""

    def __init__(self):
        self.lambda_bucket = "asf-hyp3-in-a-box-source"
        self.eb_bucket = "asf-hyp3-in-a-box-source"

        self.eb_solution_stack_name = \
            "64bit Amazon Linux 2018.03 v2.7.1 running Python 3.6"

        process_cfg = load_process_cfg()
        self.hyp3_data_bucket = process_cfg['processes_bucket']
        self.default_processes_key = process_cfg['default_processes_key']

        self.maturity = "test"

        self.set_lambda_version_variables()
        self.hyp3_api_source_zip = "hyp3_api.zip"

        self.use_name_parameters = True
        self.should_create_db = True

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
