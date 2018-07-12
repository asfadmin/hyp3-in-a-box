import sqlalchemy as sqla
from sqlalchemy import pool
from sqlalchemy import orm


def make_session(engine):
    Session = orm.sessionmaker(bind=engine)

    return Session()


def make_engine(user, password, host, db):
    connection_str = get_connection_str(user, password, host, db)

    return sqla.create_engine(
        connection_str,
        poolclass=pool.NullPool
    )


def get_connection_str(user, password, host, db):
    return 'postgresql://{}:{}@{}:5432/{}'.format(
        user, password, host, db
    )
