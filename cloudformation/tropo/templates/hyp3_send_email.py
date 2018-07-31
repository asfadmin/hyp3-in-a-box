# hyp3_send_email.py
# Rohan Weeden
# Created: June 5, 2018

"""
Troposphere template responsible for generating :ref:`send_email_lambda`.

Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3
* **IAM Policies:**

  * Lambda basic execution
  * Allow lambda to trigger SES send email using verified email

"""

from troposphere import Parameter, Ref
from troposphere.awslambda import Environment
from troposphere.iam import Policy, Role

from template import t

from . import utils
from .hyp3_db_params import db_name, db_pass, db_user
from .hyp3_api_eb import api_url

source_zip = "send_email.zip"


print('  adding send_email lambda')

source_email = t.add_parameter(Parameter(
    "VerifiedSourceEmail",
    Description=(
        "Verified source email. "
        "This is where emails will be sent from."
    ),
    Type="String",
    AllowedPattern=utils.get_email_pattern()
))

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


send_email = t.add_resource(utils.make_lambda_function(
    name='send_email',
    role=send_email_role,
    lambda_params={
        "Environment": Environment(
            Variables={
                'SOURCE_EMAIL': Ref(source_email),
                'DB_HOST': utils.get_host_address(),
                'DB_USER': Ref(db_user),
                'DB_PASSWORD': Ref(db_pass),
                'DB_NAME': Ref(db_name),
                'API_URL': api_url
            }
        )
    }
))
