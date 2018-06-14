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

from troposphere import GetAtt, Parameter, Ref
from troposphere.awslambda import Function
from troposphere.iam import Role

from . import utils

source_zip = "scheduler.zip"


print('adding scheduler lambda')


lambda_name = t.add_parameter(Parameter(
    "SchedulerName",
    Description="Name of the Scheduler lambda function",
    Default="hyp3_scheduler",
    Type="String"
))

lambda_role = t.add_resource(Role(
    "SchedulerExecutionRole",
    Path="/service-role/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))


lambda_function = t.add_resource(Function(
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
    Runtime="python3.6"
))
