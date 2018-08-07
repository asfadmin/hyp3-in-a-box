from typing import NamedTuple

import pytest
import mock

import import_scheduler
import dispatch


class FakeEvent(NamedTuple):
    event_type: str


@mock.patch('dispatch.scheduler_sqs.add_event')
@mock.patch('dispatch.scheduler_sns.push_event')
def test_dispatch(sns_mock, sqs_mock, events):
    dispatch.all_events(events)

    assert sns_mock.call_count == 10
    assert sqs_mock.call_count == 5


@pytest.fixture
def events():
    return  \
        [FakeEvent('EmailEvent') for _ in range(10)] + \
        [FakeEvent('StartEvent') for _ in range(5)]
