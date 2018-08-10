# hyp3_custom_metric.py
# Rohan Weeden
# Created: August 9, 2018

"""
Troposphere template responsible for generating :ref:`custom_metric_lambda`.

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3
* **Cloudwatch Event:** Triggers the lambda after a scheduled amount of time
* **IAM Policies:**

  * Lambda basic execution
  * Allow read access to StartEvents number of unread messages
  * Allow read access to AutoScalingGroups in order to get number of active processing instances
  * Allow write access to CloudWatch custom metrics
  * Allow cloudwatch event to trigger the lambda

"""

from awacs.aws import Allow, Policy, Statement
from awacs.autoscaling import DescribeAutoScalingGroups
from awacs.sqs import GetQueueAttributes
from awacs.cloudwatch import PutMetricData
from troposphere import GetAtt, Ref, Sub
from troposphere.awslambda import Environment, Permission
from troposphere.events import Rule, Target
from troposphere.iam import Role
from troposphere.iam import Policy as IAMPolicy

from template import t

from . import utils
from .hyp3_kms_key import kms_key
from .hyp3_sqs import start_events
from .hyp3_autoscaling_group import processing_group, custom_metric_name

source_zip = "custom_metric.zip"


print('  adding custom_metric lambda')


describe_autoscale = IAMPolicy(
    PolicyName="DescribeAutoScalingGroups",
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[DescribeAutoScalingGroups],
                Resource=["*"]
            )
        ]
    )
)

get_queue_attributes = IAMPolicy(
    PolicyName="GetQueueAttributes",
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[GetQueueAttributes],
                Resource=[GetAtt(start_events, "Arn")]
            )
        ]
    )
)

put_metric_data = IAMPolicy(
    PolicyName="PutMetricData",
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[PutMetricData],
                Resource=["*"]
            )
        ]
    )
)

role = t.add_resource(Role(
    "CustomMetricExecutionRole",
    Path="/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
    Policies=[
        describe_autoscale,
        get_queue_attributes,
        put_metric_data
    ],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))

custom_metric = t.add_resource(utils.make_lambda_function(
    name='custom_metric',
    role=role,
    lambda_params={
        "KmsKeyArn": GetAtt(kms_key, "Arn"),
        "Environment": Environment(
            Variables={
                "Hyp3StackName": Ref("AWS::StackName")
            }
        ),
        "Timeout": 60
    }
))

custom_metric_target = Target(
    "CustomMetricTarget",
    Arn=GetAtt(custom_metric, 'Arn'),
    Id="CustomMetricFunction1",
    Input=Sub(
        '{"QueueUrl":"${QueueUrl}","AutoScalingGroupName":"${AGName}","MetricName":"${MetricName}"}',
        QueueUrl=Ref(start_events),
        AGName=Ref(processing_group),
        MetricName=custom_metric_name
    )
)

custom_metric_rule = t.add_resource(Rule(
    "CustomMetricSchedule",
    ScheduleExpression="rate(1 minute)",
    State="ENABLED",
    Targets=[custom_metric_target]
))

PermissionForEventsToInvokeLambda = t.add_resource(Permission(
    "EventScheduleCustomMetricPermissions",
    FunctionName=Ref(custom_metric),
    Action="lambda:InvokeFunction",
    Principal="events.amazonaws.com",
    SourceArn=GetAtt(custom_metric_rule, "Arn")
))
