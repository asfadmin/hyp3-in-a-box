import pathlib as pl
import os
import json

import boto3

from hyp3_db import hyp3_models

import setup_db_utils as utils


def new(db):
    exisiting_processes_text_ids = [
        p.text_id for p in db.session.query(hyp3_models.Process).all()
    ]

    new_default_processes = [
        hyp3_models.Process(**p) for p in get_processes()
        if p['text_id'] not in exisiting_processes_text_ids
    ]

    for p in new_default_processes:
        print(f'adding new process {p.text_id}')

    return new_default_processes


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
