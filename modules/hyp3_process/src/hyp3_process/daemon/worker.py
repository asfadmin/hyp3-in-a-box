# hyp3_worker.py
# Rohan Weeden, William Horn
# Created: June 22, 2018

# The worker process which runs science scripts

import traceback
from enum import Enum
from multiprocessing import Process

from .logging import getLogger

log = getLogger(__name__,  "/var/log/hyp3.log")


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
        log.info("WORKER: Processing job %s", self.job)
        start_event = self.job.data

        try:
            output = self.handler(
                start_event,
                self.earthdata_creds,
                self.products_bucket
            )

            self.job.set_output(output)

            log.info("WORKER: Processing done %s", start_event.granule)
            self._set_status(WorkerStatus.DONE)
            self.conn.send(self.job.output)
        except Exception as e:
            log.error("Exception caught in Worker")
            traceback.print_exc()
            self._set_status(WorkerStatus.FAILED)
            self.conn.send(e)
        finally:
            self.conn.close()

    def _set_status(self, status):
        self.conn.send(status)
