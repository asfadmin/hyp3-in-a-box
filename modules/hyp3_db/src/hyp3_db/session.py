import sqlalchemy as sqla
from sqlalchemy import orm


def make_session(engine):
    Session = orm.sessionmaker(bind=engine)

    return Session()


def make_engine(user, password, host):
    connection_str = get_connection_str(user, password, host)

    return sqla.create_engine(connection_str)


def get_connection_str(user, password, host):
    return 'postgresql://{}:{}@{}:5432/hyp3db'.format(user, password, host)
