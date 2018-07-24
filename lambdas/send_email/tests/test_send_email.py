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
import sns
import render


def make_mock_user(wants_email):
    User = collections.namedtuple('User', ['wants_email', 'id'])

    def mock_user(*args, **kwargs):
        return User(wants_email, 1)

    return mock_user


@mock.patch('ses.send', side_effect=send_email_mocks.send_mock)
@mock.patch('send_email_queries.get_user_by_email')
@mock.patch('hyp3_db.connect_using_environment_variables')
def test_main_email(db_mock, user_mock, ses_mock, sns_event):
    environment.source_email = "test@test.com"

    user_wants_email(sns_event, user_mock, ses_mock)
    user_doesnt_want_emails(sns_event, user_mock, ses_mock)


def user_wants_email(sns_event, user_mock, ses_mock):
    user_mock.side_effect = make_mock_user(wants_email=True)
    send_email_main(sns_event)

    user_mock.assert_called_once()
    ses_mock.assert_called_once()


def user_doesnt_want_emails(sns_event, user_mock, ses_mock):
    user_mock.side_effect = make_mock_user(wants_email=False)
    send_email_main(sns_event)

    ses_mock.assert_called_once()


def test_sns_event_from_notification(sns_event):
    hyp3_event = sns.get_hyp3_event_from(sns_event)

    assert isinstance(hyp3_event, Hyp3Event)


def test_render_email(sns_event):
    hyp3_event = sns.get_hyp3_event_from(sns_event)
    rendered_email = render.email_with(hyp3_event.to_dict())

    assert isinstance(rendered_email, str)


@pytest.fixture
def sns_event():
    sns_example_path = pl.Path(__file__).parent / 'data' / 'sns-event.json'
    with sns_example_path.open('r') as f:
        return json.load(f)
