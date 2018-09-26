import contextlib
import pathlib as pl
import shutil


@contextlib.contextmanager
def create(path: pl.Path, link_dir: pl.Path):
    working_dir = setup(path, link_dir)

    try:
        yield str(working_dir)
    except Exception as e:
        raise e
    finally:
        shutil.rmtree(working_dir)


def setup(path: pl.Path, link_dir: pl.Path) -> pl.Path:
    path.mkdir(parents=True, exist_ok=True)

    link_dir_contents(link_dir, path)

    return path


def link_dir_contents(link_dir, working_dir):
    for p in link_dir.iterdir():
        link_dir_item = working_dir / p.name

        link_dir_item.symlink_to(p.resolve())
