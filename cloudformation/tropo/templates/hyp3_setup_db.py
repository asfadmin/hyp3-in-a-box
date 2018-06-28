# hyp3_setup_db.py
# Rohan Weeden, William Horn
# Created: June 13, 2018

"""
Troposphere template responsible for generating :ref:`setup_db_lambda`

Requires
~~~~~~~~
* :ref:`rds_template`
* :ref:`kms_key_template`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3.
* **IAM Policies:**

  * Lambda basic execution

"""

from troposphere import GetAtt, Ref
from troposphere.awslambda import Environment, VPCConfig
from troposphere.cloudformation import CustomResource
from troposphere.iam import Role

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

role = t.add_resource(Role(
    "FindNewGranulesExecutionRole",
    Path="/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc')
))

setup_db = t.add_resource(utils.make_lambda_function(
    name='setup_db',
    role=role,
    lambda_params={
        "KmsKeyArn": GetAtt(kms_key, "Arn"),
        "Environment": Environment(
            Variables={
                "Hyp3DBHost": utils.get_host_address(),
                "Hyp3DBName": Ref(db_name),
                "Hyp3DBRootUser": Ref(db_super_user),
                "Hyp3DBRootPass": Ref(db_super_user_pass),
                "Hyp3DBUser": Ref(db_user),
                "Hyp3DBPass": Ref(db_pass)
            }
        ),
        "Timeout": 40
    }
))

db_setup = t.add_resource(CustomResource(
    "RunDBSetup",
    ServiceToken=GetAtt(setup_db, "Arn")
))
