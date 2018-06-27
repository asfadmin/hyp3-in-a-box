# test_setup_db.py
# Rohan Weeden, William Horn
# Created: June 14, 2018

# Test cases for seting up the database

import mock

import import_setup_db

import hyp3_db
from init_db import setup_db_main


@mock.patch(
    'init_db.os.environ',
)
def test_lambda_function(environ_mock):
    d = {
        'Hyp3DBUser': 'unittest',
        'Hyp3DBName': 'hyp3db',
        'Hyp3DBPass': 'unittestpass'
    }
    environ_mock.__getitem__.side_effect = d.__getitem__

    setup_db_for_test()

    with hyp3_db.test_db() as db:
        setup_db_main(db)


def setup_db_for_test():
    with hyp3_db.test_db(db='postgres') as admindb:
        admindb.session.connection().connection.set_isolation_level(0)
        admindb.session.execute("DROP DATABASE hyp3db;")
        admindb.session.execute("CREATE DATABASE hyp3db;")
        admindb.session.execute("DROP USER IF EXISTS hyp3_user;")
        admindb.session.connection().connection.set_isolation_level(1)
