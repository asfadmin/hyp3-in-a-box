# test_setup_db.py
# Rohan Weeden, William Horn
# Created: June 14, 2018

# Test cases for seting up the database

import pathlib as pl
import json

import pytest
import mock
import hyp3_db
from hyp3_db import hyp3_models

import import_setup_db
from init_db import setup_db

TESTING_USER = 'hyp3'
TESTING_DB = 'e2e'
TESTING_PASSWORD = 'testingpassword'


@mock.patch('setup_db_utils.os.environ')
@mock.patch(
    'init_db.hyp3_db.connect',
    side_effect=hyp3_db.test_db
)
def test_setup_db(dbmock, environ_mock, event, environment):
    reset_hyp3_db()

    environ_mock.__getitem__.side_effect = environment.__getitem__
    environ_mock.get.side_effect = environment.get

    # Creds only need db name because call to
    # connect() is mocked with test_db()
    setup_db(
        event,
        [TESTING_DB],
        [TESTING_DB]
    )

    with hyp3_db.test_db(db=TESTING_DB) as db:
        check_new_user(db, environment)
        check_processes(db, environment)

    check_setup_db_still_works(event)


def check_new_user(db, mock_env):
    user = db.session.query(hyp3_models.User).one()

    assert user.email == mock_env['HyP3AdminEmail']
    assert user.username == mock_env['HyP3AdminUsername']


def check_processes(db, mock_env):
    processes = db.session.query(hyp3_models.Process).all()

    assert set(p.name for p in processes) == {'Notify Only', 'RTC Snap'}


def check_setup_db_still_works(sample_event):
    setup_db(sample_event,
             [TESTING_DB], [TESTING_DB])


def reset_hyp3_db():
    with hyp3_db.test_db(db='postgres') as admindb:
        admindb.session.connection().connection.set_isolation_level(0)
        admindb.session.execute(f"DROP DATABASE IF EXISTS {TESTING_DB};")
        admindb.session.execute(f"CREATE DATABASE {TESTING_DB};")
        admindb.session.execute(f"DROP USER IF EXISTS {TESTING_USER};")
        admindb.session.connection().connection.set_isolation_level(1)


@pytest.fixture()
def event():
    return load_json_from('data/sample_event.json')


@pytest.fixture()
def environment():
    process_cfg = load_json_from('../../../processes/.config.json')

    return {
        'HyP3DBUser': TESTING_USER,
        'HyP3DBName': TESTING_DB,
        'HyP3DBPass': TESTING_PASSWORD,

        'HyP3AdminUsername': 'testuser',
        'HyP3AdminEmail': 'test@alaska.edu',

        'DefaultProcessesBucket': 'asf-hyp3-in-a-box-source',
        'DefaultProcessesKey': process_cfg["default_processes_key"],

        'Maturity': 'test',

        'HyP3StackName': 'unittesting-hyp3-in-a-box-stack',
        'ParamNameHyP3Username': "HyP3ApiUsername",
        'ParamNameHyP3ApiKey': "HyP3ApiKey"
    }


def load_json_from(rel_path_str):
    p = get_file_path() / rel_path_str

    with p.open('r') as f:
        return json.load(f)


def get_file_path():
    return pl.Path(__file__).parent
