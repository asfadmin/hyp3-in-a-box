# setup_db.py
# Rohan Weeden
# June 14, 2018

# Database setup functions. Need to pull them out from lambda_function to avoid
# naming conflicts during unit test imports

import os

from hyp3_db.hyp3_models.base import Base
from sqlalchemy.sql import text


CREATE_POSTGIS_SQL = text("""
CREATE EXTENSION postgis;
""")

ADD_USER_SQL = text("""
CREATE USER hyp3_user WITH PASSWORD :password;
GRANT ALL PRIVILEGES ON DATABASE :db to :user;
""")


def setup_db(db):
    """ Creates hyp3 user as well as all database tables """

    USER = os.environ['Hyp3DBUser']
    PASS = os.environ['Hyp3DBPass']
    DB_NAME = os.environ['Hyp3DBName']

    db.engine.execute(CREATE_POSTGIS_SQL)
    db.engine.execute(
        ADD_USER_SQL,
        password=PASS,
        db=DB_NAME,
        user=USER
    )
    Base.metadata.create_all(db.engine)
