# setup_db/lambda_function.py
# Rohan Weeden
# Created: June 13, 2018

# Lambda function for creating the Hyp3 Database

import os

from hyp3_db import Hyp3DB
from hyp3_db.hyp3_models.base import Base
from sqlalchemy.sql import text

HOST = os.environ["Hyp3DBHost"]
USER = os.environ["Hyp3DBRootUser"]
PASS = os.environ["Hyp3DBRootPass"]

ADD_USER_SQL = text("""
CREATE USER hyp3_user WITH PASSWORD :password;
GRANT ALL PRIVILEGES ON DATABASE hyp3db to hyp3_user;
""")


def lambda_handler(event, context):
    db = Hyp3DB(
        host=HOST,
        user=USER,
        password=PASS
    )

    db.session.engine.execute(ADD_USER_SQL, password="testpass")

    Base.metadata.create_all(db.session.engine)
