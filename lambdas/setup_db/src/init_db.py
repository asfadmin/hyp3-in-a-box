# setup_db.py
# Rohan Weeden
# June 14, 2018

# Database setup functions. Need to pull them out from lambda_function to avoid
# naming conflicts during unit test imports

import os

from hyp3_db.hyp3_models.base import Base
from hyp3_db import hyp3_models
from sqlalchemy.sql import text


def setup_db(db):
    """ Creates hyp3 user as well as all database tables """
    install_postgis(db)

    add_db_admin_user(db)

    make_tables(db)
    make_hyp3_admin_user(db)

    add_default_processes(db)

    db.session.commit()


def install_postgis(db):
    create_postgis_sql = text("""
        CREATE EXTENSION postgis;
    """)
    db.engine.execute(create_postgis_sql)


def add_db_admin_user(db):
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
    db.session.commit()


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
    db.session.commit()
