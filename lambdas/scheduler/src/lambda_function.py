import os

import events
import schedule
from environment import environment


def lambda_handler(event, context):
    """ Entry point for the lambda to run.

        :param event: lambda event data

            * new_granules - A list of granules to process
        :param context: lambda runtime info
    """
    print('Setting environment variables')
    set_environment_variables()

    scheduler(event)


def set_environment_variables():
    environment.db_creds = [
        os.environ[k] for k in ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    ]

    environment.sns_arn = os.environ['SNS_ARN']
