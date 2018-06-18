# test_setup_db.py
# Rohan Weeden
# Created: June 14, 2018

# Test cases for seting up the database

import import_setup_db

from unittest import TestCase

from hyp3_db import make_test_db
from setup_db import setup_db


class TestSetupDb(TestCase):

    def setUp(self):
        admindb = make_test_db(db="postgres")
        admindb.session.connection().connection.set_isolation_level(0)
        admindb.session.execute("DROP DATABASE hyp3db;")
        admindb.session.execute("CREATE DATABASE hyp3db;")
        admindb.session.execute("DROP USER IF EXISTS hyp3_user;")
        admindb.session.connection().connection.set_isolation_level(1)
        self.db = make_test_db()

    def test_lambda_function(self):
        setup_db(self.db)
