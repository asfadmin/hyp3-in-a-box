import template as t
from tropo_env import environment
from troposphere import GetAtt, Ref
from troposphere.awslambda import Environment, VPCConfig
from troposphere .iam import Policy, Role
from .hyp3_kms_key import kms_key

from . import utils
from .hyp3_sns import finish_sns
from .hyp3_sqs import start_events

source_zip = "dispatcher.zip"

print("adding dispatcher lambda")

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
    "DispatcherExecutionRole",
    Path="/service-role/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
        "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
    ],
    Policies=[sns_policy, sqs_policy],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))

dispatcher = utils.make_lambda_function(
    name="dispatcher",
    role=lambda_role,
    lambda_params={
        "Environment": Environment(
            Variables={
                'SNS_ARN': Ref(finish_sns),
                'QUEUE_URL': Ref(start_events)
            }
        ),
        "KmsKeyArn": GetAtt(kms_key, "Arn"),
        "MemorySize": 128,
        "Timeout": 300
    }
)

if 'unittest' in environment.maturity:
    dispatcher.VpcConfig = VPCConfig(
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

t.add_resource(dispatcher)