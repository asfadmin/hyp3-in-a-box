from hyp3_db.hyp3_models import User, OneTimeAction


def get_user_by_email(db, email):
    return db.session.query(User) \
        .filter_by(email=email) \
        .first()


def get_unsub_action(db, user_id):
    return db.session.query(OneTimeAction) \
        .filter_by(user_id=user_id) \
        .filter_by(action='unsubscribe') \
        .first()
