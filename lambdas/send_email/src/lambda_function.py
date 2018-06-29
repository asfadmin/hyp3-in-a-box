import os

from environment import environment
from send_email_main import send_email_main


def lambda_handler(aws_event, aws_context):
    """ AWS Lambda entry point. Renders an email for the given parameters and
    sends it via SES.

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
