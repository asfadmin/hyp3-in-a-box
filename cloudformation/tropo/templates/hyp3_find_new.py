"""
Troposphere template responsible for generating :ref:`find_new_lambda`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3.
* **S3 Bucket:** Used to store the previous runtimes of the lambda.
* **Cloudwatch Event:** Triggers the lambda after a scheduled amount of time.
* **IAM Policies:**

  * Lambda basic execution
  * S3 read/write on ``previous time`` bucket
  * Allow cloudwatch event to trigger the lambda

"""

from template import t
from environment import environment

import troposphere as ts
from troposphere import awslambda
from troposphere import iam
from troposphere import events
from troposphere import s3

from . import utils

source_zip = "find_new_granules.zip"


print('adding find_new lambda')

previous_time_bucket = t.add_resource(s3.Bucket("S3Bucket"))

logs_policy = iam.Policy(
    PolicyName="LogAccess",
    PolicyDocument=utils.get_static_policy('logs-policy')
)

prev_time_s3_policy = iam.Policy(
    PolicyName='PreviousTimeS3ReadWriteAccess',
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:HeadObject"
            ], "Resource": ts.Join("/", [
                ts.GetAtt(previous_time_bucket, "Arn"), '*'
            ])
        }]}
)

lambda_exe_role = t.add_resource(iam.Role(
    "FindNewExecutionRole",
    Path="/",
    Policies=[logs_policy, prev_time_s3_policy],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))

find_new_granules_function = t.add_resource(awslambda.Function(
    "Hyp3FindNewGranulesFunction",
    FunctionName="hyp3-find-new-granules",
    Code=awslambda.Code(
        S3Bucket=environment.lambda_bucket,
        S3Key="{maturity}/{zip}".format(
            maturity=environment.maturity,
            zip=source_zip
        ),
        S3ObjectVersion=environment.find_new_version
    ),
    Handler='lambda_function.lambda_handler',
    Environment=awslambda.Environment(
        Variables={'PREVIOUS_TIME_BUCKET': ts.Ref(previous_time_bucket)}
    ),
    Role=ts.GetAtt(lambda_exe_role, 'Arn'),
    Runtime='python3.6',
    MemorySize=128,
    Timeout=300
))

find_new_target = events.Target(
    "FindNewTarget",
    Arn=ts.GetAtt("Hyp3FindNewGranulesFunction", 'Arn'),
    Id="FindNewFunction1"
)

find_new_event_rule = t.add_resource(events.Rule(
    "FindNewGranulesSchedule",
    ScheduleExpression="rate(1 minute)",
    State="ENABLED",
    Targets=[find_new_target]
))

PermissionForEventsToInvokeLambda = t.add_resource(awslambda.Permission(
    "SchedulePermissions",
    FunctionName=ts.Ref("Hyp3FindNewGranulesFunction"),
    Action="lambda:InvokeFunction",
    Principal="events.amazonaws.com",
    SourceArn=ts.GetAtt("FindNewGranulesSchedule", "Arn")
))
