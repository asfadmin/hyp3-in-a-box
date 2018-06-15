from .session import make_engine, make_session


class Hyp3DB:
    valid_job_status = [
        'INVALID',
        'INSERTED',
        'ERROR',
        'HOLD',
        'FAILED',
        'SUCCEEDED',
        'PROCESSING',
        'COMPLETE',
        'QUEUED',
        'CANCELLED'
    ]

    def __init__(self, host, user, password, db='hyp3db'):
        self.engine = make_engine(
            user=user,
            password=password,
            host=host,
            db=db
        )
        self.session = make_session(self.engine)
