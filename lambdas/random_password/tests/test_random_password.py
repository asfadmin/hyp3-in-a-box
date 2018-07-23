import json
import pathlib as pl

import mock

import import_random_password
import random_password


@mock.patch('random_password.custom_resource.send')
def test_random_password_send_response(send_mock):
    random_password.send_response(get_sample_event())

    send_mock.assert_called()


def test_random_password():
    event = get_sample_event()
    response = random_password.RandomPassword(event) \
        .get_response()

    assert all(k in response for k in ('Data', 'Reason', 'Status'))


def get_sample_event():
    path = pl.Path(__file__).parent / 'data' / 'sample_event.json'

    with path.open('r') as f:
        return json.load(f)
