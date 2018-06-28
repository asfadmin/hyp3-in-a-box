# test_setup_db.py
# Rohan Weeden, William Horn
# Created: June 14, 2018

# Test cases for seting up the database

import mock
import pathlib as pl
import json

import import_setup_db

import hyp3_db
from init_db import setup_db_main, setup_db

testing_user = 'hyp3_user'


@mock.patch('init_db.os.environ')
@mock.patch(
    'init_db.hyp3_db.connect',
    side_effect=hyp3_db.test_db
)
def test_custom_resource_wrapper(dbmock, environ_mock):
    setup_db_for_test()
    d = {
        'Hyp3DBUser': testing_user,
        'Hyp3DBName': 'hyp3db',
        'Hyp3DBPass': 'testingpassword'
    }
    environ_mock.__getitem__.side_effect = d.__getitem__
    e = get_sample_event()

    setup_db(e, ['hyp3db'])


def setup_db_for_test():
    with hyp3_db.test_db(db='postgres') as admindb:
        admindb.session.connection().connection.set_isolation_level(0)
        admindb.session.execute("DROP DATABASE hyp3db;")
        admindb.session.execute("CREATE DATABASE hyp3db;")
        admindb.session.execute(f"DROP USER IF EXISTS {testing_user};")
        admindb.session.connection().connection.set_isolation_level(1)


def get_sample_event():
    path = pl.Path(__file__).parent / 'data' / 'sample_event.json'

    with path.open('r') as f:
        return json.load(f)
