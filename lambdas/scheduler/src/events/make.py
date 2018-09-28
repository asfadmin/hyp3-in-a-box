from typing import Any, Dict, List
import json

from hyp3_events import HyP3Event, NewGranuleEvent


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
