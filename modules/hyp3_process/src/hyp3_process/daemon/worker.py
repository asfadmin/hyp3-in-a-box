import contextlib
from datetime import datetime
import sys
import pathlib as pl
from typing import Dict

import boto3
import asf_granule_util as gu

from hyp3_events import StartEvent


s3_client = boto3.client('s3')


class HyP3Worker:
    def __init__(self, processing_func, creds, bucket):
        self.processing_func = processing_func
        self.creds = creds
        self.bucket = bucket

    def process(self, event: StartEvent) -> Dict[str, str]:
        granule_id = gu.SentinelGranule(event.granule).unique_id
        date = str(datetime.now()).replace(" ", "")

        with logging(name=f'{granule_id}--{date}.log', bucket=self.bucket):
            return self.processing_func(
                event,
                self.creds,
                self.bucket
            )


@contextlib.contextmanager
def logging(name, bucket):
    old_stdout = sys.stdout
    log = pl.Path.home() / 'log'

    if not log.exists():
        log.mkdir(parents=True)

    log_file = log / name

    with log_file.open('w') as log:
        sys.stdout = log
        yield
        sys.stdout = old_stdout

    bucket_path = str(pl.Path('log') / name)

    s3_client.upload_file(str(log_file), bucket, bucket_path)
