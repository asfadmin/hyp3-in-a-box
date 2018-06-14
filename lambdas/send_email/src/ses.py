
import boto3

ses = boto3.client('ses')

SOURCE_EMAIL = 'wbhorn@alaska.edu'
SUBJECT_PREFIX = '[hyp3]'


def send(address, subject, message):
    ses.send_email(
        Source=SOURCE_EMAIL,
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
