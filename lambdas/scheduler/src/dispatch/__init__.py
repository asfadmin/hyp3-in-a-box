from typing import List

from schedule import Job

from . import sns


def send_all_events(new_hyp3_events: List[Job]) -> None:
    print(f'Dispatching {len(new_hyp3_events)} events')

    for event in new_hyp3_events:
        sns.push_event(event)


__all__ = ['send_all_events']
