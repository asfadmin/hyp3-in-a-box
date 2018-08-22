import os
import json

import boto3

import find_new


def lambda_handler(event, context):
    """ Entry point for the lambda to run.

        :param event: lambda event data
        :param context: lambda runtime info
    """
    print(json.dumps(event))
    setup_env()

    new_granule_events = find_new.granule_events()

    if not any_new_granules(new_granule_events):
        print('No new granules. Done.')
        return

    events_json = format_as_json(new_granule_events)
    start_scheduler_with(events_json)


def format_as_json(new_granules_events):
    event_dicts = [e.to_dict() for e in new_granules_events]

    return json.dumps({
        'new_granules': event_dicts
    })


def any_new_granules(granules):
    return len(granules) > 1


def start_scheduler_with(new_granules_json):
    print('Scheduling job')
    boto3.client('lambda').invoke(
        FunctionName=find_new.environment.scheduler_lambda,
        InvocationType='Event',
        Payload=new_granules_json,
    )


def setup_env():
    find_new.environment.maturity = 'prod'

    find_new.environment.scheduler_lambda = os.environ['SCHEDULER_LAMBDA_NAME']
    find_new.environment.ssm_previous_time_name = \
        os.environ['PREVIOUS_TIME_SSM_PARAM_NAME']
