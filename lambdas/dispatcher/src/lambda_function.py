from typing import List, Dict, Any
import json




def lambda_handler(events: List[Dict[str: Any]]) -> None:
    """

    :param event: data for the job from the scheduler
    """

    print(json.dumps(events))

    dispatch(events)
