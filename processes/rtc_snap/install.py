import pathlib as pl
import subprocess
import sys
from shutil import copyfile

REQUIREMENTS = [
    ('src/', 'hyp3-lib', 'prod'),
]

BUILD_DIR = pl.Path('build')
SNAP_REPO = 'hyp3-rtc-snap'


def hyp3_rtc_snap(clone_token):
    BUILD_DIR.mkdir(exist_ok=True)

    clone(
        'asfadmin',
        SNAP_REPO,
        'master',
        directory=BUILD_DIR,
        access_token=clone_token
    )
    snap_dir = BUILD_DIR / SNAP_REPO / 'src'

    for path, repo, branch in REQUIREMENTS:
        clone(
            'asfadmin',
            repo,
            branch,
            directory=BUILD_DIR,
            access_token=clone_token
        )
        src = BUILD_DIR / repo / path
        dst = snap_dir

        if dst.is_dir():
            print(f'copying dir {src} -> {dst}')
            copy_dir(src, dst)
        if dst.is_file():
            print(f'copying file {src} -> {dst}')
            dest = snap_dir / pl.Path(path).name
            copyfile(src, dest)

    print('copying hyp3_handler.py')
    copy_handler_to(BUILD_DIR)


def copy_handler_to(path):
    handler_path = pl.Path('src/hyp3_handler.py')

    copyfile(handler_path, path / handler_path.name)


def copy_dir(src_dir, dst, file_types=('.py')):
    files = [
        f for f in src_dir.iterdir() if
        f.is_file() and f.suffix in file_types
    ]

    for f in files:
        print(f'  {f.name} -> {dst}')
        copyfile(f, dst / f.name)


def clone(account, repo, branch, directory='.', access_token=None):
    repo_dir = pl.Path(directory) / repo

    if repo_dir.exists():
        print(f'repo {repo} exisits at {repo_dir}')
        return

    repo_url = 'https://{}github.com/{}/{}.git'.format(
        access_token + "@" if access_token else '',
        account,
        repo
    )

    subprocess.check_call([
        'git', 'clone',
        '--depth', '1',
        '--single-branch', '-b', branch,
        repo_url, f'{directory}/{repo}'
    ])


if __name__ == "__main__":
    clone_token = None
    if len(sys.argv) > 1:
        clone_token = sys.argv[1]

    hyp3_rtc_snap(clone_token)
