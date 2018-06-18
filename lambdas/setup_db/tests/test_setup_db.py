# test_setup_db.py
# Rohan Weeden
# Created: June 14, 2018

# Test cases for seting up the database

import import_setup_db

from unittest import TestCase

from hyp3_db import make_test_db
from hyp3_db.hyp3_models.base import Base
from init_db import setup_db


class TestSetupDb(TestCase):
    def setUp(self):
        self.db = make_test_db()
        Base.metadata.drop_all(self.db.engine)
        self.db.engine.execute(
            "REVOKE ALL PRIVILEGES ON DATABASE hyp3db FROM hyp3_user"
        )
        self.db.engine.execute("DROP USER hyp3_user")

    def test_lambda_function(self):
        setup_db(self.db)
