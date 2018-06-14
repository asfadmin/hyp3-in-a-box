import boto3
import hyp3_events

from render_email import Email

ses = boto3.client('ses')


def render():
    params = {
        'download_url': 'www.hello.html',
        'subject': 'New Data For Subscription',
        'browse_url': 'https://hyp3-download.asf.alaska.edu/hyp3/browse/dis_mag+S1_20180504T033546_S1_20180528T033547+256-64_50-10_0.00-0.08_2_geo.png',
        'additional_info': [
            {'name': 'granule name', 'value': '777778'}
        ]

    }

    email = Email('email.html.j2').render(**params)
    return email


def lambda_handler(event, aws_context):
    """ AWS Lambda entry point. Renders an email for the given parameters and
    sends it via SES.

        :param event: lambda event data

            * body - Email parameters
                * context - The Jinja2 template context
                * to_addresses - List of addresses to send the email to
        :param context: lambda runtime info
    """
    sns_record = event['Records'].pop()['Sns']
    event_json = sns_record['Message']

    notify_event = hyp3_events.NotifyOnlyEvent.from_json(event_json)

    # TODO: This is just a hack for testing
    if 'wbhorn@alaska.edu' not in notify_event.address:
        print('TESTING!! not sending to address {}'.format(
            notify_event.address
        ))
        notify_event.address = 'wbhorn@alaska.edu'

    to_addresses = [notify_event.address]

    context = notify_event.to_dict()
    message = Email('email.html.j2').render(**context)

    ses.send_email(
        Source='wbhorn@alaska.edu',
        Destination={
            'ToAddresses': to_addresses
        },
        Message={
            'Subject': {
                'Data': f'[hyp3] {notify_event.subject}'
            },
            'Body': {
                'Html': {
                    'Data': message
                }
            }
        },
        ReplyToAddresses=['no-reply@alaska.edu']
    )


if __name__ == "__main__":
    with open('output.html', 'w') as f:
        f.write(render())
