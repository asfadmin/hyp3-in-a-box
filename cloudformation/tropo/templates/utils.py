import json
import pathlib as pl

from troposphere.awslambda import Code

from troposphere import GetAtt, Ref, Sub
from troposphere.awslambda import Function

from tropo_env import environment
from template import t


def get_email_pattern():
    return r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'


def get_host_address():
    if environment.should_create_db:
        from .hyp3_rds import hyp3_db

        return GetAtt(hyp3_db, "Endpoint.Address")

    from .hyp3_db_params import hyp3_db
    t.add_parameter(hyp3_db)

    return Ref(hyp3_db)


def get_param_prefix():
    return 'Existing' if not environment.should_create_db else ''


def get_map(name):
    return load_json_from('maps', name)


def get_static_policy(name):
    static_policy = load_json_from('policies', name)

    return static_policy


def load_json_from(directory, name):
    file_path, file_name = pl.Path(__file__).parent, name + '.json'

    path = file_path / directory / file_name

    with path.open('r') as f:
        loaded_json = json.load(f)

    return loaded_json


def make_lambda_function(*, name, lambda_params=None, role):
    camel_case_name = get_camel_case(name)
    s3_key = "{maturity}/{source_zip}".format(
        maturity=environment.maturity,
        source_zip="{}.zip".format(name)
    )

    lambda_func = Function(
        "{}Function".format(camel_case_name),
        FunctionName=Sub(
            "${StackName}_hyp3_${FunctionName}",
            StackName=Ref('AWS::StackName'),
            FunctionName=name
        ),
        Code=make_lambda_code(
            S3Bucket=environment.lambda_bucket,
            S3Key=s3_key,
            S3ObjectVersion=getattr(environment, "{}_version".format(name))
        ),
        Handler="lambda_function.lambda_handler",
        Role=GetAtt(role, "Arn"),
        Runtime="python3.6"
    )

    if lambda_params is not None:
        for param_name, param_val in lambda_params.items():
            setattr(lambda_func, param_name, param_val)

    return lambda_func


def get_camel_case(name):
    camel_case_version = name \
        .title() \

    return remove_spacers(camel_case_version)


def remove_spacers(s):
    for c in '_- ':
        s = s.replace(c, '')

    return s


def make_lambda_code(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    return Code(**kwargs)
