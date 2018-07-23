# test_setup_db.py
# Rohan Weeden, William Horn
# Created: June 14, 2018

# Test cases for seting up the database

import pathlib as pl
import json

import mock
import hyp3_db
from hyp3_db import hyp3_models

import import_setup_db
from init_db import setup_db

TESTING_USER = 'hyp3_user'
TESTING_DB = 'setup_db_testing_db'


@mock.patch('setup_db_utils.os.environ')
@mock.patch(
    'init_db.hyp3_db.connect',
    side_effect=hyp3_db.test_db
)
def test_custom_resource_wrapper(dbmock, environ_mock):
    reset_hyp3_db()

    env = get_mock_environment()
    environ_mock.__getitem__.side_effect = env.__getitem__
    environ_mock.get.side_effect = env.get

    setup_db(load_json_from('data/sample_event.json'), [TESTING_DB])

    with hyp3_db.test_db(db=TESTING_DB) as db:
        check_new_user(db, env)
        check_processes(db, env)

    check_setup_db_still_works()


def check_new_user(db, mock_env):
    user = db.session.query(hyp3_models.User).one()

    assert user.email == mock_env['Hyp3AdminEmail']
    assert user.username == mock_env['Hyp3AdminUsername']


def check_processes(db, mock_env):
    notify_only = db.session.query(hyp3_models.Process).one()

    assert notify_only.name == 'Notify Only'


def check_setup_db_still_works():
    setup_db(load_json_from('data/sample_event.json'), [TESTING_DB])


def reset_hyp3_db():
    with hyp3_db.test_db(db='postgres') as admindb:
        admindb.session.connection().connection.set_isolation_level(0)
        admindb.session.execute(f"DROP DATABASE {TESTING_DB};")
        admindb.session.execute(f"CREATE DATABASE {TESTING_DB};")
        admindb.session.execute(f"DROP USER IF EXISTS {TESTING_USER};")
        admindb.session.connection().connection.set_isolation_level(1)


def get_mock_environment():
    process_cfg = load_json_from('../../../processes/.config.json')

    return {
        'Hyp3DBUser': TESTING_USER,
        'Hyp3DBName': TESTING_DB,

        'Hyp3DBPass': 'testingpassword',
        'Hyp3AdminUsername': 'testuser',
        'Hyp3AdminEmail': 'test@alaska.edu',

        'DefaultProcessesBucket': process_cfg["processes_bucket"],
        'DefaultProcessesKey': process_cfg["default_processes_key"],

        'Maturity': 'test',

        'Hyp3StackName': 'unittesting-hyp3-in-a-box-stack'
    }


def load_json_from(rel_path_str):
    p = get_file_path() / rel_path_str

    with p.open('r') as f:
        return json.load(f)


def get_file_path():
    return pl.Path(__file__).parent
