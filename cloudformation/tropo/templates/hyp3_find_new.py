from template import t

import troposphere as ts
from troposphere import awslambda
from troposphere import iam
from troposphere import events

from . import utils
from .hyp3_s3_buckets import previous_time_bucket

print('adding find_new lambda')


find_new_granules_function = t.add_resource(awslambda.Function(
    "Hyp3FindNewGranulesFunction",
    FunctionName="hyp3-find-new-granules",
    Code=awslambda.Code(
        S3Bucket="hyp3-in-a-box-lambdas",
        S3Key="find_new_granules.zip"
    ),
    Handler='lambda_function.lambda_handler',
    Environment=awslambda.Environment(
        Variables={'PREVIOUS_TIME_BUCKET': ts.Ref(previous_time_bucket)}
    ),
    Role=ts.GetAtt('LambdaExecutionRole', 'Arn'),
    Runtime='python3.6',
    MemorySize=128,
    Timeout=300
))

logs_policy = iam.Policy(
    PolicyName="LogAccess",
    PolicyDocument=utils.get_static_policy('logs-policy')
)

prev_time_s3_policy = iam.Policy(
    PolicyName='PreviousTimeS3ReadWriteAccess',
    PolicyDocument=utils.get_static_policy(
        'previous-time-s3-rw',
        update_with={
            "Resource": ts.Join("/", [
                ts.GetAtt(previous_time_bucket, "Arn"),
                '*'
            ])
        }
    )
)

lambda_exe_role = t.add_resource(iam.Role(
    "LambdaExecutionRole",
    Path="/",
    Policies=[logs_policy, prev_time_s3_policy],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))

find_new_target = events.Target(
    "FindNewTarget",
    Arn=ts.GetAtt("Hyp3FindNewGranulesFunction", 'Arn'),
    Id="FindNewFunction1"
)

find_new_event_rule = t.add_resource(events.Rule(
    "FindNewSchedule",
    ScheduleExpression="rate(10 minutes)",
    State="ENABLED",
    Targets=[find_new_target]
))
