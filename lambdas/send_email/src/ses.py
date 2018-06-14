import boto3

from environment import environment

ses = boto3.client('ses')

SOURCE_EMAIL = 'wbhorn@alaska.edu'
SUBJECT_PREFIX = '[hyp3]'


def send(address, subject, message):
    ses.send_email(
        Source=environment.source_email,
        Destination={
            'ToAddresses': [address]
        },
        Message={
            'Subject': {
                'Data': f'{SUBJECT_PREFIX} {subject}'
            },
            'Body': {
                'Html': {
                    'Data': message
                }
            }
        },
        ReplyToAddresses=['no-reply@alaska.edu']
    )
