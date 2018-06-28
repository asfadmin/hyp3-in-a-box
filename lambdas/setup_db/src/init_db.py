# setup_db.py
# Rohan Weeden, William Horn
# June 14, 2018

# Database setup functions. Need to pull them out from lambda_function to avoid
# naming conflicts during unit test imports

import os

from sqlalchemy.sql import text

import hyp3_db
from hyp3_db import hyp3_models
from hyp3_db.hyp3_models.base import Base
import custom_resource


def setup_db(event, db_admin_creds):
    resp = DBSetup(event, db_admin_creds) \
        .get_response()

    custom_resource.send(event, resp)


class DBSetup(custom_resource.Base):
    def __init__(self, event, db_admin_creds):
        super().__init__(event)
        self.db_creds = db_admin_creds

    def _process(self):
        print('connecting to hyp3_db')
        with hyp3_db.connect(*self.db_creds) as db:
            print('connected')
            setup_db_main(db)

        return {
            'Data': {},
            'Reason': 'Successfully setup hyp3 db'
        }


def setup_db_main(db):
    """ Creates hyp3 user as well as all database tables """
    print('Setting up database:')
    steps = [
        install_postgis,
        add_db_user,
        make_tables,
        make_hyp3_admin_user,
        add_default_processes,
    ]

    for i, step in enumerate(steps):
        count, num_steps = i + 1, len(steps)
        print(f'   ({count}/{num_steps}) - {step.__name__}')
        step(db)

    db.session.commit()


def install_postgis(db):
    create_postgis_sql = text("""
        CREATE EXTENSION postgis;
    """)
    db.engine.execute(create_postgis_sql)


def add_db_user(db):
    user, password, db_name = [
        os.environ[f'Hyp3DB{k}'] for k in ('User', 'Pass', 'Name')
    ]

    add_user_sql = text(f"""
        CREATE USER hyp3_user WITH PASSWORD :password;
        GRANT ALL PRIVILEGES ON DATABASE {db_name} to {user};
    """.format(db, user))

    db.engine.execute(
        add_user_sql,
        password=password
    )


def make_tables(db):
    Base.metadata.create_all(db.engine)


def make_hyp3_admin_user(db):
    admin_user = hyp3_models.User(
        username='admin',
        email='wbhorn@alaska.edu',
        is_admin=True,
        is_authorized=True,
        granules_processed=0
    )

    db.session.add(admin_user)


def add_default_processes(db):
    notify_only_process = hyp3_models.Process(
        name="Notify Only",
        description='Notify users when new data arives via email',
        script="N/A",
        suffix="N/A",
        database_info_required=False,
        ami_id="N/A",
        ec2_size="N/A",
        supports_pair_processing=False,
        text_id="notify_only"
    )

    db.session.add(notify_only_process)
