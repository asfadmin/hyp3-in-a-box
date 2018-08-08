class Environment:
    def __init__(self):
        self.db_creds = [
            'db host',
            'db user',
            'db pass',
            'db name'
        ]

        self.sns_arn = None
        self.queue_url = None
        self.maturity = 'test'


environment = Environment()
