import subprocess

import asf_granule_util as gu


def handler(
    granule_name: str,
    working_dir: str,
    earthdata_creds: str,
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


if __name__ == "__main__":
    handler(
        'S1A_IW_SLC__1SDV_20150325T020716_20150325T020746_005182_00689D_9D9B',
        '/home/ubuntu/jobs/test-wrk-dir',
        {"username": "hyp3_asf", "password": "8dppP7+?r<z=2jg42h"},
        '/home/ubuntu/hyp3-in-a-box/processes/rtc_snap/build/hyp3-rtc-snap/src/procSentinelRTC-3.py'
    )
