import pathlib as pl
import json
import mock

import import_send_email

from hyp3_events import Hyp3Event
from lambda_function import lambda_handler
import sns
import render


@mock.patch('ses.send')
@mock.patch(
    'os.environ'
)
def test_send_email_lambda(os, ses_mock):
    event, context = load_example_sns(), {}

    lambda_handler(event, context)
    ses_mock.assert_called_once()


def test_sns_event_from_notification():
    event = load_example_sns()

    hyp3_event = sns.get_hyp3_event_from(event)

    assert isinstance(hyp3_event, Hyp3Event)


def test_render_email():
    event = load_example_sns()

    hyp3_event = sns.get_hyp3_event_from(event)
    rendered_email = render.email_with(hyp3_event)

    assert isinstance(rendered_email, str)


def load_example_sns():
    sns_example_path = pl.Path(__file__).parent / 'data' / 'sns-event.json'
    with sns_example_path.open('r') as f:
        return json.load(f)
