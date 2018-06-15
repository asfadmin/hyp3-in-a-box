import hyp3_db_test_utils as tu


@tu.with_db
def test_db_creation(db):
    assert db is not None
