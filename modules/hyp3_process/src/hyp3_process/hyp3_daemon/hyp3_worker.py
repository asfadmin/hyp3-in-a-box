# hyp3_worker.py
# Rohan Weeden, William Horn
# Created: June 22, 2018

# The worker process which runs science scripts
from enum import Enum
from multiprocessing import Process


class WorkerStatus(Enum):
    NO_STATUS = 0
    READY = 1
    BUSY = 2
    DONE = 3


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
        print("WORKER: Processed job {}".format(self.job))
        self.handler()
        self._set_status(WorkerStatus.DONE)

        self.conn.close()

    def _set_status(self, status):
        self.conn.send(status)
