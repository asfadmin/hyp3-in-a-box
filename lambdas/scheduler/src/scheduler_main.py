
import json
from typing import Dict

import dispatch
import events
import schedule


def scheduler(event: Dict) -> None:
    """ Wrapper around scheduler lambda that can be imported by pytest."""

    granules = event['new_granules']
    new_granule_events = events.make_new_granule_events_with(granules)

    jobs = schedule.hyp3_jobs(new_granule_events)

    new_hyp3_events = events.make_from(jobs)

    dispatch.all_events(new_hyp3_events)
