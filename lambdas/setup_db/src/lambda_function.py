# setup_db/lambda_function.py
# Rohan Weeden
# Created: June 13, 2018

# Lambda function for creating the Hyp3 Database

import os

from hyp3_db import Hyp3DB
from init_db import setup_db


def lambda_handler(aws_event, aws_context):
    """ AWS Lambda entry point. Sets up the hyp3 database for the rest of the
        hyp3 system to use. The lambda is responsible for creating a new user
        and installing the postgis plugin.

        :param aws_event: lambda event data
        :param aws_context: lambda runtime info
    """
    db = get_db()
    setup_db(db)


def get_db():
    """ Create a database connection using SQLAlchemy.

        :returns: hyp3_db module database object
        :rtype: hyp3_db.Hyp3DB
    """
    HOST = os.environ.get("Hyp3DBHost")
    USER = os.environ.get("Hyp3DBRootUser")
    PASS = os.environ.get("Hyp3DBRootPass")

    return Hyp3DB(
        host=HOST,
        user=USER,
        password=PASS
    )
