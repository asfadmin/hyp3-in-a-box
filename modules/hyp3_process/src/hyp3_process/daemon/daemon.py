import time
import json
from datetime import datetime

import boto3

from hyp3_events import EmailEvent, StartEvent

from .worker import HyP3Worker
from .process_job import process_job
from .services import SNSService, SQSJob, SQSService
from .logging import getLogger

log = getLogger(__name__, "/var/log/hyp3.log")


class HyP3Daemon:
    MAX_IDLE_TIME_SECONDS = 120

    def __init__(self, job_queue, sns_topic, worker: HyP3Worker):
        self.job_queue = SQSService(sqs_queue=job_queue)
        self.sns_topic = SNSService(sns_topic=sns_topic)

        self.worker = worker
        self.last_active_time = time.time()

    def run(self):
        log.info("HyP3 Daemon starting...")

        while not self.reached_max_idle_time():
            self.main()
            time.sleep(self.MAX_IDLE_TIME_SECONDS/120)

        log.info("Max idle time reached, stopping...")

    def reached_max_idle_time(self):
        time_since_last_job = time.time() - self.last_active_time
        timeout = self.MAX_IDLE_TIME_SECONDS

        return time_since_last_job >= timeout

    def main(self):
        job = self.job_queue.get_next_message()
        if not job:
            return

        log.info("Staring new job %s", job)
        start_event = job.data

        self.last_active_time = time.time()
        try:
            email_event = process_job(start_event, self.worker)
        except Exception as e:
            raise e
        finally:
            log.debug("Deleting job %s from queue", job)
            job.delete()

            self.sns_topic.push(email_event)
