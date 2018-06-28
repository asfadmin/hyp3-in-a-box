# hyp3_scheduler.py
# Rohan Weeden
# Created: June 12, 2018

"""
Troposphere template responsible for generating :ref:`scheduler_lambda`

Requires
~~~~~~~~
* :ref:`sns_template`
* :ref:`kms_key_template`
* :ref:`rds_template`
* :ref:`db_params_template`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3.
* **SNS Topic:** This is where notify only/finish events get put.
* **IAM Policies:**

  * Lambda basic execution
  * SNS publish access

"""

from environment import environment
from template import t
from troposphere import GetAtt, Parameter, Ref
from troposphere.awslambda import Environment, Function, VPCConfig
from troposphere.iam import Policy, Role

from . import utils
from .hyp3_db_params import db_name, db_pass, db_user
from .hyp3_kms_key import kms_key
from .hyp3_sns import finish_sns

source_zip = "scheduler.zip"


print('  adding scheduler lambda')

lambda_name = t.add_parameter(Parameter(
    "LambdaSchedulerName",
    Description="Name of the Scheduler lambda function",
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
            'DB_HOST': utils.get_host_address(),
            'DB_USER': Ref(db_user),
            'DB_PASSWORD': Ref(db_pass),
            'DB_NAME': Ref(db_name)
        }),
    "KmsKeyArn": GetAtt(kms_key, "Arn"),
    "MemorySize": 128,
    "Timeout": 300
}

if 'unittest' in environment.maturity:
    scheduler_args['VpcConfig'] = VPCConfig(
        SecurityGroupIds=[
            'sg-0d8cdb7c',
            'sg-72f8c803'
        ],
        SubnetIds=[
            'subnet-e3495984',
            'subnet-77ecc73e',
            'subnet-2efd4975'
        ]
    )

scheduler = t.add_resource(Function(
    "SchedulerFunction",
    **scheduler_args
))
