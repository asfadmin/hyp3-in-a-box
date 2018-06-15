# hyp3_setup_db.py
# Rohan Weeden
# Created: June 13, 2018

"""
Troposphere template responsible for generating :ref:`setup_db_lambda`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3.
* **IAM Policies:**

  * Lambda basic execution

"""

from troposphere import GetAtt, Parameter, Ref
from troposphere.awslambda import Environment, Function
from troposphere.iam import Role

from environment import environment
from template import t

from . import utils
from .hyp3_kms_key import kms_key
from .hyp3_rds import dbpassword, dbuser, hyp3_db

source_zip = "setup_db.zip"


print('  adding setup_db lambda')

lambda_name = t.add_parameter(Parameter(
    "SetupDBName",
    Description="Name of the SetupDB lambda function",
    Default="hyp3_setup_db",
    Type="String"
))

send_email_role = t.add_resource(Role(
    "SetupDBExecutionRole",
    Path="/service-role/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))

send_email = t.add_resource(Function(
    "SetupDBFunction",
    FunctionName=Ref(lambda_name),
    Code=utils.make_lambda_code(
        S3Bucket=environment.lambda_bucket,
        S3Key="{maturity}/{source_zip}".format(
            maturity=environment.maturity,
            source_zip=source_zip
        ),
        S3ObjectVersion=environment.setup_db_version
    ),
    Handler="lambda_function.lambda_handler",
    Role=GetAtt(send_email_role, "Arn"),
    Runtime="python3.6",
    KmsKeyArn=GetAtt(kms_key, "Arn"),
    Environment=Environment(
        Variables={
            "Hyp3DBHost": GetAtt(hyp3_db, "Endpoint.Address"),
            "Hyp3DBRootUser": Ref(dbuser),
            "Hyp3DBRootPass": Ref(dbpassword)
        }
    )
))
