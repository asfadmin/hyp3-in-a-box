from typing import Union, List, Dict

from schedule import queries
from scheduler_env import environment
from hyp3_events import EmailEvent, StartEvent, NewGranuleEvent
import hyp3_db
from hyp3_db.hyp3_models import Process, User


def make_dispatchable(events: List[NewGranuleEvent]
                      ) -> Union[StartEvent, EmailEvent]:
    """
    :param events: a list of NewGranuleEvents to be turned into StartEvents
    or EmailEvents
    :return: a list of both StartEvents and EmailEvents
    """
    host, name, password, db = environment.db_creds

    with hyp3_db.connect(host, name, password, db) as db:
        print("""converting NewGranuleEvents to Start and Email Events for
              before sending to the dispatcher""")
        new_events = [
            convert(e, db) for e in events
            ]

        # turns a list of lists into a single list
        new_events = flatten_list(new_events)

        return new_events


def convert(event: NewGranuleEvent, db) -> Union[StartEvent, EmailEvent]:
    polygon = format_polygon(event.polygon)
    print(polygon)

    subs = queries.get_enabled_intersecting_subs(db, polygon)
    print(f'Found {len(subs)} subs overlapping granule')

    users = get_users_for(subs, db)
    processes = get_processes(db)

    return


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
