import hyp3_schedule


def lambda_handler(event, context):
    """ Entry point for the lambda to run.

        :param event: lambda event data

            * new_granules - A list of granules to process
        :param context: lambda runtime info
    """
    new_granules = event['new_granules']

    hyp3_schedule.hyp3_jobs(new_granules)
