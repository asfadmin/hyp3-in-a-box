import os

from environment import environment
import schedule
import events


def lambda_handler(event, context):
    """ Entry point for the lambda to run.

        :param event: lambda event data

            * new_granules - A list of granules to process
        :param context: lambda runtime info
    """
    set_environment_variables()

    new_granules = event['new_granules']
    job_packages = schedule.hyp3_jobs(new_granules)

    notify_only_events = events.make_notify_events(job_packages)

    events.send(notify_only_events)


def set_environment_variables():
    environment.db_creds = [
        os.environ[k] for k in ['DB_HOST', 'DB_USER', 'DB_PASSWORD']
    ]

    environment.sns_arn = os.environ['SNS_ARN']
