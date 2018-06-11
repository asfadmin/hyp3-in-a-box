class Environment:
    def __init__(self):
        self.db_creds = {
            'host': 'some-url',
            'user': 'hyp3',
            'pass': 'db pass here'
        }

    def get_db_creds(self):
        return [
            self.db_creds[k] for k in ['host', 'user', 'pass']
        ]

    def set_db_creds(self, creds):
        self.db_creds = creds


environment = Environment()
