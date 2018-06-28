import json
import pathlib as pl


class Environment:
    """Environment variables for the troposphere templates"""

    def __init__(self):
        self.lambda_bucket = "asf-hyp3-in-a-box-source"
        self.eb_bucket = "asf-hyp3-in-a-box-source"

        process_cfg = load_process_cfg()
        self.hyp3_data_bucket = process_cfg['processes_bucket']
        self.default_processes_key = process_cfg['default_processes_key']

        self.maturity = "test"

        self.find_new_granules_version = None
        self.send_email_version = None
        self.scheduler_version = None
        self.setup_db_version = None

        self.use_name_parameters = True
        self.should_create_db = True

    def get_variables(self):
        return [
            (k, get_var_type(v))
            for k, v in self.__dict__.items()
        ]


def load_process_cfg():
    path = pl.Path(__file__).parent / '../../processes/.config.json'

    with path.open('r') as f:
        return json.load(f)


def get_var_type(v):
    return type(v) if v is not None else str


environment = Environment()
