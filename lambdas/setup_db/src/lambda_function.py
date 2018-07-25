# setup_db/lambda_function.py
# Rohan Weeden, William Horn
# Created: June 13, 2018

# Lambda function for creating the Hyp3 Database

import os

from init_db import setup_db
import setup_db_utils as utils


def lambda_handler(aws_event, aws_context):
    """ AWS Lambda entry point. This is a cloudformation CustomResource that
        Sets up the hyp3 database for the hyp3 system to use.

        :param aws_event: lambda event data
        :param aws_context: lambda runtime info
    """
    setup_db(aws_event, get_db_creds(), get_db_low_priv_creds())


def get_db_creds():
    """ Get the db params from environment

        :returns: host, username, password, dbname in that order
        :rtype: list[str]
    """

    return utils.get_environ_params(
        'Hyp3DBHost',
        'Hyp3DBRootUser',
        'Hyp3DBRootPass',
        'Hyp3DBName'
    )


def get_db_low_priv_creds():
    """ Get the db params for the low privileged user from environment

        :returns: host, username, password, dbname in that order
        :rtype: list[str]
    """

    return utils.get_environ_params(
        'Hyp3DBHost',
        'Hyp3DBUser',
        'Hyp3DBPass',
        'Hyp3DBName'
    )
