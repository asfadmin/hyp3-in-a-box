import json
import pathlib as pl
import sqlalchemy as sqla
from sqlalchemy import orm


import hyp3_models


def main():
    user, password, host = load_creds('creds.json')
    connection_str = f'postgresql://{user}:{password}@{host}:5432/hyp3db'

    engine = sqla.create_engine(
        connection_str
    )

    # create a configured "Session" class
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    users = session.query(hyp3_models.Product).limit(5).all()

    print([user.id for user in users])


def load_creds(cred_file):
    cred_path = pl.Path(__file__).parent / cred_file
    with cred_path.open('r+') as f:
        creds = json.load(f)

    return [creds[k] for k in ('user', 'password', 'host')]


if __name__ == "__main__":
    main()
