import os

from send_email_env import environment
from send_email_main import send_email_main


def lambda_handler(aws_event, aws_context):
    """ AWS Lambda entry point. Renders an email for the given parameters and
    sends it via SES.

    The function first looks for an associated user in the HyP3 database. If no
    user can be found, or the user has unsubscribed from email notifications
    (by setting ``wants_email`` to false), the function will quit without doing
    anything.

        :param aws_event: lambda event data

            * Records - Top level object from sns trigger event
                * Sns - sns notification data
                    * Message json serialized `Hyp3Event`

        :param aws_context: lambda runtime info
    """
    setup_env()
    send_email_main(aws_event)


def setup_env():
    environment.source_email = os.environ['SOURCE_EMAIL']
    environment.api_url = os.environ['API_URL']
