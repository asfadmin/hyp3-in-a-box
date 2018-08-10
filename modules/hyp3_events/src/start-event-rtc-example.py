import random
import string

import hyp3_events


def rand(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


se = hyp3_events.StartEvent(
    granule='S1A_WV_OCN__2SSV_20180805T042601_20180805T043210_023106_028262_4799',
    user_id=1,
    sub_id=1,
    output_patterns={
        "archive": ["*/*_TC_G??.tif", "*/*.png", "*/*.txt"],
        "browse": "*/*.png"
    },
    script_path='/home/ubuntu/hyp3-in-a-box/processes/rtc_snap/build/hyp3-rtc-snap/src/procSentinelRTC-3.py',
    additional_info=[{
        'name': 'test',
        'value': rand(5)
    }]
)

print(se.to_json())