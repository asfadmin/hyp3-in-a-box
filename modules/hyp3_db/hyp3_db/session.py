import json
import pathlib as pl
import sqlalchemy as sqla
from sqlalchemy import orm


def make_session():
    engine = make_engine()
    Session = orm.sessionmaker(bind=engine)

    return Session()


def make_engine():
    user, password, host = load_creds('creds.json')
    connection_str = get_connection_str(user, password, host)

    return sqla.create_engine(connection_str)


def load_creds(cred_file):
    cred_path = pl.Path(__file__).parent / cred_file
    with cred_path.open('r+') as f:
        creds = json.load(f)

    return [creds[k] for k in ('user', 'password', 'host')]


def get_connection_str(user, password, host):
    return 'postgresql://{}:{}@{}:5432/hyp3db'.format(user, password, host)


session = make_session()
