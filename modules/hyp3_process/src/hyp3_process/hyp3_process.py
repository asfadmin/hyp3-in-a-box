from typing import Union

from .hyp3_handler import (
    hyp3_handler,
    EarthdataCredentials,
    HandlerFunction,
    ProcessingFunction
)


class Process:
    def __init__(
        self
    ) -> None:
        self.process_handler: Union[ProcessingFunction, None] = None
        self.earthdata_creds = {}
        self.products_bucket = None

    def handler(self, process_func: HandlerFunction):
        if self.process_handler is not None:
            raise HandlerRedefinitionError(
                'Process is only allowed one handler function'
            )

        self.process_handler = hyp3_handler(process_func)

    def start(self, job):
        return self.process_handler(
            job,
            self.earthdata_creds,
            self.products_bucket
        )


class HandlerRedefinitionError(Exception):
    pass
