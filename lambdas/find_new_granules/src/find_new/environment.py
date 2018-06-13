class Environment:
    """ Configure global pramas for the lambda"""
    def __init__(self):
        self.is_production = False
        self.bucket = 'hyp3-in-a-box-lambdas'
        self.scheduler_lambda = 'hyp3-scheduler-lambda'


environment = Environment()
