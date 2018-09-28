class Environment:
    def __init__(self):
        self.db_creds = [
            'db host',
            'db user',
            'db pass',
            'db name'
        ]

        self.dispatcher_lambda = None
        self.maturity = 'test'


environment = Environment()
