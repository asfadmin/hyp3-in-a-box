
from environment import environment
from hyp3_db import Hyp3DB


def hyp3_jobs(new_granule_packages):
    host, name, password = environment.db_creds
    db = Hyp3DB(host, name, password)

    emails_packages = []
    # TODO: Take out [:3] when done testing
    for package in new_granule_packages[:3]:
        polygon = format_polygon(package['polygon'])

        subs = db.get_enabled_intersecting_subs(polygon)

        users = get_users_for(subs, db)

        emails_packages += [
            (sub, users[sub.user_id], package) for sub in subs
        ]

    return emails_packages


def format_polygon(point_vals):
    points = ""

    for x, y in zip(point_vals[0::2], point_vals[1::2]):
        points += f"{y} {x},"

    return f"POLYGON(({points[:-1]}))"


def get_users_for(subs, db):
    sub_ids = [sub.user_id for sub in subs]

    users = db.get_users_by_ids(sub_ids)

    return {
        user.id: user for user in users
    }
