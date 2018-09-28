class Environment:
    def __init__(self):
        self.db_creds = [
            'db host',
            'db user',
            'db pass',
            'db name'
        ]

        #TODO this needs to be set for the scheduler to send the event data to the right AWS lambda
        self.dispatch_lambda = None
        self.maturity = 'test'


environment = Environment()
