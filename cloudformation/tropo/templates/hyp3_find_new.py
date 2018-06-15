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

import troposphere as ts
from troposphere import awslambda, events, iam, s3

from template import t

from . import utils
from . import hyp3_scheduler

source_zip = "find_new_granules.zip"


print('  adding find_new lambda')


lambda_name = t.add_parameter(ts.Parameter(
    "FindNewName",
    Description="Name of the find new granules lambda function (Optional).",
    Default="hyp3_find_new",
    Type="String"
))


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

lambda_invoke = iam.Policy(
    PolicyName='FindNewLambdaInvoke',
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:InvokeAsync"
            ],
            "Resource": "*"
        }
        ]
    }
)


lambda_exe_role = t.add_resource(iam.Role(
    "FindNewExecutionRole",
    Path="/",
    Policies=[logs_policy, prev_time_s3_policy, lambda_invoke],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))

find_new_granules_function = t.add_resource(awslambda.Function(
    "Hyp3FindNewGranulesFunction",
    FunctionName=ts.Ref(lambda_name),
    Code=utils.make_lambda_code(source_zip),
    Handler='lambda_function.lambda_handler',
    Environment=awslambda.Environment(
        Variables={
            'PREVIOUS_TIME_BUCKET': ts.Ref(previous_time_bucket),
            'SCHEDULER_LAMBDA_NAME': ts.Ref(hyp3_scheduler.scheduler)}
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
    "EventSchedulePermissions",
    FunctionName=ts.Ref("Hyp3FindNewGranulesFunction"),
    Action="lambda:InvokeFunction",
    Principal="events.amazonaws.com",
    SourceArn=ts.GetAtt("FindNewGranulesSchedule", "Arn")
))
