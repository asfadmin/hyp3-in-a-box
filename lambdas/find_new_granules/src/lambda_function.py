import os

import boto3

import find_new
import results


def lambda_handler(event, context):
    """ Entry point for the lambda to run.

        :param event: lambda event data
        :param context: lambda runtime info
    """
    setup_env()

    search_results = find_new.granules()

    new_granule_events = results.package(search_results)
    events_json = results.format_into_json(new_granule_events)

    start_scheduler_with(events_json)


def start_scheduler_with(new_granules_json):
    boto3.client('lambda').invoke(
        FunctionName=find_new.environment.scheduler_lambda,
        InvocationType='Event',
        Payload=new_granules_json,
    )


def setup_env():
    find_new.environment.maturity = 'prod'

    find_new.environment.bucket = os.environ['PREVIOUS_TIME_BUCKET']
    find_new.environment.scheduler_lambda = os.environ['SCHEDULER_LAMBDA_NAME']
