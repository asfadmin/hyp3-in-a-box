class Environment:
    """Configure global pramas for the lambda"""
    def __init__(self, is_production=False, bucket='hyp3-in-a-box-lambdas'):
        self.is_production = is_production
        self.bucket = bucket

    def set_is_production(self, val):
        """Sets if the lambda is running in production"""
        if not isinstance(val, bool):
            raise Exception('is_production can only be a boolean value')

        self.is_production = val

    def set_bucket(self, bucket):
        """Sets the s3 bucket to download from."""
        self.bucket = bucket


environment = Environment()
