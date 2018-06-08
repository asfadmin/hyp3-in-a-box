# hyp3_send_email.py
# Rohan Weeden
# Created: June 5, 2018

# Troposphere template for send_email lambda

from template import t
from envirnoment import envirnoment

from troposphere import GetAtt, Parameter, Ref
from troposphere.awslambda import Code, Function
from troposphere.iam import Policy, Role

from . import utils

print('adding send_email lambda')

lambda_name = t.add_parameter(Parameter(
    "SendEmailName",
    Description="Name of the SendEmail lambda function",
    Default="hyp3_send_email",
    Type="String"
))

lambda_policy = Policy(
    PolicyName="SESSendEmail",
    PolicyDocument=utils.get_static_policy('ses-send-email'))

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
    FunctionName=Ref(lambda_name),
    Code=Code(
        S3Bucket=envirnoment.lambda_bucket,
        S3Key="{maturity}/send_email.zip".format(
            maturity=envirnoment.maturity
        )
    ),
    Handler="lambda_function.lambda_handler",
    Role=GetAtt(send_email_role, "Arn"),
    Runtime="python3.6"
))
