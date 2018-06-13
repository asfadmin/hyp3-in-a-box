import hyp3_schedule
import events


def lambda_handler(event, context):
    """ Entry point for the lambda to run.

        :param event: lambda event data

            * new_granules - A list of granules to process
        :param context: lambda runtime info
    """
    new_granules = event['new_granules']
    job_packages = hyp3_schedule.hyp3_jobs(new_granules)

    notify_only_events = events.make_notify_event(job_packages)

    events.send(notify_only_events)

