from typing import Dict

from hyp3_events import StartEvent


class HyP3Worker:
    def __init__(self, processing_func, creds, bucket):
        self.processing_func = processing_func
        self.creds = creds
        self.bucket = bucket

    def process(self, event: StartEvent) -> Dict[str, str]:
        return self.processing_func(
            event,
            self.creds,
            self.bucket
        )
