import schedule


def lambda_handler(event, context):
    """Entry point for the lambda to run.

       :param event: lambda event data
       :param context: lambda runtime info
    """
    new_granules = event['new_granules']

    schedule.hyp3_jobs(new_granules)
