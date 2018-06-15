
from hyp3_db.hyp3_models import Subscription, User
from geoalchemy2 import WKTElement


def get_users_by_ids(db, user_ids):
    user_ids_filter = User.id.in_(user_ids)

    users = db.session.query(User) \
        .filter(user_ids_filter) \
        .all()

    return users


def get_enabled_intersecting_subs(db, polygon):
    poly = WKTElement(polygon, srid=4326)
    intersection = Subscription.location.ST_Contains(poly)

    intersecting_subs = enabled_subs_query(db) \
        .filter(intersection) \
        .all()

    return intersecting_subs


def enabled_subs_query(db):
    return db.session.query(Subscription) \
        .filter_by(enabled=True)
