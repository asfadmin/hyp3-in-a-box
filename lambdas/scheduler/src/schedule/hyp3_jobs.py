from typing import NamedTuple

import hyp3_db
from hyp3_db.hyp3_models import Subscription, User
from hyp3_events import NewGranuleEvent
from scheduler_env import environment

from . import queries


class Job(NamedTuple):
    sub: Subscription
    user: User
    granule: NewGranuleEvent


def hyp3_jobs(new_granules):
    """ Get all the hyp3 jobs from the new granules

        :param list[dict] new_granules: New granules from cmr

        :return: A named tuple of the form Job(sub, user, granule)
        :rtype: list[Job]
    """
    host, name, password, db = environment.db_creds

    with hyp3_db.connect(host, name, password, db) as db:
        jobs_for_each_granule = [
            get_jobs_for(granule, db) for granule in new_granules
        ]

        jobs = flatten_list(jobs_for_each_granule)

        print('Found {} jobs to start'.format(len(jobs)))

        return jobs


def get_jobs_for(granule, db):
    polygon = format_polygon(granule.polygon)
    print(polygon)

    subs = queries.get_enabled_intersecting_subs(db, polygon)
    print('Found {} subs overlapping granule'.format(len(subs)))

    users = get_users_for(subs, db)

    return [
        Job(sub, users[sub.user_id], granule) for sub in subs
    ]


def format_polygon(point_vals):
    points = ""

    for lat, lon in pair_up_lat_lons(point_vals):
        points += "{} {},".format(lon, lat)

    return "POLYGON(({}))".format(points[:-1])


def pair_up_lat_lons(point_vals):
    return zip(point_vals[0::2], point_vals[1::2])


def get_users_for(subs, db):
    user_ids = [sub.user_id for sub in subs]

    users = queries.get_users_by_ids(db, user_ids)

    return {
        user.id: user for user in users
    }


def flatten_list(l):
    return sum(l, [])
