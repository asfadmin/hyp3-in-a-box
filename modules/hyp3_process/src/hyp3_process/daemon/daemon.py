# hyp3_daemon.py
# Rohan Weeden, William Horn
# Created: June 22 2018

"""
Entry point for the hyp3 processing glue code. The hyp3 daemon polls the
'Start Events' sqs queue for new processing jobs, and starts processes if the
system has the appropriate dependencies and available resources.
"""

import json
import sys
import time
from datetime import datetime
from multiprocessing import Pipe
from typing import Union

import boto3
import requests

from hyp3_events import EmailEvent

from .logging import getLogger
from .services import SNSService, SQSJob, SQSService
from .worker import HyP3Worker, WorkerStatus

ssm = boto3.client('ssm')
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
        browse_url=job.output['browse_url'],
        download_url=job.output['product_url'],
    )
)


class HyP3DaemonConfig(object):
    """ Class HyP3DaemonConfig"""

    MAX_IDLE_TIME_SECONDS = 120

    def __init__(
            self,
            queue_name,
            sns_arn,
            earthdata_creds,
            products_bucket,
            are_ssm_param_names=True
    ):
        """ Querys SSM Parameter Store for configuration variables and maps them
            to class members.

            Paramaters:
              * self.queue_name: /stack/StartEventQueueName
        """
        self.are_ssm_param_names = are_ssm_param_names

        self.queue_name = self._load_param(queue_name)
        self.sns_arn = self._load_param(sns_arn)
        self.earthdata_creds = json.loads(
            self._load_param(earthdata_creds)
        )

        self.products_bucket_name = self._load_param(products_bucket)

    def _load_param(self, param):
        if not self.are_ssm_param_names:
            return param

        val = ssm.get_parameter(
            Name=param,
            WithDecryption=True
        )['Parameter']['Value']

        log.debug(f"{param} -> {val}")

        return val


class HyP3Daemon(object):
    """ Class HyP3Daemon"""

    def __init__(self, config: HyP3DaemonConfig, handler) -> None:
        """ Initialize state. This creates a new HyP3DaemonConfig object."""
        self.config = config

        self.job_queue = SQSService(
            queue_name=self.config.queue_name
        )
        self.sns_topic = SNSService(
            arn=self.config.sns_arn
        )
        self.last_active_time = time.time()

        self.handler = handler
        self.worker: Union[HyP3Worker, None] = None
        self.worker_conn = None
        self.previous_worker_status = WorkerStatus.NO_STATUS

    def run(self):
        """ Calls ``self.main()`` every second until an exception is raised.
            Terminates this EC2 instance if main does not find any jobs to
            process for a period of time longer than 2 minutes.
        """
        log.info("HyP3 Daemon starting...")
        while True:
            try:
                if self._reached_max_idle_time():
                    log.info("Max idle time reached, terminating instance...")
                    HyP3Daemon._terminate()
                    sys.exit(0)
                    return
                self.main()
                time.sleep(1)
            except KeyboardInterrupt:
                log.debug("Stopping hyp3 daemon...")
                sys.exit(0)
                return
            except Exception as e:
                log.error("Fatal error thrown in main:\n%s", e)
                self._worker_failed()

    def main(self):
        """ Polls SQS if the EC2 Instances is idle, and starts a new processing
            job if one is found. If the instance is currently processing a job
            already, SQS will not be polled. After the worker process has
            succesfully handled a job, the job will be deleted from SQS and an
            email notification will be queued via SNS. The notification
            includes the date on which processing occurred.
        """
        status = self._poll_worker_status()

        if status == WorkerStatus.DONE:
            self._worker_done()
            return
        elif status == WorkerStatus.FAILED:
            self._worker_failed()
            return
        if status not in [WorkerStatus.READY, WorkerStatus.NO_STATUS]:
            return

        new_job = self.job_queue.get_next_message()
        if not new_job:
            return

        log.info("Staring new job %s", new_job)
        self._process_job(new_job)

    def _poll_worker_status(self):
        if self.worker and self.worker_conn.poll():
            self.previous_worker_status = self.worker_conn.recv()
        return self.previous_worker_status

    def _poll_until(self, some_type):
        val = None
        while not isinstance(val, some_type):
            val = self.worker_conn.recv()

        return val

    def _process_job(self, job: SQSJob):
        if self.worker:
            raise Exception("Worker already processing")

        self.last_active_time = time.time()

        self.worker_conn, child_conn = Pipe()
        self.worker = HyP3Worker(
            child_conn,
            job,
            self.handler,
            self.config.earthdata_creds,
            self.config.products_bucket_name
        )
        self.worker.start()

    def _worker_done(self):
        self._join_worker()
        self._finish_job()
        self._reset_worker()

    def _join_worker(self):
        self.last_active_time = time.time()
        self.worker.join()

    def _finish_job(self):
        job = self.worker.job

        # Get the updated job object which has outputs set
        if self.worker_conn.poll():
            job.output = self._poll_until(dict)

        log.info("Worker finished")
        log.debug("Deleting job %s from SQS", job)
        job.delete()

        log.debug("Sending SNS notification")
        log.debug(job.output)
        email_event = EmailEvent.from_type(job)

        self.sns_topic.push(email_event)

    def _reset_worker(self):
        self.worker_conn.close()
        self.worker = None
        self.worker_conn = None
        self.previous_worker_status = WorkerStatus.NO_STATUS

    def _reached_max_idle_time(self):
        if self.previous_worker_status == WorkerStatus.BUSY:
            return False

        time_since_last_job = time.time() - self.last_active_time
        timeout = self.config.MAX_IDLE_TIME_SECONDS

        return time_since_last_job >= timeout

    def _worker_failed(self):
        log.info("Worker failed")
        self._join_worker()

        job = self.worker.job
        job.delete()

        log.debug("Sending SNS failure notification")

        email_event = EmailEvent(
            user_id=job.data.user_id,
            sub_id=job.data.sub_id,
            additional_info=[{
                "name": "Processing Date",
                "value": str(datetime.now().date())
            }, {
                "name": "Status",
                "value": "Failed"
            }],
            granule_name=job.data.granule,
            browse_url='',
            download_url='',
        )

        if self.worker_conn.poll():
            error = self._poll_until(Exception)
            email_event = email_event._replace(
                additional_info=email_event.additional_info + [{
                    "name": "Reason",
                    "value": str(error)
                }]
            )

        self.sns_topic.push(email_event)

        self._reset_worker()

    @staticmethod
    def _terminate():
        resp = requests.get(
            "http://169.254.169.254/latest/meta-data/instance-id")
        instance_id = resp.text
        boto_response = boto3.client('autoscaling').terminate_instance_in_auto_scaling_group(
            InstanceId=instance_id,
            ShouldDecrementDesiredCapacity=True
        )
        log.debug("Terminating instance: \n%s", boto_response)
