# hyp3_scheduler.py
# Rohan Weeden
# Created: June 12, 2018

"""
Troposphere template responsible for generating :ref:`scheduler_lambda`

Requires
~~~~~~~~
* :ref:`sns_template`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3.
* **SNS Topic:** This is where notify only/finish events get put.
* **IAM Policies:**

  * Lambda basic execution
  * SNS publish access

"""

from troposphere import GetAtt, Parameter, Ref
from troposphere.awslambda import Environment, Function, VPCConfig
from troposphere.iam import Policy, Role

from environment import environment
from template import t

from . import utils
from .hyp3_sns import finish_sns
from .hyp3_db_params import db_pass, db_user, db_name
from .hyp3_kms_key import kms_key

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
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
        "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
    ],
    Policies=[sns_policy],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))


scheduler_args = {
    "FunctionName": Ref(lambda_name),
    "Code": utils.make_lambda_code(
        S3Bucket=environment.lambda_bucket,
        S3Key="{maturity}/{source_zip}".format(
            maturity=environment.maturity,
            source_zip=source_zip
        ),
        S3ObjectVersion=environment.scheduler_version
    ),
    "Handler": "lambda_function.lambda_handler",
    "Role": GetAtt(lambda_role, "Arn"),
    "Runtime": "python3.6",
    "Environment": Environment(
        Variables={
            'SNS_ARN': Ref(finish_sns),
            'DB_HOST': environment.db_host,
            'DB_USER': Ref(db_user),
            'DB_PASSWORD': Ref(db_pass),
            'DB_NAME': Ref(db_name)
        }),
    "KmsKeyArn": GetAtt(kms_key, "Arn"),
    "MemorySize": 128,
    "Timeout": 300
}

if 'test' in environment.maturity:
    scheduler_args['VpcConfig'] = VPCConfig(
        SecurityGroupIds=[
            'sg-0d8cdb7c'
        ],
        SubnetIds=[
            'subnet-dc7dcaab',
            'subnet-c78f1ea2',
            'subnet-b66fa5ef'
        ]
    )

scheduler = t.add_resource(Function(
    "SchedulerFunction",
    **scheduler_args
))
