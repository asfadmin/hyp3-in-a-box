from typing import str
from hyp3_events import StartEvent


def requeue(event: StartEvent) -> str:
    return "SCHEDULER_ROUTER_ADDRESS" #TODO needs to know the url of the scheduler