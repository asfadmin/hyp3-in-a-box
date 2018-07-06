# setup_db.py
# Rohan Weeden, William Horn
# June 14, 2018

# Database setup functions. Need to pull them out from lambda_function to avoid
# naming conflicts during unit test imports

import json

from sqlalchemy.sql import text

import hyp3_db
from hyp3_db.hyp3_models.base import Base
import custom_resource

import utils
import hyp3_user
import hyp3_processes


def setup_db(event, db_admin_creds):
    print(json.dumps(event))

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
            setup_outputs = setup_db_main(db)

        return {
            'Data': setup_outputs,
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

    output = {}
    for i, step in enumerate(steps):
        count, num_steps = i + 1, len(steps)
        print(f'   ({count}/{num_steps}) - {step.__name__}')
        step_output = step(db)

        if not step_output:
            continue

        output.update(step_output)

    db.session.commit()

    return output


def install_postgis(db):
    create_postgis_sql = text("""
        CREATE EXTENSION postgis;
    """)
    db.engine.execute(create_postgis_sql)


def add_db_user(db):
    user, password, db_name = utils.get_environ_params(
        'Hyp3DBUser',
        'Hyp3DBPass',
        'Hyp3DBName'
    )

    add_user_sql = text(f"""
        CREATE USER {user} WITH PASSWORD :password;
        GRANT ALL PRIVILEGES ON DATABASE {db_name} to {user};
    """)

    db.engine.execute(
        add_user_sql,
        password=password
    )


def make_tables(db):
    Base.metadata.create_all(db.engine)


def make_hyp3_admin_user(db):
    hyp3_user.add_to(db)


def add_default_processes(db):
    processes = hyp3_processes.make_default()

    db.session.bulk_save_objects(processes)
