from environment import environment
from . import queries
from hyp3_db import Hyp3DB


def hyp3_jobs(new_granule_packages):
    host, name, password, db = environment.db_creds
    db = Hyp3DB(host, name, password, db)

    emails_packages = []
    for package in new_granule_packages:
        polygon = format_polygon(package['polygon'])
        print(polygon)

        subs = queries.get_enabled_intersecting_subs(db, polygon)
        print(f'Found {len(subs)} subs overlapping granule')

        users = get_users_for(subs, db)

        emails_packages += [
            (sub, users[sub.user_id], package) for sub in subs
        ]

    return emails_packages


def format_polygon(point_vals):
    points = ""

    for lat, lon in zip(point_vals[0::2], point_vals[1::2]):
        points += "{} {},".format(lon, lat)

    return "POLYGON(({}))".format(points[:-1])


def get_users_for(subs, db):
    user_ids = [sub.user_id for sub in subs]

    users = queries.get_users_by_ids(db, user_ids)

    return {
        user.id: user for user in users
    }

