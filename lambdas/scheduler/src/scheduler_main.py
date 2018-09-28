from typing import Dict
import json
import boto3
import events
from NewEvent_to_StartEvent import make_dispatchable


def scheduler(aws_event: Dict) -> None:
    """ Wrapper around scheduler lambda that can be imported by pytest."""
    new_granule_events = events.make_new_granule_events_with(
        aws_event['new_granules']
    )

    new_granule_events = make_dispatchable(new_granule_events)


    # send hyp3_events to the dispatcher
    boto3.client('lambda').invoke(
        FunctionName=scheduler.environment.dispatch_lambda,
        InvocationType='Event',
        Payload=json.dump(new_granule_events.to_dict())
    )
