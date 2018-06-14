from environment import environment
import sns
import render
import ses
import os


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

    notify_event = sns.get_hyp3_event_from(aws_event)

    address = get_address(notify_event)

    message = render.email_with(notify_event)
    subject = notify_event.subject

    ses.send(
        address,
        subject,
        message
    )


def setup_env():
    environment.source_email = os.environ['SOURCE_EMAIL']


def get_address(event):
    # TODO: This is just temperary for testing
    print('TESTING: got email from {event.address}')
    return 'wbhorn@alaska.edu'
