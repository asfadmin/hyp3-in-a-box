class Envirnoment:
    """Envirnoment variables for the troposphere templates"""
    def __init__(self):
        self.lambda_bucket = "hyp3-in-a-box-source"
        self.is_production = True

    def maturity(self):
        return "prod" if self.is_production else "test"

    def get_variables(self):
        return [
            ("is_production", bool),
            ("lambda_bucket", str)
        ]


envirnoment = Envirnoment()