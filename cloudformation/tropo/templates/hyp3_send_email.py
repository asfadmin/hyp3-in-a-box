# hyp3_send_email.py
# Rohan Weeden
# Created: June 5, 2018

"""
Troposphere template responsible for generating :ref:`send_email_lambda`

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3.
* **IAM Policies:**

  * Lambda basic execution
  * Allow lambda to trigger SES send email

"""

from template import t
from environment import environment

from troposphere import GetAtt, Parameter, Ref
from troposphere.awslambda import Code, Function
from troposphere.iam import Policy, Role

from . import utils

source_zip = "send_email.zip"


print('  adding send_email lambda')

lambda_policy = Policy(
    PolicyName="SESSendEmail",
    PolicyDocument=utils.get_static_policy('ses-send-email')
)

send_email_role = t.add_resource(Role(
    "SendEmailExecutionRole",
    Path="/service-role/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
    Policies=[lambda_policy],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))

send_email = t.add_resource(Function(
    "SendEmailFunction",
    Code=Code(
        S3Bucket=environment.lambda_bucket,
        S3Key="{maturity}/{zip}".format(
            maturity=environment.maturity,
            zip=source_zip
        ),
        S3ObjectVersion=environment.send_email_version
    ),
    Handler="lambda_function.lambda_handler",
    Role=GetAtt(send_email_role, "Arn"),
    Runtime="python3.6"
))
