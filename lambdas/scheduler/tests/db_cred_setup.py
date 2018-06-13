import pytest
import json

from environment import environment
import testing_utils as utils

creds_path = utils.data_path / 'creds.json'

if creds_path.exists():
    with creds_path.open('r') as f:
        creds = json.load(f)
    environment.db_creds = creds

skip_if_creds_not_availbable = pytest.mark.skipif(
    not creds_path.exists(),
    reason="Currently can't run test without creds"
)
