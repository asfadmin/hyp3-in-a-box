import subprocess


def process(granule_name: str, working_dir: str, script_path: str) -> None:
    subprocess.check_call([
        'python2', script_path,
        '--ls',
        '-r', '30',
        f'{granule_name}.zip'
    ],
        cwd=working_dir
    )
