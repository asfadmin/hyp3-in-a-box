# setup_db/lambda_function.py
# Rohan Weeden, William Horn
# Created: June 13, 2018

# Lambda function for creating the Hyp3 Database

import os

from init_db import setup_db


def lambda_handler(aws_event, aws_context):
    """ AWS Lambda entry point. This is a cloudformation CustomResource that
        Sets up the hyp3 database for the hyp3 system to use.

        :param aws_event: lambda event data
        :param aws_context: lambda runtime info
    """
    setup_db(aws_event, get_db_creds())


def get_db_creds():
    """ Get the db params from environment

        :returns: host, username, password in that order
        :rtype: list[str]
    """

    return [
        os.environ[f'Hyp3DB{k}'] for k in ('Host', 'User', 'Pass')
    ]
