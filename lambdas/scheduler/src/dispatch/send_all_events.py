from typing import List

from hyp3_events import Hyp3Event

from . import scheduler_sns as sns
from . import scheduler_sqs as sqs


def all_events(new_hyp3_events: List[Hyp3Event]) -> None:
    print(f'Dispatching {len(new_hyp3_events)} events')

    for event in new_hyp3_events:
        print(event.event_type)
        if 'Email' in event.event_type:
            print('sending email')
            sns.push_event(event)
        else:
            print('starting job')
            sqs.add_event(event)

    print('Done!')
