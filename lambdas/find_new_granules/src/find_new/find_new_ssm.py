import boto3
import botocore

ssm_client = boto3.client('ssm')


def upload(param_name, value):
    ssm_client.put_parameter(
        Name=param_name,
        Value=value,
        Type='String',
        Overwrite=True
    )


def download(param_name):
    try:
        resp = ssm_client.get_parameter(
            Name=param_name
        )
    except botocore.exceptions.ClientError as e:
        raise ParamDoesntExist(
            "can't download because param not set"
        ) from None

    return resp['Parameter']['Value']


class ParamDoesntExist(Exception):
    pass
