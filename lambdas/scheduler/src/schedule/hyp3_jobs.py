
from .environment import environment as env
from hyp3_db import Hyp3DB


def hyp3_jobs(new_granule_packages):
    host, name, password = env.get_db_creds()
    db = Hyp3DB(host, name, password)

    subs = db.get_enabled_subs()

    print(len(subs))
