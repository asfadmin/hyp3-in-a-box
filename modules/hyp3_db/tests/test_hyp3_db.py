import hyp3_db_test_utils as tu

from hyp3_db import hyp3_models


@tu.with_db
def test_api_key_generation(db):
    user = hyp3_models.User(
        username="test",
        email="test@email.com",
        is_admin=True,
        is_authorized=True,
        granules_processed=0
    )

    db.session.add(user)
    update_db_with(db, user)

    key, api_key = hyp3_models.ApiKey.generate_new(user.id)
    db.session.add(api_key)


def update_db_with(db, obj):
    db.session.flush()
    db.session.refresh(obj)
