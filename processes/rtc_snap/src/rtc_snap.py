import subprocess


def process(granule_name: str, working_dir: str) -> None:
    subprocess.check_call([
        'python2', script_path(),
        '--ls',
        '-r', '30',
        f'{granule_name}.zip'
    ],
        cwd=working_dir
    )


def script_path() -> str:
    script_dir = '/usr/local/hyp3-rtc-snap/src'

    return f'{script_dir}/procSentinelRTC-3.py'
