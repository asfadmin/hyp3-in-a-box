import subprocess

import asf_granule_util as gu


def handler(
    granule_name: str,
    working_dir: str,
    earthdata_creds: str
) -> None:
    print('processing rtc product')

    gu.download(
        granule_name,
        earthdata_creds,
        directory=str(working_dir)
    )

    subprocess.check_call([
        'python2', 'procSentinel',
        '--ls',
        '-r', '30',
        f'{granule_name}.zip'
    ],
        cwd=working_dir
    )
