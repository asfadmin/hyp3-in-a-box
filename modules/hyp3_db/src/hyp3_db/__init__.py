"""
This module is to handle connecting and making queries with the
hyp3 database. Is is a wrapper around sqlalchemy session object
and mainly handles connecting to the database.
"""
import contextlib

from .hyp3_db import Hyp3DB, connect
from . import hyp3_models


@contextlib.contextmanager
def test_db(db="hyp3db"):
    """ Connect to the hyp3 unittesting database

        :param str db: name of the database to make

        :returns: connection to the hyp3_db database
        :rtype: hyp3_db.Hyp3DB
    """
    db = Hyp3DB(
        host="unit-testing.cxpvv5ynyjaw.us-west-2.rds.amazonaws.com",
        user="unittest",
        password="unittestpass",
        db=db
    )

    yield db
    db.close()


__all__ = ['Hyp3DB', 'connect', 'hyp3_models', 'test_db']
