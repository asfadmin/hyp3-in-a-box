from geoalchemy2 import WKTElement

from environment import environment
from hyp3_db import Hyp3DB
from hyp3_db.hyp3_models import Subscription, User


def hyp3_jobs(new_granule_packages):
    host, name, password, db = environment.db_creds
    db = Hyp3DB(host, name, password, db)

    subs = db.get_enabled_subs()
    print(subs)

    emails_packages = []
    for package in new_granule_packages:
        polygon = format_polygon(package['polygon'])
        print(polygon)

        print(f'Found {len(subs)} subs overlapping granule')
        subs = get_enabled_intersecting_subs(db, polygon)

        users = get_users_for(subs, db)

        emails_packages += [
            (sub, users[sub.user_id], package) for sub in subs
        ]

    return emails_packages


def format_polygon(point_vals):
    points = ""

    for x, y in zip(point_vals[0::2], point_vals[1::2]):
        points += "{} {},".format(x, y)

    return "POLYGON(({}))".format(points[:-1])


def get_users_for(subs, db):
    user_ids = [sub.user_id for sub in subs]

    users = get_users_by_ids(db, user_ids)

    return {
        user.id: user for user in users
    }


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
