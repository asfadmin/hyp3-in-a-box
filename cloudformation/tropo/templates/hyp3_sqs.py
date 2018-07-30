# hyp3_sqs.py
# William Horn
# Created: June, 2018

"""
Troposphere template responsible for generating SQS job queues.

Resources
~~~~~~~~~

* **SQS Fifo:**

  * Start Events queue for incoming jobs
  * Failed Events queue for jobs which are not correctly recieved from the Start Events queue

"""

from troposphere import GetAtt, Ref, Sub
from troposphere.sqs import Queue, RedrivePolicy
from troposphere.ssm import Parameter

from template import t

print('  adding sqs')

failed_start_evets = t.add_resource(Queue(
    "FailedStartEvents",
    FifoQueue=True,
    ContentBasedDeduplication=True,
))

start_events = t.add_resource(Queue(
    "Hyp3StartEvents",
    FifoQueue=True,
    ContentBasedDeduplication=True,
    RedrivePolicy=RedrivePolicy(
        deadLetterTargetArn=GetAtt(failed_start_evets, "Arn"),
        maxReceiveCount=1,
    )
))

ssm_queue_name = t.add_resource(Parameter(
    "Hyp3SSMParameterStartEventQueueName",
    Name=Sub(
        "/${StackName}/StartEventQueueName",
        StackName=Ref("AWS::StackName")
    ),
    Type="String",
    Value=GetAtt(start_events, "QueueName")
))
