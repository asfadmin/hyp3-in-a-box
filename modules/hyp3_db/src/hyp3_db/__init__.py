from .hyp3_db import Hyp3DB
from . import hyp3_models


def make_test_db():
    return Hyp3DB(
        host="unit-testing.cxpvv5ynyjaw.us-west-2.rds.amazonaws.com",
        user="unittest",
        password="unittestpass"
    )


__all__ = ['Hyp3DB', 'hyp3_models', 'make_test_db']
