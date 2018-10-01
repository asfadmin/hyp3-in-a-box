"""
Print out and example hyp3_event.StartEvent as json.
This is used for manually putting testing events into
the StartEvent queue.
"""

import random
import string

import hyp3_events


def rand(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


se = hyp3_events.StartEvent(
    granule=('S1A_IW_GRDH_1SDV_20150329T013228'
             '_20150329T013253_005240_0069E3_95F9'),
    user_id=1,
    sub_id=1,
    output_patterns={
        "archive": ["*/*_TC_G??.tif", "*/*.png", "*/*.txt"],
        "browse": ["*/*rgb_large.png", "*/*rgb.png", "*/*large.png", "*/*.png"]

    },
    additional_info=[{
        'name': 'test',
        'value': rand(5)
    }]
)

print(se.to_json())
