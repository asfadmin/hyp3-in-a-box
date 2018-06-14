# setup_db/lambda_function.py
# Rohan Weeden
# Created: June 13, 2018

# Lambda function for creating the Hyp3 Database

import os

from sqlalchemy.sql import text

from hyp3_db import Hyp3DB
from hyp3_db.hyp3_models.base import Base

ADD_USER_SQL = text("""
CREATE USER hyp3_user WITH PASSWORD :password;
GRANT ALL PRIVILEGES ON DATABASE hyp3db to hyp3_user;
""")


def lambda_handler(event, context):
    db = get_db()
    setup_db(db)


def get_db():
    HOST = os.environ.get("Hyp3DBHost")
    USER = os.environ.get("Hyp3DBRootUser")
    PASS = os.environ.get("Hyp3DBRootPass")

    return Hyp3DB(
        host=HOST,
        user=USER,
        password=PASS
    )


def setup_db(db):
    db.engine.execute(ADD_USER_SQL, password="testpass")
    Base.metadata.create_all(db.engine)
