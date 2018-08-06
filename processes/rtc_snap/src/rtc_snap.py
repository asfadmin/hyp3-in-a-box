import subprocess

from hyp3_process import Process, EarthdataCredentials


def get_creds():
    pass


def get_bucket_name():
    pass


rtc_snap = Process(
    earthdata_creds=get_creds(),
    products_bucket=get_bucket_name()
)


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
