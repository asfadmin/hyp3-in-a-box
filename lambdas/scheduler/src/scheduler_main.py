import json
from typing import Dict

import events
import schedule
import dispatch


def scheduler(aws_event: Dict) -> None:
    """ Wrapper around scheduler lambda that can be imported by pytest."""
    print(json.dumps(aws_event))

    new_granule_events = events.make_new_granule_events_with(
        aws_event['new_granules']
    )

    jobs = schedule.hyp3_jobs(new_granule_events)

    new_hyp3_events = events.make_from(jobs)

    dispatch.all_events(new_hyp3_events)
