import boto3

from environment import environment

sns = boto3.client('sns')


def push(subject, payload):
    return sns.publish(
        TopicArn=environment.sns_arn,
        Subject=subject,
        Message=payload
    )
