
from troposphere import GetAtt, Ref, Output, Join
from troposphere.awslambda import Function, Code
from troposphere.cloudformation import CustomResource
from troposphere.iam import Role

from template import t

from . import utils

print('  adding random_pass')


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
    Code=Code(
        ZipFile=Join("\n", utils.get_lambda_function('random_pass'))
    ),
    Handler='index.lambda_handler',
    Role=GetAtt(lambda_role, "Arn"),
    Runtime="python2.7"
))

password = t.add_resource(CustomResource(
    "RandomPasswordString",
    Length=25,
    RDSCompatible=True,
    ServiceToken=GetAtt(random_password, "Arn")
))

setup_db_output = t.add_output(Output(
    'RandomString',
    Description=("Some random string generated in cloudformation"),
    Value=GetAtt(password, 'RandomString')
))
