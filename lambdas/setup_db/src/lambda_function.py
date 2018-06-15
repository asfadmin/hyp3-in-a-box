# setup_db/lambda_function.py
# Rohan Weeden
# Created: June 13, 2018

# Lambda function for creating the Hyp3 Database

import os

from hyp3_db import Hyp3DB
from setup_db import setup_db


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
