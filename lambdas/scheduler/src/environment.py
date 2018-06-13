class Environment:
    def __init__(self):
        self.db_creds = [
            'db host',
            'db user',
            'db pass'
        ]

        self.sns_arn = \
            'arn:aws:sns:us-west-2:765666652335:hyp3_finish_events_test'
        self.maturity = 'test'

    def get_db_creds(self):
        return self.db_creds

    def set_db_creds(self, creds):
        self.db_creds = creds


environment = Environment()
