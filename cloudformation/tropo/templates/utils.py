import json
import pathlib as pl

from troposphere.awslambda import Code

from troposphere import GetAtt, Parameter, Ref
from troposphere.awslambda import Function

from environment import environment
from template import t


def get_host_address():
    if environment.should_create_db:
        from .hyp3_rds import hyp3_db
    else:
        from .hyp3_db_params import hyp3_db
        t.add_parameter(hyp3_db)

    if environment.should_create_db:
        return GetAtt(hyp3_db, "Endpoint.Address")

    return Ref(hyp3_db)


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


def make_lambda_function(name, lambda_params, role):
    camel_case_name = get_camel_case(name)

    lambda_func = Function(
        "{}Function".format(camel_case_name),
        Code=make_lambda_code(
            S3Bucket=environment.lambda_bucket,
            S3Key="{maturity}/{source_zip}".format(
                maturity=environment.maturity,
                source_zip="{}.zip".format(name)
            ),
            S3ObjectVersion=getattr(environment, "{}_version".format(name))
        ),
        Handler="lambda_function.lambda_handler",
        Role=GetAtt(role, "Arn"),
        Runtime="python3.6"
    )

    for param_name, param_val in lambda_params.items():
        setattr(lambda_func, param_name, param_val)

    if environment.use_name_parameters:
        lambda_name = t.add_parameter(Parameter(
            "Lambda{}Name".format(camel_case_name),
            Description="Name of the {} lambda function".format(name),
            Default="hyp3_{}".format(name),
            Type="String"
        ))

        lambda_func.FunctionName = Ref(lambda_name)

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
