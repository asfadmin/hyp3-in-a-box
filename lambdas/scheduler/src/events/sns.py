import boto3
import json

from environment import environment

sns = boto3.client('sns')


def push(subject, payload):
    return sns.publish(
        TopicArn=environment.sns_arn,
        Subject="Hyp3 Notify Only",
        Message=json.dumps(payload)
    )
