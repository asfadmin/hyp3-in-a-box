# hyp3_daemon.py
# Rohan Weeden
# Created: June 22 2018

# Entry point for the hyp3 processing glue code. The hyp3 daemon polls the
# 'Start Events' sqs queue for new processing jobs, and starts processes if the
# system has the appropriate dependencies and available resources.

import sys
import time
from multiprocessing import Pipe
import logging

from hyp3_worker import HyP3Worker, WorkerStatus
from services import SQSService
from hyp3_logging import getLogger

log = getLogger(__name__)


class HyP3Daemon(object):

    def __init__(self):
        self.job_queue = None
        self.worker = None
        self.worker_conn = None
        self.previous_worker_status = WorkerStatus.NO_STATUS

    def run(self):
        log.info("HyP3 Daemon starting...")
        while True:
            try:
                self.main()
                time.sleep(1)
            except KeyboardInterrupt:
                log.debug("Shutting down...")
                sys.exit(0)
            # For now, just crash on errors

    def main(self):
        if not self.job_queue:
            self._connect_sqs()

        status = self._poll_worker_status()
        if status == WorkerStatus.DONE:
            self._join_worker()
            status = WorkerStatus.NO_STATUS
        if not (status == WorkerStatus.READY or status == WorkerStatus.NO_STATUS):
            return

        new_job = self.job_queue.get_next_message()
        if not new_job:
            return

        log.debug("Staring new job %s", new_job)
        self._process_job(new_job)
        new_job.delete()

    def _connect_sqs(self):
        if self.job_queue:
            return

        # TODO: Configure somehow (parameter store?)
        self.job_queue = SQSService(
            queue_name="hyp3-in-a-box-test-Hyp3StartEvents-1VPMA189B6AFV.fifo"
        )

    def _poll_worker_status(self):
        if self.worker and self.worker_conn.poll():
            self.previous_worker_status = self.worker_conn.recv()
        return self.previous_worker_status

    def _process_job(self, job):
        if self.worker:
            raise Exception("Worker already processing")

        self.worker_conn, child_conn = Pipe()
        self.worker = HyP3Worker(child_conn, job)
        self.worker.start()

    def _join_worker(self):
        self.worker_conn.close()
        self.worker.join()
        self.worker = None
        self.worker_conn = None
        self.previous_worker_status = WorkerStatus.NO_STATUS
        log.debug("Worker finished")


def main():
    daemon = HyP3Daemon()
    daemon.run()


if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    main()
