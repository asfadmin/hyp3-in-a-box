import boto3

ssm_client = boto3.client('ssm')


def upload(param_name, value):
    ssm_client.put_parameter(
        Name=param_name,
        Value=value,
        Type='String',
        Overwrite=True
    )


def download(param_name):
    resp = ssm_client.get_parameter(
        Name=param_name
    )

    return resp['Parameter']['Value']
