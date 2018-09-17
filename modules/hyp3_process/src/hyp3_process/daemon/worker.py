from typing import Dict

from hyp3_events import StartEvent


class HyP3Worker:
    def __init__(self, handler, creds, bucket):
        self.handler = handler
        self.creds = creds
        self.bucket = bucket

    def process(self, event: StartEvent) -> Dict[str, str]:
        return self.handler(
            event,
            self.creds,
            self.bucket
        )
