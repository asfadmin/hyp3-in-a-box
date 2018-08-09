import pathlib as pl
import subprocess
import json

import asf_granule_util as gu


def handler(
    granule_name: str,
    working_dir: str,
    earthdata_creds: str,
    script_path: str
) -> None:
    print('processing rtc product')
    files = ['hello.txt', 'browse.png']

    for f in files:
        with (pl.Path(working_dir) / f).open('w') as f:
            f.write('test file')


if __name__ == "__main__":
    handler(
        'S1A_IW_SLC__1SDV_20150325T020716_20150325T020746_005182_00689D_9D9B',
        '/home/ubuntu/jobs/test-wrk-dir',
        json.load(open('earthdata_creds.json', 'r')),
        '/home/ubuntu/hyp3-in-a-box/processes/rtc_snap/build/hyp3-rtc-snap/src/procSentinelRTC-3.py'
    )
