"""
This module is to handle connecting and making queries with the
hyp3 database. Is is a wrapper around sqlalchemy session object
and mainly handles connecting to the database.
"""
import contextlib

from .hyp3_db import HyP3DB, connect, connect_using_environment_variables
from . import hyp3_models


@contextlib.contextmanager
def test_db(db='hyp3db', commit_on_close=False):
    """ Connect to the hyp3 unittesting database

        :param str db: name of the database to make

        :returns: connection to the hyp3_db database
        :rtype: hyp3_db.HyP3DB
    """
    creds = testing_creds(db)

    db = HyP3DB(**creds)
    try:
        yield db
    except Exception as e:
        raise e
    finally:
        if commit_on_close:
            db.commit_and_close()
        else:
            db.close()


def testing_creds(db):
    return {
        "host": "unit-test.cvlquwxeogjj.us-east-1.rds.amazonaws.com",
        "user": "unittest",
        "password": "unittestpass",
        "db": db
    }


__all__ = [
    'HyP3DB', 'connect',
    'connect_using_environment_variables', 'hyp3_models',
    'test_db', 'testing_creds'
]
