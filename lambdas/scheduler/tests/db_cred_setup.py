import json
import pathlib as pl

import pytest

import testing_utils as utils
from scheduler_env import environment

creds_path = pl.Path(__file__).parent / 'data/creds.json'

if creds_path.exists():
    with creds_path.open('r') as f:
        creds = json.load(f)
    environment.db_creds = creds

skip_if_creds_not_available = pytest.mark.skipif(
    not creds_path.exists(),
    reason="Currently can't run test without creds"
)
