class Environment:
    """ Configure global pramas for the lambda"""
    def __init__(self):
        self.maturity = 'test'
        self.bucket = 'hyp3-in-a-box'
        self.scheduler_lambda = 'hyp3-scheduler-lambda'
        self.ssm_previous_time_name = None


environment = Environment()
