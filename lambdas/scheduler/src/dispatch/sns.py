import boto3

from scheduler_env import environment

sns = boto3.client('sns')


def push(subject, payload):
    return sns.publish(
        TopicArn=environment.sns_arn,
        Subject=subject,
        Message=payload
    )
