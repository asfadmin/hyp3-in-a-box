import os
import boto3

import find_new
from find_new import environment as env
import results


def lambda_handler(event, context):
    """ Entry point for the lambda to run.

        :param event: lambda event data
        :param context: lambda runtime info
    """
    setup_env()

    search_results = find_new.granules()

    new_granules = results.package(search_results)
    new_granules_json = results.format_into_json(new_granules)

    start_scheduler_with(new_granules_json)


def start_scheduler_with(new_granules_json):
    boto3.client('lambda').invoke(
        FunctionName=env.scheduler_lambda,
        InvocationType='Event',
        Payload=new_granules_json,
    )


def setup_env():
    env.is_production = True

    env.bucket = os.environ['PREVIOUS_TIME_BUCKET']
    env.scheduler_lambda = os.environ['SCHEDULER_LAMBDA_NAME']
