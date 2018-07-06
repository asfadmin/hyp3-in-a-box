import utils

from hyp3_db import hyp3_models

def add_to(db):
    username, user_email = utils.get_environ_params(
        'Hyp3AdminUsername',
        'Hyp3AdminEmail'
    )

    admin_user = add_hyp3_user(db, username, user_email)
    api_key = add_api_key(db, admin_user.id)

    return {
        'ApiKey': api_key
    }


def add_hyp3_user(db, username, user_email):
    new_user = hyp3_models.User(
        username=username,
        email=user_email,
        is_admin=True,
        is_authorized=True,
        granules_processed=0
    )

    db.session.add(new_user)

    update_db_with(db, new_user)

    return new_user


def update_db_with(db, obj):
    db.session.flush()
    db.session.refresh(obj)


def add_api_key(db, user_id):
    key, api_key = hyp3_models.ApiKey.generate_new(user_id)
    db.session.add(api_key)

    return key
