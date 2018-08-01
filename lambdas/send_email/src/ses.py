import boto3

from send_email_env import environment

ses = boto3.client('ses')

SUBJECT_PREFIX = '[hyp3]'


def send(address, subject, message):
    ses.send_email(
        Source=environment.source_email,
        Destination={
            'ToAddresses': [address]
        },
        Message={
            'Subject': {
                'Data': '{} {}'.format(SUBJECT_PREFIX, subject)
            },
            'Body': {
                'Html': {
                    'Data': message
                }
            }
        },
        ReplyToAddresses=['no-reply@alaska.edu']
    )
