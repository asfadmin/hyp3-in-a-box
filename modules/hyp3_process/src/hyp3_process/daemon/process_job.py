from datetime import datetime
from typing import Dict

from hyp3_events import StartEvent, EmailEvent

from .logging import getLogger
from .worker import HyP3Worker
log = getLogger(__name__, "/var/log/hyp3.log")


def process_job(event: StartEvent, worker: HyP3Worker) -> EmailEvent:
    try:
        output = worker.process(event)
    except Exception as e:
        log.info("Job failed to process")

        return job_failed(event, e)
    else:
        log.info("Job succeeded to process")

        return job_success(event, output)


def job_success(
    event: StartEvent,
    output: Dict[str, str]
) -> EmailEvent:
    log.debug("Sending SNS notification")

    return EmailEvent(
        user_id=event.user_id,
        sub_id=event.sub_id,
        additional_info=[{
            "name": "Processing Date",
            "value": str(datetime.now().date())
        }],
        granule_name=event.granule,
        browse_url=output['browse_url'],
        download_url=output['product_url'],
    )


def job_failed(event: StartEvent, error: Exception) -> EmailEvent:
    log.debug("Sending SNS failure notification")

    return EmailEvent(
        user_id=event.user_id,
        sub_id=event.sub_id,
        additional_info=[{
            "name": "Processing Date",
            "value": str(datetime.now().date())
        }, {
            "name": "Status",
            "value": "Failed"
        }, {
            "name": "Reason",
            "value": str(error)
        }],
        granule_name=event.granule,
        browse_url='',
        download_url='',
    )


class HandlerError(Exception):
    pass
