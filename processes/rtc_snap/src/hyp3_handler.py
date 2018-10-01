import subprocess
from typing import Dict

import asf_granule_util as gu


def handler(
    granule_name: str,
    earthdata_creds: Dict[str, str]
) -> None:
    print('processing rtc product')

    gu.download(
        granule_name,
        earthdata_creds
    )

    print(subprocess.check_output([
        'python2', 'hyp3-rtc-snap/src/procSentinelRTC-3.py',
        '--ls',
        '-r', '30',
        f'{granule_name}.zip'
    ]))
