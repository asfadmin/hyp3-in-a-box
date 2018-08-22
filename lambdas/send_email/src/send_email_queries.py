from hyp3_db import HyP3DB
from hyp3_db.hyp3_models import User, OneTimeAction, Subscription


def get_user_by_id(db: HyP3DB, user_id: int) -> User:
    return db.session.query(User) \
        .filter_by(id=user_id) \
        .one()


def get_sub_by_id(db: HyP3DB, sub_id: int) -> Subscription:
    return db.session.query(Subscription) \
        .filter_by(id=sub_id) \
        .one()


def get_unsub_action(db: HyP3DB, user_id: int) -> OneTimeAction:
    return db.session.query(OneTimeAction) \
        .filter_by(user_id=user_id) \
        .filter_by(action='unsubscribe') \
        .filter_by(enabled=True) \
        .first()
