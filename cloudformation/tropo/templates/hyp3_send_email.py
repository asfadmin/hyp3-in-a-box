# hyp3_send_email.py
# Rohan Weeden
# Created: June 5, 2018

# Troposphere template for send_email lambda

import troposphere as ts
from template import t
from troposphere.awslambda import Code, Function
from troposphere.iam import Policy, Role

print('adding send_email lambda')


lambda_policy = Policy(
    PolicyName="SESSendEmail",
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Action": ["ses:SendEmail"],
            "Resource": "*",
            "Effect": "Allow"
        }]
    })

send_email_role = t.add_resource(Role(
    "SendEmailExecutionRole",
    Path="/service-role/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
    Policies=[lambda_policy],
    AssumeRolePolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Action": ["sts:AssumeRole"],
            "Effect": "Allow",
            "Principal": {
                "Service": ["lambda.amazonaws.com"]
            }
        }]
    },
))

send_email = t.add_resource(Function(
    "SendEmailFunction",
    FunctionName="hyp3_send_email",
    Code=Code(
        S3Bucket="some-bucket",
        S3Key="my-code.zip"
    ),
    Handler="lambda_function.lambda_handler",
    Role=ts.GetAtt(send_email_role, "Arn"),
    Runtime="python3.6"
))
