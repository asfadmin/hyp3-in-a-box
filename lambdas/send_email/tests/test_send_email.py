import collections
import pathlib as pl
import json

import pytest
import mock
from hyp3_events import Hyp3Event

import import_send_email
import send_email_mocks

from send_email_main import send_email_main
from send_email_env import environment
import send_email_sns as sns
from render_email import Email


def make_mock_user(wants_email):
    User = collections.namedtuple(
        'User', ['wants_email', 'id', 'username', 'email'])

    def mock_user(*args, **kwargs):
        return User(wants_email, 1, 'testuser', 'test@example.com')

    return mock_user


@mock.patch('ses.send', side_effect=send_email_mocks.send_mock)
@mock.patch(
    'send_email_queries.get_user_by_id',
    side_effect=make_mock_user(wants_email=True)
)
@mock.patch('hyp3_db.connect_using_environment_variables')
def test_main_email_wants_email(db_mock, user_mock, ses_mock, sns_event):
    environment.source_email = "test@test.com"

    send_email_main(sns_event)

    user_mock.assert_called_once()
    ses_mock.assert_called_once()


@mock.patch('ses.send', side_effect=send_email_mocks.send_mock)
@mock.patch(
    'send_email_queries.get_user_by_id',
    side_effect=make_mock_user(wants_email=False)
)
@mock.patch('hyp3_db.connect_using_environment_variables')
def test_main_email_doesnt_want_email(db_mock, user_mock, ses_mock, sns_event):
    environment.source_email = "test@test.com"

    send_email_main(sns_event)

    user_mock.assert_called_once()
    ses_mock.assert_not_called()


def test_sns_event_from_notification(sns_event):
    hyp3_event = sns.get_hyp3_event_from(sns_event)

    assert isinstance(hyp3_event, Hyp3Event)


def test_render_email(sns_event):
    hyp3_event = sns.get_hyp3_event_from(sns_event)
    rendered_email = Email().render(**hyp3_event.to_dict())

    assert isinstance(rendered_email, str)


@pytest.fixture
def sns_event():
    sns_example_path = pl.Path(__file__).parent / 'data' / 'sns-event.json'
    with sns_example_path.open('r') as f:
        return json.load(f)
