from template import t

import troposphere as ts
from troposphere import awslambda
from troposphere import iam

from . import utils

print('adding find_new lambda')


AppendItemToListFunction = t.add_resource(awslambda.Function(
    "Hyp3FindNewGranulesFunction",
    Code=awslambda.Code(
        S3Bucket="hyp3-in-a-box-source",
        S3Key="find_new_granules.zip"
    ),
    Handler="lambda_function.lambda_handler",
    Role=ts.GetAtt("LambdaExecutionRole", "Arn"),
    Runtime="python3.6",
    MemorySize=128,
    Timeout=60
))

logs_policy = iam.Policy(
    PolicyName="LogAccess",
    PolicyDocument=utils.get_policy('logs-policy')
)

prev_time_s3_policy = iam.Policy(
    PolicyName='PreviousTimeS3ReadWriteAccess',
    PolicyDocument=utils.get_policy('previous-time-read-write')
)


LambdaExecutionRole = t.add_resource(iam.Role(
    "LambdaExecutionRole",
    Path="/",
    Policies=[logs_policy, prev_time_s3_policy],
    AssumeRolePolicyDocument=utils.get_policy('lambda-policy-doc'),
))
