class Environment:
    def __init__(self):
        self.db_creds = [
            'db host',
            'db user',
            'db pass',
            'db name'
        ]

        self.sns_arn = \
            'arn:aws:sns:us-west-2:765666652335:hyp3_finish_events_test'
        self.maturity = 'test'


environment = Environment()
