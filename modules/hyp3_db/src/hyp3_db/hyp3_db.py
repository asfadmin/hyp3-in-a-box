# hyp3_db.py

# Database wrappers

import contextlib
import os

from .session import make_engine, make_session


@contextlib.contextmanager
def connect_using_environment_variables(db='hyp3db', commit_on_close=False):
    (host, user, password) = (
        os.environ[k] for k in ['DB_HOST', 'DB_USER', 'DB_PASSWORD']
    )
    with connect(
        host, user, password,
        db=db, commit_on_close=commit_on_close
    ) as db_obj:
        yield db_obj


@contextlib.contextmanager
def connect(host, user, password, db='hyp3db', commit_on_close=False):
    db = HyP3DB(host, user, password, db)

    try:
        yield db
    except Exception as e:
        raise e
    finally:
        if commit_on_close:
            db.commit_and_close()
        else:
            db.close()


class HyP3DB:
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

    def commit_and_close(self):
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()
