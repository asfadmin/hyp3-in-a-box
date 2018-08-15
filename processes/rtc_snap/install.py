import os
import pathlib as pl
import sys
from shutil import copyfile

requirements = [
    ('src/execute.py', 'hyp3-lib'),
    ('src/getDemFor.py', 'hyp3-lib'),
    ('src/get_dem.py', 'hyp3-lib'),
    ('src/dem2isce.py', 'hyp3-lib'),
    ('src/saa_func_lib.py', 'hyp3-lib'),
    ('src/getSubSwath.py', 'hyp3-lib'),
    ('src/resample_geotiff.py', 'hyp3-lib'),
    ('src/rtc2color.py', 'hyp3-lib'),
]


def hyp3_rtc_snap(clone_token):
    build_dir = pl.Path('build')
    build_dir.mkdir(exist_ok=True)

    snap_repo = 'hyp3-rtc-snap'
    clone('asfadmin', snap_repo, directory=build_dir, access_token=clone_token)
    snap_dir = build_dir / snap_repo / 'src'

    for path, repo in requirements:
        clone('asfadmin', repo, directory=build_dir, access_token=clone_token)

        src = build_dir / repo / path
        dest = snap_dir / pl.Path(path).name

        copyfile(src, dest)


def clone(account, repo, directory='.', access_token=None):
    repo_dir = pl.Path(directory) / repo

    if repo_dir.exists():
        print(f'repo {repo} exisits at {repo_dir}')
        return

    repo_url = 'https://{}github.com/{}/{}.git'.format(
        access_token + "@" if access_token else '',
        account,
        repo
    )
    clone_cmd = f'git clone --depth 1 {repo_url} {directory}/{repo}'

    os.system(clone_cmd)


if __name__ == "__main__":
    clone_token = None
    if len(sys.argv) > 1:
        clone_token = sys.argv[1]

    hyp3_rtc_snap(clone_token)
