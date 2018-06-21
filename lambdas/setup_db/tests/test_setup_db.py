# test_setup_db.py
# Rohan Weeden
# Created: June 14, 2018

# Test cases for seting up the database


import import_setup_db

import hyp3_db
from init_db import setup_db


def test_lambda_function(self):
    setup_db_for_test()

    with hyp3_db.test_db() as db:
        setup_db(db)


def setup_db_for_test():
    with hyp3_db.test_db(db='postgres') as admindb:
        admindb.session.connection().connection.set_isolation_level(0)
        admindb.session.execute("DROP DATABASE hyp3db;")
        admindb.session.execute("CREATE DATABASE hyp3db;")
        admindb.session.execute("DROP USER IF EXISTS hyp3_user;")
        admindb.session.connection().connection.set_isolation_level(1)
