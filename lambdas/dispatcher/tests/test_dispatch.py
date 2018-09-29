import contextlib
from typing import NamedTuple
import random
import string

import boto3
import pytest
import mock

import hyp3_events
from tempaws import TemporaryQueue

import import_dispatcher
from send_all_events import all_events
import dispatcher_sqs as sqs
import dispatcher_sns
from dispatcher_env import environment as env


EMAIL_EVENTS_COUNT, START_EVENTS_COUNT = 10, 5


# @mock.patch('Client.publish', return_value='pushing e-mail')
# ideally this should be patching the publish method but i can't find the actual module information in the docs all they give is to get it with client()
@mock.patch('dispatcher_sns.push', return_value='test push')
@mock.patch('dispatcher_sqs.add_event')
@mock.patch('dispatcher_sns.push_event')
def test_dispatch(sns_mock, sqs_mock, push_mock, events):
    all_events(events)

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


class FakeEvent(NamedTuple):
    event_type: str

    def to_json(self):
        return ''


@pytest.fixture
def events():

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
        script_path='',
        additional_info=[]
    )
