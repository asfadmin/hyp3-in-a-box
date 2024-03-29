from typing import Dict, List

import hyp3_db
from hyp3_db.hyp3_models import Process, User
from hyp3_events import NewGranuleEvent
from scheduler_env import environment

from . import queries
from .job import Job


def hyp3_jobs(new_granules: List[NewGranuleEvent]):
    """ Get all the hyp3 jobs from the new granules

        :param list[dict] new_granules: New granules from cmr

        :return: A named tuple of the form Job(sub, process, user, granule)
        :rtype: list[Job]
    """
    host, name, password, db = environment.db_creds

    with hyp3_db.connect(host, name, password, db) as db:
        print('finding jobs for each granule')
        jobs_for_each_granule = [
            get_jobs_for(granule, db) for granule in new_granules
        ]

        jobs = flatten_list(jobs_for_each_granule)

        print(f'Found {len(jobs)} total jobs to start')

        return jobs


def get_jobs_for(granule: NewGranuleEvent, db) -> List[Job]:
    polygon = format_polygon(granule.polygon)
    print(polygon)

    subs = queries.get_enabled_intersecting_subs(db, polygon)
    print(f'Found {len(subs)} subs overlapping granule')

    users = get_users_for(subs, db)
    processes = get_processes(db)

    return [
        Job(
            sub=sub,
            process=processes[sub.process_id],
            user=users[sub.user_id],
            granule=granule
        )
        for sub in subs
    ]


def format_polygon(point_vals):
    points = ""

    for lat, lon in pair_up_lat_lons(point_vals):
        points += f"{lon} {lat},"

    return f"POLYGON(({points[:-1]}))"


def pair_up_lat_lons(point_vals):
    return zip(point_vals[0::2], point_vals[1::2])


def get_users_for(subs, db) -> Dict[int, User]:
    user_ids = [sub.user_id for sub in subs]

    users = queries.get_users_by_ids(db, user_ids)

    return dict_indexed_by_id(users)


def get_processes(db) -> Dict[int, Process]:
    processes = queries.get_processes(db)

    return dict_indexed_by_id(processes)


def dict_indexed_by_id(objs: List):
    return {
        obj.id: obj for obj in objs
    }


def flatten_list(l):
    return sum(l, [])
