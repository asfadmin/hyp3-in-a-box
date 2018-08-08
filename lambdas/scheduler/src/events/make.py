from typing import Any, Dict, List
import json

from hyp3_events import EmailEvent, Hyp3Event, NewGranuleEvent, StartEvent

from schedule import Job

# Add implementation for conversion from Job type
EmailEvent.impl_from(
    Job,
    lambda job: EmailEvent(
        user_id=job.user.id,
        sub_id=job.sub.id,
        additional_info=[],
        browse_url=job.granule.browse_url,
        download_url=job.granule.download_url,
        granule_name=job.granule.name
    )
)

StartEvent.impl_from(
    Job,
    lambda job: StartEvent(
        granule=job.granule.name,
        user_id=job.user.id,
        sub_id=job.sub.id,
        # TODO: Add output patterns from process here.
        output_patterns=[],
        script_path=job.process.script,
        additional_info=[]
    )
)


def make_new_granule_events_with(
        new_granule_dicts: List[Dict[str, Any]]
) -> List[NewGranuleEvent]:
    events = [
        NewGranuleEvent(**event)
        for event in new_granule_dicts
    ]

    print('Scheduling hyp3_jobs')
    print(json.dumps([g.name for g in events]))

    return events


def make_from(jobs: List[Job]) -> List[Hyp3Event]:
    """ make email packages into notify only events

        :param list(Job): jobs to make into events

        :returns: hyp3 events corresponding to each package
        :rtype: list[hyp3_events.EmailEvent]
    """
    events = [_make_event(job) for job in jobs]

    return events


def _make_event(job: Job) -> Hyp3Event:
    # NOTE: Scheduler relies on Notify Only being process 1
    if 'notify' in job.process.name.lower():
        return EmailEvent.from_type(job)

    return StartEvent.from_type(job)
