class Envirnoment:
    """Envirnoment variables for the troposphere templates"""
    def __init__(self):
        self.lambda_bucket = "hyp3-in-a-box-source"
        self.maturity = "test"

    def maturity(self):
        return self.maturity

    def get_variables(self):
        return [
            ("maturity", str),
            ("lambda_bucket", str)
        ]


envirnoment = Envirnoment()
