from typing import Any, Dict, List
import json

from hyp3_events import EmailEvent, Hyp3Event, NewGranuleEvent, StartEvent

from schedule import Job

# Add implementation for conversion from Job type
EmailEvent.impl_from(
    Job,
    lambda obj: EmailEvent(
        user_id=obj.user.id,
        sub_id=obj.sub.id,
        additional_info=[],
        browse_url=obj.granule.browse_url,
        download_url=obj.granule.download_url,
        granule_name=obj.granule.name
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

        :param list(tuple): email packages of the form schedule.Job(sub, user, granule)

        :returns: hyp3 events corresponding to each package
        :rtype: list[hyp3_events.EmailEvent]
    """
    events = [_make_event(job) for job in jobs]

    return events


def _make_event(job: Job) -> Hyp3Event:
    # NOTE: Scheduler relies on Notify Only being process 1
    if job.sub.process_id == 1:
        return EmailEvent.from_type(job)

    return StartEvent.from_type(job)
