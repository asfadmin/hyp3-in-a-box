"""
Troposphere template responsible for generating :ref:`find_new_lambda`.

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3
* **S3 Bucket:** Used to store the previous runtimes of the lambda
* **Cloudwatch Event:** Triggers the lambda after a scheduled amount of time
* **IAM Policies:**

  * Lambda basic execution
  * S3 read/write on ``previous time`` bucket
  * Allow cloudwatch event to trigger the lambda

"""

from troposphere import GetAtt, Ref, awslambda, events, iam, Sub
from troposphere.ssm import Parameter as SSMParameter

from template import t

from . import hyp3_scheduler, utils

source_zip = "find_new_granules.zip"


print('  adding find_new lambda')


ssm_previous_time = t.add_resource(SSMParameter(
    "Hyp3SSMParameterPerviousTime",
    Name=Sub(
        "/${StackName}/previous_time.json",
        StackName=Ref("AWS::StackName")
    ),
    Type="String",
    Value="_"
))

logs_policy = iam.Policy(
    PolicyName="LogAccess",
    PolicyDocument=utils.get_static_policy('logs-policy')
)

ssm_arn = "arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:parameter${ParamName}"
prev_time_s3_policy = iam.Policy(
    PolicyName='PreviousTimeSSMReadWriteAccess',
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "ssm:PutParameter",
                "ssm:GetParameter"
            ], "Resource": Sub(
                ssm_arn,
                ParamName=Ref(ssm_previous_time)
            )
        }]
    }
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

find_new_granules = t.add_resource(utils.make_lambda_function(
    name="find_new_granules",
    role=lambda_exe_role,
    lambda_params={
        "Environment": awslambda.Environment(
            Variables={
                'PREVIOUS_TIME_SSM_PARAM_NAME': Ref(ssm_previous_time),
                'SCHEDULER_LAMBDA_NAME': Ref(hyp3_scheduler.scheduler)
            }),
        "MemorySize": 128,
        "Timeout": 300
    }
))


find_new_target = events.Target(
    "FindNewTarget",
    Arn=GetAtt(find_new_granules, 'Arn'),
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
    FunctionName=Ref(find_new_granules),
    Action="lambda:InvokeFunction",
    Principal="events.amazonaws.com",
    SourceArn=GetAtt("FindNewGranulesSchedule", "Arn")
))
