class Environment:
    def __init__(self):
        self.db_creds = [
            'db host',
            'db user',
            'db pass'
        ]

    def get_db_creds(self):
        return self.db_creds

    def set_db_creds(self, creds):
        self.db_creds = creds


environment = Environment()
