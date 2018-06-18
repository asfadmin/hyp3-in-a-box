from hyp3_db import Hyp3DB

from environment import environment
from . import queries


def hyp3_jobs(new_granules):
    """ Get all the hyp3 jobs from the new granules

        :param list[dict] new_granules: New granules from cmr

        :return: A tuple of the form (sub, user, granule)
        :rtype: list[tuple]
    """
    host, name, password, db = environment.db_creds
    db = Hyp3DB(host, name, password, db)

    jobs_for_each_granule = [
        get_jobs_for(granule, db) for granule in new_granules
    ]

    jobs = flatten_list(jobs_for_each_granule)

    return jobs


def get_jobs_for(granule, db):
    polygon = format_polygon(granule['polygon'])
    print(polygon)

    subs = queries.get_enabled_intersecting_subs(db, polygon)
    print('Found {} subs overlapping granule'.format(len(subs)))

    users = get_users_for(subs, db)

    return [
        (sub, users[sub.user_id], granule) for sub in subs
    ]


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


def flatten_list(l):
    return sum(l, [])
