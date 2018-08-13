from collections import Counter
from typing import List

from hyp3_events import Hyp3Event

from . import scheduler_sns as sns
from . import scheduler_sqs as sqs


def all_events(new_hyp3_events: List[Hyp3Event]) -> None:
    print(f'Dispatching {len(new_hyp3_events)} events')

    for event in new_hyp3_events:
        if 'Email' in event.event_type:
            sns.push_event(event)
        else:
            sqs.add_event(event)

    print('sent:')
    for e_type, count in count_of_each_event_type(new_hyp3_events):
        print(f'  {e_type} -> {count} sent')

    print('Done!')


def count_of_each_event_type(events):
    return Counter(
        [e.event_type for e in events]
    ).items()
