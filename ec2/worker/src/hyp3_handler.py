from typing import Dict
import json
import subprocess

import asf_granule_util as gu


def handler(
    granule_name: str,
    working_dir: str,
    earthdata_creds: Dict[str, str],
    script_path: str
) -> None:
    print('processing rtc product')

    gu.download(
        granule_name,
        earthdata_creds,
        directory=working_dir,
        progress_bar=True

    )

    subprocess.check_call([
        'python2', script_path,
        '--ls',
        '-r', '30',
        f'{granule_name}.zip'
    ],
        cwd=working_dir
    )


if __name__ == "__main__":
    handler(
        "S1A_IW_GRDH_1SDV_20150329T013253_20150329T013318_005240_0069E3_0AE5",
        "/home/ubuntu/jobs/test",
        json.load(open('creds.json', 'r')),
        '/home/ubuntu/hyp3-in-a-box/processes/rtc_snap/build/hyp3-rtc-snap/src/procSentinelRTC-3.py'
    )
