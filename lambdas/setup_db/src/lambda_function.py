# setup_db/lambda_function.py
# Rohan Weeden
# Created: June 13, 2018

# Lambda function for creating the Hyp3 Database

import os

from init_db import setup_db


def lambda_handler(aws_event, aws_context):
    """ AWS Lambda entry point. Sets up the hyp3 database for the rest of the
        hyp3 system to use. The lambda is responsible for creating a new user
        and installing the postgis plugin.

        :param aws_event: lambda event data
        :param aws_context: lambda runtime info
    """
    setup_db(aws_event, get_db_creds())


def get_db_creds():
    """ Create a database connection using SQLAlchemy.

        :returns: hyp3_db module database object
        :rtype: hyp3_db.Hyp3DB
    """
    HOST = os.environ["Hyp3DBHost"]
    USER = os.environ["Hyp3DBRootUser"]
    PASS = os.environ["Hyp3DBRootPass"]

    return HOST, USER, PASS
