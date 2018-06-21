from .session import make_engine, make_session
import contextlib


@contextlib.contextmanager
def connect(host, user, password, db='hyp3db'):
    db = Hyp3DB(host, user, password, db)
    yield db
    db.close()


class Hyp3DB:
    """ Handles a connection to the hyp3 database."""
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
        """
            :param str host: host database url
            :param str user: database username
            :param str password: database password
            :param str db:  name of the database
        """
        self.engine = make_engine(
            user=user,
            password=password,
            host=host,
            db=db
        )

        self.session = make_session(self.engine)

    def close(self):
        """ Close the db session"""
        self.session.close()
