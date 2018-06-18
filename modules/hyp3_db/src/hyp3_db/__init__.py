from .hyp3_db import Hyp3DB
from . import hyp3_models


def make_test_db(db="hyp3db"):
    return Hyp3DB(
        host="unit-testing.cxpvv5ynyjaw.us-west-2.rds.amazonaws.com",
        user="unittest",
        password="unittestpass",
        db=db
    )


__all__ = ['Hyp3DB', 'hyp3_models', 'make_test_db']
