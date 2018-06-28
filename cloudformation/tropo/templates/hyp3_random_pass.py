"""
Troposphere template responsible for creating a custom resource that generates
random strings. This is intended to be used for random passwords and to test
the custom resource wrapper.


Resources
~~~~~~~~~

* **Lambda Function:** Python 3.6 lambda function, code is pulled from s3.
* **IAM Policies:**

  * Lambda basic execution

* **Custom Resource:** This is a random string that can be used in the template

"""
from troposphere import GetAtt, Output
from troposphere.awslambda import Function
from troposphere.cloudformation import CustomResource
from troposphere.iam import Role

from template import t
from environment import environment

from . import utils

print('  adding random_pass')
source_zip = 'random_password.zip'


lambda_role = t.add_resource(Role(
    "RandomPassExecutionRole",
    Path="/service-role/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    ],
    AssumeRolePolicyDocument=utils.get_static_policy('lambda-policy-doc'),
))

random_password = t.add_resource(Function(
    "RandomPasswordLambda",
    Code=utils.make_lambda_code(
        S3Bucket=environment.lambda_bucket,
        S3Key="{maturity}/{source_zip}".format(
            maturity=environment.maturity,
            source_zip=source_zip
        ),
        S3ObjectVersion=environment.find_new_granules_version
    ),
    Handler='lambda_function.lambda_handler',
    Role=GetAtt(lambda_role, "Arn"),
    Runtime="python3.6"
))

password = t.add_resource(CustomResource(
    "RandomPasswordString",
    Length=25,
    ServiceToken=GetAtt(random_password, "Arn")
))

setup_db_output = t.add_output(Output(
    'RandomString',
    Description=("Some random string generated in cloudformation"),
    Value=GetAtt(password, 'Password')
))
