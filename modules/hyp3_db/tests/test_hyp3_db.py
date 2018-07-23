import hyp3_db_test_utils as tu

from hyp3_db import hyp3_models


@tu.with_db
def test_hyp3_db(db):
    assert db
