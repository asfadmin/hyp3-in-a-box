import sqlalchemy as sqla
from sqlalchemy import orm


def make_session(host, user, password, db):
    engine = make_engine(user, password, host, db)
    Session = orm.sessionmaker(bind=engine)

    return Session()


def make_engine(user, password, host, db):
    connection_str = get_connection_str(user, password, host, db)
    print(connection_str)

    return sqla.create_engine(connection_str)


def get_connection_str(user, password, host, db):
    return 'postgresql://{}:{}@{}:5432/{}'.format(
        user, password, host, db
    )
