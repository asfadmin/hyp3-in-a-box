
from .environment import environment as env
from hyp3_db import Hyp3DB
from . import notifications


def hyp3_jobs(new_granule_packages):
    host, name, password = env.get_db_creds()
    db = Hyp3DB(host, name, password)

    for package in new_granule_packages[:3]:
        polygon = format_polygon(package['polygon'])

        subs = db.get_enabled_intersecting_subs(polygon)

        notifications.send(subs, package)


def format_polygon(point_vals):
    points = ""

    for x, y in zip(point_vals[0::2], point_vals[1::2]):
        points += f"{y} {x},"

    return f"POLYGON(({points[:-1]}))"


def queue_jobs(subs, package):
    for sub in subs:
        queue_job(sub, package)


def queue_job(sub, package):
    pass
