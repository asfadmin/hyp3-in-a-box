# hyp3_daemon.py
# Rohan Weeden
# Created: June 22 2018

"""
Entry point for the hyp3 processing glue code. The hyp3 daemon polls the
'Start Events' sqs queue for new processing jobs, and starts processes if the
system has the appropriate dependencies and available resources.

This script has an ifmain so it can be called from the command line.
"""

import logging
import subprocess
import sys
import time
from datetime import datetime
from multiprocessing import Pipe

import boto3

from hyp3_events import EmailEvent
from hyp3_logging import getLogger
from hyp3_worker import HyP3Worker, WorkerStatus
from services import SNSService, SQSJob, SQSService

log = getLogger(__name__)

# Add implementation for conversion from SQSJob type
EmailEvent.impl_from(
    SQSJob,
    lambda job: EmailEvent(
        user_id=job.data.user_id,
        sub_id=job.data.sub_id,
        additional_info=[{
            "name": "Processing Date",
            "value": str(datetime.now().date())
        }],
        granule_name=job.data.granule,
        browse_url="",
        download_url="",
    )
)


class HyP3DaemonConfig(object):
    """ Class HyP3DaemonConfig"""

    def __init__(self):
        """ Querys SSM Parameter Store for configuration variables and maps them
            to class members.

            Paramaters:
              * self.queue_name: /stack/StartEventQueueName
        """
        ssm = boto3.client('ssm')

        # TODO: Configure Stack Name somehow (user data?)
        self.queue_name = ssm.get_parameter(
            Name="/hyp3-in-a-box-test/StartEventQueueName"
        )['Parameter']['Value']
        self.sns_arn = ssm.get_parameter(
            Name="/hyp3-in-a-box-test/FinishEventSNSArn"
        )['Parameter']['Value']
        self.max_idle_time_seconds = 120


class HyP3Daemon(object):
    """ Class HyP3Daemon"""

    def __init__(self):
        """ Initialize state. This creates a new HyP3DaemonConfig object."""
        self.config = HyP3DaemonConfig()

        self.job_queue = SQSService(
            queue_name=self.config.queue_name
        )
        self.sns_topic = SNSService(
            arn=self.config.sns_arn
        )
        self.last_active_time = time.time()
        self.worker = None
        self.worker_conn = None
        self.previous_worker_status = WorkerStatus.NO_STATUS

    def run(self):
        """ Calls ``self.main()`` every second until an exception is raised"""
        log.info("HyP3 Daemon starting...")
        while True:
            try:
                if self._reached_max_idle_time():
                    log.info("Max idle time reached, shutting down...")
                    subprocess.call(["shutdown", "-h", "now"])
                    sys.exit(0)
                    return
                self.main()
                time.sleep(1)
            except KeyboardInterrupt:
                log.debug("Stopping hyp3 daemon...")
                sys.exit(0)
                return
            # For now, just crash on errors

    def main(self):
        """ Polls SQS if the EC2 Instances is idle, and starts a new processing
            job if one is found. If the instance is currently processing a job
            already, SQS will not be polled. After the worker process has
            succesfully handled a job, the job will be deleted from SQS and an
            email notification will be queued via SNS. The notification includes
            the date on which processing occurred.
        """

        status = self._poll_worker_status()
        if status == WorkerStatus.DONE:
            self._join_worker()
            status = WorkerStatus.NO_STATUS
            return
        if not (status == WorkerStatus.READY or status == WorkerStatus.NO_STATUS):
            return

        new_job = self.job_queue.get_next_message()
        if not new_job:
            return

        log.debug("Staring new job %s", new_job)
        self._process_job(new_job)

    def _poll_worker_status(self):
        if self.worker and self.worker_conn.poll():
            self.previous_worker_status = self.worker_conn.recv()
        return self.previous_worker_status

    def _process_job(self, job: SQSJob):
        if self.worker:
            raise Exception("Worker already processing")

        self.last_active_time = time.time()

        self.worker_conn, child_conn = Pipe()
        self.worker = HyP3Worker(child_conn, job)
        self.worker.start()

    def _join_worker(self):
        self.last_active_time = time.time()
        self.worker_conn.close()
        self.worker.join()

        self._finish_job(self.worker.job)

        self.worker = None
        self.worker_conn = None
        self.previous_worker_status = WorkerStatus.NO_STATUS

    def _finish_job(self, job: SQSJob):
        log.debug("Worker finished, deleting job %s from SQS", job)
        job.delete()

        log.debug("Sending SNS notification")
        self.sns_topic.push(EmailEvent.from_type(job))

    def _reached_max_idle_time(self):
        if self.previous_worker_status == WorkerStatus.BUSY:
            return False
        return (time.time() - self.last_active_time) >= self.config.max_idle_time_seconds


def main():
    """ Create a new HyP3Daemon instance and run forever."""
    daemon = HyP3Daemon()
    daemon.run()


if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    main()
