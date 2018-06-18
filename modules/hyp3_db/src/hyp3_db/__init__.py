"""
This module is to handle connecting and making queries with the
hyp3 database. Is is a wrapper around sqlalchemy session object
and mainly handles connecting to the database.
"""
from .hyp3_db import Hyp3DB
from . import hyp3_models


def make_test_db():
    """ Connect to the hyp3 unittesting database

        :returns: connection to the hyp3_db database
        :rtype: hyp3_db.Hyp3DB
    """
    return Hyp3DB(
        host="unit-testing.cxpvv5ynyjaw.us-west-2.rds.amazonaws.com",
        user="unittest",
        password="unittestpass"
    )


__all__ = ['Hyp3DB', 'hyp3_models', 'make_test_db']
