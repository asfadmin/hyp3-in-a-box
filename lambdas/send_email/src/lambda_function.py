import sns
import render
import ses


def lambda_handler(aws_event, aws_context):
    """ AWS Lambda entry point. Renders an email for the given parameters and
    sends it via SES.

        :param event: lambda event data

            * body - Email parameters
                * context - The Jinja2 template context
                * to_addresses - List of addresses to send the email to
        :param context: lambda runtime info
    """
    notify_event = sns.get_hyp3_event_from(aws_event)

    address = get_address(notify_event)

    message = render.email_with(notify_event)
    subject = notify_event.subject

    ses.send(
        address,
        subject,
        message
    )


def get_address(event):
    # TODO: This is just temperary for testing
    print('TESTING: got email from {event.address}')
    return 'wbhorn@alaska.edu'
