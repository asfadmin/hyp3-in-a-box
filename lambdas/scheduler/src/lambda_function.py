import os
import json

from scheduler_env import environment
from scheduler_main import scheduler


def lambda_handler(event, context):
    """ Entry point for the lambda to run.

        :param event: lambda event data

            * new_granules - A list of granules to process

        :param context: lambda runtime info
    """
    print('Setting environment variables')
    print(json.dumps(event))
    set_environment_variables()

    scheduler(event)


def set_environment_variables():
    environment.db_creds = [
        os.environ[k] for k in ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    ]
    environment.dispatcher_lambda = os.environ['DISPATCHER_LAMBDA_NAME']
