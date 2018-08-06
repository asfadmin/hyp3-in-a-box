# hyp3_worker.py
# Rohan Weeden
# Created: June 22, 2018

# The worker process which runs science scripts
import abc
from enum import Enum
from multiprocessing import Process


class WorkerStatus(Enum):
    NO_STATUS = 0
    READY = 1
    BUSY = 2
    DONE = 3


class HyP3Worker(Process):
    def __init__(self, conn, job):
        super().__init__()
        self.conn = conn
        self.job = job

    def run(self):
        self._set_status(WorkerStatus.BUSY)
        print("WORKER: Processed job {}".format(self.job))
        self.process()
        self._set_status(WorkerStatus.DONE)

        self.conn.close()

    @abc.abstractmethod
    def process(self):
        return NotImplemented

    def _set_status(self, status):
        self.conn.send(status)
