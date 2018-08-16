from typing import Any, Dict, List
import json

from hyp3_events import Hyp3Event, NewGranuleEvent

from schedule import Job


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
    events = [job.to_event() for job in jobs]

    return events
