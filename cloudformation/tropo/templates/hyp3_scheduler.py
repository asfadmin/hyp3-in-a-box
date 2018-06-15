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

from troposphere import GetAtt, Parameter, Ref
from troposphere.awslambda import Environment, Function
from troposphere.iam import Policy, Role

from environment import environment
from template import t

from . import utils
from .hyp3_sns import finish_sns

source_zip = "scheduler.zip"


print('  adding scheduler lambda')

lambda_name = t.add_parameter(Parameter(
    "SchedulerName",
    Description="Name of the Scheduler lambda function (Optional)",
    Default="hyp3_scheduler",
    Type="String"
))

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
    FunctionName=Ref(lambda_name),
    Code=utils.make_lambda_code(
        S3Bucket=environment.lambda_bucket,
        S3Key="{maturity}/{zip}".format(
            maturity=environment.maturity,
            zip=source_zip
        ),
        S3ObjectVersion=environment.scheduler_version
    ),
    Handler="lambda_function.lambda_handler",
    Role=GetAtt(lambda_role, "Arn"),
    Runtime="python3.6",
    Environment=Environment(
        Variables={
            'SNS_ARN': Ref(finish_sns),
            'DB_HOST': environment.db_host,
            'DB_USER': environment.db_user,
            'DB_PASSWORD': environment.db_pass,
            'DB_NAME': environment.db_name
        }),
    MemorySize=128,
    Timeout=300
))
