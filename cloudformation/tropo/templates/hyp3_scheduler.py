# hyp3_scheduler.py
# Rohan Weeden
# Created: June 12, 2018

"""
Troposphere template responsible for generating :ref:`scheduler_lambda`.

Requires
~~~~~~~~
* :ref:`db_params_template`
* :ref:`kms_key_template`
* :ref:`sns_template`
* :ref:`sqs_template`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3
* **IAM Role:**

  * Lambda basic execution policy
  * SNS publish policy
  * SQS send message policy
"""

from template import t
from tropo_env import environment
from troposphere import GetAtt, Ref
from troposphere.awslambda import Environment, VPCConfig
from troposphere.iam import Policy, Role

from . import utils
from .hyp3_db_params import db_name, db_pass, db_user
from .hyp3_kms_key import kms_key
from .hyp3_sns import finish_sns
from .hyp3_sqs import start_events

source_zip = "scheduler.zip"


print('  adding scheduler lambda')

sns_policy = Policy(
    PolicyName='EmailEventSNSPublish',
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": Ref(finish_sns)
        }]
    }
)

sqs_policy = Policy(
    PolicyName='StartEventSQSSend',
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "sqs:SendMessage",
            "Resource": GetAtt(start_events, 'Arn')
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
    Policies=[sns_policy, sqs_policy],
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
                'DB_USER': Ref(db_user),
                'DB_PASSWORD': Ref(db_pass),
                'DB_NAME': Ref(db_name),
                'QUEUE_URL': Ref(start_events)
            }
        ),
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
