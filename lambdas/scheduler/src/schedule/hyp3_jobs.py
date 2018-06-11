
from .environment import environment as env


def hyp3_jobs(new_granule_packages):
    host, name, password = env.get_db_creds()

    print(host)
