# hyp3_setup_db.py
# Rohan Weeden, William Horn
# Created: June 13, 2018

"""
Troposphere template responsible for generating :ref:`setup_db_lambda`.

Requires
~~~~~~~~
* :ref:`db_params_template`
* :ref:`kms_key_template`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3
* **SSM Parameters:** Values start empty and are populated by setup_db

  * HyP3ApiUsername - Username of the HyP3 API admin user
  * HyP3ApiKey - API Key of the HyP3 API admin user

* **IAM Policies:**

  * Lambda basic execution

* **Custom Resource:** Triggers the setup_db lambda during stack creation
"""

import uuid

from tropo_env import environment
from troposphere import GetAtt, Join, Output, Parameter, Ref, Sub
from troposphere.awslambda import Environment
from troposphere.cloudformation import CustomResource
from troposphere.iam import Policy, Role
from troposphere.ssm import Parameter as SSMParameter

from template import t

from . import utils
from .hyp3_db_params import (
    db_name,
    db_pass,
    db_super_user,
    db_super_user_pass,
    db_user
)
from .hyp3_kms_key import kms_key

source_zip = "setup_db.zip"


print('  adding setup_db lambda')


default_processes_s3_read = Policy(
    PolicyName='DefaultProcessesS3Read',
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:HeadObject"
            ],
            "Resource": 'arn:aws:s3:::{bucket}/{obj}'.format(
                bucket=environment.source_bucket,
                obj=environment.get_default_processes_key()
            ),
        }]}
)

ssm_param_read_write = Policy(
    PolicyName="SsmParamReadWrite",
    PolicyDocument={
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "ssm:PutParameter"
                ],
                "Resource": Join(":", [
                    "arn:aws:ssm",
                    Ref("AWS::Region"),
                    Ref("AWS::AccountId"),
                    "parameter/*"
                ])
            }
        ]
    }
)

role = t.add_resource(Role(
    "SetupDbExecutionRole",
    Path="/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
    Policies=[default_processes_s3_read, ssm_param_read_write],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc')
))

admin_email = t.add_parameter(Parameter(
    "HyP3AdminEmail",
    Description=(
        "Email for the admin hyp3 user. "
        "This is where emails will be sent to."
    ),
    Type="String",
    AllowedPattern=utils.get_email_pattern()
))

admin_username = t.add_parameter(Parameter(
    "HyP3AdminUsername",
    Description="Username for the admin hyp3 user",
    Type="String",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*"
))

ssm_hyp3_api_username_param_name = "HyP3ApiUsername"
ssm_hyp3_api_username = t.add_resource(SSMParameter(
    "HyP3SSMParameterHyP3ApiUsername",
    Name=Sub(
        "/${{StackName}}/{}".format(ssm_hyp3_api_username_param_name),
        StackName=Ref("AWS::StackName")
    ),
    Type="String",
    Value="♥"
))

ssm_hyp3_api_key_param_name = "HyP3ApiKey"
ssm_hyp3_api_key = t.add_resource(SSMParameter(
    "HyP3SSMParameterHyP3ApiKey",
    Name=Sub(
        "/${{StackName}}/{}".format(ssm_hyp3_api_key_param_name),
        StackName=Ref("AWS::StackName")
    ),
    Type="String",
    Value="♥"
))

setup_db = t.add_resource(utils.make_lambda_function(
    name='setup_db',
    role=role,
    lambda_params={
        "KmsKeyArn": GetAtt(kms_key, "Arn"),
        "Environment": Environment(
            Variables={
                "HyP3DBHost": utils.get_host_address(),
                "HyP3DBName": Ref(db_name),

                "HyP3DBRootUser": Ref(db_super_user),
                "HyP3DBRootPass": Ref(db_super_user_pass),

                "HyP3DBUser": Ref(db_user),
                "HyP3DBPass": Ref(db_pass),

                "HyP3AdminUsername": Ref(admin_username),
                "HyP3AdminEmail": Ref(admin_email),

                "DefaultProcessesBucket": environment.source_bucket,
                "DefaultProcessesKey": environment.get_default_processes_key(),

                "HyP3StackName": Ref("AWS::StackName"),

                "ParamNameHyP3Username": ssm_hyp3_api_username_param_name,
                "ParamNameHyP3ApiKey": ssm_hyp3_api_key_param_name
            }
        ),
        "Timeout": 60
    }
))

db_setup = t.add_resource(CustomResource(
    "RunDBSetup",
    ServiceToken=GetAtt(setup_db, "Arn"),
    # This is to always run the setup_db function on template updates.
    # Cloudformation only updates resources that change in the template.
    ForceUpdateId=str(uuid.uuid4())
))

t.add_output(Output(
    "HyP3Username",
    Description="HyP3 username",
    Value=GetAtt(db_setup, 'HyP3Username')
))

t.add_output(Output(
    "HyP3ApiKey",
    Description="Api key for hyp3 access",
    Value=GetAtt(db_setup, 'HyP3ApiKey')
))
