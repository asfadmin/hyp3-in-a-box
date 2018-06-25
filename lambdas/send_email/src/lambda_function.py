import os

from environment import environment
import sns
import render
import ses


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

    finish_event = sns.get_hyp3_event_from(aws_event)

    subject, address = finish_event.subject, finish_event.address
    message = render.email_with(finish_event)

    ses.send(
        address,
        subject,
        message
    )


def setup_env():
    environment.source_email = os.environ['SOURCE_EMAIL']
