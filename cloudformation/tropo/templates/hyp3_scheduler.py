# hyp3_scheduler.py
# Rohan Weeden
# Created: June 12, 2018

"""
Troposphere template responsible for generating :ref:`scheduler_lambda`.

Requires
~~~~~~~~
* :ref:`sns_template`
* :ref:`kms_key_template`
* :ref:`rds_template`
* :ref:`db_params_template`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3
* **SNS Topic:** This is where notify only/finish events get put
* **IAM Policies:**

  * Lambda basic execution
  * SNS publish access

"""

from tropo_env import environment
from template import t
from troposphere import GetAtt, Ref
from troposphere.awslambda import Environment, VPCConfig
from troposphere.iam import Policy, Role

from . import utils
from .hyp3_db_params import db_name, db_super_user_pass, db_super_user
from .hyp3_kms_key import kms_key
from .hyp3_sns import finish_sns

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
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
        "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
    ],
    Policies=[sns_policy],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))


scheduler = utils.make_lambda_function(
    name="scheduler",
    role=lambda_role,
    lambda_params={
        "Environment": Environment(
            Variables={
                'SNS_ARN': Ref(finish_sns),
                'DB_HOST': utils.get_host_address(),
                'DB_USER': Ref(db_super_user),
                'DB_PASSWORD': Ref(db_super_user_pass),
                'DB_NAME': Ref(db_name)
            }),
        "KmsKeyArn": GetAtt(kms_key, "Arn"),
        "MemorySize": 128,
        "Timeout": 300
    }
)

if 'unittest' in environment.maturity:
    scheduler.VpcConfig = VPCConfig(
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

t.add_resource(scheduler)
