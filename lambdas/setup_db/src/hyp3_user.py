from hyp3_db import hyp3_models


def is_new(db, user):
    print('checking if user exists')

    users = db.session \
        .query(hyp3_models.User) \
        .filter(hyp3_models.User.username == user.name) \
        .all()

    print(users)

    return len(users) == 0


def add_to(db, user):
    admin_user = add_hyp3_user(db, user)

    update_db_with(db, admin_user)

    api_key = add_api_key(db, admin_user.id)

    return api_key


def add_hyp3_user(db, user):
    new_user = hyp3_models.User(
        username=user.name,
        email=user.email,
        is_admin=True,
        is_authorized=True,
        granules_processed=0
    )

    db.session.add(new_user)

    return new_user


def update_db_with(db, obj):
    db.session.flush()
    db.session.refresh(obj)


def add_api_key(db, user_id):
    key, api_key = hyp3_models.ApiKey.generate_new(user_id)
    db.session.add(api_key)

    return key
