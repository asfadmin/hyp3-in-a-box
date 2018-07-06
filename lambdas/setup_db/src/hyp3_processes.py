import pathlib as pl
import os
import json

import boto3

from hyp3_db import hyp3_models

import utils


def make_default():
    return [
        hyp3_models.Process(**process) for process in get_processes()
    ]


def get_processes():
    bucket, key = utils.get_environ_params(
        'DefaultProcessesBucket',
        'DefaultProcessesKey'
    )

    s3 = boto3.resource('s3')

    base_path = pl.Path('/tmp') if \
        'prod' in os.environ.get('Maturity', 'prod') \
        else pl.Path('.')

    file_path = (base_path / pl.Path(key).name)

    print('downloading default processes')
    s3.Bucket(bucket) \
        .download_file(key, str(file_path))

    with file_path.open('r') as f:
        processes = json.load(f)

    return processes
