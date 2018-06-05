from template import t

import troposphere as ts
from troposphere import awslambda
from troposphere import iam

print('adding find_new lambda')


AppendItemToListFunction = t.add_resource(awslambda.Function(
    "AppendItemToListFunction",
    Code=awslambda.Code(
        S3Bucket="some-bucket",
        S3Key="my-code.zip"
    ),
    Handler="index.handler",
    Role=ts.GetAtt("LambdaExecutionRole", "Arn"),
    Runtime="python3.6",
    MemorySize=128,
    Timeout=60
))

lambda_policy = iam.Policy(
    PolicyName="root",
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Action": ["logs:*"],
            "Resource": "arn:aws:logs:*:*:*",
            "Effect": "Allow"
        }]
    })

policy_doc = {
    "Version": "2012-10-17",
    "Statement": [{
        "Action": ["sts:AssumeRole"],
        "Effect": "Allow",
        "Principal": {
            "Service": ["lambda.amazonaws.com"]
        }
    }]
}

LambdaExecutionRole = t.add_resource(iam.Role(
    "LambdaExecutionRole",
    Path="/",
    Policies=[lambda_policy],
    AssumeRolePolicyDocument=policy_doc,
))
