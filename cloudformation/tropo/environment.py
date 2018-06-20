class Environment:
    """Environment variables for the troposphere templates"""

    def __init__(self):
        self.lambda_bucket = "asf-hyp3-in-a-box-source"
        self.eb_bucket = "asf-hyp3-in-a-box-source"
        self.maturity = "test"

        self.find_new_granules_version = None
        self.send_email_version = None
        self.scheduler_version = None
        self.setup_db_version = None

        self.db_host = ""

    def get_variables(self):
        return [
            (k, get_var_type(v))
            for k, v in self.__dict__.items()
        ]


def get_var_type(v):
    return type(v) if v is not None else str


environment = Environment()
