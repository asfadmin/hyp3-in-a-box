# hyp3_sqs.py
# William Horn
# Created: June, 2018

"""
Troposphere template responsible for generating SQS job queues.

Resources
~~~~~~~~~

* **SQS Fifo:**

  * Start Events queue for incoming jobs
  * Failed Events queue for failed start events

"""

from template import t
from troposphere import GetAtt, Ref, Sub
from troposphere.sqs import Queue, RedrivePolicy
from troposphere.ssm import Parameter

print('  adding sqs')


def hours_in_seconds(n):
    return n * 60 * 60


failed_start_evets = t.add_resource(Queue(
    "FailedStartEvents",
    FifoQueue=True,
    ContentBasedDeduplication=True,
))

start_events = t.add_resource(Queue(
    "HyP3StartEvents",
    FifoQueue=True,
    ContentBasedDeduplication=True,
    RedrivePolicy=RedrivePolicy(
        deadLetterTargetArn=GetAtt(failed_start_evets, "Arn"),
        maxReceiveCount=1,
    ),
    VisibilityTimeout=hours_in_seconds(3)
))

ssm_queue_name = t.add_resource(Parameter(
    "HyP3SSMParameterStartEventQueueName",
    Name=Sub(
        "/${StackName}/StartEventQueueName",
        StackName=Ref("AWS::StackName")
    ),
    Type="String",
    Value=GetAtt(start_events, "QueueName")
))
