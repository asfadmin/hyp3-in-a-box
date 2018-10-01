from datetime import datetime
import traceback
from typing import Dict

from hyp3_events import StartEvent, EmailEvent

from .logging import getLogger
from .worker import HyP3Worker
from ..handler.package import PatternNotMatched

log = getLogger(__name__, "/var/log/hyp3.log")


def process_job(event: StartEvent, worker: HyP3Worker) -> EmailEvent:
    try:
        output = worker.process(event)
    except (HandlerError, PatternNotMatched) as e:
        log.info(f"Handler failed to process: {e}")

        return job_failed(event, str(e))
    except Exception as e:
        log.info(f"Error in processing code: {e}")

        return job_failed(event, traceback.format_exc(), fatal=True)
    else:
        log.info("Job succeeded to process")

        return job_success(event, output)


def job_success(
    event: StartEvent,
    output: Dict[str, str]
) -> EmailEvent:
    log.debug("Sending SNS notification")

    return EmailEvent(
        status='Success',
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


def job_failed(event: StartEvent, error: str, fatal=False) -> EmailEvent:
    log.debug("Sending SNS failure notification")

    return EmailEvent(
        status='Failure' if not fatal else 'Fatal Error',
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
            "value": error
        }],
        granule_name=event.granule,
        browse_url='',
        download_url='',
    )


class HandlerError(Exception):
    pass
