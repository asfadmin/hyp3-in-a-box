# setup_db/lambda_function.py
# Rohan Weeden
# Created: June 13, 2018

# Lambda function for creating the Hyp3 Database

import os

from sqlalchemy.sql import text

from hyp3_db import Hyp3DB

HOST = os.environ("Hyp3DBHost")
USER = os.environ("Hyp3DBRootUser")
PASS = os.environ("Hyp3DbRootPass")

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
