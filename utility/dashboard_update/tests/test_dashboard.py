import json

import pytest

import import_dashboard
import dashboard


def test_dashboard(sample_str):
    old_val, new_val = "foo", "bar"
    updated = dashboard.update(sample_str, replace_values=[
        (old_val, new_val)
    ])

    assert all([
        old_val not in updated,
        '${' + new_val + '}' in updated
    ])


def test_replace_region(full_dashboard):
    updated = dashboard.update(full_dashboard, replace_values=[
        ('us-west-2', 'AWS::Region')
    ])

    assert '${AWS::Region}' in updated


@pytest.fixture
def sample_str():
    return "foo"


@pytest.fixture
def full_dashboard():
    return json.dumps({
        "view": "timeSeries",
        "stacked": True,
        "region": "us-west-2",
        "period": 300,
        "title": "Duration Average"
    })
