# hyp3_worker.py
# Rohan Weeden, William Horn
# Created: June 22, 2018

# The worker process which runs science scripts

import traceback
from enum import Enum
from multiprocessing import Process

from .logging import getLogger

log = getLogger(__name__)


class WorkerStatus(Enum):
    NO_STATUS = 0
    READY = 1
    BUSY = 2
    DONE = 3
    FAILED = 4


class HyP3Worker(Process):
    def __init__(self, conn, job, handler, creds, bucket):
        super().__init__()
        self.conn = conn
        self.job = job
        self.handler = handler

        self.earthdata_creds = creds
        self.products_bucket = bucket

    def run(self):
        self._set_status(WorkerStatus.BUSY)
        log.info("WORKER: Processed job %s", self.job)
        try:
            output = self.handler(
                self.job.data,
                self.earthdata_creds,
                self.products_bucket
            )

            self.job.set_output(output)

            self._set_status(WorkerStatus.DONE)
            self.conn.send(self.job)
        except Exception as e:
            log.error("Excepion caught in Worker")
            traceback.print_exc()
            self._set_status(WorkerStatus.FAILED)
            self.conn.send(e)
        finally:
            self.conn.close()

    def _set_status(self, status):
        self.conn.send(status)
