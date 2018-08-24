import json
import pathlib as pl

import pytest

import import_dashboard
import dashboard


def test_dashboard_update(full_dashboard):
    new_board = dashboard.update(full_dashboard, 'hyp3-in-a-box-test')

    with open('updated-dashboard.json', 'w') as f:
        f.write(json.dumps(json.loads(new_board)))


def test_dashboard_value_update(sample_str):
    old_val, new_val = "foo", "bar"
    updated = dashboard.update_values(sample_str, replace_values=[
        (old_val, new_val)
    ])

    assert all([
        old_val not in updated,
        '${' + new_val + '}' in updated
    ])


def test_replace_region(sample_dashboard):
    updated = dashboard.update_values(sample_dashboard, replace_values=[
        ('us-west-2', 'AWS::Region')
    ])

    assert '${AWS::Region}' in updated


@pytest.fixture
def sample_str():
    return "foo"


@pytest.fixture
def sample_dashboard():
    return json.dumps({
        "view": "timeSeries",
        "stacked": True,
        "region": "us-west-2",
        "period": 300,
        "title": "Duration Average"
    })


@pytest.fixture
def full_dashboard():
    path = pl.Path(__file__).parent / 'dashboard.json'

    with path.open('r') as f:
        return f.read()
