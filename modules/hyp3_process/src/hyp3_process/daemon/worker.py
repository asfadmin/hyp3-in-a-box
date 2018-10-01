import contextlib
from datetime import datetime
import sys
import pathlib as pl
from typing import Dict

import asf_granule_util as gu

from hyp3_events import StartEvent


class HyP3Worker:
    def __init__(self, processing_func, creds, bucket):
        self.processing_func = processing_func
        self.creds = creds
        self.bucket = bucket

    def process(self, event: StartEvent) -> Dict[str, str]:
        granule_id = gu.SentinelGranule(event.granule).unique_id
        date = str(datetime.now()).replace(" ", "")

        with logging(f'{granule_id}--{date}.log'):
            return self.processing_func(
                event,
                self.creds,
                self.bucket
            )


@contextlib.contextmanager
def logging(log_name):
    old_stdout = sys.stdout
    log = pl.Path.home() / 'log'

    if not log.exists():
        log.mkdir(parents=True)

    with (log / log_name).open('w') as log_file:
        sys.stdout = log_file
        yield
        sys.stdout = old_stdout
