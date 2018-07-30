import pathlib as pl
import boto3

ssm = boto3.client('ssm')


def save_params(params):
    for full_path, param_value in params.items():
        resp = ssm.put_parameter(
            Name=full_path,
            Value=param_value,
            Description=get_description_for(full_path),
            Type='SecureString',
            Overwrite=True
        )

        print(resp)


def get_description_for(path):
    name = pl.Path(path).name

    return f'{name} for hyp3 in a box'
