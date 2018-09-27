import contextlib
from typing import NamedTuple
import random
import string

import boto3
import pytest
import mock

import hyp3_events
from tempaws import TemporaryQueue

import import_scheduler
import dispatch
from dispatch import scheduler_sqs as sqs
from scheduler_env import environment as env


EMAIL_EVENTS_COUNT, START_EVENTS_COUNT = 10, 5


@mock.patch('dispatch.scheduler_sqs.add_event')
@mock.patch('dispatch.scheduler_sns.push_event')
def test_dispatch(sns_mock, sqs_mock, events):
    dispatch.all_events(events)

    assert sns_mock.call_count == EMAIL_EVENTS_COUNT
    assert sqs_mock.call_count == START_EVENTS_COUNT


def test_sqs_add(start_event):
    with TemporaryQueue.create_fifo() as q:
        env.queue_url = q.url
        sqs.add_event(start_event)

        messages = q.receive_messages(MessageAttributeNames=['EventType'])
        assert len(messages) == 1

        event_from_queue = hyp3_events.StartEvent.from_json(messages[0].body)

        assert event_from_queue == start_event


@pytest.fixture
def events():
    class FakeEvent(NamedTuple):
        event_type: str

    return  \
        [FakeEvent('EmailEvent') for _ in range(EMAIL_EVENTS_COUNT)] + \
        [FakeEvent('StartEvent') for _ in range(START_EVENTS_COUNT)]


@pytest.fixture
def start_event():
    return hyp3_events.StartEvent(
        granule=('S1A_IW_GRDH_1SDV_20180803T125353_'
                 '20180803T125418_023082_02819A_1DBD'),
        user_id=1,
        sub_id=1,
        output_patterns=['*/*.txt'],
        additional_info=[]
    )
