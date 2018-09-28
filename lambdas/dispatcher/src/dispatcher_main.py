from typing import Dict, List, Any
from hyp3_events import StartEvent
import send_all_events


def dispatch(events: List[Dict[str : Any]]) -> None:
    print('converting back to StartEvents')
    start_events = make_new_start_events_with(events)
    send_all_events.all_events(start_events)


def make_new_start_events_with(events: List[Dict[str : Any]]
                               ) -> List[StartEvent]:
    start_events = [StartEvent(**e)
                    for e in events
                    ]

    return start_events
