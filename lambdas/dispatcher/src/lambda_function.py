from typing import List, Dict, Any
import json
import os.environ

from . import dispatch, environment




def lambda_handler(events: List[Dict[str: Any]]) -> None:
    """

    :param events: data for the StartEvents from the scheduler
    """

    print(json.dumps(events))
    setup_environment()
    dispatch(events)


def setup_environment():

    environment.sns_arn = os.environ['SNS_ARN']
    environment.queue_url = os.environ['QUEUE_URL']
