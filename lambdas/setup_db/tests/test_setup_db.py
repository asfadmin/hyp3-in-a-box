# test_setup_db.py
# Rohan Weeden
# Created: June 14, 2018

# Test cases for seting up the database

import pytest
from hyp3_db import make_test_db
from hyp3_db.hyp3_models.base import Base


def test_create_all(*args):
    db = make_test_db()

    try:
        Base.metadata.drop_all(db.engine)
        Base.metadata.create_all(db.engine)
    except Exception as e:
        pytest.fail("Error Raised: {}".format(str(e)))
