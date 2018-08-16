import subprocess
from typing import Dict

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
        directory=working_dir
    )

    subprocess.check_call([
        'python2', script_path,
        '--ls',
        '-r', '30',
        f'{granule_name}.zip'
    ],
        cwd=working_dir
    )
