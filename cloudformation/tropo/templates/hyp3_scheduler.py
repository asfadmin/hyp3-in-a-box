# hyp3_scheduler.py
# Rohan Weeden
# Created: June 12, 2018

"""
Troposphere template responsible for generating :ref:`scheduler_lambda`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3.
* **IAM Policies:**

  * Lambda basic execution
"""

from template import t
from environment import environment

from troposphere import GetAtt, Ref
from troposphere.awslambda import Function, Environment
from troposphere.iam import Role, Policy

from .hyp3_sns import finish_sns
from . import utils

source_zip = "scheduler.zip"


print('  adding scheduler lambda')


sns_policy = Policy(
    PolicyName='FinishEventSNSPublish',
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": Ref(finish_sns)
        }]
    }
)

lambda_role = t.add_resource(Role(
    "SchedulerExecutionRole",
    Path="/service-role/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
    Policies=[sns_policy],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))


scheduler = t.add_resource(Function(
    "SchedulerFunction",
    Code=utils.get_lambda_code(source_zip),
    Handler="lambda_function.lambda_handler",
    Role=GetAtt(lambda_role, "Arn"),
    Runtime="python3.6",
    Environment=Environment(
        Variables={
            'SNS_ARN': Ref(finish_sns),
            'DB_HOST': environment.db_host,
            'DB_USER': environment.db_user,
            'DB_PASSWORD': environment.db_pass
        }),
    MemorySize=128,
    Timeout=300
))
