import subprocess

from hyp3_process import Process


rtc_snap = Process()


@rtc_snap.handler
def handler(granule_name: str, working_dir: str, script_path: str) -> None:
    print('processing rtc product')
    subprocess.check_call([
        'python2', script_path,
        '--ls',
        '-r', '30',
        f'{granule_name}.zip'
    ],
        cwd=working_dir
    )
