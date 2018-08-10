import contextlib
import json

import pytest
import boto3

from find_new.previous_time import ssm

ssm_client = boto3.client('ssm')


def test_ssm_upload(param_name, expected):
    ssm.upload(param_name, json.dumps(expected))

    val = json.loads(ssm.download(param_name))

    assert val == expected

    delete_param(param_name)


@pytest.fixture
def param_name():
    return '/test/previous-time.json'


@pytest.fixture
def expected():
    return {'test': 'dict'}


def delete_param(path):
    ssm_client.delete_parameter(
        Name=path
    )
