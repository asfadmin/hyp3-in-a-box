from collections import Counter
from typing import List
import json

from hyp3_events import Hyp3Event

from . import scheduler_sns as sns
from . import scheduler_sqs as sqs


def all_events(new_hyp3_events: List[Hyp3Event]) -> None:
    print(f'Dispatching {len(new_hyp3_events)} events')

    for event in new_hyp3_events:
        print(event.event_type)
        if 'Email' in event.event_type:
            sns.push_event(event)
        else:
            sqs.add_event(event)

    log_number_of_each_event(new_hyp3_events)

    print('Done!')


def log_number_of_each_event(events):
    counts = Counter(events)

    print(json.dumps(counts.items()))
