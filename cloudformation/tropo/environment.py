class Environment:
    """Environment variables for the troposphere templates"""

    def __init__(self):
        self.lambda_bucket = "asf-hyp3-in-a-box-source"
        self.eb_bucket = "asf-hyp3-in-a-box-source"
        self.maturity = "test"

    def maturity(self):
        return self.maturity

    def get_variables(self):
        return [
            (k, type(v)) for k, v in self.__dict__.items()
        ]


environment = Environment()
