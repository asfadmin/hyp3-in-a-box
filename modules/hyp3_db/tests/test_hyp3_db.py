import pytest
import mock

import hyp3_db


def test_hyp3_db_test_connection():
    with hyp3_db.test_db() as db:
        assert db


def test_hyp3_db_connection(creds):
    with hyp3_db.connect(**creds) as db:
        assert db


@mock.patch('hyp3_db.hyp3_db.os.environ')
def test_hyp3_db_env_connection(environ_mock, environment):
    environ_mock.__getitem__.side_effect = environment.__getitem__
    environ_mock.get.side_effect = environment.get

    with hyp3_db.connect_using_environment_variables() as db:
        assert db


@pytest.fixture()
def creds():
    return hyp3_db.testing_creds('hyp3db')


@pytest.fixture()
def environment():
    creds = hyp3_db.testing_creds('hyp3db')

    return {
        'DB_HOST': creds['host'],
        'DB_USER': creds['user'],
        'DB_PASSWORD': creds['password']
    }
