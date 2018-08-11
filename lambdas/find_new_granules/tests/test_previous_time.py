import datetime as dt

import mock
import pytest

import import_find_new
import find_new_mocks
from find_new import previous_time, environment as env
from test_ssm import delete_param

env.maturity = 'test'


def test_previous_time(runtime):
    env.ssm_previous_time_name = '/some-stack/test_param_name'
    previous_time.set_time(runtime)

    assert previous_time.get_time() == runtime

    delete_param(env.ssm_previous_time_name)


@pytest.fixture
def runtime():
    return dt.datetime(2017, 12, 6, 15, 29, 43, 79060)
